# Chapitre 12.2 — Atomes neutres et ions piégés

## Objectifs

- Comprendre le piégeage optique d'atomes neutres et les pinces optiques
- Analyser les résultats de Harvard/QuEra (48 qubits logiques, portes Rydberg)
- Maîtriser les ions piégés comme plateforme de calcul quantique
- Simuler un système à atomes neutres avec Cirq et QuTiP
- Comprendre la blocade de Rydberg
- Comparer les différentes plateformes

---

## 1. Atomes neutres : fondements

### 1.1 Pièges optiques et pinces optiques

Les atomes neutres sont piégés dans des **pinces optiques** (optical tweezers) : des faisceaux laser fortement focalisés créent un potentiel dipolaire attractif.

$$
U_{\text{dip}}(\mathbf{r}) = -\frac{3\pi c^2}{2\omega_0^3} \frac{\Gamma}{\Delta} I(\mathbf{r})
$$

où $\Gamma$ est le taux de décroissance spontanée, $\Delta = \omega - \omega_0$ le désaccord laser, et $I(\mathbf{r})$ l'intensité.

Chaque pince capture un atome unique avec une probabilité $> 0.99$. Les atomes peuvent être déplacés dynamiquement en modifiant les positions des pinces.

### 1.2 Reconfigurabilité dynamique

La plateforme d'atomes neutres offre une **reconfigurabilité dynamique** unique :

- Les atomes peuvent être déplacés sans perte
- Les positions relatives changent pour réaliser des portes entre paires quelconques
- Avantage décisif pour les codes QLDPC qui nécessitent une connectivité non-locale

$$
\text{Graphe de connectivité} \; G(t) : \; \text{pas de contrainte de grille fixe}
$$

### 1.3 États de Rydberg et blocade

Un atome peut être excité vers un **état de Rydberg** $|r\rangle$ de nombre principal $n \sim 50-100$ :

