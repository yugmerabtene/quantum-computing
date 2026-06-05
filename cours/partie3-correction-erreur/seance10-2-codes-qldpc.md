# Séance 10.2 — Codes QLDPC et architectures avancées

## Objectifs

- Comprendre les codes de couleur et leurs propriétés
- Formaliser les codes de Floquet
- Maîtriser les codes QLDPC (Low-Density Parity Check)
- Analyser l'architecture SHYPS (Photonic Inc.)
- Comparer les différentes architectures de correction

---

## 1. Codes de couleur

### 1.1 Définition

Les **codes de couleur** sont une famille de codes stabilisateurs définis sur un **complexe cellulaire 2D** (triangulation). Chaque cellule (face) correspond à un stabilisateur, et les qubits sont placés sur les sommets.

$$
\text{Couleur}\;\;c(f) \in \{R, G, B\}
$$

### 1.2 Propriétés

- Distance $d$ pour un code de $O(d^2)$ qubits
- Taux de code : $k/n \to 0$ (asymptotiquement nul, comme les codes de surface)
- Avantage : toutes les portes logiques peuvent être implémentées transversalement
- Inconvénient : nécessite une géométrie 2D avec connectivité 6-voisine

### 1.3 Exemple : code triangulaire

Le code de couleur triangulaire $[\![13, 1, 3]\!]$ :

```python
import stim
import numpy as np

def color_code_triangle(d=3):
    """
    Génère un circuit de code de couleur triangulaire de distance d.
    Format simplifié pour illustration.
    """
    n_qubits = d * d + (d - 1) * (d - 1)
    circuit = stim.Circuit()
    
    # Qubits de données + auxiliaires
    n_data = d * d
    n_ancilla = (d - 1) * (d - 1)
    
    # Initialisation
    circuit.append('R', range(n_data + n_ancilla))
    
    # Mesure des stabilisateurs (une couleur à la fois)
    # Rouge : X stabilisateurs
    # Vert : Z stabilisateurs
    # Bleu : Z stabilisateurs (complément)
    
    # Pour chaque face du triangle (simplifié)
    for face in range(n_ancilla):
        ancilla_qubit = n_data + face
        # 3 ou 4 qubits voisins selon la position
        neighbors = _get_color_code_neighbors(face, d)
        
        # Stabilisateur X ou Z alterné
        if face % 3 == 0:  # Rouge : X
            for n_idx in neighbors:
                circuit.append('CX', [ancilla_qubit, n_idx])
        else:  # Vert/Bleu : Z
            for n_idx in neighbors:
                circuit.append('CX', [n_idx, ancilla_qubit])
        
        circuit.append('MR', [ancilla_qubit])
    
    return circuit

def _get_color_code_neighbors(face, d):
    """Retourne les indices des qubits voisins d'une face."""
    # Simplification : chaque face a 3 ou 4 voisins
    # Dans un vrai code de couleur, dépend de la triangulation
    seed = face * 3 % (d * d)
    return [(seed + i) % (d * d) for i in range(3 + face % 2)]

# Test
cc = color_code_triangle(d=3)
print(f"Code couleur d=3 : {len(cc)} instructions")
```

---

## 2. Codes de Floquet

### 2.1 Principe

Les codes de Floquet utilisent une **séquence périodique** de mesures qui change les stabilisateurs au fil du temps. Contrairement aux codes statiques, les stabilisateurs évoluent cycliquement.

$$
\mathcal{S}(t_1) \to \mathcal{S}(t_2) \to \cdots \to \mathcal{S}(t_T) \to \mathcal{S}(t_1)
$$

### 2.2 Avantages

- Réduction du nombre de qubits auxiliaires
- Simplification de la connectivité (2D avec interactions nearest-neighbor)
- Taux de code plus élevé

### 2.3 Code de Floquet hexagonal

Le code de Floquet sur un réseau hexagonal utilise des mesures 2-qubits alternées :

