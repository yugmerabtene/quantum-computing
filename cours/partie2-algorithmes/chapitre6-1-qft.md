# Chapitre 6.1 — Quantum Fourier Transform (QFT)

## Ce que vous allez apprendre

- Maîtriser la **définition mathématique** de la QFT et ses propriétés fondamentales
- Comprendre le **circuit $O(n^2)$** et sa décomposition en portes élémentaires (Hadamard + phases contrôlées)
- Implémenter la QFT de manière **récursive et itérative** en Qiskit
- Comparer la QFT avec la **FFT classique** et comprendre pourquoi la QFT est un outil central
- Visualiser l'effet de la QFT sur des **états périodiques** (préparation pour Shor)

---

## Motivation

La transformée de Fourier est partout : traitement du signal, compression d'images, résolution d'équations différentielles, analyse spectrale... En informatique classique, la FFT (Fast Fourier Transform) calcule la transformée de Fourier discrète sur $N$ points en $O(N \log N)$ opérations.

En calcul quantique, la QFT fait la même chose, mais sur des **amplitudes de probabilité**. Et elle le fait en seulement $O(n^2)$ portes, où $n = \log_2 N$. C'est une accélération exponentielle par rapport à la FFT classique !

Mais attention : on ne peut pas « lire » le résultat directement (la mesure donne un seul échantillon). La puissance de la QFT réside dans le fait qu'elle transforme la **périodicité** en **pics de probabilité** détectables. C'est exactement ce qu'utilise l'algorithme de Shor pour trouver la période d'une fonction et factoriser des nombres.

La QFT est aussi le composant central de l'estimation de phase quantique (QPE, chapitre 6.2), elle-même cœur de l'algorithme de Shor (chapitre 7.1).

---

## Idée principale

Imaginez que vous avez un signal musical. La transformée de Fourier vous dit quelles notes (fréquences) le composent. La QFT fait la même chose, mais pour un état quantique.

Si un état quantique a une structure périodique (par exemple, $|0\rangle + |r\rangle + |2r\rangle + \cdots$), la QFT transforme cette périodicité en **pics** aux multiples de $N/r$. C'est comme passer du domaine temporel au domaine fréquentiel.

L'astuce du circuit quantique, c'est que chaque qubit de sortie est contrôlé par une combinaison de phases qui « détecte » une fréquence spécifique. Le premier qubit détecte la fréquence la plus basse, le second la fréquence double, etc.

---

## Contenu du cours

### Section 1 : Définition mathématique

**Rappel classique** : La DFT (Discrete Fourier Transform) sur un vecteur $x = (x_0, \ldots, x_{N-1}) \in \mathbb{C}^N$ :

$$y_k = \frac{1}{\sqrt{N}} \sum_{j=0}^{N-1} x_j \, \omega_N^{jk}, \quad \omega_N = e^{2\pi i / N}$$

**Intuition** : chaque composante $y_k$ mesure « combien » le signal $x$ ressemble à l'oscillation de fréquence $k$.

**Variables** : $N$ = taille du signal, $\omega_N$ = racine $N$-ième de l'unité.

**QFT** : transformation unitaire sur $n$ qubits ($N = 2^n$) définie par :

$$QFT_N |j\rangle = \frac{1}{\sqrt{N}} \sum_{k=0}^{N-1} \omega_N^{jk} |k\rangle$$

**Exemple numérique** : $N = 4$ ($n = 2$), $j = 1$ :
$$QFT_4 |1\rangle = \frac{1}{2}(|0\rangle + i|1\rangle - |2\rangle - i|3\rangle)$$

### Section 2 : Forme produit tensoriel

C'est la forme la plus utile pour construire le circuit. En écrivant $j = j_1 j_2 \ldots j_n$ en binaire :

$$QFT_N |j\rangle = \bigotimes_{l=1}^n \frac{1}{\sqrt{2}} \left( |0\rangle + e^{2\pi i \, 0.j_{n-l+1} \ldots j_n} |1\rangle \right)$$

où $0.j_l j_{l+1} \ldots j_n = j_l/2 + j_{l+1}/4 + \cdots + j_n/2^{n-l+1}$ est une fraction binaire.

**Intuition** : chaque qubit de sortie est dans un état $\frac{1}{\sqrt{2}}(|0\rangle + e^{i\phi}|1\rangle)$ où la phase $\phi$ dépend des bits de $j$. Le qubit $l$ « lit » les $l$ derniers bits de $j$ avec des poids décroissants.

