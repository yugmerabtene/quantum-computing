# Chapitre 3.1 — Portes quantiques

## Ce que vous allez apprendre

- Connaître toutes les portes à 1 qubit (Pauli, Hadamard, phase, rotations)
- Maîtriser les portes à 2 qubits (CNOT, CZ, SWAP) et la porte Toffoli
- Comprendre le théorème d'universalité : un petit ensemble de portes suffit pour tout faire
- Implémenter et manipuler les portes en Python (Qiskit, QuTiP)
- Décomposer des opérations complexes en portes élémentaires

---

## Motivation

Dans les chapitres 1 et 2, nous avons appris à décrire des états quantiques et leurs évolutions. Maintenant, passons à la pratique : comment **construire** des circuits quantiques ? La réponse : avec des **portes quantiques**.

Les portes quantiques sont aux circuits quantiques ce que les portes logiques (ET, OU, NON) sont aux circuits électroniques. Mais avec des différences fondamentales : les portes quantiques sont **réversibles**, elles agissent sur des **amplitudes complexes**, et certaines créent de l'**intrication**.

Ce chapitre est votre catalogue de référence. Vous reviendrez le consulter régulièrement — les portes sont les briques de base de tout algorithme quantique.

---

## Idée principale

Imaginez que vous êtes un chef d'orchestre. Chaque instrument (qubit) peut jouer différentes notes. Les portes quantiques sont vos instructions : « violon, joue plus fort » (porte X), « tout le monde, harmonisez » (porte CNOT), « changez de tonalité » (porte de phase).

La bonne nouvelle : il suffit de quelques portes bien choisies pour créer n'importe quelle « mélodie » quantique. C'est le théorème d'universalité — analogue au fait qu'avec ET, OU, NON vous pouvez construire n'importe quelle fonction booléenne.

---

## Contenu du cours

### Section 1 : Portes à un qubit

#### 1.1 Portes de Pauli

> **Intuition :** Les portes de Pauli sont les rotations de 180° autour des axes x, y, z de la sphère de Bloch. Ce sont les opérations les plus simples qu'on puisse faire sur un qubit.

$$X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix},\quad Y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix},\quad Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$$

où $X, Y, Z$ sont les trois matrices de Pauli $2 \times 2$ (avec $i$ l'unité imaginaire)

| Porte | Action | Matrice |
|-------|--------|---------|
| $X$ (NON quantique) | $\ket{0} \leftrightarrow \ket{1}$ | $X$ |
| $Y$ | $\ket{0} \to i\ket{1},\; \ket{1} \to -i\ket{0}$ | $Y$ |
| $Z$ (phase) | $\ket{0} \to \ket{0},\; \ket{1} \to -\ket{1}$ | $Z$ |

> **Exemple numérique avec $X$ :**
> $$X\ket{0} = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}\begin{pmatrix} 1 \\ 0 \end{pmatrix} = \begin{pmatrix} 0 \\ 1 \end{pmatrix} = \ket{1}$$
> C'est exactement un NON logique : $0 \to 1$ et $1 \to 0$.

> **Exemple numérique avec $Z$ :**
> $$Z\ket{+} = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix} \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ 1 \end{pmatrix} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ -1 \end{pmatrix} = \ket{-}$$
> La porte $Z$ ne change rien à $\ket{0}$ mais ajoute un signe moins à $\ket{1}$.

**Avez-vous compris ?**
- Que fait $Z$ à l'état $\ket{1}$ ? (Réponse : $Z\ket{1} = -\ket{1}$)
- Que fait $X$ à l'état $\ket{+}$ ? (Réponse : $X\ket{+} = \ket{+}$ — c'est un état propre !)

#### 1.2 Porte de Hadamard

> **Intuition :** La porte Hadamard est la porte de la superposition. Elle transforme un état de base en superposition uniforme, et vice-versa. C'est la porte qu'on utilise en premier dans presque tous les algorithmes quantiques.

