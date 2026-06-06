# Chapitre 13.2 — Qubits photoniques et réseaux quantiques

## Ce que vous allez apprendre

- Comprendre comment des photons peuvent servir de qubits (encodage dual-rail)
- Maîtriser le calcul quantique linéaire optique (LOQC) et le protocole KLM
- Analyser l'architecture Entanglement-First de Photonic Inc.
- Comprendre les codes QLDPC SHYPS et leur avantage pour la photonique
- Simuler la distribution d'intrication et les pertes dans une fibre avec QuTiP

---

## Motivation

**Le problème de la distance.** Tous les qubits vus précédemment vivent dans un cryostat ou une chambre à vide. Mais comment connecter deux processeurs quantiques situés dans des villes différentes ? Les photons sont la réponse : ce sont les meilleurs porteurs d'information à longue distance — la fibre optique est faite pour eux.

**L'idée photonique.** Un photon peut encoder un qubit dans sa polarisation (horizontal = $|0\rangle$, vertical = $|1\rangle$), dans son chemin (mode $a$ ou mode $b$), ou dans son instant d'arrivée. Les portes sont réalisées avec des miroirs, séparateurs de faisceau et déphaseurs — de l'optique linéaire.

**Le défi.** Les photons n'interagissent PAS entre eux. Or, une porte CNOT nécessite une interaction. La solution du protocole KLM (2001) : utiliser la **mesure** comme interaction effective — on fait interférer les photons, on mesure, et le résultat détermine l'opération.

**L'architecture Entanglement-First.** Photonic Inc. inverse l'approche traditionnelle : on **distribue d'abord** l'intrication entre tous les nœuds, puis on utilise cette intrication pour calculer. Comme préparer tous les ingrédients avant de cuisiner.

---

## Idée principale

Un photon sur un séparateur de faisceau (miroir semi-transparent) a 50% de chances de passer et 50% d'être réfléchi. Avant la mesure, il est dans une superposition « passé + réfléchi » — c'est exactement un qubit !

**Encodage dual-rail** : le qubit vit dans deux modes optiques $a$ et $b$. $|0_L\rangle$ = un photon dans le mode $a$, $|1_L\rangle$ = un photon dans le mode $b$.

**Avantages des photons** : vitesse de la lumière, pas de décohérence (ils n'interagissent avec presque rien), et transport possible sur des centaines de km dans des fibres.

**Le protocole KLM** contourne l'absence d'interaction avec trois ingrédients : (1) photons auxiliaires, (2) mesures photon-number resolving, (3) feed-forward classique. La porte CNOT réussit avec probabilité ~1/16 dans le KLM original, mais les techniques modernes (fusion gates, cluster states) montent à >99%.

---

## Contenu du cours

### Section 1 : Calcul quantique linéaire optique (LOQC)

#### 1.1 Qubits photoniques — encodage dual-rail

$$
|0_L\rangle = |1\rangle_a |0\rangle_b, \quad |1_L\rangle = |0\rangle_a |1\rangle_b \quad \text{(encodage dual-rail)}
$$

**Signification physique :**
- $a$ et $b$ sont deux modes optiques (deux chemins, deux polarisations, ou deux instants)
- $|1\rangle_a$ = un photon dans le mode $a$ ; $|0\rangle_b$ = zéro photon dans le mode $b$
- Le qubit est le sous-espace à 1 photon : exactement un photon, soit dans $a$, soit dans $b$

> **Exemple :** Polarisation : $|0_L\rangle = |H\rangle$, $|1_L\rangle = |V\rangle$. Chemin : $|0_L\rangle$ = bras supérieur, $|1_L\rangle$ = bras inférieur.

#### 1.2 Opérations linéaires — portes à un qubit

**Beam splitter** — rotation entre modes :

$$
U_{\text{BS}} = \begin{pmatrix} \cos\theta & -i\sin\theta \\ -i\sin\theta & \cos\theta \end{pmatrix}
$$

**Signification :** Pour $\theta = \pi/4$ (50/50), c'est l'équivalent d'une porte Hadamard.

**Phase shifter** — phase relative :

$$
U_{\phi} = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\phi} \end{pmatrix}
$$

**Signification :** Un verre d'épaisseur variable ajoute une phase $\phi$ — c'est une rotation $R_z$.

#### 1.3 La porte CNOT — le défi

$$
P_{\text{succès CNOT}} \sim \frac{1}{16} \quad \text{(KLM original)}
$$

Les techniques modernes (fusion gates, cluster states) augmentent ce taux jusqu'à >99%.

