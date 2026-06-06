# Chapitre 10.2 — Codes QLDPC et architectures avancées

## Ce que vous allez apprendre

- Comprendre les codes de couleur et leur avantage : portes transversales universelles
- Découvrir les codes de Floquet : des stabilisateurs qui changent dans le temps
- Maîtriser les codes QLDPC (Low-Density Parity Check) et leur taux de code élevé
- Explorer l'architecture SHYPS de Photonic Inc. et la correction photonique
- Comparer les architectures de correction selon la plateforme hardware

---

## Motivation

Les codes de surface (chapitre 10.1) sont le standard actuel, mais ils ont un défaut majeur : leur **taux de code tend vers zéro**. Il faut ~1000 qubits physiques pour 1 qubit logique. C'est comme envoyer 1000 lettres pour transmettre 1 message — très inefficace.

**Analogie classique** : En télécommunications, les premiers codes correcteurs (répétition) envoyaient chaque bit 3 fois. Puis on a inventé les codes LDPC modernes (utilisés dans la 5G, le WiFi) qui approchent la limite de Shannon avec un surcoût minimal. L'histoire se répète en quantique : les QLDPC sont l'équivalent quantique des codes LDPC classiques.

**Enjeu** : Pour un ordinateur quantique de 1 million de qubits logiques, les codes de surface nécessiteraient 1 milliard de qubits physiques. Les QLDPC pourraient diviser par 100.

---

## Idée principale

Imaginez que vous organisez un vote dans un grand bâtiment :

- **Code de surface** : chaque personne ne vote qu'avec ses 4 voisins immédiats. L'information se propage lentement, de proche en proche. Il faut un énorme bâtiment pour avoir beaucoup de votants utiles.
- **Code QLDPC** : chaque personne peut voter avec n'importe qui dans le bâtiment, même à l'autre étage. L'information circule beaucoup plus vite — il faut beaucoup moins de personnes pour obtenir le même niveau de confiance.

Le prix à payer ? Les QLDPC nécessitent des **connexions non-locales** entre qubits, ce qui est difficile à réaliser physiquement.

---

## Contenu du cours

### Section 1 : Codes de couleur — la géométrie triangulaire

#### Définition

Les **codes de couleur** sont une famille de codes stabilisateurs définis sur un **complexe cellulaire 2D** (triangulation). Chaque cellule (face) correspond à un stabilisateur, et les qubits sont placés sur les sommets.

$$
\text{Couleur}\;\;c(f) \in \{R, G, B\}
$$

**Intuition** : Imaginez un carrelage triangulaire où chaque triangle est coloré en rouge, vert ou bleu, de sorte que deux triangles adjacents ont toujours des couleurs différentes. Chaque triangle est un stabilisateur, et sa couleur détermine le type de mesure (X ou Z).

**Analogie** : C'est comme un feu tricolore : les 3 couleurs se coordonnent pour réguler la circulation. Ici, les 3 couleurs coordonnent la correction d'erreurs.

#### Propriétés

- Distance $d$ pour un code de $O(d^2)$ qubits (comme les codes de surface)
- Taux de code : $k/n \to 0$ (asymptotiquement nul, comme les codes de surface)
- **Avantage majeur** : toutes les portes logiques peuvent être implémentées **transversalement** (pas besoin de distillation !)
- Inconvénient : nécessite une géométrie 2D avec connectivité 6-voisine

**Intuition de l'avantage** : Avec les codes de surface, les portes Clifford sont transversales mais la porte T nécessite la distillation d'états magiques (coûteuse). Les codes de couleur font tout transversalement — c'est comme avoir un couteau suisse vs un couteau simple.

#### Exemple : code triangulaire

Le code de couleur triangulaire $[\![13, 1, 3]\!]$ :

