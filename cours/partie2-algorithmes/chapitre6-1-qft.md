# Chapitre 6.1 — Quantum Fourier Transform (QFT)

## Objectifs

- Maîtriser la définition mathématique de la QFT et ses propriétés
- Comprendre le circuit $O(n^2)$ et sa décomposition en portes élémentaires
- Implémenter la QFT de manière récursive en Qiskit
- Comparer la QFT avec la FFT classique

---

## 1. Définition mathématique

### Transformée de Fourier discrète classique

Soit $x = (x_0, \ldots, x_{N-1}) \in \mathbb{C}^N$. La DFT classique est :

$$y_k = \frac{1}{\sqrt{N}} \sum_{j=0}^{N-1} x_j \, \omega_N^{jk}, \quad \omega_N = e^{2\pi i / N}$$

### Transformée de Fourier quantique

La QFT est une transformation unitaire sur $n$ qubits ($N = 2^n$) définie par son action sur les états de base $|j\rangle$ :

$$QFT_N |j\rangle = \frac{1}{\sqrt{N}} \sum_{k=0}^{N-1} \omega_N^{jk} |k\rangle$$

où $\omega_N = e^{2\pi i / N}$.

### Forme produit tensoriel

En écrivant $j = j_1 j_2 \ldots j_n$ et $k = k_1 k_2 \ldots k_n$ en binaire, avec $j = \sum_{l=1}^n j_l 2^{n-l}$ :

$$QFT_N |j\rangle = \bigotimes_{l=1}^n \frac{1}{\sqrt{2}} \left( |0\rangle + e^{2\pi i \, 0.j_{n-l+1} \ldots j_n} |1\rangle \right)$$

où $0.j_l j_{l+1} \ldots j_n = j_l/2 + j_{l+1}/4 + \cdots + j_n/2^{n-l+1}$.

**Exemple** : Pour $n=2$, $|j\rangle = |j_1 j_2\rangle$ :

$$QFT_4 |j_1 j_2\rangle = \frac{1}{2} (|0\rangle + e^{2\pi i (0.j_2)}|1\rangle) \otimes (|0\rangle + e^{2\pi i (0.j_1 j_2)}|1\rangle)$$

### Propriétés importantes

- **Unitaire** : $QFT^\dagger QFT = I$
- **Inverse** : $QFT_N^{-1} |k\rangle = \frac{1}{\sqrt{N}} \sum_{j=0}^{N-1} \omega_N^{-jk} |j\rangle$
- **Périodicité** : La QFT d'un état périodique $|\psi\rangle = \sum_r |x_0 + rP\rangle$ a des pics aux multiples de $N/P$

## 2. Circuit quantique $O(n^2)$

### Portes élémentaires

**Porte Hadamard** :
$$H = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$$

**Porte de phase contrôlée** $CR_k$ :
$$CR_k = \begin{pmatrix} I & 0 \\ 0 & R_k \end{pmatrix}, \quad R_k = \begin{pmatrix} 1 & 0 \\ 0 & e^{2\pi i / 2^k} \end{pmatrix}$$

### Circuit QFT

```
|j_1⟩ — H — CR_2 — CR_3 — ··· — CR_n — — — — — — — — — — — — — — — — —
            |       |            |
|j_2⟩ — — — • — CR_2 — ··· — CR_{n-1} — H — CR_2 — ··· — — — — — — — —
                  |            |              |
|j_3⟩ — — — — — — • — ··· — — • — — — — — — • — H — ··· — — — —
                          |                          |
⋮                        ⋮                          ⋮
|j_n⟩ — — — — — — — — — • — — — — — — — — — — — • — — — — H — SWAP
```

### Décomposition récursive

$$QFT_n = (I \otimes QFT_{n-1}) \cdot \prod_{k=2}^n CR_{k} \cdot (H \otimes I^{\otimes n-1})$$

où $CR_k$ est contrôlée par le premier qubit sur le $k$-ième qubit.

### Complexité

- Nombre de portes : $n + (n-1) + \cdots + 1 = n(n+1)/2 = O(n^2)$
- Avec les SWAP finaux pour inverser l'ordre des qubits : $O(n^2)$
- Classique FFT : $O(N \log N) = O(n 2^n)$ — exponentiellement plus lent

## 3. Implémentation récursive Qiskit

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

def qft_recursif(qc, n, start=0):
    """
    Implémente la QFT de manière récursive.
    qc : QuantumCircuit
    n : nombre de qubits
    start : index du premier qubit
    """
    if n <= 0:
        return
    if n == 1:
        qc.h(start)
        return

    # Hadamard sur le premier qubit
    qc.h(start)

    # Portes CR_k contrôlées
    for k in range(2, n + 1):
        angle = 2 * np.pi / (2**k)
        qc.cp(angle, start + k - 1, start)

    # Appel récursif sur les (n-1) qubits restants
    qft_recursif(qc, n - 1, start + 1)

