# Chapitre 12.1 — Qubits supraconducteurs

## Objectifs

- Comprendre le fonctionnement des qubits supraconducteurs (transmons)
- Analyser l'architecture de grille de couplage des processeurs IBM Condor et Google Willow
- Maîtriser l'Hamiltonien d'un transmon et le concept d'anharmonicité
- Simuler un transmon avec QuTiP
- Identifier les défis de cohérence, diaphonie et passage à l'échelle

---

## 1. Qubits supraconducteurs : principes généraux

### 1.1 Circuits LC et non-linéarité

Un circuit LC linéaire (inductance $L$, capacité $C$) a une fréquence de résonance $\omega_0 = 1/\sqrt{LC}$ mais ses niveaux d'énergie sont équidistants : impossible d'isoler deux niveaux pour former un qubit.

$$
H_{\text{LC}} = \frac{Q^2}{2C} + \frac{\Phi^2}{2L}, \quad [\Phi, Q] = i\hbar
$$

où $H_{\text{LC}}$ = Hamiltonien du circuit LC, $Q$ = charge, $\Phi$ = flux magnétique, $C$ = capacité, $L$ = inductance, $[\cdot,\cdot]$ = commutateur.

Les niveaux sont $\hbar\omega_0(n + 1/2)$ car c'est un oscillateur harmonique.

### 1.2 Jonction Josephson : la non-linéarité

La **jonction Josephson** remplace l'inductance linéaire par un élément non-linéaire :

$$
I = I_c \sin\delta, \quad V = \frac{\hbar}{2e} \frac{d\delta}{dt}
$$

où $I$ = courant Josephson, $I_c$ = courant critique, $\delta$ = différence de phase supraconductrice, $V$ = tension, $\hbar$ = constante de Planck réduite, $e$ = charge élémentaire.

L'énergie de la jonction est :

$$
E_J = -E_J^0 \cos\delta, \quad E_J^0 = \frac{\hbar I_c}{2e}
$$

où $E_J$ = énergie de Josephson, $E_J^0$ = amplitude de l'énergie Josephson, $\delta$ = phase supraconductrice, $I_c$ = courant critique.

### 1.3 Hamiltonien du transmon

Le **transmon** est un qubit supraconducteur où l'énergie de Josephson $E_J$ domine l'énergie capacitive $E_C = e^2/(2C_\Sigma)$. L'Hamiltonien s'écrit :

$$
H = 4E_C \hat{n}^2 - E_J \cos\hat{\delta}
$$

où $H$ = Hamiltonien du transmon, $E_C$ = énergie capacitive, $\hat{n}$ = nombre de paires de Cooper, $E_J$ = énergie de Josephson, $\hat{\delta}$ = phase supraconductrice.

En développant $\cos\hat{\delta}$ au second ordre puis en ajoutant la non-linéarité :

$$
H \approx \hbar\omega_q a^\dagger a + \frac{\alpha}{2} a^\dagger a^\dagger a a
$$

où $H$ = Hamiltonien approximé, $\omega_q$ = fréquence du qubit, $a^\dagger$ = opérateur de création, $a$ = opérateur d'annihilation, $\alpha$ = anharmonicité.

avec la fréquence du qubit $\omega_q = \sqrt{8E_C E_J}/\hbar$ et l'anharmonicité $\alpha = -E_C$ (négative, typiquement $-200$ à $-400$ MHz).

$$
\alpha = (E_{12} - E_{01}) / \hbar
$$

où $\alpha$ = anharmonicité, $E_{12}$ = énergie de la transition $|1\rangle \to |2\rangle$, $E_{01}$ = énergie de la transition $|0\rangle \to |1\rangle$, $\hbar$ = constante de Planck réduite.

L'anharmonicité permet d'adresser sélectivement la transition $|0\rangle \leftrightarrow |1\rangle$ sans exciter $|2\rangle$.

---

## 2. Architectures de processeurs

### 2.1 IBM Condor (433 qubits, 2023)

IBM Condor est un processeur à 433 qubits supraconducteurs utilisant une **grille de couplage en croix** (heavy-hexagonal lattice) :

- Qubits disposés en motif hexagonal avec des qubits de lecture intercalés
- Connectivité limitée à 3 voisins par qubit
- Fréquence de travail : 4–5 GHz
- Temps de cohérence $T_1 \sim 200\,\mu$s, $T_2 \sim 100\,\mu$s
- Fidélité des portes à 1 qubit : $> 99.9\%$
- Fidélité des portes à 2 qubits : $> 99\%$

Avantage : réduire la diaphonie (crosstalk) entre voisins — les qubits non adjacents sont plus isolés.

### 2.2 Google Willow (105 qubits, 2024)

Google Willow utilise une **grille rectangulaire** avec couplage adjustables :