```python
import stim

def floquet_code_circuit(rounds=3):
    """
    Circuit de code de Floquet hexagonal (Bacon-Shor version Floquet).
    
    Basé sur l'article : Hastings & Haah (2021).
    """
    circuit = stim.Circuit()
    
    # 7 qubits de données + 6 auxiliaires
    n_data = 7
    n_ancilla = 6
    n = n_data + n_ancilla
    
    # Initialisation
    circuit.append('R', range(n))
    
    # Séquence Floquet : rotation des mesures ZZ, XX, YY
    for r in range(rounds):
        # Round 1 : mesures ZZ sur les arêtes
        edges_zz = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 0)]
        for i, (q1, q2) in enumerate(edges_zz):
            a = n_data + i
            circuit.append('R', [a])
            circuit.append('CX', [a, q1])
            circuit.append('CX', [a, q2])
            circuit.append('MR', [a])
        
        # Round 2 : mesures XX
        edges_xx = [(0, 2), (2, 4), (4, 6), (6, 1), (1, 3), (3, 5), (5, 0)]
        for i, (q1, q2) in enumerate(edges_xx):
            a = n_data + i
            circuit.append('R', [a])
            circuit.append('CX', [q1, a])
            circuit.append('CX', [q2, a])
            circuit.append('MR', [a])
        
        # Round 3 : mesures YY (via H puis ZZ puis H)
        for i, (q1, q2) in enumerate(edges_zz):
            a = n_data + i + 7
            circuit.append('R', [a])
            circuit.append('H', [q1])
            circuit.append('H', [q2])
            circuit.append('CX', [a, q1])
            circuit.append('CX', [a, q2])
            circuit.append('H', [q1])
            circuit.append('H', [q2])
            circuit.append('MR', [a])
    
    return circuit

fc = floquet_code_circuit(rounds=2)
print(f"Code de Floquet (2 rounds) : {len(fc)} instructions")
```

---

## 3. Codes QLDPC (Low-Density Parity Check)

### 3.1 Motivation

Les codes de surface ont un taux de code $k/n \to 0$. Pour les ordinateurs à grande échelle, on veut un **taux de code non nul** :

$$
\frac{k}{n} = \Theta(1)
$$

### 3.2 Définition

Un code QLDPC est un code stabilisateur dont les générateurs ont un **poids constant** (chaque stabilisateur agit sur un nombre borné de qubits) et où chaque qubit est impliqué dans un nombre borné de stabilisateurs.

$$
\text{Matrice de parité } H \in \mathbb{F}_2^{m \times 2n} \quad \text{avec densité} \to 0
$$

### 3.3 Paramètres clés

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

### 3.4 Codes QLDPC par hypergraphes

Les codes QLDPC sont construits à partir de **graphes expanseurs** ou d'hypergraphes aléatoires :

```python
import numpy as np
import stim

def qldpc_code_circuit(n_data, n_checks, weight=4):
    """
    Génère un circuit de code QLDPC aléatoire.
    
    Args:
        n_data: nombre de qubits de données
        n_checks: nombre de stabilisateurs
        weight: poids de chaque stabilisateur
    
    Returns:
        circuit Stim
    """
    circuit = stim.Circuit()
    n_ancilla = n_checks
    n = n_data + n_ancilla
    
    # Initialisation
    circuit.append('R', range(n))
    
    # Génération aléatoire de la matrice de parité
    # Chaque stabilisateur est un produit de poids 'weight' opérateurs Pauli
    np.random.seed(0)
    
    # Pour chaque stabilisateur, choisir aléatoirement des qubits et des types
    for check in range(n_checks):
        ancilla = n_data + check
        
        # Choisir 'weight' qubits de données aléatoires
        qubits = np.random.choice(n_data, size=weight, replace=False)
        
        # Pour chaque qubit, choisir aléatoirement X ou Z
        types = np.random.choice(['X', 'Z'], size=weight)
        
        for q, t in zip(qubits, types):
            if t == 'X':
                circuit.append('CX', [ancilla, q])
            else:  # Z
                circuit.append('CX', [q, ancilla])
        
        circuit.append('MR', [ancilla])
    
    return circuit

# Test avec un petit code
n_data, n_checks = 10, 6
qc = qldpc_code_circuit(n_data, n_checks, weight=3)
print(f"Code QLDPC ({n_data} data, {n_checks} checks) : {len(qc)} instructions")
```

### 3.5 Décodage QLDPC

Le décodage des codes QLDPC est plus complexe que pour les codes de surface :

