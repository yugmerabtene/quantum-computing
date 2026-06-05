# Chapitre 4.1 — Opérateur densité et systèmes composites

## Objectifs

- Comprendre la matrice densité pour les états purs et mélanges
- Calculer la matrice densité réduite
- Maîtriser les mesures POVM
- Distinguer intrication et corrélations classiques

---

## 1. Matrice densité

### 1.1 Motivation

Le formalisme du vecteur d'état $\ket{\psi}$ ne décrit que les **états purs**. Pour les **mélanges statistiques**, on utilise la matrice densité $\rho$.

### 1.2 Définition

Pour un système dans un mélange statistique $\{p_i, \ket{\psi_i}\}$ :

$$
\rho = \sum_i p_i \ket{\psi_i}\bra{\psi_i}
$$

où :
- $\rho$ (rho) = **matrice densité** — représente l'état du système quantique
- $p_i$ = **probabilité classique** du $i$-ème état ($p_i \geq 0$, $\sum_i p_i = 1$)
- $\ket{\psi_i}$ = **ket** — $i$-ème état pur du mélange (vecteur dans l'espace de Hilbert)
- $\bra{\psi_i}$ = **bra** — conjugué hermitien de $\ket{\psi_i}$
- $\ket{\psi_i}\bra{\psi_i}$ = **projecteur** sur l'état $\ket{\psi_i}$

**Propriétés :**
- $\rho^\dagger = \rho$ (hermitienne) — $\dagger$ = conjugaison hermitienne (transposée + conjuguée complexe)
- $\rho \geq 0$ (positive semi-définie) — toutes les valeurs propres sont $\geq 0$
- $\text{Tr}(\rho) = 1$ — $\text{Tr}$ = **trace** (somme des éléments diagonaux)
- $\text{Tr}(\rho^2) \leq 1$ — **pureté** : vaut $1$ pour un état pur, $< 1$ pour un mélange

### 1.3 États purs vs mélanges

| Propriété | État pur | Mélange |
|-----------|----------|---------|
| Représentation | $\rho = \ket{\psi}\bra{\psi}$ | $\rho = \sum_i p_i \ket{\psi_i}\bra{\psi_i}$ |
| $\text{Tr}(\rho^2)$ | $1$ | $< 1$ |
| Exemple | $\ket{0}$ | 50% $\ket{0}$, 50% $\ket{1}$ |

### 1.4 Exemple

État pur : $\ket{+} = \frac{1}{\sqrt{2}}(\ket{0} + \ket{1})$ où $\frac{1}{\sqrt{2}}$ est le facteur de normalisation

$$
\rho_+ = \ket{+}\bra{+} = \frac{1}{2} \begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}
$$

où $\rho_+$ est la matrice densité de l'état pur $\ket{+}$, et $\frac{1}{2}$ est le facteur de normalisation.

Mélange : $\rho_{\text{mix}} = \frac{1}{2}\ket{0}\bra{0} + \frac{1}{2}\ket{1}\bra{1} = \frac{I}{2} = \frac{1}{2} \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}$

où $\rho_{\text{mix}}$ est la matrice densité du mélange 50/50, $I = \begin{pmatrix}1&0\\0&1\end{pmatrix}$ est la matrice identité $2\times2$.

Calcul de pureté :

$$
\text{Tr}(\rho_+^2) = \frac{1}{2} + \frac{1}{2} = 1, \quad
\text{Tr}(\rho_{\text{mix}}^2) = \frac{1}{4} + \frac{1}{4} = \frac{1}{2}
$$

où $\text{Tr}(\rho^2)$ est la **pureté** : elle vaut $1$ pour un état pur ($\rho_+$) et $\frac{1}{2}$ pour un mélange ($\rho_{\text{mix}}$), car $\rho_{\text{mix}}^2 = \frac{1}{4}I$.

