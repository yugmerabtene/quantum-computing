# Chapitre 1.2 — Algèbre linéaire complexe pour le calcul quantique

## Ce que vous allez apprendre

- Maîtriser la notation de Dirac (bras, kets) — le langage universel du quantique
- Comprendre les espaces de Hilbert et pourquoi ils sont le « terrain de jeu » des qubits
- Manipuler les opérateurs linéaires : unitaires (portes), hermitiens (observables)
- Calculer avec le produit tensoriel pour combiner plusieurs qubits
- Trouser valeurs propres et vecteurs propres — essentiels pour la mesure

---

## Motivation

Dans le chapitre précédent, nous avons vu qu'un qubit est décrit par un état $\alpha\ket{0} + \beta\ket{1}$. Mais qu'est-ce que $\ket{0}$ exactement ? Comment manipule-t-on ces objets mathématiquement ? Comment combine-t-on deux qubits ?

La réponse tient en un mot : **algèbre linéaire**. Tout le formalisme du calcul quantique repose sur des vecteurs (les états), des matrices (les portes), et des produits scalaires (les probabilités de mesure). Si vous avez fait de l'algèbre linéaire en licence, vous êtes déjà armés — il suffit d'apprendre la notation et les conventions spécifiques au quantique.

Ce chapitre est votre boîte à outils mathématique. Chaque concept sera illustré par des exemples numériques simples et du code Python. Ne sautez aucune section : tout le reste du cours s'appuie dessus.

---

## Idée principale

Imaginez une flèche dans l'espace 3D. Vous pouvez la décrire par ses coordonnées $(x, y, z)$, la tourner, l'additionner avec une autre flèche, mesurer l'angle entre deux flèches. Un état quantique, c'est exactement la même chose — sauf que :