```python
import numpy as np

class BeliefPropagationDecoder:
    """
    Décodeur Belief Propagation pour codes QLDPC.
    Implémente l'algorithme SPA (Sum-Product Algorithm).
    """
    
    def __init__(self, H):
        """
        Args:
            H: matrice de parité binaire (checks x qubits)
        """
        self.H = H
        self.n_checks, self.n_qubits = H.shape
        
        # Graphe de Tanner : liste des voisins
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
            erreur estimée (vecteur binaire)
        """
        n = self.n_qubits
        m = self.n_checks
        
        # Probabilités a priori (taux d'erreur physique)
        p0 = 0.99 * np.ones(n)  # P(e_j = 0)
        p1 = 0.01 * np.ones(n)  # P(e_j = 1)
        
        # Messages qubit -> check
        m_qc = np.zeros((n, max(self.qubit_neighbors[j][0] if self.qubit_neighbors[j] else 0 for j in range(n)) + 1 if n > 0 else 1))
        
        # Version simplifiée : décodage par majorité locale
        error = np.zeros(n, dtype=int)
        
        for iteration in range(max_iter):
            # Pour chaque check : violation = 1 si syndrome != parité des erreurs
            violations = np.zeros(m, dtype=int)
            for i in range(m):
                parity = sum(error[j] for j in self.check_neighbors[i]) % 2
                if parity != syndrome[i]:
                    violations[i] = 1
            
            if np.sum(violations) == 0:
                break
            
            # Mise à jour : flipper les qubits les plus "suspects"
            # Score = nombre de checks violés connectés
            scores = np.zeros(n)
            for j in range(n):
                for i in self.qubit_neighbors[j]:
                    if violations[i]:
                        scores[j] += 1
            
            # Flipper avec probabilité proportionnelle au score
            for j in range(n):
                if scores[j] > 0 and np.random.random() < 0.5:
                    error[j] ^= 1
        
        return error

# Test du décodeur
np.random.seed(42)
n_data, n_checks = 20, 10

# Matrice de parité aléatoire
H = np.random.randint(0, 2, (n_checks, n_data))

# Syndrome aléatoire
error_true = np.random.randint(0, 2, n_data)
syndrome = (H @ error_true) % 2

decoder = BeliefPropagationDecoder(H)
error_pred = decoder.decode(syndrome)

print(f"Erreur vraie :     {error_true}")
print(f"Erreur prédite :  {error_pred}")
print(f"Correct : {np.array_equal(error_true, error_pred)}")
```

---

## 4. Architecture SHYPS (Photonic Inc.)

### 4.1 Principe

SHYPS (**Scalable Holographic Yield-Protected Storage**) est une architecture de correction d'erreur développée par Photonic Inc. qui combine :

- Codes QLDPC basés sur des **hypergraphes**
- Connexions photoniques pour la **non-localité**
- **Décodage holographique** utilisant l'information globale

### 4.2 Avantages

- Taux de code élevé : $k/n \approx 0.3-0.5$
- Distance évoluant comme $d = \Theta(n^{0.48})$
- Tolérable à la perte de photons (avantage majeur pour le photonique)

### 4.3 Simulation d'un code SHYPS-like

```python
import numpy as np
import stim

def shyps_like_circuit(n_logical, p_loss=0.01):
    """
    Circuit simplifié simulant un code de type SHYPS.
    
    Les codes SHYPS utilisent des hypergraphes aléatoires
    avec une structure particulière (lifts de graphes de Ramanujan).
    """
    # Paramètres (simplifiés)
    n_data = 4 * n_logical
    n_checks = 3 * n_logical
    n = n_data + n_checks
    
    circuit = stim.Circuit()
    circuit.append('R', range(n))
    
    # Perte de photons (pour l'architecture photonique)
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
        # Connexion à ~6 qubits de données
        for offset in range(6):
            data_idx = (check_idx * 3 + offset * 7) % n_data
            # Alternance X/Z
            if offset % 2 == 0:
                circuit.append('CX', [ancilla, data_idx])
            else:
                circuit.append('CX', [data_idx, ancilla])
        circuit.append('MR', [ancilla])
    
    return circuit

# Estimation du taux de code
n_log = 10
sc = shyps_like_circuit(n_log)

# Ratio
n_data = 4 * n_log
n_checks = 3 * n_log
print(f"Architecture SHYPS-like ({n_log} qubits logiques) :")
print(f"  Qubits données : {n_data}")
print(f"  Qubits auxiliaires : {n_checks}")
print(f"  Taux de code : {n_log / (n_data + n_checks):.3f}")
print(f"  Instructions circuit : {len(sc)}")
```

---

## 5. Comparaison des architectures

### 5.1 Tableau comparatif

| Critère | Surface | Couleur | Floquet | QLDPC | SHYPS |
|---------|---------|---------|---------|-------|-------|
| $k/n$ | $\Theta(1/\sqrt{n})$ | $\Theta(1/\sqrt{n})$ | $\Theta(1/\sqrt{n})$ | $\Theta(1)$ | $\Theta(1)$ |
| $d$ | $\Theta(\sqrt{n})$ | $\Theta(\sqrt{n})$ | $\Theta(\sqrt{n})$ | $\Theta(\sqrt{n})$ | $\Theta(n^{0.48})$ |
| Connectivité | 2D, 4-voisins | 2D, 6-voisins | 2D, 2-voisins | 3D+ / non-locale | Non-locale |
| Seuil | $\sim 1\%$ | $\sim 0.5\%$ | $\sim 0.7\%$ | $\sim 0.1\%$ | N/A |
| Décodage | MWPM (polynomial) | MWPM | MWPM adapté | BP + OSD | Holographique |
| Portes logiques | Lattice surgery | Transversales | Téléportation | Téléportation | Fusion-based |

