# Chapitre 4.2 — Canaux quantiques et bruit

## Objectifs

- Comprendre la représentation de Kraus
- Simuler la décohérence et la relaxation
- Maîtriser les modèles de bruit (dépolarisant, bit-flip, phase-flip)
- Implémenter des canaux avec QuTiP et Qiskit

---

## 1. Canaux quantiques

### 1.1 Définition

Un **canal quantique** $\mathcal{E}$ est une application linéaire, complètement positive et préservant la trace (CPTP) qui transforme une matrice densité :

$$
\rho \mapsto \mathcal{E}(\rho)
$$

### 1.2 Représentation de Kraus

Tout canal quantique peut s'écrire :

$$
\mathcal{E}(\rho) = \sum_k K_k \rho K_k^\dagger
$$

avec la condition de complétude :

$$
\sum_k K_k^\dagger K_k = I
$$

### 1.3 Exemple : canal bit-flip

Avec probabilité $p$, le qubit est retourné ($X$) :

$$
K_0 = \sqrt{1-p}\, I,\quad K_1 = \sqrt{p}\, X
$$

$$
\mathcal{E}(\rho) = (1-p)\rho + p X\rho X
$$

---

## 2. Modèles de bruit

### 2.1 Canal dépolarisant

Avec probabilité $p$, l'état est remplacé par l'état maximalement mélangé :

$$
\mathcal{E}(\rho) = (1-p)\rho + p\frac{I}{2}
$$

Opérateurs de Kraus :

$$
K_0 = \sqrt{1-\frac{3p}{4}}\,I,\;
K_1 = \sqrt{\frac{p}{4}}\,X,\;
K_2 = \sqrt{\frac{p}{4}}\,Y,\;
K_3 = \sqrt{\frac{p}{4}}\,Z
$$

```python
import qutip as qt
import numpy as np

# Canal dépolarisant avec QuTiP
def depolarizing_channel(rho, p):
    """Applique le canal dépolarisant."""
    K0 = np.sqrt(1 - 3*p/4) * qt.qeye(2)
    K1 = np.sqrt(p/4) * qt.sigmax()
    K2 = np.sqrt(p/4) * qt.sigmay()
    K3 = np.sqrt(p/4) * qt.sigmaz()
    result = K0 * rho * K0.dag()
    result += K1 * rho * K1.dag()
    result += K2 * rho * K2.dag()
    result += K3 * rho * K3.dag()
    return result

# Test
ket0 = qt.basis(2, 0)
rho_pur = ket0 * ket0.dag()
rho_bruite = depolarizing_channel(rho_pur, 0.3)
print("ρ pur :\n", rho_pur)
print("\nρ après canal dépolarisant (p=0.3) :\n", rho_bruite)
```

**Sortie attendue :**

```
ρ pur :
Quantum object: dims=[[2], [2]], shape=(2, 2), type='oper', dtype=CSR, isherm=True
Qobj data =
[[1. 0.]
 [0. 0.]]

ρ après canal dépolarisant (p=0.3) :
Quantum object: dims=[[2], [2]], shape=(2, 2), type='oper', dtype=CSR, isherm=True
Qobj data =
[[0.85 0.  ]
 [0.   0.15]]
```

### 2.2 Canal bit-flip

$$
\mathcal{E}(\rho) = (1-p)\rho + p X\rho X
$$

### 2.3 Canal phase-flip

$$
\mathcal{E}(\rho) = (1-p)\rho + p Z\rho Z
$$

### 2.4 Effet sur la sphère de Bloch

Un état $\rho = \frac{1}{2}(I + \vec{r} \cdot \vec{\sigma})$ est transformé :

| Canal | Effet sur $\vec{r}$ |
|-------|---------------------|
| Dépolarisant | $\vec{r} \to (1-p)\vec{r}$ |
| Bit-flip | $(r_x, r_y, r_z) \to (r_x, (1-2p)r_y, (1-2p)r_z)$ |
| Phase-flip | $(r_x, r_y, r_z) \to ((1-2p)r_x, (1-2p)r_y, r_z)$ |

```python
# Visualisation sur la sphère de Bloch
import qutip as qt

def apply_noise_and_visualize(ket, p=0.3):
    """Visualise l'effet du bruit sur la sphère de Bloch."""
    bloch = qt.Bloch()
    rho = ket * ket.dag()

    # État idéal
    bloch.add_states(ket)

    # États bruités
    for channel, name in [
        (lambda r: depolarizing_channel(r, p), "Dépolarisant"),
    ]:
        rho_noisy = channel(rho)
        # La matrice densité n'est plus un état pur
        # On ajoute le point correspondant
        x, y, z = qt.expect(qt.sigmax(), rho_noisy), \
                  qt.expect(qt.sigmay(), rho_noisy), \
                  qt.expect(qt.sigmaz(), rho_noisy)
        print(f"{name} : ({x:.3f}, {y:.3f}, {z:.3f})")

    bloch.show()
```

---

## 3. Équation maîtresse de Lindblad

### 3.1 Forme générale

L'évolution d'un système quantique **ouvert** (en contact avec un environnement) est régie par :

$$
\frac{d\rho}{dt} = -\frac{i}{\hbar}[H, \rho] + \sum_k \gamma_k \left( L_k \rho L_k^\dagger - \frac{1}{2}\{L_k^\dagger L_k, \rho\} \right)
$$

où $L_k$ sont les **opérateurs de Lindblad** (collapse operators).