1. La flèche vit dans un espace **complexe** (les coordonnées sont des nombres complexes)
2. La longueur de la flèche vaut toujours **1** (c'est une contrainte de probabilité)
3. Au lieu de $(x, y, z)$, on écrit $\alpha\ket{0} + \beta\ket{1}$ avec $\alpha, \beta \in \mathbb{C}$

La notation $\ket{\cdot}$ (ket) de Dirac, c'est juste une façon élégante d'écrire des vecteurs. Et le bra $\bra{\cdot}$, c'est le vecteur transposé conjugué. Ensemble, $\braket{\phi}{\psi}$ donne le produit scalaire — comme mesurer l'angle entre deux flèches.

---

## Contenu du cours

### Section 1 : Espaces de Hilbert et notation de Dirac

#### 1.1 Qu'est-ce qu'un espace de Hilbert ?

Un **espace de Hilbert** $\mathcal{H}$ est un espace vectoriel complexe muni d'un **produit scalaire** et **complet** pour la norme induite.

> **Intuition :** C'est simplement un espace où vivent nos vecteurs d'état. Pour le calcul quantique, nous travaillons dans des espaces de dimension finie $\mathcal{H} \cong \mathbb{C}^n$. Pour un qubit, $n = 2$ ; pour 2 qubits, $n = 4$ ; pour $n$ qubits, $n = 2^n$.

#### 1.2 La notation de Dirac (bra-ket)

C'est la notation standard en mécanique quantique. Apprenons-la pas à pas.

**Ket** $\ket{\psi} \in \mathcal{H}$ : c'est un vecteur colonne.

$$\ket{\psi} = \begin{pmatrix} \alpha_1 \\ \alpha_2 \\ \vdots \\ \alpha_n \end{pmatrix}, \quad \alpha_i \in \mathbb{C}$$

où $\ket{\psi}$ = ket (vecteur colonne), $\alpha_i$ = $i$-ème coordonnée complexe du vecteur, $n$ = dimension de $\mathcal{H}$

> **Exemple numérique :** L'état $\ket{0}$ d'un qubit s'écrit :
> $$\ket{0} = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$$
> Et l'état $\ket{1}$ :
> $$\ket{1} = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$$

**Bra** $\bra{\psi} \in \mathcal{H}^*$ : c'est le vecteur ligne, conjugué hermitien du ket.

$$\bra{\psi} = \ket{\psi}^\dagger = \begin{pmatrix} \alpha_1^* & \alpha_2^* & \cdots & \alpha_n^* \end{pmatrix}$$

où $\bra{\psi}$ = bra (vecteur ligne adjoint), $\alpha_i^*$ = conjugué complexe de $\alpha_i$, $\dagger$ = conjugué hermitien (transposée + conjugaison complexe)

> **Exemple :** Si $\ket{\psi} = \begin{pmatrix} 1+i \\ 2 \end{pmatrix}$, alors $\bra{\psi} = \begin{pmatrix} 1-i & 2 \end{pmatrix}$

**Produit scalaire :**

$$\braket{\phi}{\psi} = \sum_i \phi_i^* \psi_i \in \mathbb{C}$$

où $\braket{\phi}{\psi}$ = produit scalaire (bra-ket), $\phi_i^*$ = $i$-ème coordonnée complexe conjuguée de $\bra{\phi}$, $\psi_i$ = $i$-ème coordonnée de $\ket{\psi}$

> **Exemple numérique :**
> $$\braket{0}{1} = \begin{pmatrix} 1 & 0 \end{pmatrix} \begin{pmatrix} 0 \\ 1 \end{pmatrix} = 0$$
> $$\braket{0}{0} = \begin{pmatrix} 1 & 0 \end{pmatrix} \begin{pmatrix} 1 \\ 0 \end{pmatrix} = 1$$
> Les états $\ket{0}$ et $\ket{1}$ sont **orthonormaux**.

**Produit externe :**

$$\ket{\phi}\bra{\psi} = \text{matrice } n \times n$$

où $\ket{\phi}\bra{\psi}$ = produit externe, matrice $n \times n$ d'éléments $\phi_i \psi_j^*$

> **Exemple :**
> $$\ket{0}\bra{0} = \begin{pmatrix} 1 \\ 0 \end{pmatrix} \begin{pmatrix} 1 & 0 \end{pmatrix} = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$$

**Avez-vous compris ?**
- Que vaut $\braket{+}{-}$ où $\ket{+} = \frac{1}{\sqrt{2}}\begin{pmatrix}1\\1\end{pmatrix}$ et $\ket{-} = \frac{1}{\sqrt{2}}\begin{pmatrix}1\\-1\end{pmatrix}$ ?
- Réponse : $\frac{1}{2}(1 \times 1 + 1 \times (-1)) = 0$. Ils sont orthogonaux !

#### 1.3 Base canonique

En dimension 2 (un qubit) :

$$\ket{0} = \begin{pmatrix} 1 \\ 0 \end{pmatrix}, \quad \ket{1} = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$$

où $\ket{0}$ et $\ket{1}$ forment la base canonique (ou base $Z$) de $\mathbb{C}^2$, états propres de $\sigma_z$

Tout état pur à un qubit s'écrit :

$$\ket{\psi} = \alpha \ket{0} + \beta \ket{1}, \quad |\alpha|^2 + |\beta|^2 = 1$$

où $\alpha, \beta \in \mathbb{C}$ = amplitudes de probabilité, $|\alpha|^2$ = probabilité de mesurer $\ket{0}$, $|\beta|^2$ = probabilité de mesurer $\ket{1}$

> **Exemple :** L'état $\ket{+} = \frac{1}{\sqrt{2}}(\ket{0} + \ket{1})$ a $\alpha = \beta = \frac{1}{\sqrt{2}}$.
> Probabilité de mesurer $\ket{0}$ : $|\alpha|^2 = \frac{1}{2} = 50\%$.
> Probabilité de mesurer $\ket{1}$ : $|\beta|^2 = \frac{1}{2} = 50\%$.

---

### Section 2 : Opérateurs linéaires

#### 2.1 Définitions fondamentales

Un **opérateur linéaire** $A : \mathcal{H} \to \mathcal{H}$ est une application linéaire. En dimension finie, c'est une matrice.

> **Intuition :** Un opérateur est une « action » qu'on applique à un état. Les portes quantiques sont des opérateurs !

**Adjoint** $A^\dagger$ : $(A^\dagger)_{ij} = A_{ji}^*$ (transposée + conjuguée complexe)

**Opérateur unitaire** : $U^\dagger U = U U^\dagger = I$

> **Pourquoi c'est important :** Les portes quantiques sont unitaires ! Cela garantit que la norme de l'état est préservée (les probabilités somment toujours à 1).

**Opérateur hermitien** : $H^\dagger = H$

> **Pourquoi c'est important :** Les observables (ce qu'on mesure) sont hermitiens. Leurs valeurs propres sont réelles — ce qui correspond au fait qu'on mesure des nombres réels.