def qft_swap(qc, n):
    """Inverse l'ordre des qubits (étape finale de la QFT)"""
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)

def qft_complet(qc, n):
    """QFT complète avec SWAP finaux"""
    qft_recursif(qc, n)
    qft_swap(qc, n)

# Test sur 3 qubits
n = 3
qc = QuantumCircuit(n, n)
qft_complet(qc, n)

print("Circuit QFT (3 qubits) :")
print(qc.draw())

# Vérification sur un état de base
def test_qft_basis(j, n=3):
    qc = QuantumCircuit(n, n)
    # Préparer |j⟩
    j_bits = format(j, f'0{n}b')
    for i, bit in enumerate(j_bits):
        if bit == '1':
            qc.x(i)

    # Appliquer QFT
    qft_complet(qc, n)

    # Mesurer
    qc.measure(range(n), range(n))

    backend = AerSimulator()
    result = backend.run(qc, shots=2048).result()
    counts = result.get_counts()

    # Distribution de probabilité (devrait être uniforme)
    print(f"\nÉtat |{j}⟩ → QFT → distribution :")
    for state, count in sorted(counts.items(), key=lambda x: int(x[0])):
        prob = count / 2048
        print(f"  |{state}⟩ : {prob:.3f}")

test_qft_basis(3, n=3)
```

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def qft_iteratif(qc, n):
    """Version itérative de la QFT pour comparaison"""
    for i in range(n):
        qc.h(i)
        for j in range(i + 1, n):
            angle = 2 * np.pi / (2**(j - i + 1))
            qc.cp(angle, j, i)
    qft_swap(qc, n)

# Comparaison des deux implémentations
def qft_dagger(qc, n):
    """QFT inverse (utilisée dans QPE)"""
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            angle = -2 * np.pi / (2**(j - i + 1))
            qc.cp(angle, j, i)
        qc.h(i)

# Test de la QFT inverse
print("Test QFT + QFT† = Identité")
n = 3
qc = QuantumCircuit(n, n)
# État quelconque
qc.x(0)
qc.x(2)

# QFT
qft_complet(qc, n)

# QFT†
qft_dagger(qc, n)

# Mesure
qc.measure(range(n), range(n))

backend = AerSimulator()
result = backend.run(qc, shots=1024).result()
counts = result.get_counts()
print(f"Résultat (devrait être 101) : {counts}")
```

## 4. Comparaison avec la FFT classique

```python
import numpy as np
import time

def fft_classique(x):
    """FFT classique via NumPy"""
    return np.fft.fft(x) / np.sqrt(len(x))

def qft_simule(x):
    """
    Simulation de la QFT sur un état classique.
    x : vecteur de taille N=2^n
    """
    N = len(x)
    n = int(np.log2(N))
    assert 2**n == N

    result = np.zeros(N, dtype=complex)
    for j in range(N):
        for k in range(N):
            result[k] += x[j] * np.exp(2j * np.pi * j * k / N)
    return result / np.sqrt(N)

def qft_matrice(N):
    """Matrice de la QFT"""
    n = int(np.log2(N))
    omega = np.exp(2j * np.pi / N)
    Q = np.zeros((N, N), dtype=complex)
    for j in range(N):
        for k in range(N):
            Q[j, k] = omega**(j * k) / np.sqrt(N)
    return Q

# Vérification sur un état simple
N = 8
x = np.zeros(N)
x[0] = 1.0  # |000⟩

# FFT classique
y_fft = fft_classique(x)

# Matrice QFT
Q = qft_matrice(N)
y_qft = Q @ x

print("Comparaison QFT vs FFT sur |000⟩ :")
print(f"  QFT[0] = {y_qft[0]:.6f}")
print(f"  FFT[0] = {y_fft[0]:.6f}")
print(f"  Match : {np.allclose(y_qft, y_fft)}")

# Analyse de complexité
print("\nComplexité temporelle :")
for n in range(2, 8):
    N = 2**n
    x = np.random.rand(N)

    t0 = time.perf_counter()
    _ = np.fft.fft(x)
    t_fft = time.perf_counter() - t0

    t0 = time.perf_counter()
    _ = qft_matrice(N) @ x
    t_qft = time.perf_counter() - t0

    print(f"  n={n}, N={N} : FFT={t_fft:.6f}s, QFT naïve={t_qft:.6f}s, ratio={t_qft/t_fft:.1f}")
```

**Sortie attendue :**

