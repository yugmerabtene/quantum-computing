# Chapitre 6.2 — Quantum Phase Estimation (QPE)

## Ce que vous allez apprendre

- Maîtriser l'algorithme d'**estimation de phase quantique** (QPE)
- Comprendre l'**analyse de précision** et la probabilité de succès
- Utiliser les **portes contrôlées** $U^{2^j}$ et la **QFT inverse**
- Appliquer la QPE à la **simulation Hamiltonienne** et à l'algorithme de Shor

---

## Motivation

Imaginez que vous avez une machine (un opérateur unitaire $U$) qui, appliquée à un état spécial $|\psi\rangle$, ne fait que lui ajouter une phase : $U|\psi\rangle = e^{2\pi i \theta}|\psi\rangle$. Vous connaissez $U$ et $|\psi\rangle$, mais vous ignorez $\theta$. Comment estimer $\theta$ ?

Classiquement, il faudrait préparer $|\psi\rangle$, appliquer $U$ many times, et faire des mesures interférométriques. Quantiquement, l'algorithme QPE estime $\theta$ avec $m$ bits de précision en utilisant $m$ qubits auxiliaires et des applications contrôlées de $U^{2^j}$.

La QPE est l'un des algorithmes les plus importants en calcul quantique. C'est le **cœur de l'algorithme de Shor** (chapitre 7.1) : trouver la période d'une fonction revient à estimer les phases d'un opérateur d'exponentiation modulaire. C'est aussi un outil fondamental pour la **simulation quantique** : estimer les énergies propres d'un Hamiltonien.

---

## Idée principale

Pensez à une horloge. L'aiguille tourne d'un angle $2\pi\theta$ à chaque tick. Si vous pouvez geler l'horloge après $1, 2, 4, 8, \ldots$ ticks et lire la position de l'aiguille, vous pouvez reconstituer $\theta$ bit par bit.

La QPE fait exactement ça. Chaque qubit de contrôle « lit » un bit de $\theta$ : le premier qubit lit le bit le plus significatif (après avoir appliqué $U^{2^{m-1}}$), le second lit le bit suivant, etc. La QFT inverse sert à « décoder » les phases accumulées en un état binaire lisible.

---

## Contenu du cours

### Section 1 : Le problème de l'estimation de phase

**Problème** : Soit $U$ un opérateur unitaire avec un état propre $|\psi\rangle$ tel que :

$$U|\psi\rangle = e^{2\pi i \theta} |\psi\rangle$$

Étant donné $U$ et $|\psi\rangle$, estimer $\theta$ avec $m$ bits de précision.

**Intuition** : $\theta$ est la « phase » associée à l'état propre. C'est un nombre réel entre $0$ et $1$.

**Variables** : $U$ = opérateur unitaire, $|\psi\rangle$ = état propre, $\theta \in [0, 1)$ = phase à estimer, $m$ = nombre de bits de précision.

**Exemple** : $U = R_z(\phi)$, $|\psi\rangle = |1\rangle$. Alors $U|1\rangle = e^{i\phi/2}|1\rangle$, donc $\theta = \phi/(4\pi)$.

### Section 2 : Le circuit QPE

```
|0⟩ — H — • — • — • — • — • — • — QFT† — M₀
|0⟩ — H — | — | — | — | — • — | — — — — M₁
|0⟩ — H — | — | — • — | — — — | — — — — M₂
|0⟩ — H — | — • — — — | — — — — — — — — M₃
            |   |       |
|ψ⟩ — — — U^{1} U^{2} U^{4} — — — — — — —
```

**Étape 1** — État initial :
$$|\psi_0\rangle = |0\rangle^{\otimes m} \otimes |\psi\rangle$$

**Étape 2** — Hadamard sur les qubits de contrôle :
$$|\psi_1\rangle = \frac{1}{\sqrt{2^m}} \sum_{k=0}^{2^m-1} |k\rangle \otimes |\psi\rangle$$

**Intuition** : chaque qubit de contrôle est en superposition, ce qui permet d'appliquer $U$ en parallèle sur différentes « puissances ».

**Étape 3** — Portes contrôlées $U^{2^j}$ :
$$|\psi_2\rangle = \frac{1}{\sqrt{2^m}} \sum_{k=0}^{2^m-1} |k\rangle \otimes U^k |\psi\rangle = \frac{1}{\sqrt{2^m}} \sum_{k=0}^{2^m-1} e^{2\pi i k \theta} |k\rangle \otimes |\psi\rangle$$