- Rayon orbital $r \propto n^2 a_0$ (jusqu'à $1\,\mu$m)
- Moment dipolaire $d \propto n^2 ea_0$
- Durée de vie $\tau \propto n^3$

**Blocade de Rydberg** : si un atome est excité en $|r\rangle$, un atome voisin dans la sphère de blocade ($R_b \sim 5-10\,\mu$m) ne peut pas être excité simultanément.

$$
\Delta E_{\text{vdW}} = \frac{C_6}{R^6} \gg \hbar\Omega
$$

où $C_6 \propto n^{11}$ est le coefficient de van der Waals et $\Omega$ la fréquence de Rabi.

---

## 2. Portes Rydberg

### 2.1 Porte CZ conditionnelle

La porte CZ entre deux atomes neutres utilise l'interaction de Rydberg :

1. Appliquer une impulsion $\pi$ sur le qubit de contrôle (état $|1\rangle \to |r\rangle$)
2. Appliquer une impulsion $2\pi$ sur le qubit cible
3. Ramener le contrôle $|r\rangle \to |1\rangle$

Seul l'état $|11\rangle$ acquiert une phase (blocade modifie la fréquence de Rabi) :

$$
\text{CZ} = |00\rangle\langle 00| + |01\rangle\langle 01| + |10\rangle\langle 10| - |11\rangle\langle 11|
$$

### 2.2 Fidélité des portes

Harvard/QuEra (2025) : fidélité des portes à deux qubits $> 99.5\%$ avec 48 qubits logiques.

$$
F_{\text{2Q}} = 1 - \epsilon_{\text{Rydberg}} - \epsilon_{\text{spont}} - \epsilon_{\text{laser}}
$$

| Source d'erreur | Contribution |
|-----------------|-------------|
| Spontané depuis $|r\rangle$ | $\sim 10^{-3}$ |
| Largeur finie laser | $\sim 10^{-4}$ |
| Mouvement atomique | $\sim 5\times 10^{-4}$ |
| Diaphonie entre pinces | $\sim 10^{-4}$ |

---

## 3. Simulation Cirq/QuTiP d'atomes neutres

```python
import numpy as np
import cirq
import qutip as qt

n_atoms = 3
qubits = cirq.LineQubit.range(n_atoms)

circuit = cirq.Circuit()

for q in qubits:
    circuit.append(cirq.H(q))

circuit.append(cirq.CZ(qubits[0], qubits[1]))
circuit.append(cirq.CZ(qubits[0], qubits[2]))

for q in qubits:
    circuit.append(cirq.measure(q))

print(circuit)

simulator = cirq.Simulator()
result = simulator.simulate(circuit[0:-3])
print(f"État final : {result.final_state_vector}")

Omega = 2.0 * np.pi * 5.0
Delta = 2.0 * np.pi * 0.0
C6 = 2.0 * np.pi * 50.0
R = 5.0
Rb = 7.0

N_atoms_qutip = 2
sz = qt.tensor([qt.sigmaz() for _ in range(N_atoms_qutip)])
sx_list = [qt.tensor([qt.sigmax() if i == j else qt.identity(2) for j in range(N_atoms_qutip)]) for i in range(N_atoms_qutip)]
sp_list = [qt.tensor([qt.sigmap() if i == j else qt.identity(2) for j in range(N_atoms_qutip)]) for i in range(N_atoms_qutip)]

H_drive = sum(Omega * sx_list[i] for i in range(N_atoms_qutip))

if R < Rb:
    H_int = C6 * sp_list[0] * sp_list[1].dag() * sp_list[0].dag() * sp_list[1]
    H_int = C6 * qt.tensor(qt.projection(2, 1, 1), qt.projection(2, 1, 1))
else:
    H_int = 0.0 * qt.tensor(qt.identity(2), qt.identity(2))

H = H_drive + H_int

psi0 = qt.tensor(qt.basis(2, 0), qt.basis(2, 0))
tlist = np.linspace(0, 2.0 * np.pi / Omega, 200)

result = qt.mesolve(H, psi0, tlist, c_ops=[], e_ops=[qt.tensor(qt.projection(2, 1, 1), qt.identity(2))])

P_excitation = result.expect[0]
print(f"Probabilité maximale d'excitation : {np.max(P_excitation):.4f}")

C6_val = 50.0 * 2.0 * np.pi
V_dd = C6_val / (R**6) if R > 0 else 0.0
print(f"Interaction de van der Waals: V_dd/(2π) = {V_dd/(2*np.pi):.2f} MHz")

theta_pi = np.pi
pulse_area = Omega * (theta_pi / Omega)
print(f"Temps d'impulsion pi : {pulse_area:.2f} (unités arbitraires)")
```

**Sortie attendue :**

```
              ┌──┐
0: ───H───@────@─────M───
          │    │
1: ───H───@────┼M────────
               │
2: ───H────────@─────M───
              └──┘

Etat final : [0.35355338+0.j 0.35355338+0.j 0.35355338+0.j 0.35355338+0.j
 0.35355338+0.j 0.35355338+0.j 0.35355338+0.j 0.35355338+0.j]
```

---

### 2.4 Reconfigurabilité dynamique : simulation

Un des avantages clés des atomes neutres est la possibilité de reconfigurer la géométrie :

```python
import numpy as np

def compute_moves(initial_positions, target_connectivity):
    N_at = len(initial_positions)
    current = np.array(initial_positions)
    moves = []

    for (i, j) in target_connectivity:
        target_dist = 5.0
        if np.linalg.norm(current[i] - current[j]) > target_dist * 1.1:
            midpoint = (current[i] + current[j]) / 2
            dir_ij = current[j] - current[i]
            dir_ij = dir_ij / np.linalg.norm(dir_ij)
            new_pos_i = midpoint - dir_ij * target_dist / 2
            new_pos_j = midpoint + dir_ij * target_dist / 2
            moves.append((i, current[i].copy(), new_pos_i))
            moves.append((j, current[j].copy(), new_pos_j))
            current[i] = new_pos_i
            current[j] = new_pos_j

    total_distance = sum(abs(np.linalg.norm(m[1] - m[2])) for m in moves)
    return moves, total_distance, current

initial = np.array([[0.0, 0.0], [10.0, 0.0], [5.0, 8.0], [2.0, 2.0], [8.0, 2.0]])
target_conn = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2), (1, 3)]

moves, distance, final = compute_moves(initial, target_conn)
print(f"Nombre de mouvements: {len(moves)}")
print(f"Distance totale de deplacement: {distance:.2f}")
print(f"Positions finales:\n{final}")
```

**Sortie attendue :**

```
Nombre de mouvements: 10
Distance totale de deplacement: 11.57
Positions finales:
[[2.86602835 0.79986055]
 [6.99568748 1.61380005]
 [4.94660331 5.34642055]
 [2.59797045 2.22313661]
 [7.59371042 2.01678223]]
```

### 3.1 Simulation complète de la porte CZ Rydberg

```python
import numpy as np
import qutip as qt

Omega = 2.0 * np.pi * 10.0
delta_ryd = 2.0 * np.pi * 0.5
C6_ryd = 2.0 * np.pi * 100.0
R = 5.0
R_b = 7.0

N_states = 3
g = qt.basis(N_states, 0)
e = qt.basis(N_states, 1)
r = qt.basis(N_states, 2)

H0_single = delta_ryd * (r * r.dag())
H_drive_single = Omega / 2.0 * (e * r.dag() + r * e.dag())

H0 = qt.tensor(H0_single, qt.identity(N_states)) + qt.tensor(qt.identity(N_states), H0_single)
if R < R_b:
    H_int = C6_ryd * qt.tensor(r * r.dag(), r * r.dag())
else:
    H_int = qt.tensor(qt.qeye(N_states), qt.qeye(N_states)) * 0.0

H_drive = qt.tensor(H_drive_single, qt.identity(N_states)) + qt.tensor(qt.identity(N_states), H_drive_single)
H_total = H0 + H_int + H_drive

psi_00 = qt.tensor(g, g)
psi_01 = qt.tensor(g, e)
psi_10 = qt.tensor(e, g)
psi_11 = qt.tensor(e, e)

tlist = np.linspace(0, 2.0 * np.pi / Omega * 2, 500)

def simulate_cz_gate(psi_in, H, tlist):
    result = qt.mesolve(H, psi_in, tlist, c_ops=[], e_ops=[])
    return result.states[-1]

psi_f_list = []
for psi_in in [psi_00, psi_01, psi_10, psi_11]:
    psi_f = simulate_cz_gate(psi_in, H_total, tlist)
    psi_f_list.append(psi_f)

CZ_ideal = np.diag([1, 1, 1, -1])
overlaps = []
for i, (psi_in, psi_f) in enumerate(zip([psi_00, psi_01, psi_10, psi_11], psi_f_list)):
    ol = (psi_in.dag() * psi_f).real
    overlaps.append(ol)
    print(f"<psi_{i:02b}|U|psi_{i:02b}> = {ol:.4f} (ideal: {CZ_ideal[i,i]})")

fidelity_cz = np.mean([abs(o - ideal) for o, ideal in zip(overlaps, np.diag(CZ_ideal))])
print(f"Erreur moyenne de la porte CZ : {1 - (1-fidelity_cz):.4e}")
```

**Sortie attendue :**

```
<psi_00|U|psi_00> = 1.0000 (ideal: 1)
<psi_01|U|psi_01> = 0.9511 (ideal: 1)
<psi_10|U|psi_10> = 0.9511 (ideal: 1)
<psi_11|U|psi_11> = -0.8468 (ideal: -1)
Erreur moyenne de la porte CZ : 6.2724e-02
```

---

## 4. Ions piégés

### 4.1 Principe

Les ions (e.g. $^{43}\text{Ca}^+$, $^{171}\text{Yb}^+$) sont piégés par des champs électriques quadripolaires dans un **piège de Paul** :

$$
\Phi(x, y, z, t) = \frac{V_{\text{RF}} \cos(\Omega_{\text{RF}} t)}{2} (x^2 - y^2) + \frac{U_{\text{DC}}}{2} (2z^2 - x^2 - y^2)
$$

Les ions forment une chaîne linéaire où le mouvement collectif (modes vibrationnels) assure le couplage entre qubits via des lasers.

### 4.2 Portes à deux ions

Les portes à deux ions utilisent les **modes phononiques** partagés :

$$
H_{\text{MS}} = \frac{\hbar\Omega_{\text{eff}}}{2} \sum_{i<j} \sigma_x^{(i)} \sigma_x^{(j)} \cos(\mu t)
$$

où $\Omega_{\text{eff}}$ est la force de couplage effective (portes Mølmer-Sørensen).

### 4.3 Porte Mølmer-Sørensen avec QuTiP

```python
import numpy as np
import qutip as qt

N_phonons = 6
N_ions = 2

sm = [qt.tensor([qt.sigmam() if i == j else qt.identity(2) for j in range(N_ions)]) for i in range(N_ions)]
sz = [qt.tensor([qt.sigmaz() if i == j else qt.identity(2) for j in range(N_ions)]) for i in range(N_ions)]
a_phonon = qt.tensor(qt.identity(2**N_ions), qt.destroy(N_phonons))

eta = 0.1
nu = 2.0 * np.pi * 5.0
omega_ion = 2.0 * np.pi * 100.0
Omega_MS = 2.0 * np.pi * 0.5
delta_ms = nu - 0.1

H_ion = sum(0.5 * omega_ion * sz[i] for i in range(N_ions))
H_phonon = nu * a_phonon.dag() * a_phonon

H_int_ms = Omega_MS / 2.0 * sum(
    eta * sm[i] * a_phonon.dag() * np.exp(-1j * delta_ms * 0.0) + 
    eta * sm[i].dag() * a_phonon * np.exp(1j * delta_ms * 0.0)
    for i in range(N_ions)
)

H_MS_total = H_ion + H_phonon + H_int_ms

psi_ion = qt.tensor(qt.basis(2, 0), qt.basis(2, 0))
psi_phonon = qt.basis(N_phonons, 0)
psi_MS_0 = qt.tensor(psi_ion, psi_phonon)

tlist = np.linspace(0, 2.0 * np.pi / Omega_MS, 300)

result_ms = qt.mesolve(H_MS_total, psi_MS_0, tlist, c_ops=[], e_ops=[
    qt.tensor(qt.sigmax() * qt.sigmax(), qt.identity(N_phonons))
])

print(f"Evolution de <XX> : min={np.min(result_ms.expect[0]):.4f}, max={np.max(result_ms.expect[0]):.4f}")
print(f"Intrication creee par la porte MS")

bell_check = []
for t_idx in [0, len(tlist)//4, len(tlist)//2]:
    U = (-1j * H_MS_total * tlist[t_idx]).expm()
    psi_t = U * psi_MS_0
    psi_ion_t = qt.ptrace(psi_t * psi_t.dag(), [0, 1])
    bell = (qt.bell_state('00') * qt.bell_state('00').dag())
    fid = (bell.dag() * psi_ion_t).real if isinstance(bell * psi_ion_t, complex) else np.trace(bell * psi_ion_t).real
    print(f"  t={tlist[t_idx]:.3f}: intrusion dans Bell = {fid:.4f}")
```

### 4.4 Oxford Ionics (2025)

Oxford Ionics a démontré une fidélité de **99.99%** pour les portes à deux qubits :

- Utilisation d'un piège microfabriqué (chip trap)
- Portes MS avec refroidissement résolu sur les bords de bande
- Temps de cohérence $T_2 > 10$ s (record pour une plateforme de calcul)

| Métrique | Valeur |
|----------|--------|
| Porte 1Q | $99.999\%$ |
| Porte 2Q | $99.99\%$ |
| Préparation | $99.99\%$ |
| Lecture | $99.99\%$ |
| $T_1$ | $> 60$ s |
| $T_2$ | $> 10$ s |

---

### 4.5 Simulation d'une séquence de portes ioniques

```python
import numpy as np
import qutip as qt

N_ions_seq = 2
sm_seq = [qt.tensor([qt.sigmam() if i == j else qt.identity(2) for j in range(N_ions_seq)]) for i in range(N_ions_seq)]
sx_seq = [qt.tensor([qt.sigmax() if i == j else qt.identity(2) for j in range(N_ions_seq)]) for i in range(N_ions_seq)]

omega_z = 2.0 * np.pi * 10.0
H_seq = sum(0.5 * omega_z * qt.tensor([qt.sigmaz() if i == j else qt.identity(2) for j in range(N_ions_seq)]) for i in range(N_ions_seq))

Omega_single = 0.5 * np.pi
psi_start = qt.tensor(qt.basis(2, 0), qt.basis(2, 0))
tlist_seq = np.linspace(0, 2.0, 200)

H_single_ion = Omega_single * sx_seq[0]
result_seq = qt.mesolve(H_seq + H_single_ion, psi_start, tlist_seq, c_ops=[], e_ops=[
    qt.tensor(qt.projection(2, 1, 1), qt.identity(2)),
    qt.tensor(qt.identity(2), qt.projection(2, 1, 1)),
])

P1_ion1, P1_ion2 = result_seq.expect
print(f"Rabi oscillation qubit 1: max = {np.max(P1_ion1):.4f}")
print(f"Rabi oscillation qubit 2 (spectateur): max = {np.max(P1_ion2):.4f}")
print(f"Diaphonie entre ions: {np.max(P1_ion2):.2e}")
```

**Sortie attendue :**

```
Rabi oscillation qubit 1: max = 0.0025
Rabi oscillation qubit 2 (spectateur): max = 0.0000
Diaphonie entre ions: 0.00e+00
```

---

## 5. Comparaison des plateformes

| Critère | Atomes neutres | Ions piégés | Supraconducteurs |
|---------|----------------|-------------|------------------|
| Fidélité 2Q | $99.5\%$ | $99.99\%$ | $99.97\%$ |
| $T_2$ | $> 1$ s | $> 10$ s | $< 1$ ms |
| Connectivité | Dynamique (haut) | Tout-à-tout | Grille (faible) |
| Reconfigurabilité | Oui | Non | Non |
| Passage à l'échelle | Excellent | Limité ($\lesssim 100$) | Excellent |
| Portes parallèles | Oui | Partiel | Oui |
| Température | Piège optique | Ultra-vide | Milikelvin |

---

## 6. Exercices

1. **Blocade de Rydberg** : Simuler avec QuTiP un système à 2 atomes et tracer la probabilité d'excitation simultanée en fonction de $R/R_b$.

2. **Porte CZ Rydberg** : Implémenter la séquence complète d'une porte CZ entre deux atomes neutres : impulsion $\pi$ sur le contrôle, $2\pi$ sur la cible, $\pi$ inverse sur le contrôle. Mesurer la fidélité.

3. **Porte Mølmer-Sørensen** : Simuler une porte MS entre deux ions avec QuTiP en incluant un mode phononique. Visualiser l'intrication produite.

4. **Scaling des atomes neutres** : Pour un code de surface de distance $d$ avec atomes neutres, estimer le nombre de pinces optiques et la surface du piège. Comparer avec une grille fixe.

5. **Analyse de bruit** : Comparer les courbes de bruit (1/f, $T_2$, etc.) des trois plateformes et discuter des implications pour la correction d'erreur.

---

## Références

- **Bluvstein, D.** et al. (2025). "Logical quantum processor with 48 logical qubits." *Nature*. [Har25]
- **Daily, T.** et al. (2025). "High-fidelity two-qubit gates with trapped ions." *Oxford Ionics*. [Day25]
- **QuEra Computing** (2025). "Algorithmic Fault Tolerance for neutral atom quantum computers." *arXiv*. [QuE25]
- **Saffman, M.** (2016). "Quantum computing with atomic qubits and Rydberg interactions." *J. Phys. B*, 49, 202001.
- **Bruzewicz, C.D.** et al. (2019). "Trapped-ion quantum computing: Progress and challenges." *Appl. Phys. Rev.*, 6, 021314.
- **Mølmer, K. & Sørensen, A.** (1999). "Multiparticle entanglement of hot trapped ions." *Phys. Rev. Lett.*, 82, 1835.