$$H = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$$

**Action :**

$$\begin{aligned} H\ket{0} &= \frac{\ket{0} + \ket{1}}{\sqrt{2}} = \ket{+} \\ H\ket{1} &= \frac{\ket{0} - \ket{1}}{\sqrt{2}} = \ket{-} \end{aligned}$$

> **Exemple numérique :**
> $$H\ket{0} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}\begin{pmatrix} 1 \\ 0 \end{pmatrix} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ 1 \end{pmatrix} = \ket{+}$$

Propriété : $H^2 = I$, $HXH = Z$, $HZH = X$

> **Intuition de $H^2 = I$ :** Appliquer Hadamard deux fois ramène à l'état initial. C'est comme faire un demi-tour puis un autre demi-tour : on revient au point de départ.

#### 1.3 Portes de phase

> **Intuition :** Les portes de phase ne changent pas les probabilités de mesure dans la base Z, mais elles modifient la phase relative — ce qui change le comportement dans d'autres bases.

$$S = \begin{pmatrix} 1 & 0 \\ 0 & i \end{pmatrix}, \quad T = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{pmatrix}$$

$S = T^2$, $T = S^{1/2}$

> **Exemple :** $S\ket{+} = \frac{1}{\sqrt{2}}(\ket{0} + i\ket{1}) = \ket{+i}$
> La porte $S$ ajoute un quart de tour ($\pi/2$) autour de l'axe $z$ sur la sphère de Bloch.

#### 1.4 Rotations générales

> **Intuition :** Les portes de rotation $R_x, R_y, R_z$ permettent de tourner d'un angle quelconque autour des axes de la sphère de Bloch. Les portes de Pauli sont des cas particuliers (rotation de $\pi$).

$$R_x(\theta) = e^{-i\theta X/2} = \cos\frac{\theta}{2}I - i\sin\frac{\theta}{2}X = \begin{pmatrix} \cos(\theta/2) & -i\sin(\theta/2) \\ -i\sin(\theta/2) & \cos(\theta/2) \end{pmatrix}$$

$$R_y(\theta) = e^{-i\theta Y/2} = \begin{pmatrix} \cos(\theta/2) & -\sin(\theta/2) \\ \sin(\theta/2) & \cos(\theta/2) \end{pmatrix}$$

$$R_z(\theta) = e^{-i\theta Z/2} = \begin{pmatrix} e^{-i\theta/2} & 0 \\ 0 & e^{i\theta/2} \end{pmatrix}$$

> **Exemple numérique :** $R_z(\pi/2)$ :
> $$R_z(\pi/2) = \begin{pmatrix} e^{-i\pi/4} & 0 \\ 0 & e^{i\pi/4} \end{pmatrix} = \begin{pmatrix} \frac{1-i}{\sqrt{2}} & 0 \\ 0 & \frac{1+i}{\sqrt{2}} \end{pmatrix}$$

#### 1.5 Décomposition universelle à 1 qubit

Toute porte $U$ à 1 qubit peut s'écrire :

$$U = e^{i\alpha} R_z(\beta) R_y(\gamma) R_z(\delta)$$

> **Intuition :** Comme on peut orienter un objet 3D avec 3 rotations d'Euler, on peut construire n'importe quelle porte à 1 qubit avec 3 rotations et une phase globale.

---

### Section 2 : Portes à deux qubits

#### 2.1 CNOT (CX) — La porte la plus importante

> **Intuition :** Le CNOT est la porte qui crée l'intrication ! Elle agit comme un NON conditionnel : si le contrôle est $\ket{1}$, on applique $X$ à la cible. Sinon, on ne fait rien. C'est la seule porte à 2 qubits dont vous avez absolument besoin.

$$\text{CNOT} = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix}$$

**Action :**
- Si le qubit de contrôle est $\ket{0}$ : rien
- Si le qubit de contrôle est $\ket{1}$ : $X$ sur la cible