### 5.2 Estimation du coût pour 100 qubits logiques

```python
import numpy as np

def cost_estimate(architecture, n_logical, p_phys=1e-3):
    """
    Estime le nombre de qubits physiques nécessaires pour
    obtenir n_logical qubits logiques à un taux d'erreur cible.
    """
    target_pL = 1e-12  # Erreur logique cible
    
    if architecture == "surface":
        # k/n ~ 1/(d^2), p_L ~ (p/p_th)^((d+1)/2)
        p_th = 0.01
        for d in range(3, 50, 2):
            pL = (p_phys / p_th) ** ((d + 1) // 2)
            if pL < target_pL:
                n_per_logical = 2 * d * d  # rotatif
                return n_per_logical * n_logical, d
    
    elif architecture == "qldpc":
        # k/n ~ 0.3, d ~ sqrt(n)
        code_rate = 0.3
        n_total = int(n_logical / code_rate)
        d = int(np.sqrt(n_total))
        # Vérification du taux d'erreur
        return n_total, d
    
    elif architecture == "shyps":
        # k/n ~ 0.4, d ~ n^0.48
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

### 5.3 Compromis fondamentaux

$$
\text{Coût} \propto \frac{\text{nombre de qubits logiques}}{\text{taux de code}} \times \text{facteur de distillaion}
$$

Le choix de l'architecture dépend de la plateforme physique :

- **Supraconducteurs** (Google, IBM) : codes de surface (connectivité limitée)
- **Atomes neutres** (Harvard/QuEra) : codes QLDPC (reconfigurables)
- **Photonique** (Photonic Inc.) : SHYPS (perte tolérante)
- **Ions piégés** (Oxford Ionics) : codes de couleur (connectivité tous-à-tous)

```python
# Comparaison des architectures pour différents budgets
print("Nombre de qubits logiques réalisables par architecture :")
budgets = [1000, 10000, 100000]

for budget in budgets:
    results = {}
    # Surface : ~200 qubits/logique (d=7, pL=~1e-5)
    n_surface = budget // 200
    # QLDPC : ~3.3 qubits/logique
    n_qldpc = int(budget * 0.3)
    # SHYPS : ~2.5 qubits/logique
    n_shyps = int(budget * 0.4)
    
    print(f"  Budget {budget:6d} qubits:")
    print(f"    Surface : {n_surface:4d} qubits logiques")
    print(f"    QLDPC   : {n_qldpc:4d} qubits logiques")
    print(f"    SHYPS   : {n_shyps:4d} qubits logiques")
```

---

## 6. Tendances et perspectives

### 6.1 Codes QLDPC chez IBM (2025)

IBM a démontré un code QLDPC $[\![72, 12, 6]\!]$ sur leur processeur Heron :

- Taux : 16.7%
- Distance : 6 (corrige 2 erreurs)
- Décodage par Belief Propagation + Ordered Statistics Decoding

### 6.2 Codes de Floquet chez Google (2025)

Google explore les codes de Floquet pour réduire le nombre de qubits auxiliaires :

- Surface code modifié avec séquence Floquet
- Réduction de 30% du nombre de qubits
- Compatible avec le décodage MWPM standard

### 6.3 Défis ouverts

1. **Décodage temps réel** : les décodeurs QLDPC sont trop lents pour le feedback en temps réel
2. **Connectivité non-locale** : difficile à réaliser dans la plupart des plateformes
3. **Tolérance aux fuites** : les qubits peuvent fuir hors de l'espace de calcul
4. **Codes QLDPC avec bonne distance** : existence de familles avec $d = \Theta(n)$ ?

---

## Exercices

1. Implémenter un code de couleur triangulaire de distance 5 avec Stim. Compter le nombre de qubits et de stabilisateurs.

2. Comparer les taux d'erreur logique pour un code de surface et un code QLDPC de même nombre de qubits physiques ($n=100$).

3. Simuler un code de Floquet avec Stim pour 5 rounds et calculer le taux d'erreur logique avec pymatching.

4. **Recherche** : Lire l'article "High-rate quantum LDPC codes" (Panteleev & Kalachev, 2022) et résumer la construction.

5. Implémenter un décodeur Belief Propagation + OSD pour un petit code QLDPC et le comparer à MWPM.

6. **Projet** : Estimer le nombre de qubits physiques nécessaires pour exécuter l'algorithme de Shor sur un entier RSA-2048 avec chaque architecture de correction.
