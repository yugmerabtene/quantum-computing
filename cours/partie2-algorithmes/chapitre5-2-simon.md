# Chapitre 5.2 — Algorithme de Simon

## Ce que vous allez apprendre

- Comprendre le problème de la **période cachée** et pourquoi il est difficile classiquement
- Maîtriser le circuit de l'algorithme de Simon et le rôle de la transformée de Hadamard
- Savoir **reconstruire la période** $s$ à partir des mesures par résolution d'un système linéaire
- Établir le lien avec la **Quantum Fourier Transform** (QFT) et le **problème du sous-groupe caché**
- Implémenter l'algorithme en **Qiskit** et vérifier les résultats

---

## Motivation

Imaginez que vous avez une fonction $f$ qui associe à chaque nombre de $n$ bits un autre nombre de $n$ bits. On vous promet qu'il existe un nombre secret $s$ tel que $f(x) = f(y)$ si et seulement si $y = x \oplus s$ (où $\oplus$ est le XOR bit à bit). Autrement dit, $f$ regroupe les entrées par paires qui donnent la même sortie, et $s$ est « l'écart » entre les deux éléments de chaque paire.

Combien de temps vous faut-il pour trouver $s$ ? Classiquement, c'est comme chercher une aiguille dans une botte de foin : il faut en moyenne $O(2^{n/2})$ évaluations (c'est le paradoxe des anniversaires). Pour $n = 50$, cela fait environ un million d'évaluations.

L'algorithme de Simon résout ce problème en $O(n)$ évaluations quantiques — c'est le **premier avantage exponentiel prouvé** dans le modèle des boîtes noires. Plus important encore, c'est le **précurseur direct de l'algorithme de Shor** : la structure mathématique est la même, et comprendre Simon est la clé pour comprendre Shor.

---

## Idée principale

Pensez à un motif sur un papier peint. Si le motif se répète avec une période $s$, vous pouvez le découvrir en regardant comment les motifs s'alignent. L'algorithme de Simon fait la même chose, mais en version quantique.

On prépare toutes les entrées en superposition, on évalue $f$ partout, puis on applique une transformée de Hadamard. Résultat : les mesures ne donnent que des vecteurs $y$ qui sont **perpendiculaires** à $s$ (au sens du produit scalaire binaire : $s \cdot y = 0 \pmod 2$). Chaque mesure nous donne une « équation » sur $s$. Avec $n-1$ équations indépendantes, on peut résoudre le système et trouver $s$.

C'est exactement comme faire de la triangulation : chaque mesure élimine la moitié des possibilités pour $s$.

---

## Contenu du cours

### Section 1 : Le problème de Simon

**Problème** : Soit $f : \{0,1\}^n \to \{0,1\}^n$ avec la **promesse** qu'il existe $s \in \{0,1\}^n \setminus \{0^n\}$ tel que :

$$f(x) = f(y) \iff y = x \oplus s \quad \forall x,y \in \{0,1\}^n$$

**Intuition** : $f$ est une fonction « 2-vers-1 » : chaque sortie a exactement deux antécédents, séparés par $s$.

**Variables** : $x, y, s \in \{0,1\}^n$, $\oplus$ = XOR bit à bit.

**Exemple** : $n = 3$, $s = 110$. Alors $f(000) = f(110)$, $f(001) = f(111)$, $f(010) = f(100)$, $f(011) = f(101)$.

**Complexité classique** : $O(2^{n/2})$ appels (paradoxe des anniversaires). **Quantique** : $O(n)$ appels.

### Section 2 : Le circuit de Simon

```
|0⟩^{\otimes n} — H^{\otimes n} — U_f — H^{\otimes n} — M
                                 |
|0⟩^{\otimes n} — — — — — — — — — — — — M
```

**Étape 1** — État initial :
$$|\psi_0\rangle = |0\rangle^{\otimes n}|0\rangle^{\otimes n}$$

**Étape 2** — Hadamard sur le premier registre :
$$|\psi_1\rangle = \frac{1}{\sqrt{2^n}} \sum_{x=0}^{2^n-1} |x\rangle |0\rangle^{\otimes n}$$

**Intuition** : le premier registre est en superposition uniforme de toutes les entrées possibles.

**Étape 3** — Oracle $U_f : |x\rangle|y\rangle \mapsto |x\rangle|y \oplus f(x)\rangle$ :
$$|\psi_2\rangle = \frac{1}{\sqrt{2^n}} \sum_{x=0}^{2^n-1} |x\rangle |f(x)\rangle$$

**Intuition** : le second registre contient maintenant $f(x)$ pour chaque $x$ en superposition. Les paires $(x, x \oplus s)$ partagent la même valeur $f(x) = f(x \oplus s)$.

