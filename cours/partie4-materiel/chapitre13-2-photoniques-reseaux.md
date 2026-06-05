# Chapitre 13.2 — Qubits photoniques et réseaux quantiques

## Objectifs

- Comprendre le calcul quantique linéaire optique (LOQC)
- Analyser l'architecture Entanglement-First de Photonic Inc.
- Maîtriser les codes QLDPC SHYPS
- Étudier les réseaux quantiques et répéteurs
- Simuler la distribution d'intrication et les pertes dans une fibre avec QuTiP
- Comprendre l'Internet quantique

---

## 1. Calcul quantique linéaire optique (LOQC)

### 1.1 Qubits photoniques

Les qubits sont encodés dans les états de la lumière :

$$
|0_L\rangle = |1\rangle_a |0\rangle_b, \quad |1_L\rangle = |0\rangle_a |1\rangle_b \quad \text{(encodage dual-rail)}
$$

où $a$ et $b$ sont deux modes optiques distincts (polarisation, chemin, ou modes temporels).

### 1.2 Opérations linéaires

Les portes sont réalisées avec des éléments optiques linéaires :

- **Beam splitter** : rotation entre modes

$$
U_{\text{BS}} = \begin{pmatrix} \cos\theta & -i\sin\theta \\ -i\sin\theta & \cos\theta \end{pmatrix}
$$

- **Phase shifter** : phase relative

$$
U_{\phi} = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\phi} \end{pmatrix}
$$

- **Porte CNOT** : nécessite une non-linéarité (mesure auxiliaire + feed-forward)

### 1.3 Limitations et solutions

La **KLM protocol** (Knill, Laflamme, Milburn, 2001) montre que le LOQC universel est possible avec :

- États de base (squeezed states, single photons)
- Mesures photon-number resolving
- Feed-forward classique

$$
P_{\text{succès CNOT}} \sim \frac{1}{16} \quad \text{(KLM original)}
$$

Les techniques modernes (fusion gates, cluster states) augmentent ce taux.

---

## 2. Architecture Entanglement-First (Photonic Inc.)

### 2.1 Principe

L'architecture **Entanglement-First** de Photonic Inc. inverse l'ordre traditionnel :

1. Distribuer l'intrication entre les nœuds via des photons
2. Utiliser cette intrication pour réaliser des portes logiques

Cette approche est particulièrement adaptée aux codes QLDPC qui nécessitent une connectivité non-locale.

### 2.2 Blocs de construction

Les qubits sont stockés dans des **mémoires quantiques** (centres NV diamant, qubits de spin) :

$$
|\psi\rangle_{\text{spin}} \xrightarrow{\text{SWAP}} |\psi\rangle_{\text{photon}}
$$

Les photons intriqués sont transportés par fibres optiques pour créer un **réseau d'intrication** :

$$
|\Phi^+\rangle = \frac{1}{\sqrt{2}} (|00\rangle + |11\rangle)
$$

### 2.3 Performance

Photonic Inc. (2025) : démonstration de 100+ qubits logiques avec des codes QLDPC.

| Métrique | Valeur |
|----------|--------|
| Fidélité portes logiques | $> 99\%$ |
| Taux de génération d'intrication | $> 10^3$ paires/s |
| Distance de fibre démontrée | $> 50$ km |
| Durée de vie mémoire | $> 1$ ms |

---

## 3. Codes QLDPC SHYPS

### 3.1 SHYPS (Scalable Holographic Yield-Protected Storage)

SHYPS est un code QLDPC développé par Photonic Inc. :

- **Hypergraphe de Tanner** à haute dimension
- Degré de connectivité $d_v, d_c \sim O(1)$
- Distance $d \sim O(n)$ pour $n$ qubits
- Taux de code $k/n \sim 0.1-0.5$

$$
H = \begin{pmatrix} H_X & 0 \\ 0 & H_Z \end{pmatrix}, \quad H_X H_Z^T = 0
$$

### 3.2 Avantages pour la photonique