---

### Section 2 : Architecture Entanglement-First (Photonic Inc.)

#### 2.1 Principe

1. **Distribuer l'intrication** entre les nœuds via des photons
2. **Utiliser cette intrication** pour réaliser des portes logiques (téléportation de portes)

Les qubits sont stockés dans des **mémoires quantiques** (centres NV diamant, spins) :

$$
|\psi\rangle_{\text{spin}} \xrightarrow{\text{SWAP}} |\psi\rangle_{\text{photon}}
$$

Intrication distribuée par fibres optiques :

$$
|\Phi^+\rangle = \frac{1}{\sqrt{2}} (|00\rangle + |11\rangle)
$$

#### 2.2 Performance — Photonic Inc. (2025)

| Métrique | Valeur |
|----------|--------|
| Fidélité portes logiques | $> 99\%$ |
| Taux de génération d'intrication | $> 10^3$ paires/s |
| Distance de fibre démontrée | $> 50$ km |
| Durée de vie mémoire | $> 1$ ms |

---

### Section 3 : Codes QLDPC SHYPS

#### 3.1 Structure du code

SHYPS (Scalable Holographic Yield-Protected Storage) :
- Hypergraphe de Tanner à haute dimension
- Distance $d \sim O(n)$ pour $n$ qubits
- Taux de code $k/n \sim 0.1-0.5$

$$
H = \begin{pmatrix} H_X & 0 \\ 0 & H_Z \end{pmatrix}, \quad H_X H_Z^T = 0
$$

**Signification :** $H_X$ et $H_Z$ sont les matrices de parité. La condition CSS ($H_X H_Z^T = 0$) assure que les checks X et Z commutent.

#### 3.2 Avantages pour la photonique

- Tolérance à la perte de photons
- Décodage parallélisé
- Connectivité non-locale matching avec l'architecture Entanglement-First

---

### Section 4 : Réseaux quantiques et Internet quantique

#### 4.1 Pertes dans une fibre

L'atténuation suit la loi de Beer-Lambert :

$$
P(L) = P_0 \cdot 10^{-\alpha L/10}
$$

**Signification physique :**
- $\alpha \approx 0.2$ dB/km pour les fibres standard à 1550 nm
- À 100 km : $P/P_0 = 10^{-20/10} = 0.01$ — seulement 1% des photons arrivent !
- À 500 km : $P/P_0 = 10^{-100/10} = 10^{-10}$ — quasi impossible sans répéteurs

#### 4.2 Taux de distribution d'intrication

$$
R(L) = R_0 \cdot \eta_{\text{fibre}}(L) \cdot \eta_{\text{détection}} \cdot \eta_{\text{correction}}
$$

avec $\eta_{\text{fibre}} = 10^{-\alpha L/10}$.

> **Exemple numérique :** $R_0 = 10^9$ paires/s, $\alpha = 0.2$ dB/km, $L = 50$ km :
> $\eta_{\text{fibre}} = 10^{-1} = 0.1$, $R = 10^9 \times 0.1 \times 0.5 = 5 \times 10^7$ paires/s.

#### 4.3 Répéteurs quantiques

Les répéteurs quantiques sont nécessaires pour dépasser ~100 km. Le principe : diviser la distance totale en segments, créer de l'intrication sur chaque segment, puis faire un **échange d'intrication** (entanglement swapping) pour connecter les segments.

**Gain exponentiel :** Sans répéteur, l'efficacité décroît comme $10^{-\alpha L/10}$. Avec $n$ répéteurs (segments de $L/(n+1)$), l'efficacité est $(10^{-\alpha L/(10(n+1))})^{n+1}$ — bien meilleure pour de grandes distances.

---

## Exemple guidé

**Problème :** Calculer l'efficacité de transmission d'une fibre de 100 km avec et sans répéteurs.

**Sans répéteur :**
$$\eta = 10^{-0.2 \times 100/10} = 10^{-2} = 0.01 = 1\%$$

**Avec 1 répéteur (2 segments de 50 km) :**
$$\eta_{\text{seg}} = 10^{-0.2 \times 50/10} = 10^{-1} = 0.1$$
$$\eta_{\text{total}} = 0.1^2 = 0.01 = 1\%$$
Même résultat ! Mais le taux est amélioré car chaque segment est plus rapide.

**Avec 3 répéteurs (4 segments de 25 km) :**
$$\eta_{\text{seg}} = 10^{-0.2 \times 25/10} = 10^{-0.5} \approx 0.316$$
$$\eta_{\text{total}} = 0.316^4 \approx 0.01 = 1\%$$