$$\text{CNOT} : \ket{c}\ket{t} \to \ket{c}\ket{t \oplus c}$$

> **Exemple numérique :**
> $$\text{CNOT}\ket{10} = \ket{11} \quad \text{(contrôle=1, donc on flippe la cible : 0→1)}$$
> $$\text{CNOT}\ket{00} = \ket{00} \quad \text{(contrôle=0, rien ne se passe)}$$
> $$\text{CNOT}(\ket{+}\otimes\ket{0}) = \frac{1}{\sqrt{2}}(\ket{00} + \ket{11}) = \ket{\Phi^+}$$
> Ce dernier exemple montre comment CNOT crée de l'intrication !

#### 2.2 CZ (Controlled-Z)

$$\text{CZ} = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & -1 \end{pmatrix}$$

> **Intuition :** CZ applique un signe moins uniquement à l'état $\ket{11}$. C'est une porte symétrique : peu importe quel qubit est « contrôle » et quel qubit est « cible ».

Relation : $\text{CNOT} = (I \otimes H) \cdot \text{CZ} \cdot (I \otimes H)$

#### 2.3 SWAP

$$\text{SWAP} = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}$$

Échange deux qubits : $\text{SWAP}\ket{\psi}\ket{\phi} = \ket{\phi}\ket{\psi}$

> **Exemple :** $\text{SWAP}\ket{01} = \ket{10}$

#### 2.4 Toffoli (CCNOT)

Porte à 3 qubits (2 contrôles, 1 cible) :

$$\text{Toffoli} : \ket{a}\ket{b}\ket{c} \to \ket{a}\ket{b}\ket{c \oplus (a \land b)}$$

> **Intuition :** C'est un ET logique réversible. La cible est retournée si et seulement si les deux contrôles sont à 1. Universelle pour le calcul classique (réversible).

---

## Symboles des portes quantiques

```
    ──────────              : Fil quantique (wire)

    ──[ H ]──               : Porte d'Hadamard (superposition)

    ──[ X ]──               : Porte Pauli-X (bit-flip)

    ──[ Y ]──               : Porte Pauli-Y

    ──[ Z ]──               : Porte Pauli-Z (phase-flip)

    ──[ S ]──               : Porte de phase S (π/2)

    ──[ T ]──               : Porte T (π/8 = π/4)

    ──[ Rx ]──              : Rotation autour de l'axe x
         θ

    ──•──                    : Contrôle (qubit de contrôle)
       │
       │
    ──⊕──                    : Cible CNOT (X conditionnel)

    ──•──                    : Contrôle CZ (Z conditionnel)
       │
       │
    ──●──
```

## Vue d'ensemble de la sphère de Bloch avec les portes

```
                           |0⟩
                             ●
                           ╱ │ ╲
                          ╱  │  ╲      Y
                         ╱   │   ╲   ↗
                        ╱    │    ╲↗
                       ╱     │     ●  |+i⟩
        |+⟩  ●──────────────┼──────────────●  |−⟩
                       ╲     │     ╱
                        ╲    │    ╱
                         ╲   │   ╱
                          ╲  │  ╱
                           ╲ │ ╱       X
                             ●
                           |1⟩

         H : |0⟩ → |+⟩  (rotation +90° autour de y)
         X : |+⟩ ↔ |−⟩  (rotation 180° autour de x)
         Z : |+⟩ ↔ |−⟩  (rotation 180° autour de z)
         S : rotation +90° autour de z
         T : rotation +45° autour de z
```

---

### Section 3 : Universalité

#### 3.1 Génération de l'intrication

Le circuit Bell : $H$ + CNOT