**Intuition** : le qubit de contrôle $j$ applique $U^{2^j}$, donc accumule une phase $e^{2\pi i \cdot 2^j \theta}$. L'état du premier registre encode maintenant $\theta$ dans ses phases.

**Étape 4** — QFT inverse :
$$|\psi_3\rangle = QFT_{2^m}^{-1} \left( \frac{1}{\sqrt{2^m}} \sum_{k=0}^{2^m-1} e^{2\pi i k \theta} |k\rangle \right) \otimes |\psi\rangle$$

**Pourquoi la QFT inverse ?** L'état $\frac{1}{\sqrt{2^m}} \sum_k e^{2\pi i k \theta} |k\rangle$ est exactement $QFT_{2^m}|\theta_1\ldots\theta_m\rangle$ si $\theta = 0.\theta_1\theta_2\ldots\theta_m$ en binaire. Donc appliquer $QFT^{-1}$ donne $|\theta_1\ldots\theta_m\rangle$.

### Section 3 : Analyse de précision

Quand $\theta$ n'a pas de représentation exacte sur $m$ bits :

$$\theta = \frac{a}{2^m} + \delta, \quad 0 < |\delta| \leq 2^{-(m+1)}$$

La probabilité de mesurer la meilleure approximation $\hat{\theta} = a/2^m$ est :

$$P(|a\rangle) = \frac{1}{2^{2m}} \left| \sum_{k=0}^{2^m-1} e^{2\pi i k \delta} \right|^2 = \frac{1}{2^{2m}} \frac{\sin^2(\pi \delta 2^m)}{\sin^2(\pi \delta)}$$

**Intuition** : c'est une fonction de type « peigne de Dirichlet ». Le pic principal est à $a$, et les pics secondaires décroissent rapidement.

**Borne inférieure** : $P(|a\rangle) \geq \frac{4}{\pi^2} \approx 0.405$

**Pour $m + p$ bits de précision** : la probabilité de succès est $1 - 2^{-p}$.

**Exemple numérique** : $\theta = 0.1$, $m = 4$. Meilleure approximation : $a/16 = 2/16 = 0.125$. Erreur : $|\delta| = 0.025$. Probabilité de mesurer $|0010\rangle$ :
$$P = \frac{1}{256} \frac{\sin^2(\pi \cdot 0.025 \cdot 16)}{\sin^2(\pi \cdot 0.025)} = \frac{1}{256} \frac{\sin^2(0.4\pi)}{\sin^2(0.025\pi)} \approx 0.59$$

### Section 4 : Nombre de qubits nécessaires

| Précision $\epsilon$ | Qubits $m$ | Probabilité |
|---------------------|-------------|-------------|
| $10^{-1}$ | 4 | $\approx 0.97$ |
| $10^{-2}$ | 7 | $\approx 0.99$ |
| $10^{-3}$ | 10 | $\approx 0.999$ |

$$m = \lceil \log_2(1/\epsilon) \rceil + \lceil \log_2(2 + 1/(2\epsilon)) \rceil$$

**Intuition** : pour $p$ bits de précision supplémentaires (au-delà de $\log_2(1/\epsilon)$), il faut $p$ qubits de plus, mais la probabilité de succès augmente exponentiellement.

---

## Exemple guidé

Prenons $U = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\pi/2} \end{pmatrix}$, $|\psi\rangle = |1\rangle$. Alors $U|1\rangle = e^{i\pi/2}|1\rangle$, donc $\theta = 1/4 = 0.01_2$.

Avec $m = 2$ qubits de contrôle :

**État après Hadamard** :
$$|\psi_1\rangle = \frac{1}{2}(|00\rangle + |01\rangle + |10\rangle + |11\rangle) \otimes |1\rangle$$

**Après portes contrôlées** :
- Qubit 0 contrôle $U^{2^0} = U$ : phase $e^{i\pi/2}$ si qubit 0 = 1
- Qubit 1 contrôle $U^{2^1} = U^2$ : phase $e^{i\pi} = -1$ si qubit 1 = 1

$$|\psi_2\rangle = \frac{1}{2}(|00\rangle + e^{i\pi/2}|01\rangle + e^{i\pi}|10\rangle + e^{i3\pi/2}|11\rangle) \otimes |1\rangle$$
$$= \frac{1}{2}(|00\rangle + i|01\rangle - |10\rangle - i|11\rangle) \otimes |1\rangle$$

**Après QFT inverse** :
On applique $QFT_4^{-1}$. Comme $\theta = 0.01_2$ est exactement représentable sur 2 bits, on doit obtenir $|01\rangle$.