- Tolérance à la perte de photons (loss-tolerant)
- Décodage parallélisé
- Connectivity matching avec l'architecture Entanglement-First

```python
import numpy as np
from scipy.sparse import csr_matrix

def generate_shyps_like_code(n_data, dv=3, dc=6):
    n_checks = n_data * dv // dc
    H = np.zeros((n_checks, n_data), dtype=int)

    for c in range(n_checks):
        cols = np.random.choice(n_data, dc, replace=False)
        H[c, cols] = 1

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

n_q = 100
dv_q = 3
dc_q = 6

H_X, _ = generate_shyps_like_code(n_q, dv_q, dc_q)
H_Z, _ = generate_shyps_like_code(n_q, dv_q, dc_q)

commutator = (H_X @ H_Z.T) % 2
print(f"Condition CSS: H_X @ H_Z^T = 0 mod 2 : {np.all(commutator == 0)}")
print(f"Taux de code approx: 1 - {2*H_X.shape[0]}/{n_q} = {1 - 2*H_X.shape[0]/n_q:.3f}")

rate = 1 - 2 * H_X.shape[0] / n_q
print(f"Nombre de qubits de donnees : {n_q}")
print(f"Nombre de checks X/Z : {H_X.shape[0]}")
print(f"Taux du code : {rate:.3f}")
```

**Sortie attendue :**

```
Condition CSS: H_X @ H_Z^T = 0 mod 2 : False
Taux de code approx: 1 - 100/100 = 0.000
Nombre de qubits de donnees : 100
Nombre de checks X/Z : 50
Taux du code : 0.000
```

---

## 4. Réseaux quantiques et Internet quantique

### 4.1 Architecture

L'Internet quantique connecte des processeurs quantiques via des canaux optiques :

$$
\text{Nœud A} \xrightarrow{\text{fibre optique}} \text{Répéteur} \xrightarrow{\text{fibre optique}} \text{Nœud B}
$$

Les **répéteurs quantiques** sont nécessaires pour dépasser la distance limite des fibres ($\sim 100$ km).

### 4.2 Pertes dans une fibre

L'atténuation dans une fibre optique suit la loi de Beer-Lambert :

$$
P(L) = P_0 \cdot 10^{-\alpha L/10}
$$

où $\alpha \approx 0.2$ dB/km pour les fibres standard à 1550 nm.

### 4.3 Taux de distribution d'intrication

Le taux de paires intriquées distribuées sur une distance $L$ est :

$$
R(L) = R_0 \cdot \eta_{\text{fibre}}(L) \cdot \eta_{\text{détection}} \cdot \eta_{\text{correction}}
$$

avec $\eta_{\text{fibre}} = 10^{-\alpha L/10}$.

```python
import numpy as np
import qutip as qt

alpha = 0.2
L = 50.0
efficiency_fiber = 10 ** (-alpha * L / 10)
print(f"Efficacite fibre ({L} km, {alpha} dB/km): {efficiency_fiber:.4f}")

psi_bell = (qt.basis(2, 0) * qt.basis(2, 0).dag() + qt.basis(2, 1) * qt.basis(2, 1).dag()).unit()
rho_bell = psi_bell * psi_bell.dag()

loss_rate = 1 - efficiency_fiber
c_ops_loss = [
    np.sqrt(loss_rate) * qt.tensor(qt.destroy(2), qt.identity(2)),
    np.sqrt(loss_rate) * qt.tensor(qt.identity(2), qt.destroy(2)),
]

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

fidelity_bell = []
for rho_t in result_loss.states:
    overlap = (psi_bell.dag() * rho_t * psi_bell).real
    fidelity_bell.append(overlap)

print(f"Fidelite initiale avec l'etat Bell: {fidelity_bell[0]:.4f}")
print(f"Fidelite finale apres pertes: {fidelity_bell[-1]:.4f}")

L_range = np.array([10, 50, 100, 200, 500, 1000])
eff_range = 10 ** (-alpha * L_range / 10)

for L_val, eff in zip(L_range, eff_range):
    print(f"L = {L_val:4d} km: efficacite = {eff:.2e}")

T_rep = 1e-6
R0 = 1e9
L_vals = np.array([10, 50, 100])
for L_val in L_vals:
    eff_fiber = 10 ** (-alpha * L_val / 10)
    rate = R0 * eff_fiber * 0.5
    print(f"L = {L_val} km: taux = {rate:.2e} paires/s")
```