```python
from qiskit import QuantumCircuit

# --- Circuit de création d'un état de Bell ---
qc = QuantumCircuit(2)
qc.h(0)    # Hadamard sur le qubit 0 : |0⟩ → |+⟩
qc.cx(0, 1) # CNOT avec contrôle=0, cible=1 : crée l'intrication
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

#### 3.2 Théorème de Solovay–Kitaev

> Toute porte à 1 qubit peut être approximée avec une précision $\varepsilon$ en utilisant $O(\log^c(1/\varepsilon))$ portes d'un ensemble discret universel.

**Ensemble universel standard :** $\{H, T, \text{CNOT}\}$

> **Intuition :** C'est comme dire qu'avec seulement 3 types de portes, on peut approximer n'importe quelle opération quantique. C'est fondamental pour l'implémentation pratique, car on ne peut pas réaliser des rotations continues avec une précision infinie.

#### 3.3 Décomposition de portes

```python
import numpy as np
from qiskit import QuantumCircuit

# --- Décomposition d'une porte arbitraire en H, T, CNOT ---
qc = QuantumCircuit(1)
qc.h(0)      # Hadamard : crée une superposition
qc.t(0)      # Porte T : rotation de π/4 autour de z
qc.s(0)      # Porte S = T² : rotation de π/2 autour de z
qc.h(0)      # Hadamard : retour à la base d'origine
# Résultat : rotation combinée
```

---

## Exemple guidé

**Problème :** Montrer que $HXH = Z$.

**Étape 1 — Écrivons les matrices :**

$$H = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}, \quad X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$$

**Étape 2 — Calculons $XH$ d'abord :**

$$XH = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & -1 \\ 1 & 1 \end{pmatrix}$$

**Étape 3 — Calculons $H(XH)$ :**

$$HXH = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix} \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & -1 \\ 1 & 1 \end{pmatrix} = \frac{1}{2}\begin{pmatrix} 2 & 0 \\ 0 & -2 \end{pmatrix} = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix} = Z \quad \checkmark$$

> **Interprétation :** Hadamard échange les rôles de $X$ et $Z$. C'est logique : $H$ échange les bases $X$ et $Z$ ($H\ket{0} = \ket{+}$, $H\ket{+} = \ket{0}$).

---

## Implémentation Python

### Portes avec QuTiP

```python
import qutip as qt
import numpy as np

# ============================================================
# PORTE H (Hadamard) construite manuellement
# ============================================================
# H = |0⟩⟨0| + |0⟩⟨1| + |1⟩⟨0| - |1⟩⟨1| (puis normalisation)
H = (qt.basis(2,0) * qt.basis(2,0).dag() +    # |0⟩⟨0|
     qt.basis(2,0) * qt.basis(2,1).dag() +     # |0⟩⟨1|
     qt.basis(2,1) * qt.basis(2,0).dag() -     # |1⟩⟨0|
     qt.basis(2,1) * qt.basis(2,1).dag()).unit() # -|1⟩⟨1|

# --- Vérification : H|0⟩ = |+⟩ ---
ket0 = qt.basis(2, 0)
ket_plus = H * ket0
print("H|0⟩ =", ket_plus)

# ============================================================
# PORTE CNOT (4×4) construite manuellement
# ============================================================
CNOT = qt.Qobj(
    np.array([
        [1,0,0,0],  # |00⟩ → |00⟩
        [0,1,0,0],  # |01⟩ → |01⟩
        [0,0,0,1],  # |10⟩ → |11⟩
        [0,0,1,0]   # |11⟩ → |10⟩
    ]),
    dims=[[2,2],[2,2]]  # 2 qubits en entrée, 2 qubits en sortie
)

# ============================================================
# CRÉATION D'UN ÉTAT DE BELL
# ============================================================
# État initial |00⟩
ket00 = qt.tensor(qt.basis(2,0), qt.basis(2,0))

# H ⊗ I : Hadamard sur le premier qubit, identité sur le second
H_I = qt.tensor(H, qt.qeye(2))