#### 2.2 Les matrices de Pauli

Les matrices de Pauli sont des opérateurs hermitiens **et** unitaires fondamentaux :

$$\sigma_x = X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad \sigma_y = Y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \quad \sigma_z = Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$$

où $\sigma_x, \sigma_y, \sigma_z$ = matrices de Pauli (hermitiennes et unitaires) ; $X$ = porte NON quantique (bit-flip), $Z$ = porte de phase (phase-flip)

**Propriétés :**
- $X\ket{0} = \ket{1},\; X\ket{1} = \ket{0}$
- $Z\ket{0} = \ket{0},\; Z\ket{1} = -\ket{1}$
- $X^2 = Y^2 = Z^2 = I$
- $[X,Y] = 2iZ$ (commutateur)

> **Exemple numérique avec $X$ :**
> $$X\ket{0} = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} \begin{pmatrix} 1 \\ 0 \end{pmatrix} = \begin{pmatrix} 0 \\ 1 \end{pmatrix} = \ket{1}$$
> C'est bien un NON logique !

#### 2.3 Représentation matricielle d'un état

Un état $\ket{\psi} = \alpha\ket{0} + \beta\ket{1}$ se représente :

$$\ket{\psi} = \begin{pmatrix} \alpha \\ \beta \end{pmatrix}$$

Application d'une porte $X$ :

$$X\ket{\psi} = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} \begin{pmatrix} \alpha \\ \beta \end{pmatrix} = \begin{pmatrix} \beta \\ \alpha \end{pmatrix}$$

où $X$ = matrice de Pauli $X$, $\alpha,\beta$ = amplitudes de l'état $\ket{\psi}$ ; la porte $X$ échange les amplitudes

> **Exemple :** Si $\ket{\psi} = \frac{1}{\sqrt{3}}\ket{0} + \sqrt{\frac{2}{3}}\ket{1} = \begin{pmatrix} 1/\sqrt{3} \\ \sqrt{2/3} \end{pmatrix}$, alors :
> $$X\ket{\psi} = \begin{pmatrix} \sqrt{2/3} \\ 1/\sqrt{3} \end{pmatrix} = \sqrt{\frac{2}{3}}\ket{0} + \frac{1}{\sqrt{3}}\ket{1}$$

---

### Section 3 : Produit tensoriel

#### 3.1 Pourquoi le produit tensoriel ?

Le produit tensoriel $\otimes$ permet de construire l'espace d'état d'un système composite. Si vous avez 2 qubits, chacun dans $\mathbb{C}^2$, l'espace total est $\mathbb{C}^2 \otimes \mathbb{C}^2 = \mathbb{C}^4$.

> **Intuition :** C'est comme combiner deux dés. Un dé a 6 faces, deux dés ont $6 \times 6 = 36$ combinaisons. De même, 1 qubit a 2 états de base, 2 qubits en ont $2 \times 2 = 4$.

Pour $\ket{\psi} \in \mathcal{H}_A$ et $\ket{\phi} \in \mathcal{H}_B$ :