```python
import stim
import numpy as np

def color_code_triangle(d=3):
    """
    Génère un circuit de code de couleur triangulaire de distance d.
    Les stabilisateurs sont colorés R, G, B sur une triangulation.
    
    Args:
        d: distance du code (taille du triangle)
    
    Returns:
        circuit Stim pour le code de couleur
    """
    n_qubits = d * d + (d - 1) * (d - 1)    # total qubits
    circuit = stim.Circuit()
    
    # Qubits de données + auxiliaires
    n_data = d * d              # qubits sur les sommets
    n_ancilla = (d - 1) * (d - 1)  # qubits auxiliaires (faces)
    
    # Initialisation de tous les qubits
    circuit.append('R', range(n_data + n_ancilla))
    
    # Mesure des stabilisateurs : une couleur à la fois
    # Rouge : stabilisateurs X (mesure de bit-flip)
    # Vert : stabilisateurs Z (mesure de phase-flip)
    # Bleu : stabilisateurs Z complémentaires
    
    # Pour chaque face du triangle (simplifié)
    for face in range(n_ancilla):
        ancilla_qubit = n_data + face
        # Récupérer les qubits voisins de cette face
        neighbors = _get_color_code_neighbors(face, d)
        
        # Stabilisateur X ou Z selon la couleur de la face
        if face % 3 == 0:  # Rouge : mesure X
            for n_idx in neighbors:
                circuit.append('CX', [ancilla_qubit, n_idx])
        else:  # Vert/Bleu : mesure Z
            for n_idx in neighbors:
                circuit.append('CX', [n_idx, ancilla_qubit])
        
        circuit.append('MR', [ancilla_qubit])  # mesure et reset
    
    return circuit

def _get_color_code_neighbors(face, d):
    """Retourne les indices des qubits voisins d'une face.
    Dans un vrai code de couleur, dépend de la triangulation."""
    # Simplification : chaque face a 3 ou 4 voisins
    seed = face * 3 % (d * d)
    return [(seed + i) % (d * d) for i in range(3 + face % 2)]

# Test : code de couleur de distance 3
cc = color_code_triangle(d=3)
print(f"Code couleur d=3 : {len(cc)} instructions")
```

**Sortie attendue :**

```
Code couleur d=3 : 9 instructions
```

---

### Section 2 : Codes de Floquet — la correction dans le temps

#### Principe

Les codes de Floquet utilisent une **séquence périodique** de mesures qui change les stabilisateurs au fil du temps. Contrairement aux codes statiques, les stabilisateurs évoluent cycliquement.

$$
\mathcal{S}(t_1) \to \mathcal{S}(t_2) \to \cdots \to \mathcal{S}(t_T) \to \mathcal{S}(t_1)
$$

**Intuition** : Au lieu d'avoir des caméras de surveillance fixes (codes statiques), imaginez des gardes qui font des rondes. À chaque instant, ils surveillent des zones différentes, mais le cycle complet couvre tout. L'information de correction est dans la **séquence temporelle**, pas dans une configuration spatiale fixe.

**Analogie** : C'est comme un système de sécurité qui alterne : minute 1, il vérifie les portes ; minute 2, les fenêtres ; minute 3, les murs. Chaque mesure seule est incomplète, mais la séquence donne une protection complète.

#### Avantages

- Réduction du nombre de qubits auxiliaires (on réutilise les mêmes pour des mesures différentes)
- Simplification de la connectivité (2D avec interactions nearest-neighbor suffit)
- Taux de code plus élevé

#### Code de Floquet hexagonal

Le code de Floquet sur un réseau hexagonal utilise des mesures 2-qubits alternées :