**Étape 4** — Hadamard sur le premier registre :
$$|\psi_3\rangle = \frac{1}{2^n} \sum_{x=0}^{2^n-1} \sum_{y=0}^{2^n-1} (-1)^{x\cdot y} |y\rangle |f(x)\rangle$$

### Section 3 : Analyse de la mesure

On mesure le premier registre et on obtient un vecteur $y$. Quelle est la distribution ?

Pour chaque paire $(x, x \oplus s)$, les termes associés à $|y\rangle|f(x)\rangle$ s'additionnent :

$$(-1)^{x\cdot y} + (-1)^{(x\oplus s)\cdot y} = (-1)^{x\cdot y}\left[1 + (-1)^{s\cdot y}\right]$$

**Intuition** : si $s \cdot y = 1 \pmod 2$, les deux termes s'annulent (interférence destructive). Si $s \cdot y = 0 \pmod 2$, ils s'additionnent (interférence constructive).

**Conclusion** :
- Si $s \cdot y = 0 \pmod 2$ → $P(y) > 0$ (on peut mesurer $y$)
- Si $s \cdot y = 1 \pmod 2$ → $P(y) = 0$ (on ne mesure **jamais** $y$)

**Exemple numérique** : $n = 3$, $s = 110$. Les $y$ mesurés satisfont $110 \cdot y = 0 \pmod 2$, c'est-à-dire $y_1 \oplus y_2 = 0$. Donc $y \in \{000, 001, 011, 100, 101, 110\}$.

### Section 4 : Reconstruction de $s$

Après $O(n)$ itérations, on obtient $n-1$ vecteurs $y_1, \ldots, y_{n-1}$ linéairement indépendants. On résout :

$$\begin{pmatrix} y_1^{(1)} & \cdots & y_1^{(n)} \\ \vdots & \ddots & \vdots \\ y_{n-1}^{(1)} & \cdots & y_{n-1}^{(n)} \end{pmatrix} \begin{pmatrix} s_1 \\ \vdots \\ s_n \end{pmatrix} = \mathbf{0} \pmod 2$$

**Intuition** : chaque $y_i$ donne une équation linéaire $y_i \cdot s = 0 \pmod 2$. Avec $n-1$ équations indépendantes sur $n$ inconnues, l'espace des solutions est de dimension 1, ce qui détermine $s$ de manière unique (à part $s = 0^n$, exclu par la promesse).

**Exemple** : $n = 3$, on mesure $y_1 = 011, y_2 = 101$. Le système :
$$\begin{pmatrix} 0 & 1 & 1 \\ 1 & 0 & 1 \end{pmatrix} \begin{pmatrix} s_1 \\ s_2 \\ s_3 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix} \pmod 2$$

Solution : $s_2 = s_3$ et $s_1 = s_3$, donc $s = (1, 1, 1)$ ou $s = (0, 0, 0)$. Par la promesse, $s \neq 000$, donc $s = 111$.

---

## Exemple guidé

Prenons $n = 2$, $s = 11$. Donc $f(00) = f(11)$ et $f(01) = f(10)$.

Disons $f(00) = f(11) = 00$ et $f(01) = f(10) = 01$.

**État après oracle** :
$$|\psi_2\rangle = \frac{1}{2}(|00\rangle|00\rangle + |01\rangle|01\rangle + |10\rangle|01\rangle + |11\rangle|00\rangle)$$

**Regroupons par valeur de $f$** :
$$|\psi_2\rangle = \frac{1}{2}(|00\rangle + |11\rangle)|00\rangle + \frac{1}{2}(|01\rangle + |10\rangle)|01\rangle$$

**Après Hadamard sur le premier registre** (rappel : $H^{\otimes 2}|x\rangle = \frac{1}{2}\sum_y (-1)^{x\cdot y}|y\rangle$) :

Pour le terme $|00\rangle + |11\rangle$ :
- $H^{\otimes 2}|00\rangle = \frac{1}{2}(|00\rangle + |01\rangle + |10\rangle + |11\rangle)$
- $H^{\otimes 2}|11\rangle = \frac{1}{2}(|00\rangle - |01\rangle - |10\rangle + |11\rangle)$
- Somme : $|00\rangle + |11\rangle$

Donc le premier registre donne $|00\rangle$ ou $|11\rangle$.

Vérifions : $s \cdot y = 11 \cdot y = y_1 \oplus y_2 = 0$ → $y \in \{00, 11\}$. ✓

Si on mesure $y = 11$ : l'équation $11 \cdot s = 0 \pmod 2$ donne $s_1 \oplus s_2 = 0$, donc $s_1 = s_2$. Avec une autre itération donnant $y = 00$ (trivial), on conclut $s = 11$.

---

## Implémentation Python

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit.providers.aer import QasmSimulator

