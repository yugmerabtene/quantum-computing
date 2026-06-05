# Séance 1.2 — Algèbre linéaire complexe pour le calcul quantique

## Objectifs

- Maîtriser la notation de Dirac (bras, kets)
- Comprendre les espaces de Hilbert et les opérateurs linéaires
- Manipuler le produit tensoriel
- Se familiariser avec les représentations matricielles

---

## 1. Espaces de Hilbert

### 1.1 Définition

Un **espace de Hilbert** $\mathcal{H}$ est un espace vectoriel complexe muni d'un **produit scalaire** et **complet** pour la norme induite.

Pour le calcul quantique, nous travaillons dans des espaces de dimension finie $\mathcal{H} \cong \mathbb{C}^n$.

### 1.2 Notation de Dirac (bra-ket)

**Ket** $\ket{\psi} \in \mathcal{H}$ : vecteur colonne

$$
\ket{\psi} = \begin{pmatrix} \alpha_1 \\ \alpha_2 \\ \vdots \\ \alpha_n \end{pmatrix}, \quad \alpha_i \in \mathbb{C}
$$

**Bra** $\bra{\psi} \in \mathcal{H}^*$ : vecteur ligne, conjugué hermitien du ket

$$
\bra{\psi} = \ket{\psi}^\dagger = \begin{pmatrix} \alpha_1^* & \alpha_2^* & \cdots & \alpha_n^* \end{pmatrix}
$$

**Produit scalaire :**

$$
\braket{\phi}{\psi} = \sum_i \phi_i^* \psi_i \in \mathbb{C}
$$

**Produit externe :**

$$
\ket{\phi}\bra{\psi} = \text{matrice } n \times n
$$

### 1.3 Base canonique

En dimension 2 (un qubit) :

$$
\ket{0} = \begin{pmatrix} 1 \\ 0 \end{pmatrix}, \quad
\ket{1} = \begin{pmatrix} 0 \\ 1 \end{pmatrix}
$$

Tout état pur à un qubit s'écrit :

$$
\ket{\psi} = \alpha \ket{0} + \beta \ket{1}, \quad |\alpha|^2 + |\beta|^2 = 1
$$

---

## 2. Opérateurs linéaires

### 2.1 Définition

Un **opérateur linéaire** $A : \mathcal{H} \to \mathcal{H}$ est une application linéaire.
En dimension finie, c'est une matrice.

**Adjoint** $A^\dagger$ : $(A^\dagger)_{ij} = A_{ji}^*$

**Opérateur unitaire** : $U^\dagger U = U U^\dagger = I$

**Opérateur hermitien** : $H^\dagger = H$ (observables)

### 2.2 Matrices de Pauli

Les matrices de Pauli sont des opérateurs hermitiens et unitaires fondamentaux :

$$
\sigma_x = X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad
\sigma_y = Y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \quad
\sigma_z = Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}
$$

**Propriétés :**
- $X\ket{0} = \ket{1},\; X\ket{1} = \ket{0}$
- $Z\ket{0} = \ket{0},\; Z\ket{1} = -\ket{1}$
- $X^2 = Y^2 = Z^2 = I$
- $[X,Y] = 2iZ$ (commutateur)

### 2.3 Représentation matricielle d'un état

Un état $\ket{\psi} = \alpha\ket{0} + \beta\ket{1}$ se représente :

$$
\ket{\psi} = \begin{pmatrix} \alpha \\ \beta \end{pmatrix}
$$

Application d'une porte $X$ :

$$
X\ket{\psi} = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} \begin{pmatrix} \alpha \\ \beta \end{pmatrix} = \begin{pmatrix} \beta \\ \alpha \end{pmatrix}
$$

---

## 3. Produit tensoriel

### 3.1 Définition

Le produit tensoriel $\otimes$ permet de construire l'espace d'état d'un système composite.

Pour $\ket{\psi} \in \mathcal{H}_A$ et $\ket{\phi} \in \mathcal{H}_B$ :

$$
\ket{\psi} \otimes \ket{\phi} \in \mathcal{H}_A \otimes \mathcal{H}_B
$$

En coordonnées :

$$
\ket{\psi} = \begin{pmatrix} a \\ b \end{pmatrix},\;
\ket{\phi} = \begin{pmatrix} c \\ d \end{pmatrix}
\;\Rightarrow\;
\ket{\psi} \otimes \ket{\phi} = \begin{pmatrix} a\begin{pmatrix}c\\d\end{pmatrix} \\ b\begin{pmatrix}c\\d\end{pmatrix} \end{pmatrix} = \begin{pmatrix} ac \\ ad \\ bc \\ bd \end{pmatrix}
$$