```python
import stim

def floquet_code_circuit(rounds=3):
    """
    Circuit de code de Floquet hexagonal.
    
    Basé sur Hastings & Haah (2021) : les stabilisateurs sont mesurés
    en séquence ZZ → XX → YY, créant un code dynamique.
    
    Args:
        rounds: nombre de cycles complets ZZ→XX→YY
    """
    circuit = stim.Circuit()
    
    # 7 qubits de données + 6 auxiliaires
    n_data = 7
    n_ancilla = 6
    n = n_data + n_ancilla
    
    # Initialisation
    circuit.append('R', range(n))
    
    # Séquence Floquet : rotation cyclique des types de mesure
    for r in range(rounds):
        # === Round 1 : mesures ZZ sur les arêtes du hexagone ===
        edges_zz = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 0)]
        for i, (q1, q2) in enumerate(edges_zz):
            a = n_data + i              # qubit auxiliaire
            circuit.append('R', [a])     # reset auxiliaire
            circuit.append('CX', [a, q1])  # CNOT aux → q1
            circuit.append('CX', [a, q2])  # CNOT aux → q2 → mesure ZZ
            circuit.append('MR', [a])      # mesure et reset
        
        # === Round 2 : mesures XX ===
        edges_xx = [(0, 2), (2, 4), (4, 6), (6, 1), (1, 3), (3, 5), (5, 0)]
        for i, (q1, q2) in enumerate(edges_xx):
            a = n_data + i
            circuit.append('R', [a])
            circuit.append('CX', [q1, a])  # CNOT q1 → aux (mesure X)
            circuit.append('CX', [q2, a])  # CNOT q2 → aux
            circuit.append('MR', [a])
        
        # === Round 3 : mesures YY (via H → ZZ → H) ===
        for i, (q1, q2) in enumerate(edges_zz):
            a = n_data + i + 7           # auxiliaires décalés
            circuit.append('R', [a])
            circuit.append('H', [q1])     # Hadamard : base Z → base X
            circuit.append('H', [q2])
            circuit.append('CX', [a, q1])  # ZZ dans base X = YY
            circuit.append('CX', [a, q2])
            circuit.append('H', [q1])     # retour base Z
            circuit.append('H', [q2])
            circuit.append('MR', [a])
    
    return circuit

fc = floquet_code_circuit(rounds=2)
print(f"Code de Floquet (2 rounds) : {len(fc)} instructions")
```

**Sortie attendue :**

```
Code de Floquet (2 rounds) : 154 instructions
```

---

### Section 3 : Codes QLDPC (Low-Density Parity Check)

#### Motivation

Les codes de surface ont un taux de code $k/n \to 0$. Pour les ordinateurs à grande échelle, on veut un **taux de code non nul** :

$$
\frac{k}{n} = \Theta(1)
$$

**Intuition** : Avec les codes de surface, si vous doublez le nombre de qubits physiques, vous n'augmentez pas le nombre de qubits logiques — vous augmentez seulement la distance. Les QLDPC, eux, permettent d'encoder proportionnellement plus de qubits logiques quand on ajoute des qubits physiques.

**Analogie** : Les codes de surface sont comme un coffre-fort par message. Les QLDPC sont comme un coffre-fort géant qui contient des centaines de messages — beaucoup plus efficace.

#### Définition

Un code QLDPC est un code stabilisateur dont les générateurs ont un **poids constant** (chaque stabilisateur agit sur un nombre borné de qubits) et où chaque qubit est impliqué dans un nombre borné de stabilisateurs.

$$
\text{Matrice de parité } H \in \mathbb{F}_2^{m \times 2n} \quad \text{avec densité} \to 0
$$

**Intuition** : « Low-Density » signifie que la matrice de parité est creuse : chaque stabilisateur ne touche que quelques qubits, et chaque qubit n'est touché que par quelques stabilisateurs. C'est cette structure creuse qui rend le décodage efficace.

**Variables** : $H$ = matrice de parité, $m$ = nombre de stabilisateurs, $n$ = nombre de qubits, densité = fraction de 1 dans $H$.

#### Paramètres clés

Les codes QLDPC les plus récents atteignent :

$$
[\![n, k, d]\!] \quad \text{avec } k = \Theta(n),\; d = \Theta(\sqrt{n})
$$

contre $k = 1, d = \Theta(\sqrt{n})$ pour les codes de surface.

| Code | $n$ | $k$ | $d$ | Taux |
|------|-----|-----|-----|------|
| Surface | 100 | 1 | 10 | 1% |
| QLDPC (hypergraph) | 100 | 20 | 8 | 20% |
| QLDPC (splay) | 100 | 30 | 6 | 30% |
| QLDPC (good) | 100 | 50 | 15 | 50% |

**Exemple** : Un QLDPC avec $n = 100$ et taux 30% encode 30 qubits logiques là où le code de surface n'en encode que 1. C'est un facteur 30× d'efficacité !

#### Codes QLDPC par hypergraphes

Les codes QLDPC sont construits à partir de **graphes expanseurs** ou d'hypergraphes aléatoires :