```python
import qutip as qt
import numpy as np

# État pur |+⟩
ket_plus = (qt.basis(2,0) + qt.basis(2,1)).unit()
rho_pur = ket_plus * ket_plus.dag()
print("ρ pur =", rho_pur)
print("Tr(ρ²) =", (rho_pur * rho_pur).tr())

# Mélange 50/50
rho_mix = 0.5 * qt.ket2dm(qt.basis(2,0)) + 0.5 * qt.ket2dm(qt.basis(2,1))
print("\nρ mix =", rho_mix)
print("Tr(ρ²) =", (rho_mix * rho_mix).tr())
```

**Sortie :**

```
ρ pur = Quantum object: dims = [[2], [2]]
[[0.5 0.5]
 [0.5 0.5]]
Tr(ρ²) = 1.0

ρ mix = Quantum object: dims = [[2], [2]]
[[0.5 0. ]
 [0.  0.5]]
Tr(ρ²) = 0.5
```

---

## 2. Matrice densité réduite

### 2.1 Trace partielle

Pour un système bipartite $\rho_{AB} \in \mathcal{H}_A \otimes \mathcal{H}_B$, la matrice densité réduite de $A$ est :

$$
\rho_A = \text{Tr}_B(\rho_{AB}) = \sum_i (I_A \otimes \bra{i}_B) \rho_{AB} (I_A \otimes \ket{i}_B)
$$

### 2.2 Exemple : Bell state

Pour $\ket{\Phi^+} = (\ket{00} + \ket{11})/\sqrt{2}$ :

$$
\rho_{\Phi^+} = \frac{1}{2} \begin{pmatrix}
1 & 0 & 0 & 1 \\
0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 \\
1 & 0 & 0 & 1
\end{pmatrix}
$$

$$
\rho_A = \text{Tr}_B(\rho_{\Phi^+}) = \frac{I}{2} = \begin{pmatrix} 1/2 & 0 \\ 0 & 1/2 \end{pmatrix}
$$

L'état réduit est un mélange maximal — l'information est dans les corrélations.

```python
import qutip as qt

# État de Bell
ket00 = qt.tensor(qt.basis(2,0), qt.basis(2,0))
ket11 = qt.tensor(qt.basis(2,1), qt.basis(2,1))
phi_plus = (ket00 + ket11).unit()
rho_AB = phi_plus * phi_plus.dag()

# Trace partielle sur B
rho_A = rho_AB.ptrace(0)
print("ρ_A =", rho_A)
print("S(ρ_A) =", qt.entropy_vn(rho_A))  # = ln 2 pour un état intriqué maximal
```

**Sortie attendue :**

```
ρ_A = Quantum object: dims=[[2], [2]], shape=(2, 2), type='oper', dtype=CSR, isherm=True
Qobj data =
[[0.5 0. ]
 [0.  0.5]]
S(ρ_A) = 0.6931471805599454
```

---

## 3. Entropie d'intrication

### 3.1 Définition

L'entropie de von Neumann mesure le désordre d'un état quantique :

$$
S(\rho) = -\text{Tr}(\rho \log \rho) = -\sum_i \lambda_i \log \lambda_i
$$

où $\lambda_i$ sont les valeurs propres de $\rho$.

### 3.2 Intrication

Pour un état pur bipartite $\ket{\psi}_{AB}$, l'intrication est mesurée par :

$$
E(\ket{\psi}) = S(\rho_A) = S(\rho_B)
$$

- État séparable : $E = 0$
- État maximalement intriqué : $E = \log d$ (où $d = \dim \mathcal{H}_A$)

| État | $\rho_A$ | $S(\rho_A)$ |
|------|----------|-------------|
| $\ket{00}$ | $\ket{0}\bra{0}$ | $0$ |
| $\ket{\Phi^+}$ | $I/2$ | $\ln 2$ |
| $(\sqrt{0.8}\ket{00} + \sqrt{0.2}\ket{11})$ | $\begin{pmatrix}0.8&0\\0&0.2\end{pmatrix}$ | $-(0.8\log0.8 + 0.2\log0.2)$ |