```
Comparaison QFT vs FFT sur |000⟩ :
  QFT[0] = 0.353553+0.000000j
  FFT[0] = 0.353553+0.000000j
  Match : True

Complexité temporelle :
  n=2, N=4 : FFT=0.000132s, QFT naïve=0.000256s, ratio=1.9
  n=3, N=8 : FFT=0.000060s, QFT naïve=0.000708s, ratio=11.9
  n=4, N=16 : FFT=0.000057s, QFT naïve=0.002948s, ratio=52.0
  n=5, N=32 : FFT=0.000122s, QFT naïve=0.011235s, ratio=91.7
  n=6, N=64 : FFT=0.000082s, QFT naïve=0.054307s, ratio=665.2
  n=7, N=128 : FFT=0.000107s, QFT naïve=0.272459s, ratio=2545.6
```

```python
import numpy as np
import matplotlib.pyplot as plt

def visualisation_qft_periodique():
    """
    Visualise le comportement de la QFT sur un état périodique.
    Utile pour comprendre l'algorithme de Shor.
    """
    N = 16
    period = 4  # Période du signal

    # État périodique : |0⟩ + |4⟩ + |8⟩ + |12⟩
    psi = np.zeros(N)
    for r in range(0, N, period):
        psi[r] = 1.0
    psi = psi / np.linalg.norm(psi)

    print(f"État périodique (période={period}) :")
    print(f"  |ψ⟩ = {[f'{amp:.2f}' for amp in psi]}")

    # QFT
    Q = qft_matrice(N)
    psi_qft = Q @ psi
    probs = np.abs(psi_qft)**2

    print(f"\nDistribution après QFT :")
    for i, p in enumerate(probs):
        if p > 0.01:
            print(f"  |{i}⟩ : p={p:.3f}")

    # Les pics sont à k = 0, N/4, N/2, 3N/4 = 0, 4, 8, 12
    # N/period = 4
    expected_peaks = [0, N // period, 2 * N // period, 3 * N // period]
    print(f"\nPics attendus à {expected_peaks}")

visualisation_qft_periodique()
```

**Sortie attendue :**

```
État périodique (période=4) :
  |ψ⟩ = ['0.50', '0.00', '0.00', '0.00', '0.50', '0.00', '0.00', '0.00', '0.50', '0.00', '0.00', '0.00', '0.50', '0.00', '0.00', '0.00']

Distribution après QFT :
  |0⟩ : p=0.250
  |4⟩ : p=0.250
  |8⟩ : p=0.250
  |12⟩ : p=0.250

Pics attendus à [0, 4, 8, 12]
```

## 5. Exercices

### Exercice 1 : Preuve de l'unitarité
Montrez que $QFT_N$ est unitaire : $QFT_N^\dagger QFT_N = I$.

### Exercice 2 : Circuit à 3 qubits — vérification manuelle
Calculez explicitement $QFT_8 |5\rangle$ (où $5 = 101_2$) en utilisant la forme produit tensoriel.

### Exercice 3 : Implémentation Cirq
Implémentez la QFT en Cirq et comparez le circuit avec Qiskit.

```python
import cirq
import numpy as np

def qft_cirq(qubits):
    """QFT en Cirq"""
    n = len(qubits)
    operations = []
    for i in range(n):
        operations.append(cirq.H(qubits[i]))
        for j in range(i + 1, n):
            angle = 2 * np.pi / (2**(j - i + 1))
            operations.append(cirq.CZPowGate(exponent=angle/np.pi).on(
                qubits[j], qubits[i]))
    # SWAP
    for i in range(n // 2):
        operations.append(cirq.SWAP(qubits[i], qubits[n - 1 - i]))
    return cirq.Circuit(operations)

# Complétez...
```

### Exercice 4 : QFT exacte vs approchée
Comparez la QFT exacte avec la QFT approchée (en tronquant les rotations à $R_m$ pour $m < n$). Quelle est la fidélité en fonction de $m$ ?

### Exercice 5 : Application — Addition quantique
Utilisez la QFT pour implémenter l'addition quantique : $QFT^\dagger (QFT|a\rangle \cdot QFT|b\rangle)$.

### Exercice 6 : Profondeur du circuit
Analysez la profondeur du circuit QFT. Montrez qu'elle peut être réduite à $O(n)$ en utilisant l'architecture de qubits voisins (nearest-neighbor).

---

## Références

- Coppersmith, D. (1994). "An approximate Fourier transform useful in quantum factoring". *IBM Research Report* RC19642.
- Nielsen, M. A. & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*.
- Cleve, R. & Watrous, J. (2000). "Fast parallel circuits for the quantum Fourier transform". *Proc. 41st FOCS*, 526–536.