Vérifions : $QFT_4 |01\rangle = \frac{1}{2}(|0\rangle + e^{i\pi/2}|1\rangle) \otimes (|0\rangle + e^{i\pi}|1\rangle) = \frac{1}{2}(|00\rangle + i|01\rangle - |10\rangle - i|11\rangle)$ ✓

Donc $QFT_4^{-1} |\psi_2\rangle = |01\rangle$, ce qui correspond à $\theta = 01_2 / 4 = 1/4$. ✓

---

## Implémentation Python

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# --- QFT inverse ---
def qft_dagger(qc, n):
    """
    QFT inverse (QFT†).
    Applique les portes dans l'ordre inverse avec des angles négatifs.
    """
    # SWAP pour remettre les qubits dans le bon ordre
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)
    # Portes dans l'ordre inverse
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            angle = -2 * np.pi / (2**(j - i + 1))
            qc.cp(angle, j, i)
        qc.h(i)

# --- Circuit QPE ---
def qpe_simple(U, theta, m=4):
    """
    QPE pour estimer la phase θ de U.
    U : opérateur unitaire (circuit Qiskit)
    theta : phase exacte (pour comparaison)
    m : nombre de qubits de contrôle
    """
    n = U.num_qubits  # qubits pour l'état propre
    qc = QuantumCircuit(m + n, m)

    # Hadamard sur les qubits de contrôle
    qc.h(range(m))

    # U^(2^j) contrôlé pour chaque qubit de contrôle j
    for j in range(m):
        # Appliquer U contrôlé 2^j fois
        for _ in range(2**j):
            qc.append(U.control(), [j] + list(range(m, m + n)))

    # QFT inverse sur les qubits de contrôle
    qft_dagger(qc, m)

    # Mesure des qubits de contrôle
    qc.measure(range(m), range(m))

    return qc

# --- Exemple : U = R_z(θ) ---
def u_rz(theta):
    """Crée le circuit pour U = R_z(θ)"""
    qc = QuantumCircuit(1)
    qc.rz(theta, 0)
    return qc

# --- Test ---
theta = 0.25  # phase à estimer
U = u_rz(theta)
qc_qpe = qpe_simple(U, theta, m=4)

print(f"Circuit QPE (θ={theta}, m=4) :")
print(qc_qpe.draw())

# Exécution
backend = AerSimulator()
result = backend.run(qc_qpe, shots=2048).result()
counts = result.get_counts()

# Conversion des mesures en estimateur de θ
print("\nDistribution des estimations :")
estimates = {}
for bits, count in counts.items():
    # Convertir les bits en valeur décimale
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
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# --- QPE avec préparation explicite de l'état propre ---
def qpe_avec_etat_propre(theta, m=5):
    """
    QPE pour U = R_z(2πθ), état propre |1⟩.
    Utilise des portes de phase contrôlées directement.
    """
    qc = QuantumCircuit(m + 1, m)

    # Préparation de l'état propre |1⟩
    qc.x(m)

    # Hadamard sur les qubits de contrôle
    qc.h(range(m))

    # U^(2^j) contrôlé : pour R_z, c'est une phase contrôlée
    for j in range(m):
        angle = 2 * np.pi * theta * (2**j)
        qc.cp(angle, j, m)

    # QFT inverse
    qft_dagger(qc, m)

    qc.measure(range(m), range(m))
    return qc

# --- Analyse de la précision en fonction de m ---
print("Analyse de précision QPE :")
for m in range(2, 8):
    theta = 0.1  # phase non-représentable exactement en binaire
    qc = qpe_avec_etat_propre(theta, m)

    backend = AerSimulator()
    result = backend.run(qc, shots=4096).result()
    counts = result.get_counts()

    # Estimation de θ
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