**Exemple** : $n = 2$, $|j\rangle = |j_1 j_2\rangle$ :
$$QFT_4 |j_1 j_2\rangle = \frac{1}{2} (|0\rangle + e^{2\pi i (0.j_2)}|1\rangle) \otimes (|0\rangle + e^{2\pi i (0.j_1 j_2)}|1\rangle)$$

Pour $j = 1$ ($j_1 = 0, j_2 = 1$) :
- Qubit 1 : $\frac{1}{\sqrt{2}}(|0\rangle + e^{2\pi i \cdot 0.1}|1\rangle) = \frac{1}{\sqrt{2}}(|0\rangle + e^{i\pi}|1\rangle) = |-\rangle$
- Qubit 2 : $\frac{1}{\sqrt{2}}(|0\rangle + e^{2\pi i \cdot 0.01}|1\rangle) = \frac{1}{\sqrt{2}}(|0\rangle + e^{i\pi/2}|1\rangle) = \frac{1}{\sqrt{2}}(|0\rangle + i|1\rangle)$

### Section 3 : Le circuit $O(n^2)$

**Portes élémentaires** :

Porte Hadamard :
$$H = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$$

Porte de phase contrôlée $CR_k$ :
$$CR_k = \begin{pmatrix} I & 0 \\ 0 & R_k \end{pmatrix}, \quad R_k = \begin{pmatrix} 1 & 0 \\ 0 & e^{2\pi i / 2^k} \end{pmatrix}$$

**Intuition** : $CR_k$ applique une rotation de phase $e^{2\pi i / 2^k}$ sur le qubit cible, **seulement si** le qubit de contrôle est $|1\rangle$.

**Circuit QFT** :
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

**Pourquoi ce circuit ?** Sur le premier qubit, on applique $H$ puis des $CR_k$ contrôlés par les qubits $2, 3, \ldots, n$. Cela construit la phase $0.j_1 j_2 \ldots j_n$. Puis on répète récursivement sur les $n-1$ qubits restants.

**Complexité** : $n + (n-1) + \cdots + 1 = n(n+1)/2 = O(n^2)$ portes. Plus $n/2$ SWAP pour inverser l'ordre des qubits.

### Section 4 : Propriétés importantes

- **Unitaire** : $QFT^\dagger QFT = I$ (on peut inverser la transformation)
- **Inverse** : $QFT_N^{-1} |k\rangle = \frac{1}{\sqrt{N}} \sum_{j=0}^{N-1} \omega_N^{-jk} |j\rangle$
- **Périodicité** : La QFT d'un état périodique $|\psi\rangle = \sum_r |x_0 + rP\rangle$ a des pics aux multiples de $N/P$

**Exemple** : $N = 16$, période $P = 4$. État : $|0\rangle + |4\rangle + |8\rangle + |12\rangle$. Après QFT : pics à $k = 0, 4, 8, 12$ (multiples de $16/4 = 4$).

---

## Exemple guidé

Calculons $QFT_4 |3\rangle$ (où $3 = 11_2$, donc $j_1 = 1, j_2 = 1$).

**Formule produit tensoriel** :
$$QFT_4 |11\rangle = \frac{1}{2}(|0\rangle + e^{2\pi i \cdot 0.1}|1\rangle) \otimes (|0\rangle + e^{2\pi i \cdot 0.11}|1\rangle)$$

- $0.1 = 1/2$, donc $e^{2\pi i \cdot 1/2} = e^{i\pi} = -1$
- $0.11 = 1/2 + 1/4 = 3/4$, donc $e^{2\pi i \cdot 3/4} = e^{i 3\pi/2} = -i$

$$QFT_4 |3\rangle = \frac{1}{2}(|0\rangle - |1\rangle) \otimes (|0\rangle - i|1\rangle) = |-\rangle \otimes \frac{1}{\sqrt{2}}(|0\rangle - i|1\rangle)$$

**Vérification par la définition** :
$$QFT_4 |3\rangle = \frac{1}{2}\sum_{k=0}^{3} \omega_4^{3k}|k\rangle = \frac{1}{2}(|0\rangle + i^3|1\rangle + i^6|2\rangle + i^9|3\rangle)$$
$$= \frac{1}{2}(|0\rangle - i|1\rangle - |2\rangle + i|3\rangle)$$

Développons notre résultat :
$$\frac{1}{2}(|00\rangle - i|01\rangle - |10\rangle + i|11\rangle) = \frac{1}{2}(|0\rangle - i|1\rangle - |2\rangle + i|3\rangle) \quad ✓$$