import random
from collections import Counter

# --- Oracle de Simon ---
def oracle_simon(qc, n, s):
    """
    Oracle pour Simon : f(x) = f(x⊕s).
    Implémente une fonction 2-vers-1 avec période s.
    Stratégie : copier x dans le registre de sortie,
    puis si s ≠ 0, modifier la copie pour que f(x) = f(x⊕s).
    """
    # Copier les qubits d'entrée vers la sortie : |x⟩|0⟩ → |x⟩|x⟩
    for i in range(n):
        qc.cx(i, n + i)

    # Si s ≠ 0, on applique un XOR avec s pour créer la collision
    if any(s):
        for i in range(n):
            if s[i] == '1':
                for j in range(n):
                    qc.cx(i, n + j)

# --- Circuit de Simon ---
def simon_circuit(n, s):
    """
    Construit le circuit complet de Simon.
    n : nombre de qubits
    s : string binaire représentant la période cachée
    """
    qc = QuantumCircuit(2 * n, n)

    # Hadamard sur les n premiers qubits → superposition uniforme
    qc.h(range(n))

    # Oracle de Simon
    oracle_simon(qc, n, s)

    # Hadamard sur les n premiers qubits → interférences
    qc.h(range(n))

    # Mesure des n premiers qubits
    qc.measure(range(n), range(n))

    return qc

# --- Algorithme complet de Simon ---
def simon_algorithm(n, s_bits, shots=10):
    """
    Exécute l'algorithme de Simon et détermine s.
    s_bits : string binaire, ex. '110'
    """
    qc = simon_circuit(n, s_bits)
    backend = QasmSimulator()

    results = []
    while len(results) < n - 1:
        result = backend.run(qc, shots=1).result()
        counts = result.get_counts()
        y = list(counts.keys())[0]
        # Ignorer y = 0...0 (trivial) et les doublons
        if y != '0' * n and y not in results:
            results.append(y)
        if len(results) >= n - 1:
            break

    print(f"Période cachée s = {s_bits}")
    print(f"Équations linéaires collectées : {results}")

    # Résolution du système linéaire modulo 2
    if len(results) >= n - 1:
        mat = np.array([[int(b) for b in y] for y in results[:n-1]])
        # SVD pour trouver l'espace nul
        _, _, vh = np.linalg.svd(mat, full_matrices=True)
        s_found = vh[-1, :]
        s_found_bits = ''.join(str(round(abs(x))) for x in s_found)
        print(f"s reconstruit (SVD) : {s_found_bits}")
        return s_found_bits
    return None

# --- Test ---
print("=== Algorithme de Simon ===")
n = 3
s_test = '110'
simon_algorithm(n, s_test, shots=20)
```

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# --- Circuit complet avec affichage détaillé ---
def circuit_complet_simon(n=3, s='101'):
    """
    Circuit de Simon avec affichage de la distribution.
    Vérifie que seuls les y tels que s·y = 0 apparaissent.
    """
    qc = QuantumCircuit(2 * n, n)

    # Hadamard sur les n premiers qubits
    qc.h(range(n))

    # Oracle : f(x) = f(x ⊕ s)
    for i in range(n):
        if s[i] == '1':
            for j in range(n):
                qc.cx(i, n + j)

    # Hadamard sur les n premiers qubits
    qc.h(range(n))

    # Mesure
    qc.measure(range(n), range(n))

    print(f"Circuit Simon (s={s}) :")
    print(qc.draw())

    backend = AerSimulator()
    result = backend.run(qc, shots=2048).result()
    counts = result.get_counts()

    # Vérification : seuls les y tq s·y=0 apparaissent
    print("\nDistribution des mesures :")
    for y, count in sorted(counts.items(), key=lambda x: -x[1])[:8]:
        dot = sum(int(y[i]) * int(s[i]) for i in range(n)) % 2
        mark = "✓" if dot == 0 else "✗ (devrait être nul)"
        print(f"  y={y} : {count:4d}  s·y={dot} {mark}")

    return qc, counts

qc_s, counts_s = circuit_complet_simon(3, '101')
```

---

## Complexité et avantage quantique

| Approche | Requêtes à $f$ | Complexité classique post-traitement |
|----------|----------------|--------------------------------------|
| Classique | $O(2^{n/2})$ | — |
| **Simon** | $O(n)$ | $O(n^3)$ (système linéaire) |
| **Avantage** | **Exponentiel** | — |

**Pourquoi l'algorithme est-il plus rapide ?** Chaque mesure quantique donne une équation $y \cdot s = 0 \pmod 2$ qui élimine la moitié des candidats pour $s$. Il suffit donc de $n-1$ équations indépendantes pour déterminer $s$ parmi les $2^n - 1$ possibilités. Classiquement, il faut explorer $O(2^{n/2})$ valeurs pour trouver une collision.