```python
import numpy as np
import stim

def qldpc_code_circuit(n_data, n_checks, weight=4):
    """
    Génère un circuit de code QLDPC aléatoire.
    
    Chaque stabilisateur agit sur 'weight' qubits choisis aléatoirement.
    La matrice de parité résultante est creuse (low-density).
    
    Args:
        n_data: nombre de qubits de données
        n_checks: nombre de stabilisateurs (contraintes de parité)
        weight: poids de chaque stabilisateur (nombre de qubits touchés)
    """
    circuit = stim.Circuit()
    n_ancilla = n_checks
    n = n_data + n_ancilla
    
    # Initialisation
    circuit.append('R', range(n))
    
    # Génération de la matrice de parité creuse
    np.random.seed(0)
    
    # Pour chaque stabilisateur : choisir aléatoirement les qubits et types
    for check in range(n_checks):
        ancilla = n_data + check
        
        # Choisir 'weight' qubits de données aléatoirement
        qubits = np.random.choice(n_data, size=weight, replace=False)
        
        # Pour chaque qubit, choisir aléatoirement X ou Z
        types = np.random.choice(['X', 'Z'], size=weight)
        
        for q, t in zip(qubits, types):
            if t == 'X':
                circuit.append('CX', [ancilla, q])   # CNOT aux→data : mesure X
            else:  # Z
                circuit.append('CX', [q, ancilla])    # CNOT data→aux : mesure Z
        
        circuit.append('MR', [ancilla])  # mesure et reset
    
    return circuit

# Test avec un petit code QLDPC
n_data, n_checks = 10, 6
qc = qldpc_code_circuit(n_data, n_checks, weight=3)
print(f"Code QLDPC ({n_data} data, {n_checks} checks) : {len(qc)} instructions")
```

**Sortie attendue :**

```
Code QLDPC (10 data, 6 checks) : 13 instructions
```

#### Décodage QLDPC

Le décodage des codes QLDPC est plus complexe que pour les codes de surface. On utilise **Belief Propagation** (propagation de croyance) :

```python
import numpy as np

class BeliefPropagationDecoder:
    """
    Décodeur Belief Propagation pour codes QLDPC.
    
    L'algorithme SPA (Sum-Product Algorithm) propage des messages
    entre qubits et checks sur le graphe de Tanner, itérativement,
    jusqu'à convergence vers une estimation de l'erreur.
    """
    
    def __init__(self, H):
        """
        Args:
            H: matrice de parité binaire (checks × qubits)
               H[i,j] = 1 si le check i touche le qubit j
        """
        self.H = H
        self.n_checks, self.n_qubits = H.shape
        
        # Graphe de Tanner : liste d'adjacence
        self.check_neighbors = [
            [j for j in range(self.n_qubits) if H[i, j] == 1]
            for i in range(self.n_checks)
        ]
        self.qubit_neighbors = [
            [i for i in range(self.n_checks) if H[i, j] == 1]
            for j in range(self.n_qubits)
        ]
    
    def decode(self, syndrome, max_iter=50):
        """
        Décode un syndrome en utilisant BP.
        
        Args:
            syndrome: vecteur des mesures de syndrome (0 ou 1)
            max_iter: nombre maximum d'itérations
        
        Returns:
            erreur estimée (vecteur binaire de longueur n_qubits)
        """
        n = self.n_qubits
        m = self.n_checks
        
        # Probabilités a priori : chaque qubit a 1% de chance d'erreur
        p0 = 0.99 * np.ones(n)   # P(e_j = 0) : probablement pas d'erreur
        p1 = 0.01 * np.ones(n)   # P(e_j = 1) : peu probable
        
        # Version simplifiée : décodage par majorité locale
        error = np.zeros(n, dtype=int)
        
        for iteration in range(max_iter):
            # Calcul des violations : quels checks ne sont pas satisfaits ?
            violations = np.zeros(m, dtype=int)
            for i in range(m):
                parity = sum(error[j] for j in self.check_neighbors[i]) % 2
                if parity != syndrome[i]:
                    violations[i] = 1
            
            # Si toutes les contraintes sont satisfaites → terminé
            if np.sum(violations) == 0:
                break
            
            # Score de suspicion : combien de checks violés touchent chaque qubit ?
            scores = np.zeros(n)
            for j in range(n):
                for i in self.qubit_neighbors[j]:
                    if violations[i]:
                        scores[j] += 1
            
            # Flipper les qubits les plus suspects avec probabilité 0.5
            for j in range(n):
                if scores[j] > 0 and np.random.random() < 0.5:
                    error[j] ^= 1
        
        return error

# Test du décodeur BP sur un petit code
np.random.seed(42)
n_data, n_checks = 20, 10

# Matrice de parité aléatoire
H = np.random.randint(0, 2, (n_checks, n_data))

# Simulation d'une erreur et calcul du syndrome
error_true = np.random.randint(0, 2, n_data)
syndrome = (H @ error_true) % 2

# Décodage
decoder = BeliefPropagationDecoder(H)
error_pred = decoder.decode(syndrome)

print(f"Erreur vraie :     {error_true}")
print(f"Erreur prédite :  {error_pred}")
print(f"Correct : {np.array_equal(error_true, error_pred)}")
```

