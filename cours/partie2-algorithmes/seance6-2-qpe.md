# Séance 6.2 — Quantum Phase Estimation (QPE)

## Objectifs d'apprentissage

- Maîtriser l'algorithme d'estimation de phase quantique
- Comprendre l'analyse de précision et la probabilité de succès
- Utiliser les portes contrôlées et la QFT inverse
- Appliquer la QPE à des problèmes fondamentaux

---

## 1. Problème de l'estimation de phase

**Problème** : Soit $U$ un opérateur unitaire avec un état propre $|\psi\rangle$ tel que $U|\psi\rangle = e^{2\pi i \theta} |\psi\rangle$. Étant donné $U$ et $|\psi\rangle$, estimer $\theta$ avec $m$ bits de précision.

**Solution** : L'algorithme QPE utilise $m$ qubits de contrôle et la QFT inverse.

### Circuit QPE

```
|0⟩ — H — • — • — • — • — • — • — QFT† — M₀
|0⟩ — H — | — | — | — | — • — | — — — — M₁
|0⟩ — H — | — | — • — | — — — | — — — — M₂
|0⟩ — H — | — • — — — | — — — — — — — — M₃
           |   |       |
|ψ⟩ — — — U^{1} U^{2} U^{4} — — — — — — —
```

## 2. Analyse mathématique

### État initial
$$|\psi_0\rangle = |0\rangle^{\otimes m} \otimes |\psi\rangle$$

### Après Hadamard
$$|\psi_1\rangle = \frac{1}{\sqrt{2^m}} \sum_{k=0}^{2^m-1} |k\rangle \otimes |\psi\rangle$$

### Après portes contrôlées
$$|\psi_2\rangle = \frac{1}{\sqrt{2^m}} \sum_{k=0}^{2^m-1} |k\rangle \otimes U^k |\psi\rangle = \frac{1}{\sqrt{2^m}} \sum_{k=0}^{2^m-1} e^{2\pi i k \theta} |k\rangle \otimes |\psi\rangle$$

### Le premier registre est exactement
$$\frac{1}{\sqrt{2^m}} \sum_{k=0}^{2^m-1} e^{2\pi i k \theta} |k\rangle$$

Si $\theta = 0.\theta_1\theta_2\ldots\theta_m$ (binaire), alors c'est $QFT_{2^m} |\theta_1\ldots\theta_m\rangle$.

### Après QFT inverse
$$|\psi_3\rangle = QFT_{2^m}^{-1} \left( \frac{1}{\sqrt{2^m}} \sum_{k=0}^{2^m-1} e^{2\pi i k \theta} |k\rangle \right) \otimes |\psi\rangle$$

Si $\theta$ s'écrit exactement sur $m$ bits : $|\psi_3\rangle = |\hat{\theta}\rangle \otimes |\psi\rangle$ où $\hat{\theta} = 0.\theta_1\ldots\theta_m$.

## 3. Analyse de précision

Quand $\theta$ n'a pas de représentation exacte sur $m$ bits :

$$\theta = \frac{a}{2^m} + \delta, \quad 0 < |\delta| \leq 2^{-(m+1)}$$

La probabilité de mesurer la meilleure approximation $\hat{\theta} = a/2^m$ est :

$$P(|a\rangle) = \frac{1}{2^{2m}} \left| \sum_{k=0}^{2^m-1} e^{2\pi i k \delta} \right|^2 = \frac{1}{2^{2m}} \frac{\sin^2(\pi \delta 2^m)}{\sin^2(\pi \delta)}$$

**Borne inférieure** : $P(|a\rangle) \geq \frac{4}{\pi^2} \approx 0.405$

**Pour $m + p$ bits de précision** : la probabilité de succès est $1 - 2^{-p}$.

### Erreur et nombre de qubits

| Précision $\epsilon$ | Qubits $m$ | Probabilité |
|---------------------|-------------|-------------|
| $10^{-1}$ | 4 | $\approx 0.97$ |
| $10^{-2}$ | 7 | $\approx 0.99$ |
| $10^{-3}$ | 10 | $\approx 0.999$ |

$$m = \lceil \log_2(1/\epsilon) \rceil + \lceil \log_2(2 + 1/(2\epsilon)) \rceil$$

## 4. Portes contrôlées

Pour implémenter $U^{2^j}$, on utilise la répétition de la porte $U$.

**Exemple** : $U = R_z(\phi) = \begin{pmatrix} e^{-i\phi/2} & 0 \\ 0 & e^{i\phi/2} \end{pmatrix}$

$$U^{2^j} = R_z(2^j \phi) = \begin{pmatrix} e^{-i 2^{j-1} \phi} & 0 \\ 0 & e^{i 2^{j-1} \phi} \end{pmatrix}$$

### Implémentation avec portes $CR_k$

Pour le QPE, on utilise des portes de phase contrôlées :