### 3.2 Notation abrégée

$$
\ket{0} \otimes \ket{0} = \ket{00}, \quad
\ket{0} \otimes \ket{1} = \ket{01}, \quad
\ket{\psi} \otimes \ket{\phi} = \ket{\psi\phi}
$$

### 3.3 Opérateurs sur systèmes composites

$$
(A \otimes B)(\ket{\psi} \otimes \ket{\phi}) = (A\ket{\psi}) \otimes (B\ket{\phi})
$$

Pour un système à $n$ qubits, la dimension est $2^n$.

---

## 4. Valeurs et vecteurs propres

### 4.1 Équation aux valeurs propres

$$
A \ket{v} = \lambda \ket{v}
$$

- $\lambda$ : valeur propre (réelle si $A$ est hermitien)
- $\ket{v}$ : vecteur propre

### 4.2 Décomposition spectrale

Pour $A$ hermitien :

$$
A = \sum_i \lambda_i \ket{v_i}\bra{v_i}
$$

### 4.3 Applications en quantique

- Les **observables** sont des opérateurs hermitiens
- Les **portes** sont des opérateurs unitaires
- La **mesure** projette sur les sous-espaces propres

---

## 5. Code Python — Premiers pas avec QuTiP

```python
import numpy as np
import qutip as qt

# États de base
ket0 = qt.basis(2, 0)  # |0⟩
ket1 = qt.basis(2, 1)  # |1⟩

# Superposition
psi = (ket0 + ket1).unit()  # (|0⟩ + |1⟩) / √2
print("État :", psi)

# Matrices de Pauli
sx, sy, sz = qt.sigmax(), qt.sigmay(), qt.sigmaz()
print("X|0⟩ =", sx * ket0)
print("Z|1⟩ =", sz * ket1)

# Produit tensoriel
ket00 = qt.tensor(ket0, ket0)
ket01 = qt.tensor(ket0, ket1)
print("|00⟩ :", ket00)
print("|01⟩ :", ket01)

# Vérification de la normalisation
print("⟨ψ|ψ⟩ =", psi.dag() * psi)
```

**Sortie attendue :**

```
État : Quantum object: dims = [[2]], shape = (2, 2)
[[0.707]
 [0.707]]
X|0⟩ = Quantum object: dims = [[2]], shape = (2, 1)
[[0.]
 [1.]]
⟨ψ|ψ⟩ = 1.0
```

---

## 6. Code Python — Opérations avec Qiskit

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# Création d'un circuit à 1 qubit
qc = QuantumCircuit(1)
qc.h(0)  # Porte de Hadamard : crée la superposition

# Affichage du circuit
print(qc.draw())

# État final
state = Statevector.from_instruction(qc)
print("État :", state)
print("Amplitudes :", state.data)
```

---

## 7. Points clés à retenir

- Un **ket** $\ket{\psi}$ est un vecteur complexe ; un **bra** $\bra{\psi}$ est son adjoint
- Le **produit scalaire** $\braket{\phi}{\psi}$ donne l'amplitude de probabilité
- Les **opérateurs unitaires** ($U^\dagger U = I$) préservent la norme — ce sont les portes
- Les **opérateurs hermitiens** ($H^\dagger = H$) sont les observables
- Le **produit tensoriel** $\otimes$ compose les systèmes : la dimension croît exponentiellement

---

## Exercices

1. Calculer $X\ket{+}$ où $\ket{+} = (\ket{0} + \ket{1})/\sqrt{2}$. Quel état obtient-on ?
2. Montrer que les matrices de Pauli sont à la fois hermitiennes et unitaires.
3. Soit $\ket{\psi} = \frac{1}{\sqrt{2}}(\ket{00} + \ket{11})$. Écrire ce vecteur dans la base $\{\ket{00}, \ket{01}, \ket{10}, \ket{11}\}$.
4. Vérifier que $(A \otimes B)(\ket{\psi} \otimes \ket{\phi}) = (A\ket{\psi}) \otimes (B\ket{\phi})$.
5. Implémenter la superposition $\frac{\ket{0} + e^{i\theta}\ket{1}}{\sqrt{2}}$ avec QuTiP pour $\theta = \pi/4$.