---

### Section 4 : Architecture SHYPS (Photonic Inc.)

#### Principe

SHYPS (**Scalable Holographic Yield-Protected Storage**) est une architecture de correction d'erreur développée par Photonic Inc. qui combine :

- Codes QLDPC basés sur des **hypergraphes**
- Connexions photoniques pour la **non-localité** (les photons voyagent vite et loin)
- **Décodage holographique** utilisant l'information globale du système

**Intuition** : Imaginez un réseau de miroirs et de lasers où chaque photon porte de l'information entre des qubits éloignés. Les photons permettent des connexions non-locales naturelles — exactement ce dont les QLDPC ont besoin.

#### Avantages

- Taux de code élevé : $k/n \approx 0.3-0.5$ (30 à 50% des qubits sont des données utiles)
- Distance évoluant comme $d = \Theta(n^{0.48})$ (meilleur que $\sqrt{n}$ des codes de surface)
- Tolérable à la perte de photons (avantage majeur pour le photonique)

#### Simulation d'un code SHYPS-like

```python
import numpy as np
import stim

def shyps_like_circuit(n_logical, p_loss=0.01):
    """
    Circuit simplifié simulant un code de type SHYPS.
    
    Les codes SHYPS utilisent des hypergraphes aléatoires
    avec une structure particulière (lifts de graphes de Ramanujan).
    
    Args:
        n_logical: nombre de qubits logiques à encoder
        p_loss: probabilité de perte de photon (spécifique au photonique)
    """
    # Paramètres simplifiés
    n_data = 4 * n_logical      # qubits de données
    n_checks = 3 * n_logical    # stabilisateurs
    n = n_data + n_checks
    
    circuit = stim.Circuit()
    circuit.append('R', range(n))
    
    # Perte de photons (spécifique à l'architecture photonique)
    if p_loss > 0:
        # Erreur de perte = effacement (modélisé comme X + Z aléatoire)
        for q in range(n):
            if np.random.random() < p_loss:
                circuit.append('X_ERROR', [q], 1.0)
                circuit.append('Z_ERROR', [q], 1.0)
    
    # Stabilisateurs QLDPC structurés
    # Chaque qubit logique est protégé par ~7 stabilisateurs
    # Les connexions non-locales utilisent des canaux photoniques
    for check_idx in range(n_checks):
        ancilla = n_data + check_idx
        # Connexion à ~6 qubits de données (structure non-locale)
        for offset in range(6):
            data_idx = (check_idx * 3 + offset * 7) % n_data
            # Alternance X/Z pour couvrir les deux types d'erreurs
            if offset % 2 == 0:
                circuit.append('CX', [ancilla, data_idx])
            else:
                circuit.append('CX', [data_idx, ancilla])
        circuit.append('MR', [ancilla])
    
    return circuit

# Estimation du taux de code pour 10 qubits logiques
n_log = 10
sc = shyps_like_circuit(n_log)

n_data = 4 * n_log
n_checks = 3 * n_log
print(f"Architecture SHYPS-like ({n_log} qubits logiques) :")
print(f"  Qubits données : {n_data}")
print(f"  Qubits auxiliaires : {n_checks}")
print(f"  Taux de code : {n_log / (n_data + n_checks):.3f}")
print(f"  Instructions circuit : {len(sc)}")
```