```python
# Intrication en fonction du paramètre
import numpy as np

def entanglement_entropy(theta):
    """Calcule S(ρ_A) pour |ψ⟩ = cos(θ)|00⟩ + sin(θ)|11⟩"""
    c, s = np.cos(theta), np.sin(theta)
    psi = c * ket00 + s * ket11
    rho = psi * psi.dag()
    rho_A = rho.ptrace(0)
    return qt.entropy_vn(rho_A)

thetas = np.linspace(0, np.pi/2, 100)
entropies = [entanglement_entropy(t) for t in thetas]
```

---

## 4. Mesures POVM

### 4.1 Définition

Un **POVM** (Positive Operator-Valued Measure) est un ensemble $\{E_m\}$ tel que :
- $E_m \geq 0$ (positifs)
- $\sum_m E_m = I$

La probabilité d'obtenir $m$ est $p(m) = \text{Tr}(E_m \rho)$.

Contrairement aux mesures projectives, les $E_m$ n'ont pas besoin d'être orthogonaux.

### 4.2 Exemple : discrimination de 3 états

Discriminer $\ket{0}$, $\ket{+}$, $\ket{+i}$ avec une seule mesure :

```python
import qutip as qt
import numpy as np

# États à discriminer
states = [
    qt.basis(2, 0),           # |0⟩
    (qt.basis(2,0) + qt.basis(2,1)).unit(),  # |+⟩
    (qt.basis(2,0) + 1j*qt.basis(2,1)).unit() # |+i⟩
]

# POVM éléments (exemple)
E = []
for i, s in enumerate(states):
    # Projecteur sur l'état
    E.append(s * s.dag())

# Normalisation
E_sum = sum(E)  # devrait être proche de I

# Probabilité de mesurer m=0 pour chaque état
for i, s in enumerate(states):
    prob = (s.dag() * E[0] * s).real
    print(f"États[{i}] → P(0) = {prob:.4f}")
```

**Sortie attendue :**

```
États[0] → P(0) = 1.0000
États[1] → P(0) = 0.5000
États[2] → P(0) = 0.5000
```

---

## 5. Distinguer intrication et corrélations classiques

### 5.1 États séparables vs intriqués

Un état $\rho_{AB}$ est **séparable** s'il peut s'écrire :

$$
\rho_{AB} = \sum_i p_i \; \rho_A^{(i)} \otimes \rho_B^{(i)}
$$

Sinon, il est **intriqué**.

### 5.2 Critère PPT (Peres–Horodecki)

Pour un système $2 \times 2$ ou $2 \times 3$, un état est intriqué ssi sa **transposée partielle** a une valeur propre négative.

```python
# Test PPT pour l'état de Bell
rho_AB = phi_plus * phi_plus.dag()
rho_AB_transposed = rho_AB.ptrace(0)  # non, c'est la transposée partielle

# Transposée partielle
rho_PT = qt.partial_transpose(rho_AB, [0, 1])  # Transposer B
eigvals = rho_PT.eigenenergies()
print(f"Valeurs propres de ρ^{T_B} : {eigvals}")
print("État intriqué ?", any(v < -1e-10 for v in eigvals))
```

**Sortie attendue :**

```
Valeurs propres de ρ^{T_B} : [-0.5  0.5  0.5  0.5]
État intriqué ? True
```

---

## Exercices

1. Calculer $\rho_A$ pour $\ket{\Psi^-} = (\ket{01} - \ket{10})/\sqrt{2}$ et vérifier que $S(\rho_A) = \ln 2$.
2. Montrer que $\rho = \frac{3}{4}\ket{0}\bra{0} + \frac{1}{4}\ket{1}\bra{1}$ a $\text{Tr}(\rho^2) < 1$.
3. Implémenter la discrimination optimale entre $\ket{0}$ et $\ket{+}$ avec un POVM.
4. Vérifier le critère PPT pour l'état $\rho = p\ket{\Phi^+}\bra{\Phi^+} + (1-p)I/4$ en fonction de $p$.
5. Calculer l'intrication de formation pour l'état de Werner à 2 qubits.
