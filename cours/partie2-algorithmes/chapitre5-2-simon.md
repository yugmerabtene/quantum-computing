# Chapitre 5.2 — Algorithme de Simon

## Objectifs d'apprentissage

- Comprendre le problème de la période cachée en groupe abélien
- Maîtriser la transformée de Hadamard pour la détection de période
- Établir le lien avec la Quantum Fourier Transform (QFT)
- Implémenter l'algorithme de Simon en Qiskit

---

## 1. Problème de Simon

**Problème** : Soit $f : \{0,1\}^n \to \{0,1\}^n$ avec la **promesse** qu'il existe $s \in \{0,1\}^n \setminus \{0\}$ tel que :

$$
f(x) = f(y) \iff y = x \oplus s \quad \forall x,y \in \{0,1\}^n
$$

où $\oplus$ est le XOR bit à bit. Trouver $s$.

Classiquement : $O(2^{n/2})$ appels (recherche de collision). Quantiquement : $O(n)$ appels.

C'est le premier algorithme démontrant un avantage exponentiel **prouvé** sur un oracle.

## 2. Circuit de Simon

```
|0⟩^{\otimes n} — H^{\otimes n} — U_f — H^{\otimes n} — M
                                 |
|0⟩^{\otimes n} — — — — — — — — — — — — M
```

### Étapes détaillées

**État initial** :
$$|\psi_0\rangle = |0\rangle^{\otimes n}|0\rangle^{\otimes n}$$

**Première Hadamard** :
$$|\psi_1\rangle = \frac{1}{\sqrt{2^n}} \sum_{x=0}^{2^n-1} |x\rangle |0\rangle^{\otimes n}$$

**Oracle** $U_f : |x\rangle|y\rangle \mapsto |x\rangle|y \oplus f(x)\rangle$ :
$$|\psi_2\rangle = \frac{1}{\sqrt{2^n}} \sum_{x=0}^{2^n-1} |x\rangle |f(x)\rangle$$

**Seconde Hadamard** sur le premier registre :
$$|\psi_3\rangle = \frac{1}{2^n} \sum_{x=0}^{2^n-1} \sum_{y=0}^{2^n-1} (-1)^{x\cdot y} |y\rangle |f(x)\rangle$$

### Mesure du premier registre

On mesure $y$. Quelle est la distribution ?

$$P(y) = \frac{1}{2^n} \sum_{x: f(x)=f(x_0)} |(-1)^{x\cdot y} + (-1)^{(x\oplus s)\cdot y}|^2$$

Pour chaque paire $(x, x\oplus s)$ :
$$(-1)^{x\cdot y} + (-1)^{(x\oplus s)\cdot y} = (-1)^{x\cdot y}\left[1 + (-1)^{s\cdot y}\right]$$

Donc :
- Si $s \cdot y = 0 \pmod 2$ → $P(y) > 0$
- Si $s \cdot y = 1 \pmod 2$ → $P(y) = 0$

Les $y$ mesurés satisfont tous $s \cdot y = 0$ (mod 2).

## 3. Reconstruction de $s$

Après $O(n)$ itérations, on obtient $n-1$ vecteurs $y_1, \ldots, y_{n-1}$ linéairement indépendants. On résout le système linéaire :

$$
\begin{pmatrix}
y_1^{(1)} & \cdots & y_1^{(n)} \\
\vdots & \ddots & \vdots \\
y_{n-1}^{(1)} & \cdots & y_{n-1}^{(n)}
\end{pmatrix}
\begin{pmatrix} s_1 \\ \vdots \\ s_n \end{pmatrix} = \mathbf{0} \pmod 2
$$

$s$ est le vecteur non nul de l'espace nul de dimension 1.

### Complexité

- Classique : $O(2^{n/2})$ requêtes à $f$
- Quantique : $O(n)$ requêtes + $O(n^3)$ classique pour le système linéaire
- **Avantage exponentiel** prouvé dans le modèle des boîtes noires