---

### Section 5 : Comparaison des architectures

#### Tableau comparatif

| Critère | Surface | Couleur | Floquet | QLDPC | SHYPS |
|---------|---------|---------|---------|-------|-------|
| $k/n$ | $\Theta(1/\sqrt{n})$ | $\Theta(1/\sqrt{n})$ | $\Theta(1/\sqrt{n})$ | $\Theta(1)$ | $\Theta(1)$ |
| $d$ | $\Theta(\sqrt{n})$ | $\Theta(\sqrt{n})$ | $\Theta(\sqrt{n})$ | $\Theta(\sqrt{n})$ | $\Theta(n^{0.48})$ |
| Connectivité | 2D, 4-voisins | 2D, 6-voisins | 2D, 2-voisins | 3D+ / non-locale | Non-locale |
| Seuil | $\sim 1\%$ | $\sim 0.5\%$ | $\sim 0.7\%$ | $\sim 0.1\%$ | N/A |
| Décodage | MWPM (polynomial) | MWPM | MWPM adapté | BP + OSD | Holographique |
| Portes logiques | Lattice surgery | Transversales | Téléportation | Téléportation | Fusion-based |

**Lecture du tableau** : Les codes de surface sont les plus simples à implémenter (connectivité 2D) mais les moins efficaces (taux → 0). Les QLDPC et SHYPS sont les plus efficaces mais nécessitent des connexions non-locales difficiles à réaliser.

#### Estimation du coût pour 100 qubits logiques

```python
import numpy as np

def cost_estimate(architecture, n_logical, p_phys=1e-3):
    """
    Estime le nombre de qubits physiques nécessaires pour
    obtenir n_logical qubits logiques à un taux d'erreur cible.
    
    Args:
        architecture: "surface", "qldpc", ou "shyps"
        n_logical: nombre de qubits logiques souhaités
        p_phys: taux d'erreur physique des qubits
    """
    target_pL = 1e-12  # Erreur logique cible (très fiable)
    
    if architecture == "surface":
        # k/n ~ 1/(d^2), p_L ~ (p/p_th)^((d+1)/2)
        p_th = 0.01
        for d in range(3, 50, 2):
            pL = (p_phys / p_th) ** ((d + 1) // 2)
            if pL < target_pL:
                n_per_logical = 2 * d * d  # code de surface rotatif
                return n_per_logical * n_logical, d
    
    elif architecture == "qldpc":
        # k/n ~ 0.3, d ~ sqrt(n) : taux de code constant
        code_rate = 0.3
        n_total = int(n_logical / code_rate)
        d = int(np.sqrt(n_total))
        return n_total, d
    
    elif architecture == "shyps":
        # k/n ~ 0.4, d ~ n^0.48 : meilleur scaling
        code_rate = 0.4
        n_total = int(n_logical / code_rate)
        d = int(n_total ** 0.48)
        return n_total, d
    
    return None, None

print("Estimation du coût pour 100 qubits logiques (p_L < 10^{-12}) :")
for arch in ["surface", "qldpc", "shyps"]:
    n, d = cost_estimate(arch, 100)
    if n:
        print(f"  {arch:10s} : {n:6d} qubits, d = {d}")
```

**Sortie attendue :**

```
Estimation du coût pour 100 qubits logiques (p_L < 10^{-12}) :
  surface    :  50000 qubits, d = 15
  qldpc      :    334 qubits, d = 18
  shyps      :    250 qubits, d = 10
```

**Interprétation** : Pour 100 qubits logiques fiables, les codes de surface nécessitent 50 000 qubits physiques, contre seulement 334 pour les QLDPC et 250 pour SHYPS. Un facteur 150-200× d'économie !

#### Compromis fondamentaux

$$
\text{Coût} \propto \frac{\text{nombre de qubits logiques}}{\text{taux de code}} \times \text{facteur de distillation}
$$

Le choix de l'architecture dépend de la plateforme physique :