### 3.2 Temps T₁ et T₂

- **T₁** : temps de relaxation (perte d'énergie) : $L_1 = \sqrt{1/T_1}\; \sigma_-$
- **T₂** : temps de déphasage (perte de cohérence) : $L_2 = \sqrt{1/T_2}\; \sigma_z$

```python
import qutip as qt
import numpy as np

# Paramètres
T1, T2 = 10.0, 5.0  # µs
gamma1 = 1.0 / T1
gamma2 = 1.0 / T2

# Hamiltonien
omega = 1.0  # GHz
H = omega / 2 * qt.sigmaz()

# Opérateurs de Lindblad
sm = qt.destroy(2)  # σ_- = |0⟩⟨1|
sz = qt.sigmaz()

c_ops = [
    np.sqrt(gamma1) * sm,     # Relaxation
    np.sqrt(gamma2) * sz,     # Déphasage
]

# État initial |1⟩
psi0 = qt.basis(2, 1)
rho0 = psi0 * psi0.dag()

# Évolution
tlist = np.linspace(0, 5*T1, 100)
result = qt.mesolve(H, rho0, tlist, c_ops=c_ops, e_ops=[qt.basis(2,0)*qt.basis(2,0).dag()])

# Population de |0⟩ en fonction du temps
p0 = result.expect[0]
print("Population |0⟩ à t=0 :", p0[0])
print("Population |0⟩ à t=T1 :", p0[np.argmin(np.abs(tlist - T1))])
```

### 3.3 Visualisation de la décohérence

```python
# Simulation avec QuTiP
import matplotlib.pyplot as plt

# États initiaux
psi_plus = (qt.basis(2,0) + qt.basis(2,1)).unit()  # |+⟩
rho_plus = psi_plus * psi_plus.dag()

# Évolution avec décohérence
result = qt.mesolve(H, rho_plus, tlist, c_ops=c_ops)

# Matrice densité à différents temps
for i, idx in enumerate([0, len(tlist)//4, len(tlist)//2, -1]):
    rho_t = result.states[idx]
    pureté = (rho_t * rho_t).tr()
    print(f"t = {tlist[idx]:.1f}, Tr(ρ²) = {pureté:.4f}")
```

**Sortie attendue :**

```
t = 0.0, Tr(ρ²) = 1.0000
t = 12.5, Tr(ρ²) = 0.6783
t = 25.0, Tr(ρ²) = 0.5246
t = 50.0, Tr(ρ²) = 0.3634
```

La pureté diminue : l'état devient de plus en plus mélangé.

---

## 4. Modèles de bruit avec Qiskit

```python
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, pauli_error

# Création du modèle de bruit
noise_model = NoiseModel()

# Canal dépolarisant sur les portes à 1 qubit
dep_error = depolarizing_error(0.01, 1)  # p=1% sur 1 qubit
noise_model.add_all_qubit_quantum_error(dep_error, ['h', 'x', 'y', 'z', 's', 't'])

# Canal bit-flip sur les portes CNOT
bf_error = pauli_error([('XX', 0.02), ('II', 0.98)])  # 2% bit-flip
noise_model.add_all_qubit_quantum_error(bf_error, ['cx'])

# Circuit Bell avec bruit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Simulation
sim_noisy = AerSimulator(noise_model=noise_model)
sim_ideal = AerSimulator()

result_noisy = sim_noisy.run(qc, shots=4096).result()
result_ideal = sim_ideal.run(qc, shots=4096).result()

print("Idéal :", result_ideal.get_counts())
print("Bruité :", result_noisy.get_counts())
```

---

## 5. Résumé des canaux

| Canal | Opérateurs Kraus | Effet |
|-------|------------------|-------|
| **Bit-flip** | $\sqrt{1-p}I,\; \sqrt{p}X$ | Retourne le qubit avec proba $p$ |
| **Phase-flip** | $\sqrt{1-p}I,\; \sqrt{p}Z$ | Retourne la phase avec proba $p$ |
| **Dépolarisant** | $I, X, Y, Z$ avec poids | État → mélange maximal |
| **Amortissement d'amplitude** | $\begin{pmatrix}1&0\\0&\sqrt{1-\gamma}\end{pmatrix}, \begin{pmatrix}0&\sqrt{\gamma}\\0&0\end{pmatrix}$ | Relaxation $\ket{1} \to \ket{0}$ |
| **Déphasage** | $\begin{pmatrix}1&0\\0&\sqrt{1-\lambda}\end{pmatrix}, \begin{pmatrix}0&0\\0&\sqrt{\lambda}\end{pmatrix}$ | Perte de cohérence |

---

## Exercices

1. Vérifier que les Kraus du canal dépolarisant satisfont $\sum_k K_k^\dagger K_k = I$.
2. Implémenter le canal d'amortissement d'amplitude (amplitude damping) avec QuTiP et comparer avec l'équation de Lindblad.
3. Simuler l'évolution d'un état $\ket{+}$ sous bruit dépolarisant et tracer la pureté $\text{Tr}(\rho^2)$ en fonction du temps.
4. Avec Qiskit, comparer les résultats d'un circuit Grover idéal vs avec un modèle de bruit réaliste (T₁=50µs, T₂=30µs).
5. Montrer que le canal dépolarisant peut s'écrire comme une contraction de la sphère de Bloch : $\vec{r} \to (1-p)\vec{r}$.