## 4. Lien avec QFT

Le problème de Simon est un cas particulier du **problème du sous-groupe caché** (Hidden Subgroup Problem) sur $(\mathbb{Z}/2\mathbb{Z})^n$, où le sous-groupe $H = \{0, s\}$ est caché par $f$.

La transformée de Hadamard généralisée est la QFT sur $(\mathbb{Z}/2\mathbb{Z})^n$ :

$$H^{\otimes n}|x\rangle = \frac{1}{\sqrt{2^n}} \sum_{y=0}^{2^n-1} (-1)^{x\cdot y} |y\rangle$$

La QFT sur $\mathbb{Z}/N\mathbb{Z}$ est :
$$QFT_N |x\rangle = \frac{1}{\sqrt{N}} \sum_{y=0}^{N-1} \omega_N^{xy} |y\rangle, \quad \omega_N = e^{2\pi i/N}$$

Simon généralise à $\mathbb{Z}/2\mathbb{Z}$, tandis que Shor utilise $\mathbb{Z}/N\mathbb{Z}$.

## 5. Implémentation Qiskit

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit.providers.aer import QasmSimulator

import random
from collections import Counter

def oracle_simon(qc, n, s):
    """
    Oracle pour Simon : f(x) = f(x⊕s)
    Implémente une fonction 2-vers-1 avec période s.
    """
    # On duplique les qubits d'entrée vers la sortie
    for i in range(n):
        qc.cx(i, n + i)

    # Si s ≠ 0, on applique un XOR avec s sur une copie
    # Pour simplifier : on choisit f(x) = min(x, x⊕s)
    if any(s):
        # On copie x dans le registre de sortie
        # puis on applique CX pour chaque bit de s
        for i in range(n):
            if s[i] == '1':
                for j in range(n):
                    qc.cx(i, n + j)

def simon_circuit(n, s):
    """Construit le circuit de Simon pour une période s donnée"""
    qc = QuantumCircuit(2 * n, n)

    # Hadamard sur les n premiers qubits
    qc.h(range(n))

    # Oracle de Simon
    oracle_simon(qc, n, s)

    # Hadamard sur les n premiers qubits
    qc.h(range(n))

    # Mesure des n premiers qubits
    qc.measure(range(n), range(n))

    return qc

def simon_algorithm(n, s_bits, shots=10):
    """
    Exécute l'algorithme de Simon et détermine s.
    s_bits : string binaire représentant s, ex. '110'
    """
    qc = simon_circuit(n, s_bits)
    backend = QasmSimulator()

    results = []
    while len(results) < n - 1:
        result = backend.run(qc, shots=1).result()
        counts = result.get_counts()
        y = list(counts.keys())[0]
        if y != '0' * n and y not in results:
            results.append(y)
        if len(results) >= n - 1:
            break

    print(f"Période cachée s = {s_bits}")
    print(f"Équations linéaires collectées : {results}")

    # Résolution du système linéaire modulo 2
    # On cherche s ≠ 0 tq y_i · s = 0 (mod 2)
    if len(results) >= n - 1:
        mat = np.array([[int(b) for b in y] for y in results[:n-1]])
        # Résoudre mat @ s = 0 (mod 2)
        # L'espace nul de dimension 1 donne s
        _, _, vh = np.linalg.svd(mat, full_matrices=True)
        s_found = vh[-1, :]
        # Conversion en binaire et arrondi
        s_found_bits = ''.join(str(round(abs(x))) for x in s_found)
        print(f"s reconstruit (SVD) : {s_found_bits}")
        return s_found_bits
    return None