# Application : CNOT · (H ⊗ I) · |00⟩
bell = CNOT * H_I * ket00
print("|Φ⁺⟩ =", bell)
```

**Sortie attendue :**

```
H|0⟩ = Quantum object: dims=[[2], [1]], shape=(2, 1), type='ket', dtype=Dense
Qobj data =
[[0.35355339]
 [0.35355339]]
|Φ⁺⟩ = Quantum object: dims=[[2, 2], [1]], shape=(4, 1), type='ket', dtype=Dense
Qobj data =
[[0.35355339]
 [0.        ]
 [0.        ]
 [0.35355339]]
```

### Qiskit — Catalogue de portes

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
import numpy as np

# --- Circuit à 3 qubits avec toutes les portes ---
qc = QuantumCircuit(3)

# Portes à 1 qubit
qc.x(0)      # Pauli X : bit-flip (|0⟩ ↔ |1⟩)
qc.y(0)      # Pauli Y : bit-flip + phase-flip
qc.z(0)      # Pauli Z : phase-flip (|1⟩ → -|1⟩)
qc.h(1)      # Hadamard : crée une superposition
qc.s(1)      # Phase S : rotation π/2 autour de z
qc.t(2)      # Porte T : rotation π/4 autour de z
qc.sdg(2)    # S† : rotation -π/2 autour de z
qc.tdg(2)    # T† : rotation -π/4 autour de z
qc.p(np.pi/3, 0)  # Phase arbitraire : rotation π/3 autour de z

# Portes à 2 qubits
qc.cx(0, 1)  # CNOT : contrôle=0, cible=1
qc.cz(0, 2)  # CZ : Z conditionnel
qc.swap(1, 2) # SWAP : échange les qubits 1 et 2

# Portes à 3 qubits
qc.ccx(0, 1, 2)  # Toffoli : double contrôle, cible=2

# Rotations paramétrées
qc.rx(np.pi/2, 0)   # Rotation π/2 autour de x
qc.ry(np.pi/4, 1)   # Rotation π/4 autour de y
qc.rz(np.pi/8, 2)   # Rotation π/8 autour de z

print(qc.draw())
```

**Sortie attendue :**

```
     ┌───┐ ┌───┐  ┌───┐ ┌────────┐                ┌─────────┐
q_0: ┤ X ├─┤ Y ├──┤ Z ├─┤ P(π/3) ├──■───■──────■──┤ Rx(π/2) ├
     ├───┤ ├───┤  └───┘ └────────┘┌─┴─┐ │      │  ├─────────┤
q_1: ┤ H ├─┤ S ├──────────────────┤ X ├─┼──X───■──┤ Ry(π/4) ├
     ├───┤┌┴───┴┐┌─────┐          └───┘ │  │ ┌─┴─┐├─────────┤
q_2: ┤ T ├┤ Sdg ├┤ Tdg ├────────────────■──X─┤ X ├┤ Rz(π/8) ├
     └───┘└─────┘└─────┘                     └───┘└─────────┘
```

---

## Tableau récapitulatif

| Porte | Symbole | Matrice | Action |
|-------|---------|---------|--------|
| $X$ | $\oplus$ | $\begin{pmatrix}0&1\\1&0\end{pmatrix}$ | $\ket{0}\leftrightarrow\ket{1}$ |
| $Z$ | | $\begin{pmatrix}1&0\\0&-1\end{pmatrix}$ | Phase $\pi$ sur $\ket{1}$ |
| $H$ | | $\frac{1}{\sqrt{2}}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$ | Base $Z \leftrightarrow$ base $X$ |
| $S$ | | $\begin{pmatrix}1&0\\0&i\end{pmatrix}$ | Phase $\pi/2$ |
| $T$ | | $\begin{pmatrix}1&0\\0&e^{i\pi/4}\end{pmatrix}$ | Phase $\pi/4$ |
| CNOT | $\bullet$—$\oplus$ | $\begin{pmatrix}1&0&0&0\\0&1&0&0\\0&0&0&1\\0&0&1&0\end{pmatrix}$ | $\ket{c}\ket{t}\to\ket{c}\ket{t\oplus c}$ |