---

## Implémentation Python

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# --- QFT récursive ---
def qft_recursif(qc, n, start=0):
    """
    Implémente la QFT de manière récursive.
    qc : QuantumCircuit
    n : nombre de qubits sur lesquels appliquer la QFT
    start : index du premier qubit
    """
    if n <= 0:
        return
    if n == 1:
        qc.h(start)  # Cas de base : QFT sur 1 qubit = Hadamard
        return

    # Hadamard sur le premier qubit
    qc.h(start)

    # Portes de phase contrôlées CR_k
    # Le qubit 'start+k-1' contrôle une rotation de phase sur 'start'
    for k in range(2, n + 1):
        angle = 2 * np.pi / (2**k)
        qc.cp(angle, start + k - 1, start)

    # Appel récursif sur les (n-1) qubits restants
    qft_recursif(qc, n - 1, start + 1)

# --- SWAP finaux pour inverser l'ordre des qubits ---
def qft_swap(qc, n):
    """Inverse l'ordre des qubits (nécessaire car la QFT les produit en ordre inversé)"""
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)

# --- QFT complète ---
def qft_complet(qc, n):
    """QFT complète avec SWAP finaux"""
    qft_recursif(qc, n)
    qft_swap(qc, n)

# --- Test sur 3 qubits ---
n = 3
qc = QuantumCircuit(n, n)
qft_complet(qc, n)

print("Circuit QFT (3 qubits) :")
print(qc.draw())

# --- Vérification sur un état de base ---
def test_qft_basis(j, n=3):
    """
    Teste la QFT sur l'état |j⟩.
    La QFT d'un état de base donne une distribution uniforme en module,
    mais avec des phases différentes.
    """
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

    # Distribution de probabilité (doit être uniforme)
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

# --- QFT itérative ---
def qft_iteratif(qc, n):
    """Version itérative de la QFT (plus facile à déboguer)"""
    for i in range(n):
        qc.h(i)  # Hadamard sur le qubit i
        for j in range(i + 1, n):
            angle = 2 * np.pi / (2**(j - i + 1))
            qc.cp(angle, j, i)  # Phase contrôlée
    qft_swap(qc, n)

# --- QFT inverse (QFT†) ---
def qft_dagger(qc, n):
    """
    QFT inverse : applique QFT†.
    Nécessaire dans QPE et Shor.
    C'est l'inverse exact : QFT† · QFT = I.
    """
    # D'abord les SWAP (dans l'ordre inverse)
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)
    # Puis les portes dans l'ordre inverse, avec angles négatifs
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            angle = -2 * np.pi / (2**(j - i + 1))
            qc.cp(angle, j, i)
        qc.h(i)

# --- Test : QFT + QFT† = Identité ---
print("Test QFT + QFT† = Identité")
n = 3
qc = QuantumCircuit(n, n)
# État quelconque : |101⟩
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

