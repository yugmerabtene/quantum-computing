# Séance 3.1 — Portes quantiques

## Objectifs

- Connaître les portes à 1 et 2 qubits
- Comprendre l'universalité et la décomposition de circuits
- Manipuler les portes en Python (Qiskit, QuTiP)

---

## 1. Portes à un qubit

### 1.1 Portes de Pauli

$$
X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix},\quad
Y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix},\quad
Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}
$$

| Porte | Action | Matrice |
|-------|--------|---------|
| $X$ (NON quantique) | $\ket{0} \leftrightarrow \ket{1}$ | $X$ |
| $Y$ | $\ket{0} \to i\ket{1},\; \ket{1} \to -i\ket{0}$ | $Y$ |
| $Z$ (phase) | $\ket{0} \to \ket{0},\; \ket{1} \to -\ket{1}$ | $Z$ |

### 1.2 Porte de Hadamard

$$
H = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}
$$

**Action :**

$$
\begin{aligned}
H\ket{0} &= \frac{\ket{0} + \ket{1}}{\sqrt{2}} = \ket{+} \\
H\ket{1} &= \frac{\ket{0} - \ket{1}}{\sqrt{2}} = \ket{-}
\end{aligned}
$$

Propriété : $H^2 = I$, $HXH = Z$, $HZH = X$

### 1.3 Portes de phase

$$
S = \begin{pmatrix} 1 & 0 \\ 0 & i \end{pmatrix}, \quad
T = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{pmatrix}
$$

$S = T^2$, $T = S^{1/2}$

### 1.4 Rotations générales

$$
R_x(\theta) = e^{-i\theta X/2} = \cos\frac{\theta}{2}I - i\sin\frac{\theta}{2}X
= \begin{pmatrix} \cos(\theta/2) & -i\sin(\theta/2) \\ -i\sin(\theta/2) & \cos(\theta/2) \end{pmatrix}
$$

$$
R_y(\theta) = e^{-i\theta Y/2} = \begin{pmatrix} \cos(\theta/2) & -\sin(\theta/2) \\ \sin(\theta/2) & \cos(\theta/2) \end{pmatrix}
$$

$$
R_z(\theta) = e^{-i\theta Z/2} = \begin{pmatrix} e^{-i\theta/2} & 0 \\ 0 & e^{i\theta/2} \end{pmatrix}
$$

### 1.5 Décomposition universelle à 1 qubit

Toute porte $U$ à 1 qubit peut s'écrire :

$$
U = e^{i\alpha} R_z(\beta) R_y(\gamma) R_z(\delta)
$$

---

## 2. Portes à deux qubits

### 2.1 CNOT (CX)

La porte CNOT (Controlled-NOT) est la porte à 2 qubits fondamentale :