- 105 qubits en grille $11 \times 11$ (avec coins tronqués)
- Coupleurs accordables (tunable couplers) : chaque qubit peut être connecté/déconnecté dynamiquement
- Réduction exponentielle des erreurs sous le seuil de correction
- Temps de cohérence : $T_1 \sim 350\,\mu$s (record pour des qubits de grille)
- Fidélité des portes à 2 qubits : $99.97\%$
- Lecture : $99.9\%$ en $1\,\mu$s

$$
\text{Erreur logique} \propto \left(\frac{p}{p_{\text{th}}}\right)^{\lfloor d/2 \rfloor}
$$

où $\text{Erreur logique}$ = taux d'erreur du qubit logique, $p$ = taux d'erreur physique, $p_{\text{th}}$ = seuil de correction d'erreur, $d$ = distance du code, $\lfloor \cdot \rfloor$ = partie entière.

---

## 3. Simulation QuTiP d'un transmon

```python
import numpy as np
import qutip as qt

E_J = 20.0
E_C = 0.25
N = 6

n = qt.num(N)
a = qt.destroy(N)
adag = qt.create(N)

H_lin = 4.0 * E_C * (adag * a + 0.5) - E_J * (a + adag) / 2.0

phi = (a + adag) * (8.0 * E_C / E_J) ** 0.25 / np.sqrt(2.0)
H_transmon = 4.0 * E_C * n**2 - E_J * (1.0 - phi**2 / 2.0 + phi**4 / 24.0)
H_transmon = H_transmon - H_transmon[0, 0] * qt.identity(N)

evals = H_transmon.eigenenergies()
omega_q = evals[1] - evals[0]
anharmonicity = (evals[2] - evals[1]) - (evals[1] - evals[0])

print(f"Frequence qubit omega_q/(2pi) = {omega_q / (2*np.pi):.4f}")
print(f"Anharmonicite alpha/(2pi) = {anharmonicity / (2*np.pi):.4f}")

w = np.linspace(0.5 * omega_q, 1.5 * omega_q, 500)
H0 = H_transmon

psi0 = qt.basis(N, 0)
d = qt.destroy(N)

spectrum = []
for wi in w:
    H_drive = H0 + 0.01 * (d * np.exp(-1j * wi * 0.0) + adag * np.exp(1j * wi * 0.0))
    H_drive = H0 + 0.01 * (d + adag)
    tlist = np.linspace(0, 200.0 / omega_q, 500)
    result = qt.mesolve(H0 + 0.01 * (d + adag), psi0, tlist, c_ops=[], e_ops=[d + adag])
    prob = np.abs(result.expect[0]) ** 2
    spectrum.append(np.max(prob))

spectrum = np.array(spectrum)

from scipy.signal import find_peaks
peaks, _ = find_peaks(spectrum, height=0.5)
if len(peaks) > 0:
    print(f"Resonance ω/(2π) ≈ {w[peaks[0]] / (2*np.pi):.4f}")

print(f"Rapport E_J/E_C = {E_J/E_C:.1f}")
print(f"Taille du sous-espace : {N} niveaux")
```

---

## 4. Grille de couplage et diaphonie

### 4.1 Hamiltonien de grille complète

Pour un processeur à $N$ qubits avec couplage entre voisins :

$$
H = \sum_{i=1}^N \hbar\omega_i a_i^\dagger a_i + \sum_{\langle i,j \rangle} g_{ij}(a_i^\dagger a_j + a_i a_j^\dagger)
$$

où $g_{ij}$ est la force de couplage. Sur une grille, chaque qubit n'interagit qu'avec ses voisins directs.

### 4.2 Diaphonie (crosstalk)

La diaphonie est un problème majeur :

- **ZZ-crosstalk** : décalage de fréquence d'un qubit induit par l'état d'un voisin
- **Readout crosstalk** : influence de la mesure d'un qubit sur ses voisins
- **Control crosstalk** : impulsion destinée à un qubit affectant ses voisins

$$
\Delta\omega_i = \sum_{j \neq i} \zeta_{ij} \langle Z_j \rangle
$$

où $\zeta_{ij}$ est le coefficient de diaphonie (typiquement 10–100 kHz).

```python
import numpy as np

N_qubits = 4
omega = np.array([5.0, 5.1, 4.9, 5.05])
g = 0.05

H_qubits = np.diag(omega)
for i in range(N_qubits - 1):
    H_qubits[i, i+1] = g
    H_qubits[i+1, i] = g

evals, evecs = np.linalg.eigh(H_qubits)
print("Modes du systeme couple :")
for i in range(N_qubits):
    print(f"  ω_{i}/(2π) = {evals[i]:.4f} GHz")

zeta = np.array([
    [0.0, 0.02, 0.01, 0.005],
    [0.02, 0.0, 0.015, 0.008],
    [0.01, 0.015, 0.0, 0.012],
    [0.005, 0.008, 0.012, 0.0]
])

Z_states = np.array([[1], [-1], [-1], [1]])
for i in range(N_qubits):
    shift = np.sum(zeta[i] * Z_states.flatten())
    print(f"ZZ-decalage qubit {i} : {shift:.4f} GHz")
```