```python
import numpy as np
import qutip as qt

# --- Simulation QPE en QuTiP ---
def qpe_qutip(U, m=4):
    """
    Simulation du QPE en QuTiP (matrices de densité).
    U : matrice unitaire (Qobj)
    m : nombre de qubits de contrôle
    """
    N = U.shape[0]
    n = int(np.log2(N))
    assert 2**n == N, "U doit agir sur un nombre entier de qubits"

    dim_cont = 2**m
    dim_sys = N

    # État propre |1⟩ du système
    psi_sys = qt.basis(N, 1)

    # État initial : |0⟩_cont ⊗ |1⟩_sys
    psi0 = qt.tensor(qt.basis(dim_cont, 0), psi_sys)

    # Hadamard sur les qubits de contrôle
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
        # Construire le contrôlé : appliquer U_pow si le j-ème qubit = |1⟩
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

---

## Complexité et avantage quantique

| Tâche | Classique | Quantique (QPE) |
|-------|-----------|-----------------|
| Estimer $\theta$ à $\epsilon$ près | $O(1/\epsilon)$ applications de $U$ | $O(1/\epsilon)$ applications de $U$ |
| Simulation d'énergie propre | Diagonalisation $O(2^{3n})$ | QPE $O(n^2/\epsilon)$ |
| Trouver l'ordre $r$ (Shor) | $O(e^{n^{1/3}})$ (crible) | $O(n^3)$ (QPE + class post) |

**Pourquoi la QPE est-elle puissante ?** Elle permet d'estimer les valeurs propres d'un opérateur exponentiellement grand ($2^n \times 2^n$) en utilisant seulement $n$ qubits. C'est la base de la simulation quantique et de l'algorithme de Shor.

---

## À retenir

1. La QPE estime la phase $\theta$ d'un état propre $U|\psi\rangle = e^{2\pi i\theta}|\psi\rangle$
2. Elle utilise $m$ qubits de contrôle et des applications contrôlées de $U^{2^j}$
3. La **QFT inverse** décode les phases accumulées en un état binaire lisible
4. La précision est $\epsilon \sim 2^{-m}$ avec probabilité $\geq 4/\pi^2$
5. Pour une probabilité $1 - 2^{-p}$, il faut $m + p$ qubits de contrôle
6. La QPE est le cœur de **Shor** (estimation de période) et de la **simulation Hamiltonienne**
7. L'efficacité dépend de la capacité à implémenter $U^{2^j}$ efficacement

---

## Pièges à éviter

1. **Confondre $\theta$ et $e^{2\pi i\theta}$** : $\theta$ est la phase (réelle), $e^{2\pi i\theta}$ est la valeur propre
2. **Oublier de préparer l'état propre** : si $|\psi\rangle$ n'est pas un état propre, la QPE donne un mélange de phases
3. **Négliger l'erreur d'approximation** : si $\theta$ n'est pas exactement représentable sur $m$ bits, il y a une fuite de probabilité
4. **Confondre QPE et QFT** : la QPE utilise la QFT inverse, mais son but est d'estimer une phase, pas de transformer un état
5. **Sous-estimer le coût de $U^{2^j}$** : pour Shor, $U^{2^j}$ nécessite $O(2^j)$ portes, ce qui domine la complexité

---

## Exercices

### Niveau 1 — Application directe

**Exercice 1** : Montrez que $P(|a\rangle) \geq 4/\pi^2$ quand $\theta$ est approximé sur $m$ bits.

**Exercice 2** : Implémentez le QPE en Cirq pour $U = T = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{pmatrix}$.

### Niveau 2 — Compréhension

**Exercice 3** : Implémentez le QPE itératif (IQPE) qui utilise 1 seul qubit de contrôle et améliore itérativement la précision.

```python
def iqpe(U, theta_true, precision_bits=8):
    """
    QPE itératif : 1 qubit de contrôle, mesure séquentielle.
    À chaque étape k, on estime le k-ème bit de θ.
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

**Exercice 4** : Utilisez QPE pour estimer l'énergie de l'état fondamental de $H_2$ (Hamiltonien de Pariseau). Utilisez QuTiP pour diagonaliser $H$ et vérifiez.

### Niveau 3 — Défi

**Exercice 5** : Simulez le QPE avec un canal de déphasage (dephasing noise) sur les qubits de contrôle. Tracez la fidélité en fonction du taux de bruit.

**Exercice 6** : Pour l'algorithme de Shor avec $N=15$, combien de qubits de contrôle sont nécessaires pour distinguer les facteurs avec probabilité $>0.99$ ?

---

## Pour aller plus loin

- Le **QPE itératif** (IQPE) réduit le nombre de qubits à 1 au prix de mesures séquentielles
- L'**estimation d'amplitude** (Amplitude Estimation) combine QPE et Grover pour accélérer l'estimation de probabilités
- La **simulation Hamiltonienne** utilise QPE pour estimer les énergies propres, avec des applications en chimie quantique

---

## Références

- Kitaev, A. Y. (1995). "Quantum measurements and the Abelian Stabilizer Problem". *arXiv:quant-ph/9511026*.
- Nielsen, M. A. & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*.
- Aspuru-Guzik, A. et al. (2005). "Simulated Quantum Computation of Molecular Energies". *Science*, 309, 1704–1707.