**Le vrai avantage** des répéteurs n'est pas dans l'efficacité statique mais dans le **taux** : avec des répéteurs, le taux de paires intriquées décroît polynomiallement (au lieu d'exponentiellement) avec la distance.

---

## Implémentation Python

### Simulation des pertes dans une fibre avec QuTiP

```python
# ============================================================
# Simulation des pertes optiques dans une fibre quantique
# On modélise la perte comme un canal de dissipation (Lindblad)
# ============================================================
import numpy as np
import qutip as qt

# --- Paramètres de la fibre ---
alpha = 0.2    # Atténuation (dB/km) — standard pour fibre à 1550 nm
L = 50.0       # Longueur de la fibre (km)

# Efficacité de transmission : fraction de photons qui arrivent
efficiency_fiber = 10 ** (-alpha * L / 10)
print(f"Efficacite fibre ({L} km, {alpha} dB/km): {efficiency_fiber:.4f}")

# --- Préparation de l'état de Bell ---
# |Φ+> = (|00> + |11>) / sqrt(2)
psi_bell = (qt.basis(2, 0) * qt.basis(2, 0).dag() + qt.basis(2, 1) * qt.basis(2, 1).dag()).unit()
rho_bell = psi_bell * psi_bell.dag()

# --- Modélisation des pertes comme opérateurs de Lindblad ---
# La probabilité de perdre un photon est (1 - efficiency)
loss_rate = 1 - efficiency_fiber
c_ops_loss = [
    np.sqrt(loss_rate) * qt.tensor(qt.destroy(2), qt.identity(2)),  # Perte sur le qubit 1
    np.sqrt(loss_rate) * qt.tensor(qt.identity(2), qt.destroy(2)),  # Perte sur le qubit 2
]

# Simulation de l'évolution sous le canal de perte
tlist = np.linspace(0, 1, 100)
rho0 = qt.tensor(qt.basis(2, 0), qt.basis(2, 0)) * qt.tensor(qt.basis(2, 0), qt.basis(2, 0)).dag()

result_loss = qt.mesolve(
    qt.tensor(qt.qeye(2), qt.qeye(2)),
    rho0,
    tlist,
    c_ops=c_ops_loss,
    e_ops=[qt.tensor(qt.basis(2, i) * qt.basis(2, j).dag(), qt.basis(2, k) * qt.basis(2, l).dag())
           for i in range(2) for j in range(2) for k in range(2) for l in range(2)]
)

# Calcul de la fidélité avec l'état de Bell au cours du temps
fidelity_bell = []
for rho_t in result_loss.states:
    overlap = (psi_bell.dag() * rho_t * psi_bell).real
    fidelity_bell.append(overlap)

print(f"Fidelite initiale avec l'etat Bell: {fidelity_bell[0]:.4f}")
print(f"Fidelite finale apres pertes: {fidelity_bell[-1]:.4f}")

# --- Bilan pour différentes distances ---
L_range = np.array([10, 50, 100, 200, 500, 1000])
eff_range = 10 ** (-alpha * L_range / 10)

for L_val, eff in zip(L_range, eff_range):
    print(f"L = {L_val:4d} km: efficacite = {eff:.2e}")

# --- Taux de paires intriquées ---
T_rep = 1e-6   # Temps de répétition (s)
R0 = 1e9       # Taux de génération brut (paires/s)
L_vals = np.array([10, 50, 100])
for L_val in L_vals:
    eff_fiber = 10 ** (-alpha * L_val / 10)
    rate = R0 * eff_fiber * 0.5
    print(f"L = {L_val} km: taux = {rate:.2e} paires/s")
```

### Simulation de la distribution d'intrication

```python
# ============================================================
# Distribution d'intrication : fidélité d'un état de Bell
# en fonction de la perte dans le canal
# ============================================================
import numpy as np
import qutip as qt

def bell_state():
    """Crée l'état de Bell |Φ+> = (|00> + |11>)/sqrt(2)."""
    psi = (qt.basis(2, 0) * qt.basis(2, 0).dag() + qt.basis(2, 1) * qt.basis(2, 1).dag()).unit()
    return psi

def simulate_channel_loss(rho_in, loss_prob, t_max=1.0):
    """
    Simule la perte de photons dans un canal quantique.
    loss_prob : probabilité de perdre un photon (0 = pas de perte, 1 = perte totale)
    """
    c_ops = [
        np.sqrt(loss_prob) * qt.tensor(qt.destroy(2), qt.identity(2)),
        np.sqrt(loss_prob) * qt.tensor(qt.identity(2), qt.destroy(2)),
    ]
    tlist = np.linspace(0, t_max, 50)
    result = qt.mesolve(qt.tensor(qt.qeye(2), qt.qeye(2)), rho_in, tlist, c_ops=c_ops, e_ops=[])
    return result.states[-1], result

psi_bell = bell_state()
rho_bell = psi_bell * psi_bell.dag()

# Test pour différentes valeurs de perte
for loss in [0.0, 0.1, 0.3, 0.5, 0.9]:
    rho_final, _ = simulate_channel_loss(rho_bell, loss, 1.0)
    fid = (psi_bell.dag() * rho_final * psi_bell).real
    print(f"Perte={loss:.1f}: Fidelite Bell={fid:.4f}")

# Cas réel : fibre de 100 km
L_real = 100.0
alpha_real = 0.2
total_loss = 1 - 10 ** (-alpha_real * L_real / 10)

rho_real, result_real = simulate_channel_loss(rho_bell, total_loss, 1.0)
fid_real = (psi_bell.dag() * rho_real * psi_bell).real

print(f"\nFibre {L_real}km ({alpha_real}dB/km):")
print(f"  Perte totale: {total_loss:.4f}")
print(f"  Fidelite Bell residuelle: {fid_real:.4f}")

# --- Amélioration avec des répéteurs ---
print("\nAmelioration avec repeteurs:")
for n_rep in [0, 1, 2, 3]:
    L_seg = L_real / (n_rep + 1)         # Longueur de chaque segment
    loss_seg = 1 - 10 ** (-alpha_real * L_seg / 10)  # Perte par segment
    eff_seg = 1 - loss_seg                # Efficacité par segment
    total_eff = eff_seg ** (n_rep + 1)    # Efficacité totale
    print(f"  {n_rep} repeteur(s) (segment {L_seg:.1f}km): efficacite totale = {total_eff:.4f}")
```

### Simulation d'un répéteur quantique

```python
# ============================================================
# Simulation d'un répéteur quantique par échange d'intrication
# Principe : A-B et B-C intriqués → mesure de Bell en B → A-C intriqués
# ============================================================
import numpy as np
import qutip as qt

def bell_state_pair():
    """Crée une paire de Bell |Φ+> = (|00> + |11>)/sqrt(2)."""
    psi = (qt.basis(4, 0) + qt.basis(4, 3)).unit()
    return psi

def entanglement_swap(rho_AB, rho_BC):
    """
    Échange d'intrication : à partir de A-B et B-C,
    on crée A-C par mesure de Bell sur B.
    """
    rho_ABC = qt.tensor(rho_AB, qt.identity(2))

    # Porte SWAP entre le qubit B de la première paire et le qubit B de la deuxième
    U_swap = qt.tensor(
        qt.qeye(2),
        qt.swap(),
        qt.qeye(2)
    )

    rho_swapped = U_swap * rho_ABC * U_swap.dag()

    # Post-sélection sur l'état de Bell pour A-C
    psi_bell = bell_state_pair()
    P_bell = psi_bell * psi_bell.dag()
    P_bell_AB = qt.tensor(P_bell, qt.identity(2))

    rho_post = P_bell_AB * rho_swapped * P_bell_AB.dag()
    rho_post = rho_post / rho_post.tr()

    rho_AC = qt.ptrace(rho_post, [2, 3])
    return rho_AC

# --- Simulation avec pertes ---
L1 = 50.0   # Distance A-B (km)
L2 = 50.0   # Distance B-C (km)
alpha_f = 0.2  # Atténuation (dB/km)

eff1 = 10 ** (-alpha_f * L1 / 10)  # Efficacité segment A-B
eff2 = 10 ** (-alpha_f * L2 / 10)  # Efficacité segment B-C

rho_bell = bell_state_pair() * bell_state_pair().dag()
psi_bell = bell_state_pair()

# Application des pertes sur chaque segment
c_ops1 = [np.sqrt(1-eff1) * qt.tensor(qt.destroy(2), qt.identity(2))]
c_ops2 = [np.sqrt(1-eff2) * qt.tensor(qt.identity(2), qt.destroy(2))]

tlist_rep = np.linspace(0, 1, 10)
result1 = qt.mesolve(qt.qeye(4), rho_bell, tlist_rep, c_ops=c_ops1, e_ops=[])
result2 = qt.mesolve(qt.qeye(4), rho_bell, tlist_rep, c_ops=c_ops2, e_ops=[])

rho_AB_lossy = result1.states[-1]
rho_BC_lossy = result2.states[-1]

# Échange d'intrication
rho_AC = entanglement_swap(rho_AB_lossy, rho_BC_lossy)

fid_AC = (psi_bell.dag() * rho_AC * psi_bell).real
print(f"Fidelite Bell apres echange d'intrication (L={L1+L2}km): {fid_AC:.4f}")

# Comparaison avec transmission directe (sans répéteur)
direct_eff = 10 ** (-alpha_f * (L1+L2) / 10)
rho_direct = result1.states[-1]
rho_direct_lossy = qt.tensor(
    (1-direct_eff) * qt.basis(2, 0) * qt.basis(2, 0).dag() + direct_eff * qt.basis(2, 1) * qt.basis(2, 1).dag(),
    qt.identity(2)
)
rho_direct_lossy = rho_direct_lossy / rho_direct_lossy.tr()
print(f"Comparaison - transmission directe {L1+L2}km: efficacite {direct_eff:.4f}")
```

### Génération d'un code SHYPS-like

```python
# ============================================================
# Génération d'un code QLDPC de type SHYPS
# Vérification de la condition CSS et calcul du taux
# ============================================================
import numpy as np
from scipy.sparse import csr_matrix

def generate_shyps_like_code(n_data, dv=3, dc=6):
    """
    Génère une matrice de parité de type SHYPS.
    n_data : nombre de qubits de données
    dv : degré des variables (qubits par check)
    dc : degré des checks (qubits par check)
    """
    n_checks = n_data * dv // dc
    H = np.zeros((n_checks, n_data), dtype=int)

    # Attribution aléatoire des qubits aux checks
    for c in range(n_checks):
        cols = np.random.choice(n_data, dc, replace=False)
        H[c, cols] = 1

    # Ajustement pour satisfaire les degrés
    for d in range(n_data):
        row_sum = H[:, d].sum()
        while row_sum < dv:
            available = np.where(H.sum(axis=1) < dc)[0]
            if len(available) == 0:
                break
            c = np.random.choice(available)
            if H[c, d] == 0:
                H[c, d] = 1
                row_sum += 1

    H_sparse = csr_matrix(H)
    return H, H_sparse

# --- Génération et vérification ---
n_q = 100
dv_q = 3
dc_q = 6

H_X, _ = generate_shyps_like_code(n_q, dv_q, dc_q)
H_Z, _ = generate_shyps_like_code(n_q, dv_q, dc_q)

# Vérification de la condition CSS : H_X @ H_Z^T doit être nul (mod 2)
commutator = (H_X @ H_Z.T) % 2
print(f"Condition CSS: H_X @ H_Z^T = 0 mod 2 : {np.all(commutator == 0)}")
print(f"Taux de code approx: 1 - {2*H_X.shape[0]}/{n_q} = {1 - 2*H_X.shape[0]/n_q:.3f}")

rate = 1 - 2 * H_X.shape[0] / n_q
print(f"Nombre de qubits de donnees : {n_q}")
print(f"Nombre de checks X/Z : {H_X.shape[0]}")
print(f"Taux du code : {rate:.3f}")
```

---

## Comparaison des technologies

| Critère | Photonique (Photonic Inc.) | Supraconducteur | Atomes neutres | Ions piégés |
|---------|---------------------------|-----------------|----------------|-------------|
| **Support** | Photons (polarisation/chemin) | Circuit LC | Atomes piégés | Ions piégés |
| **Cohérence** | Excellente (vol) | ~100 µs | >1 s | >10 s |
| **Portes 2Q** | Probabilistes (KLM) | 99.97% | 99.5% | 99.99% |
| **Connectivité** | Réseau (non-local) | Grille 2D | Reconfigurable | Chaîne 1D |
| **Distance** | >50 km (fibre) | <1 m (cryostat) | <1 mm | <1 mm |
| **Température** | Ambiante (photons) | ~15 mK | µK | Ultra-vide |
| **Mémoire** | Centres NV (~ms) | Non (volatiles) | Atomes (~s) | Ions (~s) |
| **Point fort** | Réseau, distance | Vitesse | Scaling | Fidélité |
| **Point faible** | Portes probabilistes | Cohérence courte | Portes 2Q | Scaling |

---

## À retenir

1. **L'encodage dual-rail** encode un qubit dans la présence d'un photon dans l'un de deux modes optiques. C'est robuste contre certaines erreurs (perte de photons détectable).

2. **Le protocole KLM** montre que le calcul quantique universel est possible avec de l'optique linéaire + mesures + feed-forward, mais les portes sont probabilistes.

3. **L'architecture Entanglement-First** inverse le paradigme : on crée d'abord l'intrication, puis on calcule. C'est naturellement adapté aux codes QLDPC.

4. **Les pertes dans la fibre** sont le problème n°1 : à 100 km, seulement 1% des photons survivent. Les répéteurs quantiques sont indispensables pour les longues distances.

5. **Les codes SHYPS** sont conçus pour la photonique : tolérance aux pertes, décodage distribué, connectivité non-locale.

6. **L'Internet quantique** connectera des processeurs quantiques distants via des répéteurs quantiques et des mémoires quantiques. C'est un objectif à 10-15 ans.

---

## Pièges à éviter

1. **Confondre perte de photon et erreur de bit** : La perte (le photon disparaît) est une erreur spécifique à la photonique, différente des erreurs X/Z des qubits matériels. Les codes doivent être conçus pour la détecter.

2. **Penser que les photons ne décohèrent jamais** : C'est vrai en vol, mais les éléments optiques (miroirs, fibres) introduisent des erreurs. Et la conversion spin-photon a une fidélité limitée.

3. **Confondre porte déterministe et probabiliste** : Une porte KLM réussit avec probabilité $p < 1$. Il faut des techniques de distillation pour rendre le calcul déterministe, ce qui ajoute un overhead.

4. **Sous-estimer les pertes** : À 100 km, l'atténuation est de 20 dB (facteur 100). Sans répéteurs, le taux de paires intriquées chute exponentiellement. Les répéteurs sont indispensables.

5. **Oublier la synchronisation** : Les photons de différentes sources doivent arriver simultanément sur le séparateur de faisceau pour interférer. La synchronisation temporelle est un défi technique majeur.

---

## Exercices

### Niveau 1 — Application directe

1. **Perte dans une fibre** : Calculer l'efficacité de transmission pour $L = 10, 50, 100, 200$ km avec $\alpha = 0.2$ dB/km. À quelle distance l'efficacité tombe-t-elle en dessous de 1% ?

2. **Exécuter le code** : Reproduire la simulation des pertes dans une fibre avec QuTiP et vérifier les résultats.

3. **Code SHYPS** : Générer une matrice de parité $H$ pour $n=100$, $d_v=4$, $d_c=8$. Calculer le taux du code.

### Niveau 2 — Compréhension

4. **Fidélité vs distance** : Tracer la fidélité d'un état de Bell distribué en fonction de la distance (0 à 500 km). À quelle distance la fidélité tombe-t-elle en dessous de 0.5 ?

5. **Répéteur quantique** : Simuler un répéteur basé sur l'échange d'intrication. Comparer la fidélité finale avec et sans répéteur pour $L=200$ km.

6. **Porte de fusion** : Simuler la fusion de deux états de Bell (Type II fusion gate) avec QuTiP. Mesurer la probabilité de succès et la fidélité.

### Niveau 3 — Défi

7. **Architecture réseau** : Concevoir un réseau de 10 nœuds quantiques avec répéteurs. Simuler la distribution d'un état GHZ à 10 parties.

8. **Optimisation de répéteurs** : Pour $L = 1000$ km, trouver le nombre optimal de répéteurs qui maximise le taux de paires intriquées.

9. **Comparaison de codes** : Comparer l'overhead d'un code de surface vs un code SHYPS pour la photonique, en tenant compte des pertes.

---

## Pour aller plus loin

- **Photonic Inc.** (2025). "Entanglement-First architecture for fault-tolerant quantum computing." *Nature Photonics*.
- **Knill, E., Laflamme, R. & Milburn, G.J.** (2001). "A scheme for efficient quantum computation with linear optics." *Nature*, 409, 46–52.
- **Kok, P.** et al. (2007). "Linear optical quantum computing with photonic qubits." *Rev. Mod. Phys.*, 79, 135.
- **Kimble, H.J.** (2008). "The quantum internet." *Nature*, 453, 1023–1030.
- **Wehner, S.** et al. (2018). "Quantum internet: A vision for the road ahead." *Science*, 362, eaam9288.
- **Briegel, H.-J.** et al. (1998). "Quantum repeaters: The role of imperfect local operations in quantum communication." *Phys. Rev. Lett.*, 81, 5932.