**Sortie attendue :**

```
Modes du systeme couple :
  omega_0/(2pi) = 4.8737 GHz
  omega_1/(2pi) = 4.9820 GHz
  omega_2/(2pi) = 5.0628 GHz
  omega_3/(2pi) = 5.1315 GHz
ZZ-decalage qubit 0 : -0.0250 GHz
ZZ-decalage qubit 1 : 0.0130 GHz
ZZ-decalage qubit 2 : 0.0070 GHz
ZZ-decalage qubit 3 : -0.0150 GHz
```

---

### 4.3 Simulation de porte à deux qubits

```python
import numpy as np
import qutip as qt

N1, N2 = 4, 4
a1 = qt.tensor(qt.destroy(N1), qt.identity(N2))
a2 = qt.tensor(qt.identity(N1), qt.destroy(N2))

omega1 = 5.0
omega2 = 5.1
alpha1 = -0.3
alpha2 = -0.3
g_cpl = 0.05

H_single = omega1 * a1.dag() * a1 + alpha1/2 * a1.dag() * a1.dag() * a1 * a1
H_single += omega2 * a2.dag() * a2 + alpha2/2 * a2.dag() * a2.dag() * a2 * a2
H_cpl = g_cpl * (a1.dag() * a2 + a1 * a2.dag())
H_total = H_single + H_cpl

psi0 = qt.tensor(qt.basis(N1, 0), qt.basis(N2, 1))
tlist = np.linspace(0, 500, 1000)

result_swap = qt.mesolve(H_total, psi0, tlist, c_ops=[], e_ops=[
    qt.tensor(qt.projection(N1, 1, 1), qt.projection(N2, 0, 0))
])

P_swap = result_swap.expect[0]
t_opt = tlist[np.argmax(P_swap)]
print(f"Temps optimal pour iSWAP : {t_opt:.2f} ns")
print(f"Probabilité max de swap : {np.max(P_swap):.4f}")

def swap_fidelity(t, H, psi_t, target_state):
    U = (-1j * H * t).expm()
    psi_f = U * psi_t
    return (target_state.dag() * psi_f).real

target = qt.tensor(qt.basis(N1, 1), qt.basis(N2, 0))
fid_max = swap_fidelity(t_opt, H_total, psi0, target)
print(f"Fidélité de l'iSWAP au temps optimal : {fid_max:.6f}")

g_vals = np.linspace(0.01, 0.2, 20)
fidelities = []
for gtest in g_vals:
    Htest = H_single + gtest * (a1.dag() * a2 + a1 * a2.dag())
    evals = Htest.eigenenergies()
    gap = evals[1] - evals[0]
    t_swap_test = np.pi / (2 * gap)
    fid_test = swap_fidelity(t_swap_test, Htest, psi0, target)
    fidelities.append(fid_test)

for gv, fv in zip(g_vals, fidelities):
    print(f"g = {gv:.3f} : fidelite = {fv:.6f}")
```

### 4.4 Simulation de la relaxation T1

```python
import numpy as np
import qutip as qt

N = 3
a = qt.destroy(N)
H = 5.0 * a.dag() * a - 0.15 * a.dag() * a.dag() * a * a

T1 = 100.0
c_ops = [np.sqrt(1.0 / T1) * a]

psi1 = qt.basis(N, 1)
rho1 = psi1 * psi1.dag()
tlist = np.linspace(0, 500, 200)

result = qt.mesolve(H, rho1, tlist, c_ops=c_ops, e_ops=[
    qt.projection(N, 0, 0),
    qt.projection(N, 1, 1),
    qt.projection(N, 2, 2)
])

P0, P1, P2 = result.expect
print(f"Population |0> a t=0 : {P0[0]:.4f}")
print(f"Population |0> a t=T1 : {P0[np.argmin(np.abs(tlist - T1))]:.4f}")
print(f"T1 extrait : {tlist[np.argmin(np.abs(P1 - 0.5))]:.2f}")
```

**Sortie attendue :**

```
Population |0> a t=0 : 0.0000
Population |0> a t=T1 : 0.6340
T1 extrait : 70.35
```

---

## 5. Défis et perspectives

### 5.1 Temps de cohérence

Les limites fondamentales de $T_1$ et $T_2$ :

- $T_1$ limité par les quasi-particules, les pertes diélectriques, le couplage aux modes parasites
- $T_2 \leq 2T_1$ (limite théorique)
- Objectif 2027 : $T_1 > 1$ ms