```
CR_k = diag(1, 1, 1, exp(2πi/2^k))
```

## 5. Implémentation Qiskit

```python
import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram

def qpe_simple(U, theta, m=4):
    """
    QPE pour estimer la phase θ de U.
    U : opérateur unitaire (circuit Qiskit)
    theta : phase exacte (pour comparaison)
    m : nombre de qubits de contrôle
    """
    n = U.num_qubits  # qubits pour l'état propre
    qc = QuantumCircuit(m + n, m)

    # Hadamard sur qubits de contrôle
    qc.h(range(m))

    # U^(2^j) contrôlé
    for j in range(m):
        # Application répétée de U, 2^j fois
        for _ in range(2**j):
            qc.append(U.control(), [j] + list(range(m, m + n)))

    # QFT inverse
    qft_dagger(qc, m)

    # Mesure
    qc.measure(range(m), range(m))

    return qc

def qft_dagger(qc, n):
    """QFT inverse"""
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            angle = -2 * np.pi / (2**(j - i + 1))
            qc.cp(angle, j, i)
        qc.h(i)

# Exemple : U = R_z(θ), état propre |1⟩
def u_rz(theta):
    qc = QuantumCircuit(1)
    qc.rz(theta, 0)
    return qc

# Test
theta = 0.25  # phase à estimer
U = u_rz(theta)
qc_qpe = qpe_simple(U, theta, m=4)

print(f"Circuit QPE (θ={theta}, m=4) :")
print(qc_qpe.draw())

# Exécution
backend = Aer.get_backend('qasm_simulator')
result = execute(qc_qpe, backend, shots=2048).result()
counts = result.get_counts()

# Conversion des mesures en estimateur de θ
print("\nDistribution des estimations :")
estimates = {}
for bits, count in counts.items():
    # bits → float
    val = sum(int(bits[i]) / (2**(i+1)) for i in range(len(bits)))
    estimates[val] = count
    print(f"  0.{bits} = {val:.4f} : {count:4d} shots")

best = max(estimates, key=estimates.get)
print(f"\nMeilleure estimation : {best:.4f}")
print(f"Valeur exacte : {theta:.4f}")
print(f"Erreur : {abs(best - theta):.6f}")
```

```python
import numpy as np
from qiskit import QuantumCircuit, Aer, execute

def qpe_avec_etat_propre(theta, m=5):
    """
    QPE avec préparation de l'état propre de U.
    U = R_z(θ), état propre |1⟩
    """
    qc = QuantumCircuit(m + 1, m)

    # Préparation de l'état propre |1⟩
    qc.x(m)

    # Hadamard
    qc.h(range(m))

    # U^(2^j) contrôlé
    for j in range(m):
        angle = 2 * np.pi * theta * (2**j)
        qc.cp(angle, j, m)

    # QFT inverse
    qft_dagger(qc, m)

    qc.measure(range(m), range(m))
    return qc

# Analyse de la précision en fonction de m
print("Analyse de précision QPE :")
for m in range(2, 8):
    theta = 0.1  # phase non-représentable exactement
    qc = qpe_avec_etat_propre(theta, m)

    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend, shots=4096).result()
    counts = result.get_counts()

    # Estimation
    estimates = {}
    for bits, count in counts.items():
        val = sum(int(bits[i]) / (2**(i+1)) for i in range(len(bits)))
        estimates[val] = estimates.get(val, 0) + count

    best = max(estimates, key=estimates.get)
    error = abs(best - theta)

    # Probabilité de la meilleure estimation
    p_best = estimates[best] / 4096
    print(f"  m={m} : θ̂={best:.6f}, erreur={error:.6f}, P(succès)={p_best:.3f}")
```

## 6. Application fondamentale : algorithme de Shor

Le QPE est le cœur de l'algorithme de Shor :

1. Choisir $a$ aléatoire, $1 < a < N$
2. Définir $U_a |x\rangle = |ax \bmod N\rangle$
3. L'ordre $r$ de $a$ modulo $N$ est la période de $U_a$ : $U_a^r = I$
4. Les valeurs propres de $U_a$ sont $e^{2\pi i k/r}$ pour $k=0,\ldots,r-1$
5. QPE sur $U_a$ donne une estimation de $k/r$ → on en déduit $r$

### Application : simulation Hamiltonienne

Le QPE permet de simuler $e^{-iHt}$ pour un Hamiltonien $H$ :

$$H|\psi_j\rangle = E_j |\psi_j\rangle \implies e^{-iHt} |\psi_j\rangle = e^{-iE_j t} |\psi_j\rangle$$

QPE sur $U = e^{-iHt}$ donne une estimation de $E_j t / (2\pi)$.