# Test
print("=== Algorithme de Simon ===")
n = 3
s_test = '110'
simon_algorithm(n, s_test, shots=20)
```

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def circuit_complet_simon(n=3, s='101'):
    """Circuit complet de Simon avec affichage"""
    qc = QuantumCircuit(2 * n, n)

    # Initialisation
    qc.h(range(n))

    # Oracle : f(x) = f(x ⊕ s)
    # Utilisation de CX pour chaque bit
    for i in range(n):
        if s[i] == '1':
            for j in range(n):
                qc.cx(i, n + j)

    qc.h(range(n))

    qc.measure(range(n), range(n))

    print(f"Circuit Simon (s={s}) :")
    print(qc.draw())

    backend = AerSimulator()
    result = backend.run(qc, shots=2048).result()
    counts = result.get_counts()

    # Filtrer : seuls les y tq s·y=0 apparaissent
    print("\nDistribution des mesures :")
    for y, count in sorted(counts.items(), key=lambda x: -x[1])[:8]:
        dot = sum(int(y[i]) * int(s[i]) for i in range(n)) % 2
        mark = "✓" if dot == 0 else "✗ (devrait être nul)"
        print(f"  y={y} : {count:4d}  s·y={dot} {mark}")

    return qc, counts

qc_s, counts_s = circuit_complet_simon(3, '101')
```

## 6. Interprétation en terme de sous-groupe caché

Le problème du sous-groupe caché (HSP) est central :

**Définition** : Soit $G$ un groupe abélien, $H$ un sous-groupe de $G$, et $f: G \to X$ telle que $f$ est constante et distincte sur chaque classe $gH$. Trouver un ensemble de générateurs de $H$.

- Simon : $G = (\mathbb{Z}/2\mathbb{Z})^n$, $H = \{0, s\}$
- Shor : $G = \mathbb{Z}/N\mathbb{Z} \times \mathbb{Z}/N\mathbb{Z}$, $H = \{(r, -a \cdot r \bmod N)\}$ (facteurs de $N$)

## 7. Exercices

### Exercice 1 : Simulateur classique
Écrivez un simulateur classique de l'algorithme de Simon pour $n=4$ et vérifiez que $P(y) > 0$ ssi $s \cdot y = 0$.

### Exercice 2 : Analyse de la probabilité
Montrez que $P(y=0) = 2^{-n}$. Combien d'itérations sont nécessaires en moyenne pour obtenir $n-1$ vecteurs indépendants ?

### Exercice 3 : Implémentation avec NumPy
Sans Qiskit, implémentez l'algorithme en utilisant uniquement des matrices NumPy pour $n=3$.

```python
import numpy as np

def hadamard_n(n):
    """Matrice de Hadamard sur n qubits"""
    H1 = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    Hn = H1
    for _ in range(n - 1):
        Hn = np.kron(Hn, H1)
    return Hn

def oracle_simon_mat(n, s):
    """Matrice de l'oracle pour Simon"""
    N = 2**n
    U = np.zeros((N, N))
    for x in range(N):
        x_xor_s = x ^ s
        U[x, x] = 1
        U[x, x_xor_s] = 1
    return U / np.sqrt(2)

# Complétez l'implémentation...
```

### Exercice 4 : Comparaison classique-quantique
Implémentez la recherche classique de collision pour $n$ bits. Comparez le nombre de requêtes pour $n=8,10,12$.

### Exercice 5 : Lien avec le problème du sous-groupe caché
Montrez que l'algorithme de Simon est un cas particulier de l'algorithme HSP sur $(\mathbb{Z}/2\mathbb{Z})^n$ avec $H=\{0,s\}$. Génénalisez à $(\mathbb{Z}/d\mathbb{Z})^n$.

### Exercice 6 : Qiskit — Oracle avec fonction aléatoire
Générez une fonction $f$ 2-vers-1 aléatoire et implémentez l'oracle. Vérifiez que l'algorithme retrouve $s$.

---

## Références

- Simon, D. R. (1997). "On the Power of Quantum Computation". *SIAM J. Comput.*, 26(5), 1474–1483.
- Nielsen, M. A. & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*.
- Childs, A. M. & van Dam, W. (2010). "Quantum algorithms for algebraic problems". *Rev. Mod. Phys.*, 82, 1–52.