---

## 5. Distribution d'intrication simulée

```python
import numpy as np
import qutip as qt

def bell_state():
    psi = (qt.basis(2, 0) * qt.basis(2, 0).dag() + qt.basis(2, 1) * qt.basis(2, 1).dag()).unit()
    return psi

def simulate_channel_loss(rho_in, loss_prob, t_max=1.0):
    c_ops = [
        np.sqrt(loss_prob) * qt.tensor(qt.destroy(2), qt.identity(2)),
        np.sqrt(loss_prob) * qt.tensor(qt.identity(2), qt.destroy(2)),
    ]
    tlist = np.linspace(0, t_max, 50)
    result = qt.mesolve(qt.tensor(qt.qeye(2), qt.qeye(2)), rho_in, tlist, c_ops=c_ops, e_ops=[])
    return result.states[-1], result

psi_bell = bell_state()
rho_bell = psi_bell * psi_bell.dag()

for loss in [0.0, 0.1, 0.3, 0.5, 0.9]:
    rho_final, _ = simulate_channel_loss(rho_bell, loss, 1.0)
    fid = (psi_bell.dag() * rho_final * psi_bell).real
    print(f"Perte={loss:.1f}: Fidelite Bell={fid:.4f}")

L_real = 100.0
alpha_real = 0.2
total_loss = 1 - 10 ** (-alpha_real * L_real / 10)

rho_real, result_real = simulate_channel_loss(rho_bell, total_loss, 1.0)
fid_real = (psi_bell.dag() * rho_real * psi_bell).real

print(f"\nFibre {L_real}km ({alpha_real}dB/km):")
print(f"  Perte totale: {total_loss:.4f}")
print(f"  Fidelite Bell residuelle: {fid_real:.4f}")

print("\nAmelioration avec repeteurs:")
for n_rep in [0, 1, 2, 3]:
    L_seg = L_real / (n_rep + 1)
    loss_seg = 1 - 10 ** (-alpha_real * L_seg / 10)
    eff_seg = 1 - loss_seg
    total_eff = eff_seg ** (n_rep + 1)
    print(f"  {n_rep} repeteur(s) (segment {L_seg:.1f}km): efficacite totale = {total_eff:.4f}")
```

---

## 6. Défis et perspectives

### 6.1 Défis techniques

| Défi | Problème | Approche |
|------|----------|----------|
| Perte de photons | $\propto 10^{-\alpha L/10}$ | Répéteurs, multiplexage |
| Fidélité des portes | Portes probabilistes | Fusion gates, purification |
| Mémoire quantique | Cohérence limitée | Centres NV, qubits de spin |
| Synchronisation | Arrivée temporelle des photons | Buffer optique, mémoire |

### 6.2 Simulation d'un répéteur quantique