$$
\text{CNOT} = \begin{pmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1 \\
0 & 0 & 1 & 0
\end{pmatrix}
$$

**Action :**
- Si le qubit de contrôle est $\ket{0}$ : rien
- Si le qubit de contrôle est $\ket{1}$ : $X$ sur la cible

$$
\text{CNOT} : \ket{c}\ket{t} \to \ket{c}\ket{t \oplus c}
$$

### 2.2 CZ (Controlled-Z)

$$
\text{CZ} = \begin{pmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & -1
\end{pmatrix}
$$

Relation : $\text{CNOT} = (I \otimes H) \cdot \text{CZ} \cdot (I \otimes H)$

### 2.3 SWAP

$$
\text{SWAP} = \begin{pmatrix}
1 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1
\end{pmatrix}
$$

Échange deux qubits : $\text{SWAP}\ket{\psi}\ket{\phi} = \ket{\phi}\ket{\psi}$

### 2.4 Toffoli (CCNOT)

Porte à 3 qubits (2 contrôles, 1 cible) :

$$
\text{Toffoli} : \ket{a}\ket{b}\ket{c} \to \ket{a}\ket{b}\ket{c \oplus (a \land b)}
$$

Universelle pour le calcul classique (réversible).

---

## 3. Universalité

### 3.1 Génération de l'intrication

Le circuit Bell : $H$ + CNOT

```python
from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
print(qc.draw())
```

```
     ┌───┐     
q_0: ┤ H ├──■──
     └───┘┌─┴─┐
q_1: ─────┤ X ├
          └───┘
```

Produit $\ket{\Phi^+} = (\ket{00} + \ket{11})/\sqrt{2}$.

### 3.2 Théorème de Solovay–Kitaev

> Toute porte à 1 qubit peut être approximée avec une précision $\varepsilon$ en utilisant $O(\log^c(1/\varepsilon))$ portes d'un ensemble discret universel.

**Ensemble universel standard :** $\{H, T, \text{CNOT}\}$

### 3.3 Décomposition de portes

```python
import numpy as np
from qiskit import QuantumCircuit

# Décomposition d'une porte arbitraire en H, T, CNOT
qc = QuantumCircuit(1)
qc.h(0)      # Hadamard
qc.t(0)      # T gate
qc.s(0)      # Phase gate = T^2
qc.h(0)
# Résultat : rotation combinée
```

---

## 4. Implémentation QuTiP

```python
import qutip as qt
import numpy as np

# Portes à 1 qubit
H = (qt.basis(2,0) * qt.basis(2,0).dag() +
     qt.basis(2,0) * qt.basis(2,1).dag() +
     qt.basis(2,1) * qt.basis(2,0).dag() -
     qt.basis(2,1) * qt.basis(2,1).dag()).unit()

# Vérification
ket0 = qt.basis(2, 0)
ket_plus = H * ket0
print("H|0⟩ =", ket_plus)

# Porte CNOT (4x4)
CNOT = qt.Qobj(
    np.array([
        [1,0,0,0],
        [0,1,0,0],
        [0,0,0,1],
        [0,0,1,0]
    ]),
    dims=[[2,2],[2,2]]
)

# Bell state
ket00 = qt.tensor(qt.basis(2,0), qt.basis(2,0))
H_I = qt.tensor(H, qt.qeye(2))
bell = CNOT * H_I * ket00
print("|Φ⁺⟩ =", bell)
```

---

## 5. Qiskit — Catalogue de portes

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
import numpy as np

qc = QuantumCircuit(3)

# Portes à 1 qubit
qc.x(0)      # Pauli X
qc.y(0)      # Pauli Y
qc.z(0)      # Pauli Z
qc.h(1)      # Hadamard
qc.s(1)      # Phase
qc.t(2)      # T gate
qc.sdg(2)    # S†
qc.tdg(2)    # T†
qc.p(np.pi/3, 0)  # Phase arbitraire

# Portes à 2 qubits
qc.cx(0, 1)  # CNOT (control=0, target=1)
qc.cz(0, 2)  # CZ
qc.swap(1, 2) # SWAP

# Portes à 3 qubits
qc.ccx(0, 1, 2)  # Toffoli

# Rotations
qc.rx(np.pi/2, 0)
qc.ry(np.pi/4, 1)
qc.rz(np.pi/8, 2)

print(qc.draw())
```

---

## 6. Tableau récapitulatif

| Porte | Symbole | Matrice | Action |
|-------|---------|---------|--------|
| $X$ | $\oplus$ | $\begin{pmatrix}0&1\\1&0\end{pmatrix}$ | $\ket{0}\leftrightarrow\ket{1}$ |
| $Z$ | | $\begin{pmatrix}1&0\\0&-1\end{pmatrix}$ | Phase $\pi$ sur $\ket{1}$ |
| $H$ | | $\frac{1}{\sqrt{2}}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$ | Base $Z \leftrightarrow$ base $X$ |
| $S$ | | $\begin{pmatrix}1&0\\0&i\end{pmatrix}$ | Phase $\pi/2$ |
| $T$ | | $\begin{pmatrix}1&0\\0&e^{i\pi/4}\end{pmatrix}$ | Phase $\pi/4$ |
| CNOT | $\bullet$—$\oplus$ | $\begin{pmatrix}1&0&0&0\\0&1&0&0\\0&0&0&1\\0&0&1&0\end{pmatrix}$ | $\ket{c}\ket{t}\to\ket{c}\ket{t\oplus c}$ |

---

## Exercices

1. Montrer que $HXH = Z$ et $HZH = X$.
2. Démontrer que CNOT ne peut pas être factorisé en produit de portes à 1 qubit.
3. Construire une porte $R_x(\theta) R_z(\phi)$ avec Qiskit et vérifier la matrice.
4. Implémenter le circuit de téléportation quantique en utilisant uniquement $H$, CNOT, et des mesures.
5. Vérifier que Toffoli est équivalent à un CNOT avec une porte $T$ supplémentaire (décomposition de circuit).