---

## À retenir

1. **Portes de Pauli** ($X, Y, Z$) : rotations de 180° autour des axes x, y, z. $X$ est le NON quantique.
2. **Hadamard** ($H$) : crée la superposition. $H\ket{0} = \ket{+}$, $H^2 = I$.
3. **Portes de phase** ($S, T$) : modifient la phase relative sans changer les probabilités dans la base Z.
4. **CNOT** : la porte à 2 qubits essentielle. Crée de l'intrication à partir d'une superposition.
5. **Universalité** : $\{H, T, \text{CNOT}\}$ suffit pour approximer toute opération quantique.
6. **Toffoli** : porte à 3 qubits, universelle pour le calcul classique réversible.
7. **Toute porte à 1 qubit** se décompose en $R_z R_y R_z$ (3 rotations).

---

## Pièges à éviter

1. **Confondre CNOT et copie** — CNOT ne copie pas l'état du contrôle. Si le contrôle est en superposition $\alpha\ket{0} + \beta\ket{1}$, le résultat est un état intriqué, PAS deux copies.

2. **Penser que $X$ et $Z$ commutent** — $XZ \neq ZX$. En fait, $XZ = -ZX$. L'ordre des portes compte !

3. **Oublier que $H$ est sa propre inverse** — $H^2 = I$, donc $H^{-1} = H$. Appliquer Hadamard deux fois annule son effet.

4. **Confondre la matrice CNOT 4×4 avec un produit tensoriel** — CNOT ne peut PAS s'écrire $A \otimes B$. C'est une porte genuinely à 2 qubits.

5. **Penser qu'il faut une infinité de portes** — Le théorème de Solovay-Kitaev dit qu'un ensemble fini $\{H, T, \text{CNOT}\}$ suffit pour tout approximer.

---

## Exercices

### Niveau 1 — Application directe

1. Montrer que $HXH = Z$ et $HZH = X$.
   *(Suivez l'exemple guidé ci-dessus !)*

2. Calculer l'action de la porte $T$ sur l'état $\ket{+}$. Quel état obtient-on ?
   *(Indice : $T\ket{+} = \frac{1}{\sqrt{2}}(\ket{0} + e^{i\pi/4}\ket{1})$)*

3. Construire une porte $R_x(\theta) R_z(\phi)$ avec Qiskit et vérifier la matrice avec `Operator`.

### Niveau 2 — Compréhension

4. Démontrer que CNOT ne peut pas être factorisé en produit de portes à 1 qubit.
   *(Indice : si CNOT = $A \otimes B$, alors CNOT ne créerait pas d'intrication...)*

5. Décomposer la porte SWAP en 3 CNOT. (Cherchez « SWAP decomposition » — c'est un résultat classique.)

6. Montrer que Toffoli est équivalent à un CNOT avec des portes $T$ supplémentaires (décomposition de circuit).

### Niveau 3 — Défi

7. Implémenter le circuit de téléportation quantique en utilisant uniquement $H$, CNOT, et des mesures. (Voir chapitre 3.2 pour le détail du protocole.)

8. Construire un circuit qui prépare l'état GHZ à 3 qubits : $\ket{GHZ} = \frac{1}{\sqrt{2}}(\ket{000} + \ket{111})$. Combien de portes faut-il ?

---

## Pour aller plus loin

- Nielsen & Chuang, Ch. 4 — Décomposition universelle et synthèse de circuits
- Vidéo : [Quantum Gates Explained](https://www.youtube.com/watch?v=quMUwrI10ks) — Visualisation sur la sphère de Bloch
- Qiskit Textbook, Ch. 1.4 — Interactive quantum gates avec simulateur en ligne