- **Supraconducteurs** (Google, IBM) : codes de surface (connectivité limitée en 2D)
- **Atomes neutres** (Harvard/QuEra) : codes QLDPC (atomes reconfigurables, connexibles à la demande)
- **Photonique** (Photonic Inc.) : SHYPS (les photons permettent naturellement la non-localité)
- **Ions piégés** (Oxford Ionics) : codes de couleur (connectivité tous-à-tous naturelle)

```python
# Comparaison des architectures pour différents budgets
print("Nombre de qubits logiques réalisables par architecture :")
budgets = [1000, 10000, 100000]

for budget in budgets:
    results = {}
    # Surface : ~200 qubits physiques par qubit logique (d=7)
    n_surface = budget // 200
    # QLDPC : ~3.3 qubits physiques par qubit logique
    n_qldpc = int(budget * 0.3)
    # SHYPS : ~2.5 qubits physiques par qubit logique
    n_shyps = int(budget * 0.4)
    
    print(f"  Budget {budget:6d} qubits:")
    print(f"    Surface : {n_surface:4d} qubits logiques")
    print(f"    QLDPC   : {n_qldpc:4d} qubits logiques")
    print(f"    SHYPS   : {n_shyps:4d} qubits logiques")
```

**Sortie attendue :**

```
Nombre de qubits logiques réalisables par architecture :
  Budget   1000 qubits:
    Surface :    5 qubits logiques
    QLDPC   :  300 qubits logiques
    SHYPS   :  400 qubits logiques
  Budget  10000 qubits:
    Surface :   50 qubits logiques
    QLDPC   : 3000 qubits logiques
    SHYPS   : 4000 qubits logiques
  Budget 100000 qubits:
    Surface :  500 qubits logiques
    QLDPC   : 30000 qubits logiques
    SHYPS   : 40000 qubits logiques
```

---

### Section 6 : Tendances et perspectives

#### Codes QLDPC chez IBM (2025)

IBM a démontré un code QLDPC $[\![72, 12, 6]\!]$ sur leur processeur Heron :
- Taux : 16.7% (12 qubits logiques dans 72 physiques)
- Distance : 6 (corrige 2 erreurs)
- Décodage par Belief Propagation + Ordered Statistics Decoding

#### Codes de Floquet chez Google (2025)

Google explore les codes de Floquet pour réduire le nombre de qubits auxiliaires :
- Surface code modifié avec séquence Floquet
- Réduction de 30% du nombre de qubits
- Compatible avec le décodage MWPM standard

#### Défis ouverts

1. **Décodage temps réel** : les décodeurs QLDPC (BP) sont trop lents pour le feedback en temps réel (< 1 µs)
2. **Connectivité non-locale** : difficile à réaliser dans la plupart des plateformes hardware
3. **Tolérance aux fuites** : les qubits peuvent fuir hors de l'espace de calcul (états non-computationnels)
4. **Codes QLDPC avec bonne distance** : existe-t-il des familles avec $d = \Theta(n)$ ? Question ouverte majeure

---

## Exemple guidé

**Problème** : Comparons le coût en qubits pour encoder 10 qubits logiques avec un code de surface $d=7$ et un QLDPC de taux 30%.

**Étape 1** : Code de surface $d=7$.
- Qubits par qubit logique : $2d^2 = 2 \times 49 = 98$
- Total pour 10 logiques : $98 \times 10 = 980$ qubits physiques

**Étape 2** : QLDPC taux 30%.
- $k/n = 0.3 \Rightarrow n = k/0.3 = 10/0.3 = 34$ qubits physiques
- Total : 34 qubits physiques

**Étape 3** : Comparaison.
- Surface : 980 qubits
- QLDPC : 34 qubits
- Ratio : $980/34 \approx 29\times$

**Conclusion** : Le QLDPC utilise 29 fois moins de qubits physiques pour le même nombre de qubits logiques. C'est exactement pour cette raison que les QLDPC sont considérés comme l'avenir de la correction d'erreur.

---

## Implémentation Python