$$\ket{\psi} \otimes \ket{\phi} \in \mathcal{H}_A \otimes \mathcal{H}_B$$

En coordonnées :

$$\ket{\psi} = \begin{pmatrix} a \\ b \end{pmatrix},\; \ket{\phi} = \begin{pmatrix} c \\ d \end{pmatrix} \;\Rightarrow\; \ket{\psi} \otimes \ket{\phi} = \begin{pmatrix} a\begin{pmatrix}c\\d\end{pmatrix} \\ b\begin{pmatrix}c\\d\end{pmatrix} \end{pmatrix} = \begin{pmatrix} ac \\ ad \\ bc \\ bd \end{pmatrix}$$

> **Exemple numérique :**
> $$\ket{0} \otimes \ket{1} = \begin{pmatrix} 1 \\ 0 \end{pmatrix} \otimes \begin{pmatrix} 0 \\ 1 \end{pmatrix} = \begin{pmatrix} 1 \times \begin{pmatrix}0\\1\end{pmatrix} \\ 0 \times \begin{pmatrix}0\\1\end{pmatrix} \end{pmatrix} = \begin{pmatrix} 0 \\ 1 \\ 0 \\ 0 \end{pmatrix} = \ket{01}$$

#### 3.2 Notation abrégée

$$\ket{0} \otimes \ket{0} = \ket{00}, \quad \ket{0} \otimes \ket{1} = \ket{01}, \quad \ket{\psi} \otimes \ket{\phi} = \ket{\psi\phi}$$

#### 3.3 Opérateurs sur systèmes composites

$$(A \otimes B)(\ket{\psi} \otimes \ket{\phi}) = (A\ket{\psi}) \otimes (B\ket{\phi})$$

Pour un système à $n$ qubits, la dimension est $2^n$.

> **Exemple :** Appliquer $X$ au premier qubit et $Z$ au second :
> $$(X \otimes Z)(\ket{0} \otimes \ket{0}) = (X\ket{0}) \otimes (Z\ket{0}) = \ket{1} \otimes \ket{0} = \ket{10}$$

**Avez-vous compris ?**
- Quelle est la dimension de l'espace d'état pour 3 qubits ? (Réponse : $2^3 = 8$)
- Que vaut $\ket{1} \otimes \ket{0}$ en vecteur colonne ? (Réponse : $(0, 0, 1, 0)^T$)

---

### Section 4 : Valeurs et vecteurs propres

#### 4.1 L'équation aux valeurs propres

$$A \ket{v} = \lambda \ket{v}$$

- $\lambda$ : valeur propre (réelle si $A$ est hermitien)
- $\ket{v}$ : vecteur propre

> **Intuition :** Un vecteur propre est un état qui ne change pas de « direction » quand on lui applique l'opérateur $A$. Il est juste multiplié par un facteur $\lambda$. En mécanique quantique, les résultats de mesure sont les valeurs propres !

#### 4.2 Décomposition spectrale

Pour $A$ hermitien :

$$A = \sum_i \lambda_i \ket{v_i}\bra{v_i}$$

> **Exemple avec $Z$ :**
> $$Z = (+1)\ket{0}\bra{0} + (-1)\ket{1}\bra{1} = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} + \begin{pmatrix} 0 & 0 \\ 0 & -1 \end{pmatrix} = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$$

#### 4.3 Applications en quantique

- Les **observables** sont des opérateurs hermitiens → valeurs propres réelles = résultats de mesure
- Les **portes** sont des opérateurs unitaires → préservent la norme
- La **mesure** projette sur les sous-espaces propres

---

## Exemple guidé

**Problème :** Calculer l'action de la porte $Z$ sur l'état $\ket{+} = \frac{1}{\sqrt{2}}(\ket{0} + \ket{1})$, puis vérifier que $\ket{+}$ est un vecteur propre de $X$.

**Étape 1 — Action de $Z$ sur $\ket{+}$ :**