```python
import numpy as np
import qutip as qt

def bell_state_pair():
    psi = (qt.basis(4, 0) + qt.basis(4, 3)).unit()
    return psi

def entanglement_swap(rho_AB, rho_BC):
    rho_ABC = qt.tensor(rho_AB, qt.identity(2))

    U_swap = qt.tensor(
        qt.qeye(2),
        qt.swap(),
        qt.qeye(2)
    )

    rho_swapped = U_swap * rho_ABC * U_swap.dag()

    psi_bell = bell_state_pair()
    P_bell = psi_bell * psi_bell.dag()
    P_bell_AB = qt.tensor(P_bell, qt.identity(2))

    rho_post = P_bell_AB * rho_swapped * P_bell_AB.dag()
    rho_post = rho_post / rho_post.tr()

    rho_AC = qt.ptrace(rho_post, [2, 3])
    return rho_AC

L1 = 50.0
L2 = 50.0
alpha_f = 0.2

eff1 = 10 ** (-alpha_f * L1 / 10)
eff2 = 10 ** (-alpha_f * L2 / 10)

rho_bell = bell_state_pair() * bell_state_pair().dag()
psi_bell = bell_state_pair()

c_ops1 = [np.sqrt(1-eff1) * qt.tensor(qt.destroy(2), qt.identity(2))]
c_ops2 = [np.sqrt(1-eff2) * qt.tensor(qt.identity(2), qt.destroy(2))]

tlist_rep = np.linspace(0, 1, 10)
result1 = qt.mesolve(qt.qeye(4), rho_bell, tlist_rep, c_ops=c_ops1, e_ops=[])
result2 = qt.mesolve(qt.qeye(4), rho_bell, tlist_rep, c_ops=c_ops2, e_ops=[])

rho_AB_lossy = result1.states[-1]
rho_BC_lossy = result2.states[-1]

rho_AC = entanglement_swap(rho_AB_lossy, rho_BC_lossy)

fid_AC = (psi_bell.dag() * rho_AC * psi_bell).real
print(f"Fidelite Bell apres echange d'intrication (L={L1+L2}km): {fid_AC:.4f}")

direct_eff = 10 ** (-alpha_f * (L1+L2) / 10)
rho_direct = result1.states[-1]
rho_direct_lossy = qt.tensor(
    (1-direct_eff) * qt.basis(2, 0) * qt.basis(2, 0).dag() + direct_eff * qt.basis(2, 1) * qt.basis(2, 1).dag(),
    qt.identity(2)
)
rho_direct_lossy = rho_direct_lossy / rho_direct_lossy.tr()
print(f"Comparaison - transmission directe {L1+L2}km: efficacite {direct_eff:.4f}")
```

### 6.3 Feuille de route

$$
N_{\text{log}}(t) = N_0 \exp(t/\tau_{\text{scale}})
$$

avec $\tau_{\text{scale}} \sim 1-2$ ans pour les plateformes photoniques.

---

## 7. Exercices

1. **Perte dans une fibre** : Tracer la fidélité d'un état de Bell distribué en fonction de la distance (0 à 500 km). À quelle distance la fidélité tombe-t-elle en dessous de 0.5 ?

2. **Répéteur quantique** : Simuler un répéteur quantique basé sur l'échange d'intrication. Comparer la fidélité finale avec et sans répéteur pour $L=200$ km.

3. **Code SHYPS** : Générer une matrice de parité $H$ pour un code SHYPS avec $n=100$, $d_v=4$, $d_c=8$. Vérifier la condition CSS. Calculer le taux.

4. **Porte de fusion** : Simuler la fusion de deux états de Bell (Type II fusion gate) avec QuTiP. Mesurer la probabilité de succès et la fidélité.

5. **Architecture réseau** : Concevoir un réseau de 10 nœuds quantiques avec répéteurs. Simuler la distribution d'un état de Greenberger-Horne-Zeilinger (GHZ) à 10 parties.

---

## Références

- **Photonic Inc.** (2025). "Entanglement-First architecture for fault-tolerant quantum computing." *Nature Photonics*. [Pho25]
- **Knill, E., Laflamme, R. & Milburn, G.J.** (2001). "A scheme for efficient quantum computation with linear optics." *Nature*, 409, 46–52.
- **Kok, P.** et al. (2007). "Linear optical quantum computing with photonic qubits." *Rev. Mod. Phys.*, 79, 135.
- **Kimble, H.J.** (2008). "The quantum internet." *Nature*, 453, 1023–1030.
- **Wehner, S.** et al. (2018). "Quantum internet: A vision for the road ahead." *Science*, 362, eaam9288.
- **Briegel, H.-J.** et al. (1998). "Quantum repeaters: The role of imperfect local operations in quantum communication." *Phys. Rev. Lett.*, 81, 5932.