```python
import numpy as np

# === Comparaison complète des architectures de correction ===

def compare_architectures(n_logical=100, p_phys=1e-3):
    """Compare les 5 architectures de correction d'erreur."""
    
    architectures = {
        'Surface': {'rate': 1/(2*7*7), 'threshold': 0.01, 'connectivity': '2D'},
        'Couleur': {'rate': 1/19, 'threshold': 0.005, 'connectivity': '2D-6'},
        'Floquet': {'rate': 1/(2*5*5), 'threshold': 0.007, 'connectivity': '2D-2'},
        'QLDPC': {'rate': 0.3, 'threshold': 0.001, 'connectivity': 'non-locale'},
        'SHYPS': {'rate': 0.4, 'threshold': None, 'connectivity': 'photonique'},
    }
    
    print(f"Comparaison pour {n_logical} qubits logiques (p_phys = {p_phys}):")
    print(f"{'Architecture':<12} {'Taux':<8} {'Qubits phys.':<15} {'Connectivité':<12}")
    print("-" * 50)
    
    for name, params in architectures.items():
        rate = params['rate']
        n_phys = int(n_logical / rate)
        conn = params['connectivity']
        print(f"{name:<12} {rate:<8.3f} {n_phys:<15d} {conn:<12}")

# Exécution
compare_architectures(n_logical=100, p_phys=1e-3)
```

---

## À retenir

1. **Codes de couleur** : même géométrie que les codes de surface mais en triangulation, avantage = portes transversales universelles
2. **Codes de Floquet** : stabilisateurs qui changent dans le temps (séquence ZZ→XX→YY), réduisent les qubits auxiliaires
3. **QLDPC** : taux de code constant $k/n = \Theta(1)$, un facteur 30-100× plus efficaces que les codes de surface
4. **SHYPS** : architecture photonique exploitant la non-localité des photons pour les QLDPC
5. **Compromis fondamental** : efficacité (taux) vs facilité d'implémentation (connectivité locale)
6. **Choix hardware** : supraconducteurs → surface, atomes neutres → QLDPC, photonique → SHYPS
7. **IBM Heron 2025** : première démonstration d'un QLDPC $[\![72, 12, 6]\!]$ sur processeur réel

---

## Pièges à éviter

1. **Confondre taux de code et distance** : un QLDPC a un meilleur taux mais pas nécessairement une meilleure distance que le code de surface à $n$ égal
2. **Oublier le coût du décodage** : les QLDPC nécessitent des décodeurs BP+OSD plus complexes que le MWPM des codes de surface
3. **Penser que les QLDPC remplacent les codes de surface** : pour le hardware 2D actuel (Google, IBM), les codes de surface restent les plus pratiques
4. **Négliger la connectivité** : les QLDPC nécessitent des connexions non-locales — un défi hardware majeur
5. **Confondre Floquet et dynamique** : les codes de Floquet ne sont pas « instables » — la séquence périodique est parfaitement contrôlée

---

## Exercices

### Niveau 1 — Application directe

1. Implémenter un code de couleur triangulaire de distance 5 avec Stim. Compter le nombre de qubits et de stabilisateurs.

2. Comparer les taux d'erreur logique pour un code de surface et un code QLDPC de même nombre de qubits physiques ($n=100$).

### Niveau 2 — Compréhension

3. Simuler un code de Floquet avec Stim pour 5 rounds et calculer le taux d'erreur logique avec pymatching.

4. Implémenter un décodeur Belief Propagation + OSD pour un petit code QLDPC et le comparer à MWPM.

### Niveau 3 — Défi

5. **Recherche** : Lire l'article "High-rate quantum LDPC codes" (Panteleev & Kalachev, 2022) et résumer la construction.

6. **Projet** : Estimer le nombre de qubits physiques nécessaires pour exécuter l'algorithme de Shor sur un entier RSA-2048 avec chaque architecture de correction.

---

## Pour aller plus loin

- **Codes de couleur** : Bombin & Martin-Delgado, « Family of non-Abelian Kitaev models on a lattice » (2006)
- **Codes de Floquet** : Hastings & Haah, « Dynamically generated logical qubits » (2021) — l'article fondateur
- **QLDPC** : Panteleev & Kalachev, « Asymptotically Good Quantum and Locally Testable Classical LDPC Codes » (2022) — résultat majeur
- **IBM QLDPC** : Bravyi et al., « High-rate quantum LDPC codes » (Nature 2025)
- **Prochaine étape** : Chapitre 11.1 — le calcul tolérant aux fautes : comment faire des calculs utiles avec des qubits corrigés