$$Z\ket{+} = Z \cdot \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ 1 \end{pmatrix} = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix} \begin{pmatrix} 1 \\ 1 \end{pmatrix} = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ -1 \end{pmatrix} = \ket{-}$$

**Étape 2 — Vérifier que $\ket{+}$ est vecteur propre de $X$ :**

$$X\ket{+} = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ 1 \end{pmatrix} = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ 1 \end{pmatrix} = (+1) \cdot \ket{+}$$

Donc $\ket{+}$ est vecteur propre de $X$ avec valeur propre $\lambda = +1$.

**Étape 3 — Vérifions aussi pour $\ket{-}$ :**

$$X\ket{-} = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ -1 \end{pmatrix} = \frac{1}{\sqrt{2}} \begin{pmatrix} -1 \\ 1 \end{pmatrix} = -\ket{-}$$

Donc $\ket{-}$ est vecteur propre de $X$ avec valeur propre $\lambda = -1$.

---

## Implémentation Python

### Premiers pas avec QuTiP

```python
import numpy as np
import qutip as qt

# --- États de base ---
# qt.basis(2, 0) crée le vecteur |0⟩ = (1, 0)^T dans C^2
# qt.basis(2, 1) crée le vecteur |1⟩ = (0, 1)^T dans C^2
ket0 = qt.basis(2, 0)  # |0⟩
ket1 = qt.basis(2, 1)  # |1⟩

# --- Superposition ---
# On additionne |0⟩ + |1⟩ puis on normalise (divise par la norme)
# .unit() divise par la norme : (|0⟩ + |1⟩) / √2
psi = (ket0 + ket1).unit()  # (|0⟩ + |1⟩) / √2
print("État |ψ⟩ :", psi)

# --- Matrices de Pauli ---
# qt.sigmax(), qt.sigmay(), qt.sigmaz() renvoient les matrices X, Y, Z
sx, sy, sz = qt.sigmax(), qt.sigmay(), qt.sigmaz()

# Application de X à |0⟩ : devrait donner |1⟩
print("X|0⟩ =", sx * ket0)

# Application de Z à |1⟩ : devrait donner -|1⟩
print("Z|1⟩ =", sz * ket1)

# --- Produit tensoriel ---
# qt.tensor() calcule le produit tensoriel ⊗
ket00 = qt.tensor(ket0, ket0)  # |00⟩ = |0⟩ ⊗ |0⟩
ket01 = qt.tensor(ket0, ket1)  # |01⟩ = |0⟩ ⊗ |1⟩
print("|00⟩ :", ket00)
print("|01⟩ :", ket01)

# --- Vérification de la normalisation ---
# psi.dag() calcule le bra ⟨ψ|, et le produit ⟨ψ|ψ⟩ doit valoir 1
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

### Opérations avec Qiskit

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# Création d'un circuit à 1 qubit
qc = QuantumCircuit(1)

# Porte de Hadamard : crée la superposition (|0⟩ + |1⟩)/√2
qc.h(0)

# Affichage du circuit
print(qc.draw())

# Extraction du statevector (état quantique complet)
state = Statevector.from_instruction(qc)

# Affichage de l'état et des amplitudes complexes
print("État :", state)
print("Amplitudes :", state.data)
```

**Sortie attendue :**

```
   ┌───┐
q: ┤ H ├
   └───┘
État : Statevector([0.70710678+0.j, 0.70710678+0.j],
            dims=(2,))
Amplitudes : [0.70710678+0.j  0.70710678+0.j]
```

---

## À retenir