```python
import numpy as np
import time

# --- Comparaison QFT vs FFT classique ---
def fft_classique(x):
    """FFT classique via NumPy (normalisée)"""
    return np.fft.fft(x) / np.sqrt(len(x))

def qft_matrice(N):
    """
    Construit la matrice de la QFT de taille N×N.
    Attention : exponentiel en mémoire ! Seulement pour petit N.
    """
    n = int(np.log2(N))
    omega = np.exp(2j * np.pi / N)
    Q = np.zeros((N, N), dtype=complex)
    for j in range(N):
        for k in range(N):
            Q[j, k] = omega**(j * k) / np.sqrt(N)
    return Q

# Vérification sur |000⟩
N = 8
x = np.zeros(N)
x[0] = 1.0  # |000⟩

y_fft = fft_classique(x)
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

# --- Visualisation : QFT sur un état périodique ---
def visualisation_qft_periodique():
    """
    Montre que la QFT transforme la périodicité en pics.
    C'est le principe utilisé par Shor.
    """
    N = 16
    period = 4  # Période du signal

    # État périodique : |0⟩ + |4⟩ + |8⟩ + |12⟩ (normalisé)
    psi = np.zeros(N)
    for r in range(0, N, period):
        psi[r] = 1.0
    psi = psi / np.linalg.norm(psi)

    print(f"État périodique (période={period}) :")
    print(f"  |ψ⟩ = {[f'{amp:.2f}' for amp in psi]}")

    # Application de la QFT
    Q = qft_matrice(N)
    psi_qft = Q @ psi
    probs = np.abs(psi_qft)**2

    print(f"\nDistribution après QFT :")
    for i, p in enumerate(probs):
        if p > 0.01:
            print(f"  |{i}⟩ : p={p:.3f}")

    # Les pics sont à k = 0, N/period, 2N/period, 3N/period
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

---

## Complexité et avantage quantique

| Opération | Classique | Quantique |
|-----------|-----------|-----------|
| DFT sur $N = 2^n$ éléments | $O(N \log N) = O(n 2^n)$ (FFT) | $O(n^2)$ portes |
| Transformation des amplitudes | $O(N^2)$ naïf | $O(n^2)$ |
| Accès au résultat | Complet (tous les $y_k$) | Un seul échantillon par mesure |

**Pourquoi la QFT est-elle plus rapide ?** La FFT classique exploite la structure récursive de la DFT pour passer de $O(N^2)$ à $O(N \log N)$. La QFT exploite la même structure, mais en plus elle travaille sur des **amplitudes** encodées dans des qubits, ce qui permet de représenter $N$ valeurs avec seulement $n = \log_2 N$ qubits.

**Attention** : la QFT ne donne pas un accès rapide à tous les coefficients de Fourier. Elle transforme l'état quantique, mais la mesure ne donne qu'un échantillon. Sa puissance réside dans les **interférences** qu'elle crée, pas dans le calcul de la DFT elle-même.

---

## À retenir

1. La QFT est la version quantique de la transformée de Fourier discrète
2. Elle s'écrit comme un **produit tensoriel** de qubits avec des phases contrôlées
3. Le circuit utilise $O(n^2)$ portes : Hadamard + portes de phase contrôlées $CR_k$
4. La QFT transforme la **périodicité** en **pics de probabilité**
5. La QFT inverse ($QFT^\dagger$) est essentielle dans QPE et Shor
6. Comparée à la FFT classique ($O(N \log N)$), la QFT est exponentiellement plus rapide en nombre de portes
7. Mais on ne peut pas « lire » tous les coefficients : la mesure donne un seul échantillon

---

## Pièges à éviter

1. **Confondre QFT et FFT** : la QFT transforme un état quantique, pas un tableau classique
2. **Oublier les SWAP finaux** : sans eux, les qubits de sortie sont en ordre inversé
3. **Penser qu'on peut lire tous les coefficients** : la mesure ne donne qu'un échantillon aléatoire
4. **Négliger la précision** : pour des phases non exactes, la QFT approchée peut suffire (tronquer les $R_k$ pour $k$ grand)
5. **Confondre $n$ et $N$** : $n$ = nombre de qubits, $N = 2^n$ = dimension de l'espace

---

## Exercices

### Niveau 1 — Application directe

**Exercice 1** : Montrez que $QFT_N$ est unitaire : $QFT_N^\dagger QFT_N = I$.

**Exercice 2** : Calculez explicitement $QFT_8 |5\rangle$ (où $5 = 101_2$) en utilisant la forme produit tensoriel.

### Niveau 2 — Compréhension

**Exercice 3** : Implémentez la QFT en Cirq et comparez le circuit avec Qiskit.

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

**Exercice 4** : Comparez la QFT exacte avec la QFT approchée (en tronquant les rotations à $R_m$ pour $m < n$). Quelle est la fidélité en fonction de $m$ ?

### Niveau 3 — Défi

**Exercice 5** : Utilisez la QFT pour implémenter l'addition quantique : $QFT^\dagger (QFT|a\rangle \cdot QFT|b\rangle)$.

**Exercice 6** : Analysez la profondeur du circuit QFT. Montrez qu'elle peut être réduite à $O(n)$ en utilisant l'architecture de qubits voisins (nearest-neighbor).

---

## Pour aller plus loin

- La **QFT approchée** (approximate QFT) tronque les petites rotations et reste fidèle avec $O(n \log n)$ portes
- La QFT est le composant central de la **QPE** (chapitre 6.2) et de l'**algorithme de Shor** (chapitre 7.1)
- L'**addition quantique** via QFT est plus efficace que l'addition par portes logiques

---

## Références

- Coppersmith, D. (1994). "An approximate Fourier transform useful in quantum factoring". *IBM Research Report* RC19642.
- Nielsen, M. A. & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*.
- Cleve, R. & Watrous, J. (2000). "Fast parallel circuits for the quantum Fourier transform". *Proc. 41st FOCS*, 526–536.