**Intuition de la preuve** : l'interférence destructive annule tous les $y$ tels que $s \cdot y = 1$. C'est la transformée de Hadamard qui crée cette interférence, en « projetant » l'état sur la base des fréquences.

---

## À retenir

1. Le problème de Simon cherche une **période cachée** $s$ dans une fonction 2-vers-1
2. L'algorithme utilise **Hadamard → Oracle → Hadamard** (même structure que Deutsch-Jozsa)
3. Les mesures donnent des $y$ tels que $s \cdot y = 0 \pmod 2$
4. Avec $n-1$ mesures indépendantes, on résout un **système linéaire mod 2** pour trouver $s$
5. C'est le **premier avantage exponentiel prouvé** dans le modèle des boîtes noires
6. Simon est un cas particulier du **Hidden Subgroup Problem** sur $(\mathbb{Z}/2\mathbb{Z})^n$
7. La structure est identique à celle de Shor : Simon utilise la QFT sur $\mathbb{Z}_2^n$, Shor sur $\mathbb{Z}_N$

---

## Pièges à éviter

1. **Confondre $s = 0^n$ et $s \neq 0^n$** : la promesse exclut $s = 0^n$ (sinon $f$ serait 1-vers-1)
2. **Oublier que le système est mod 2** : les calculs sont en arithmétique binaire, pas réelle
3. **Penser qu'une seule exécution suffit** : il faut $O(n)$ exécutions pour collecter $n-1$ équations indépendantes
4. **Négliger le post-traitement classique** : la résolution du système linéaire est en $O(n^3)$, ce qui reste polynomial
5. **Confondre avec Deutsch-Jozsa** : ici l'oracle n'est pas un simple phase kickback, il écrit $f(x)$ dans un registre

---

## Exercices

### Niveau 1 — Application directe

**Exercice 1** : Écrivez un simulateur classique de l'algorithme de Simon pour $n=4$ et vérifiez que $P(y) > 0$ ssi $s \cdot y = 0$.

**Exercice 2** : Montrez que $P(y=0) = 2^{-n}$. Combien d'itérations sont nécessaires en moyenne pour obtenir $n-1$ vecteurs indépendants ?

### Niveau 2 — Compréhension

**Exercice 3** : Implémentez l'algorithme en utilisant uniquement des matrices NumPy pour $n=3$ (sans Qiskit).

```python
import numpy as np

def hadamard_n(n):
    """Matrice de Hadamard sur n qubits (produit tensoriel H⊗ⁿ)"""
    H1 = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    Hn = H1
    for _ in range(n - 1):
        Hn = np.kron(Hn, H1)
    return Hn

def oracle_simon_mat(n, s):
    """Matrice de l'oracle pour Simon (simplifiée)"""
    N = 2**n
    U = np.zeros((N, N))
    for x in range(N):
        x_xor_s = x ^ s
        U[x, x] = 1
        U[x, x_xor_s] = 1
    return U / np.sqrt(2)

# Complétez l'implémentation...
```

**Exercice 4** : Implémentez la recherche classique de collision pour $n$ bits. Comparez le nombre de requêtes pour $n=8,10,12$.

### Niveau 3 — Défi

**Exercice 5** : Montrez que Simon est un cas particulier de l'algorithme HSP sur $(\mathbb{Z}/2\mathbb{Z})^n$ avec $H=\{0,s\}$. Généralisez à $(\mathbb{Z}/d\mathbb{Z})^n$.

**Exercice 6** : Générez une fonction $f$ 2-vers-1 aléatoire et implémentez l'oracle. Vérifiez que l'algorithme retrouve $s$.

---

## Pour aller plus loin

- Le problème de Simon est un cas particulier du **Hidden Subgroup Problem** (HSP) : $G = (\mathbb{Z}/2\mathbb{Z})^n$, $H = \{0, s\}$
- L'algorithme de **Shor** (chapitre 7.1) généralise cette idée à $G = \mathbb{Z}/N\mathbb{Z}$ avec la QFT
- La transformée de Hadamard généralisée est la **QFT sur $(\mathbb{Z}/2\mathbb{Z})^n$** : $H^{\otimes n}|x\rangle = \frac{1}{\sqrt{2^n}} \sum_{y} (-1)^{x\cdot y} |y\rangle$

---

## Références

- Simon, D. R. (1997). "On the Power of Quantum Computation". *SIAM J. Comput.*, 26(5), 1474–1483.
- Nielsen, M. A. & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*.
- Childs, A. M. & van Dam, W. (2010). "Quantum algorithms for algebraic problems". *Rev. Mod. Phys.*, 82, 1–52.