1. Un **ket** $\ket{\psi}$ est un vecteur complexe ; un **bra** $\bra{\psi}$ est son adjoint (transposé conjugué)
2. Le **produit scalaire** $\braket{\phi}{\psi}$ donne l'amplitude de probabilité de transition entre deux états
3. Les **opérateurs unitaires** ($U^\dagger U = I$) préservent la norme — ce sont les portes quantiques
4. Les **opérateurs hermitiens** ($H^\dagger = H$) sont les observables — leurs valeurs propres sont les résultats de mesure
5. Le **produit tensoriel** $\otimes$ compose les systèmes : la dimension croît exponentiellement ($2^n$ pour $n$ qubits)
6. Les **matrices de Pauli** $X, Y, Z$ sont à la fois hermitiennes et unitaires — elles servent de portes et d'observables
7. Tout état d'un qubit s'écrit $\alpha\ket{0} + \beta\ket{1}$ avec $|\alpha|^2 + |\beta|^2 = 1$

---

## Pièges à éviter

1. **Oublier que les amplitudes sont complexes** — $\alpha$ et $\beta$ ne sont pas des probabilités, ce sont des amplitudes complexes. Les probabilités sont $|\alpha|^2$ et $|\beta|^2$.

2. **Confondre $\braket{\phi}{\psi}$ et $\ket{\phi}\bra{\psi}$** — Le premier est un nombre (produit scalaire), le second est une matrice (produit externe / projecteur).

3. **Penser que $\ket{01}$ signifie « 0 + 1 »** — Non ! C'est le produit tensoriel $\ket{0} \otimes \ket{1}$, un vecteur de dimension 4 : $(0, 1, 0, 0)^T$.

4. **Oublier la normalisation** — Tout état quantique doit avoir une norme égale à 1. Si vous calculez $\ket{0} + \ket{1}$, il faut diviser par $\sqrt{2}$.

5. **Confondre $X^2 = I$ et $X = I$** — Appliquer $X$ deux fois revient à l'identité, mais $X$ n'est PAS l'identité !

---

## Exercices

### Niveau 1 — Application directe

1. Calculer $X\ket{+}$ où $\ket{+} = (\ket{0} + \ket{1})/\sqrt{2}$. Quel état obtient-on ?
   *(Indice : appliquez la matrice X au vecteur colonne)*

2. Écrire l'état $\ket{\psi} = \frac{1}{2}\ket{0} + \frac{i\sqrt{3}}{2}\ket{1}$ sous forme de vecteur colonne. Vérifier que $\|\ket{\psi}\| = 1$.

3. Calculer le produit scalaire $\braket{0}{+}$. Quelle est la probabilité de mesurer $\ket{0}$ si le système est dans l'état $\ket{+}$ ?

### Niveau 2 — Compréhension

4. Montrer que les matrices de Pauli sont à la fois hermitiennes et unitaires.
   *(Indice : calculez $X^\dagger$, puis $X^\dagger X$, et vérifiez les deux propriétés)*

5. Soit $\ket{\psi} = \frac{1}{\sqrt{2}}(\ket{00} + \ket{11})$. Écrire ce vecteur dans la base $\{\ket{00}, \ket{01}, \ket{10}, \ket{11}\}$. Calculer $\rho = \ket{\psi}\bra{\psi}$.

6. Calculer les valeurs propres et vecteurs propres de la matrice $Y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}$.

### Niveau 3 — Défi

7. Vérifier que $(A \otimes B)(\ket{\psi} \otimes \ket{\phi}) = (A\ket{\psi}) \otimes (B\ket{\phi})$ pour $A = X$, $B = Z$, $\ket{\psi} = \ket{+}$, $\ket{\phi} = \ket{0}$.

8. Implémenter la superposition $\frac{\ket{0} + e^{i\theta}\ket{1}}{\sqrt{2}}$ avec QuTiP pour $\theta = \pi/4$. Calculer la probabilité de mesurer $\ket{0}$ et $\ket{1}$.

---

## Pour aller plus loin

- Nielsen & Chuang, *Quantum Computation and Quantum Information*, Appendix 2 — Revue complète d'algèbre linéaire pour le quantique
- 3Blue1Brown, *Essence of Linear Algebra* (vidéos YouTube) — Excellente intuition visuelle
- [Aperçu QuTiP](https://qutip.org/docs/latest/) — Documentation officielle pour aller plus loin avec le code