$$
\frac{1}{T_1} = \frac{1}{T_{1,\text{quasi}}} + \frac{1}{T_{1,\text{dielec}}} + \frac{1}{T_{1,\text{radiation}}}
$$

### 5.2 Passage à l'échelle (scaling)

| Défi | Problème | Solution possible |
|------|----------|-------------------|
| Câblage | 1000+ lignes de contrôle | Multiplexage fréquentiel, cryo-CMOS |
| Chaleur | Dissipation au niveau du mélangeur | Réfrigération dilution + cryo-électronique |
| Connectivité | Grille 2D limitée | Coupleurs accordables, interconnexion 3D |
| Taux d'erreur | Portes 2 qubits $> 10^{-3}$ | Matériaux, optimisation des pulses |

### 5.3 Évolution des performances

$$
\text{Fidélité}_{2Q}(t) = 1 - \epsilon_0 \exp(-t/\tau_{\text{opt}})
$$

où $\tau_{\text{opt}}$ est l'échelle de temps d'optimisation des portes.

### 5.4 Leakage et gestion des niveaux

Le transmon n'est pas un système à 2 niveaux parfait ; la population peut fuir vers $|2\rangle$ (leakage) :

$$
L = \langle 2 | \rho | 2 \rangle
$$

Le leakage réduit la fidélité des portes et complexifie la correction d'erreur :

$$
F_{\text{porte}} = F_{\text{idéal}} - \alpha_L L - \alpha_{\text{crosstalk}} \sum_{j \neq i} \langle Z_j \rangle
$$

```python
import numpy as np
import qutip as qt

N = 4
a = qt.destroy(N)
adag = a.dag()
H0 = 5.0 * adag * a - 0.15 * adag * adag * a * a

psi0 = qt.basis(N, 1)
Omega_drive = 0.1
omega_drive = 4.85
T_gate = 50.0
tlist = np.linspace(0, T_gate, 500)

H_drive_func = lambda t, args: Omega_drive * (a * np.exp(1j * omega_drive * t) + adag * np.exp(-1j * omega_drive * t))

result_drive = qt.mesolve(H0, psi0, tlist, c_ops=[], e_ops=[
    qt.projection(N, 0, 0),
    qt.projection(N, 1, 1),
    qt.projection(N, 2, 2)
], args={})

P0_d, P1_d, P2_d = result_drive.expect
leakage_max = np.max(P2_d)
print(f"Leakage maximal vers |2> : {leakage_max:.4f}")

omega_scan = np.linspace(4.5, 5.5, 100)
leakages = []
for wd in omega_scan:
    H_drive = H0 + Omega_drive * (a * np.exp(1j * wd * 0) + adag * np.exp(-1j * wd * 0))
    r = qt.mesolve(H_drive, psi0, tlist, c_ops=[], e_ops=[qt.projection(N, 2, 2)])
    leakages.append(np.max(r.expect[0]))

print(f"Leakage minimal : {np.min(leakages):.4f} a ω_drive = {omega_scan[np.argmin(leakages)]:.3f}")
```

---

## 6. Exercices

1. **Simulation de transmon** : Faire varier le rapport $E_J/E_C$ de 10 à 100 et tracer $\alpha/\omega_q$ en fonction. Interpréter.

2. **Porte à deux qubits** : Simuler une porte iSWAP entre deux transmons couplés avec QuTiP. Calculer la fidélité en fonction de $g$ et du temps d'interaction.

3. **Analyse de crosstalk** : Sur un réseau $3\times3$ avec ZZ-crosstalk réaliste, simuler l'erreur cumulée lors d'une séquence de portes sur un qubit central.

4. **Budget d'erreur** : Pour IBM Condor, construire un budget d'erreur détaillé (T1, T2, leakage, crosstalk, lecture) et estimer le nombre de portes correctes avant correction.

5. **Comparaison** : Comparer les architectures de grille (heavy-hexagonal IBM vs rectangulaire Google) en termes de connectivité, diamètre du graphe et tolérance au crosstalk.

---

## Références

- **Koch, J.** et al. (2007). "Charge-insensitive qubit design derived from the Cooper pair box." *Phys. Rev. A*, 76, 042319. [Transmon]
- **IBM Quantum** (2023). "IBM Quantum Condor: 433-qubit processor." *IBM Research*. [IBM24]
- **Google Quantum AI** (2024). "Quantum error correction below the surface code threshold." *Nature*, 636, 74–79. [Goo24]
- **Kjaergaard, M.** et al. (2020). "Superconducting qubits: Current state of play." *Annual Review of Condensed Matter Physics*, 11, 369–395.
- **Blais, A.** et al. (2021). "Circuit quantum electrodynamics." *Rev. Mod. Phys.*, 93, 025005.