```python
import numpy as np
import qutip as qt

def qpe_qutip(U, m=4):
    """
    Simulation du QPE en QuTiP.
    U : matrice unitaire (Qobj)
    m : nombre de qubits de contrôle
    """
    N = U.shape[0]
    n = int(np.log2(N))
    assert 2**n == N, "U doit agir sur un nombre entier de qubits"

    dim_cont = 2**m
    dim_sys = N

    # État initial : |0⟩_cont ⊗ |ψ⟩_sys
    # On utilise l'état propre |1⟩
    psi_sys = qt.basis(N, 1)

    psi0 = qt.tensor(qt.basis(dim_cont, 0), psi_sys)

    # Hadamard sur les qubits de contrôle
    H_m = qt.qeye(2)
    for _ in range(m - 1):
        H_m = qt.tensor(H_m, qt.qeye(2))
    H1 = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    H_full = qt.qeye(1)
    for _ in range(m):
        H_full = qt.tensor(H_full, qt.Qobj(H1))
    H_full = qt.tensor(H_full, qt.qeye(N))

    psi1 = H_full * psi0

    # U^(2^j) contrôlé
    U_full = qt.qeye(dim_cont * dim_sys)
    for j in range(m):
        factor = 2**j
        U_pow = U**factor
        # Contrôlé : applique U_pow si le j-ème qubit de contrôle est |1⟩
        for k in range(dim_cont):
            if (k >> j) & 1:
                proj = qt.basis(dim_cont, k) * qt.basis(dim_cont, k).dag()
                U_full += qt.tensor(proj, U_pow - qt.qeye(N))

    psi2 = U_full * psi1

    # QFT inverse sur les qubits de contrôle
    QFT_mat = np.zeros((dim_cont, dim_cont), dtype=complex)
    omega = np.exp(2j * np.pi / dim_cont)
    for i in range(dim_cont):
        for j in range(dim_cont):
            QFT_mat[i, j] = omega**(-i * j) / np.sqrt(dim_cont)
    QFT_dag = qt.Qobj(QFT_mat, dims=[[dim_cont], [dim_cont]])

    QFT_full = qt.tensor(QFT_dag, qt.qeye(N))
    psi3 = QFT_full * psi2

    # Mesure des qubits de contrôle
    probs = np.zeros(dim_cont)
    for k in range(dim_cont):
        proj = qt.tensor(qt.basis(dim_cont, k) * qt.basis(dim_cont, k).dag(),
                         qt.qeye(N))
        probs[k] = (psi3.dag() * proj * psi3).real

    estimates = np.where(probs > 0.01)[0]
    print("Estimations de phase (QuTiP) :")
    for k in estimates:
        phase_est = k / dim_cont
        print(f"  k={k}, θ̂={phase_est:.4f}, P={probs[k]:.3f}")

    return psi3, probs

# Test
theta = 0.25
U = qt.Qobj(np.diag([1, np.exp(2j * np.pi * theta)]),
            dims=[[2], [2]])
psi_qpe, probs_qpe = qpe_qutip(U, m=4)
```

## 7. Exercices

### Exercice 1 : Preuve de l'estimation
Montrez que $P(|a\rangle) \geq 4/\pi^2$ quand $\theta$ est approximé sur $m$ bits.

### Exercice 2 : Implémentation Cirq
Implémentez le QPE en Cirq pour $U = T = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{pmatrix}$.

### Exercice 3 : Précision adaptative
Implémentez le QPE itératif (IQPE) qui utilise 1 seul qubit de contrôle et améliore itérativement la précision.

```python
def iqpe(U, theta_true, precision_bits=8):
    """
    QPE itératif : 1 qubit de contrôle, mesure séquentielle.
    """
    phase = 0.0
    for k in range(precision_bits):
        qc = QuantumCircuit(2, 1)
        qc.h(0)
        # U^(2^(precision_bits-1-k))
        # Rotation de phase adaptative
        # Complétez...
        pass
```

### Exercice 4 : Application — Simulation moléculaire
Utilisez QPE pour estimer l'énergie de l'état fondamental de $H_2$ (Hamiltonien de Pariseau). Utilisez QuTiP pour diagonaliser $H$ et vérifiez.

### Exercice 5 : Analyse d'erreur avec bruit
Simulez le QPE avec un canal de déphasage (dephasing noise) sur les qubits de contrôle. Tracez la fidélité en fonction du taux de bruit.

### Exercice 6 : Ordre de grandeur
Pour l'algorithme de Shor avec $N=15$, combien de qubits de contrôle sont nécessaires pour distinguer les facteurs avec probabilité $>0.99$ ?

---

## Références

- Kitaev, A. Y. (1995). "Quantum measurements and the Abelian Stabilizer Problem". *arXiv:quant-ph/9511026*.
- Nielsen, M. A. & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*.
- Aspuru-Guzik, A. et al. (2005). "Simulated Quantum Computation of Molecular Energies". *Science*, 309, 1704–1707.
