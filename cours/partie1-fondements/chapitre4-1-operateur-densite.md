# Chapitre 4.1 — Opérateur densité et systèmes composites

## Ce que vous allez apprendre

- Comprendre la matrice densité pour décrire états purs ET mélanges statistiques
- Calculer la matrice densité réduite (trace partielle) pour les sous-systèmes
- Maîtriser les mesures POVM (généralisation des mesures projectives)
- Distinguer intrication quantique et simples corrélations classiques
- Quantifier l'intrication avec l'entropie de von Neumann

---

## Motivation

Jusqu'ici, nous avons décrit les états quantiques par des vecteurs $\ket{\psi}$. C'est le formalisme des **états purs**. Mais dans la vraie vie, les systèmes quantiques ne sont jamais parfaitement isolés : ils interagissent avec leur environnement, on ne connaît pas exactement leur état, ou on ne voit qu'une partie d'un système plus grand.

Comment décrire un qubit dont on sait qu'il est dans l'état $\ket{0}$ avec probabilité 50% et $\ket{1}$ avec probabilité 50% ? Ce n'est PAS la superposition $\ket{+}$ ! C'est un **mélange statistique**, et le formalisme du vecteur d'état ne peut pas le décrire.

La réponse : la **matrice densité** (ou opérateur densité). Ce formalisme plus général unifie états purs, mélanges, sous-systèmes intriqués, et mesures généralisées. C'est l'outil indispensable pour le chapitre sur le bruit (4.2).

---

## Idée principale

Imaginez deux situations :

**Situation A :** Votre ami lance une pièce cachée. C'est pile ou face, 50/50. Vous ne savez pas le résultat, mais la pièce EST dans un état défini.

**Situation B :** Votre ami prépare un qubit. Soit $\ket{0}$ (avec proba 50%), soit $\ket{1}$ (avec proba 50%). Vous ne savez pas lequel. C'est un **mélange statistique**.

Maintenant, comparez avec la **Situation C :** Le qubit est dans l'état $\ket{+} = \frac{1}{\sqrt{2}}(\ket{0}+\ket{1})$. C'est une **superposition**, pas un mélange !

Les situations B et C donnent les mêmes probabilités si on mesure dans la base Z (50/50). Mais si on mesure dans la base X :
- Situation B : 50/50 (c'est un mélange)
- Situation C : 100% $\ket{+}$ (c'est une superposition)

La matrice densité capture cette différence, là où le vecteur d'état ne le peut pas.

---

## Contenu du cours

### Section 1 : Matrice densité

#### 1.1 Pourquoi un nouveau formalisme ?

Le formalisme du vecteur d'état $\ket{\psi}$ ne décrit que les **états purs**. Pour les **mélanges statistiques**, on utilise la matrice densité $\rho$.

> **Intuition :** Un état pur, c'est comme savoir exactement où est une bille. Un mélange, c'est comme savoir que la bille est dans une boîte, avec 50% de chance d'être à gauche et 50% à droite, mais sans superposition.

#### 1.2 Définition

Pour un système dans un mélange statistique $\{p_i, \ket{\psi_i}\}$ :

$$\rho = \sum_i p_i \ket{\psi_i}\bra{\psi_i}$$

où :
- $\rho$ (rho) = **matrice densité** — représente l'état du système quantique
- $p_i$ = **probabilité classique** du $i$-ème état ($p_i \geq 0$, $\sum_i p_i = 1$)
- $\ket{\psi_i}$ = **ket** — $i$-ème état pur du mélange (vecteur dans l'espace de Hilbert)
- $\bra{\psi_i}$ = **bra** — conjugué hermitien de $\ket{\psi_i}$
- $\ket{\psi_i}\bra{\psi_i}$ = **projecteur** sur l'état $\ket{\psi_i}$

> **Intuition :** Chaque état pur $\ket{\psi_i}$ contribue à la matrice densité avec son « poids » $p_i$. La matrice densité est une moyenne pondérée de projecteurs.

**Propriétés fondamentales :**
- $\rho^\dagger = \rho$ (hermitienne) — $\dagger$ = conjugaison hermitienne (transposée + conjuguée complexe)
- $\rho \geq 0$ (positive semi-définie) — toutes les valeurs propres sont $\geq 0$
- $\text{Tr}(\rho) = 1$ — $\text{Tr}$ = **trace** (somme des éléments diagonaux)
- $\text{Tr}(\rho^2) \leq 1$ — **pureté** : vaut $1$ pour un état pur, $< 1$ pour un mélange

#### 1.3 États purs vs mélanges

| Propriété | État pur | Mélange |
|-----------|----------|---------|
| Représentation | $\rho = \ket{\psi}\bra{\psi}$ | $\rho = \sum_i p_i \ket{\psi_i}\bra{\psi_i}$ |
| $\text{Tr}(\rho^2)$ | $1$ | $< 1$ |
| Exemple | $\ket{0}$ | 50% $\ket{0}$, 50% $\ket{1}$ |

> **Pourquoi $\text{Tr}(\rho^2)$ mesure la pureté ?** Pour un état pur, $\rho^2 = \ket{\psi}\bra{\psi}\ket{\psi}\bra{\psi} = \ket{\psi}\bra{\psi} = \rho$ (car $\braket{\psi}{\psi}=1$), donc $\text{Tr}(\rho^2) = \text{Tr}(\rho) = 1$. Pour un mélange, les termes croisés manquent.

#### 1.4 Exemple fondamental

**État pur :** $\ket{+} = \frac{1}{\sqrt{2}}(\ket{0} + \ket{1})$ où $\frac{1}{\sqrt{2}}$ est le facteur de normalisation

$$\rho_+ = \ket{+}\bra{+} = \frac{1}{2} \begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$$

> **Vérification :** $\text{Tr}(\rho_+^2) = \text{Tr}\left(\frac{1}{4}\begin{pmatrix} 2 & 2 \\ 2 & 2 \end{pmatrix}\right) = \frac{1}{4}(2+2) = 1$ ✓

**Mélange :** $\rho_{\text{mix}} = \frac{1}{2}\ket{0}\bra{0} + \frac{1}{2}\ket{1}\bra{1} = \frac{I}{2} = \frac{1}{2} \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}$

> **Vérification :** $\text{Tr}(\rho_{\text{mix}}^2) = \text{Tr}\left(\frac{1}{4}I\right) = \frac{1}{4} \times 2 = \frac{1}{2} < 1$ ✓ (c'est un mélange)

Calcul de pureté :

$$\text{Tr}(\rho_+^2) = \frac{1}{2} + \frac{1}{2} = 1, \quad \text{Tr}(\rho_{\text{mix}}^2) = \frac{1}{4} + \frac{1}{4} = \frac{1}{2}$$

où $\text{Tr}(\rho^2)$ est la **pureté** : elle vaut $1$ pour un état pur ($\rho_+$) et $\frac{1}{2}$ pour un mélange ($\rho_{\text{mix}}$), car $\rho_{\text{mix}}^2 = \frac{1}{4}I$.

> **Différence clé :** $\rho_+$ a des termes hors-diagonaux (les « 1 » en haut à droite et bas à gauche) qui représentent la **cohérence quantique**. $\rho_{\text{mix}}$ n'en a pas — c'est purement classique.

```python
import qutip as qt
import numpy as np

# ============================================================
# ÉTAT PUR |+⟩
# ============================================================
# Créer |+⟩ = (|0⟩ + |1⟩)/√2
ket_plus = (qt.basis(2,0) + qt.basis(2,1)).unit()

# Matrice densité : ρ = |+⟩⟨+|
rho_pur = ket_plus * ket_plus.dag()
print("ρ pur =", rho_pur)

# Pureté : Tr(ρ²)
print("Tr(ρ²) =", (rho_pur * rho_pur).tr())  # = 1.0 (état pur)

# ============================================================
# MÉLANGE 50/50 : 50% |0⟩ + 50% |1⟩
# ============================================================
# qt.ket2dm() convertit un ket en matrice densité |ψ⟩⟨ψ|
rho_mix = 0.5 * qt.ket2dm(qt.basis(2,0)) + 0.5 * qt.ket2dm(qt.basis(2,1))
print("\nρ mix =", rho_mix)

# Pureté
print("Tr(ρ²) =", (rho_mix * rho_mix).tr())  # = 0.5 (mélange)
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

> **Observez la différence :** $\rho_{\text{pur}}$ a des termes hors-diagonaux (0.5), tandis que $\rho_{\text{mix}}$ est diagonale. Les termes hors-diagonaux sont la signature de la cohérence quantique !

**Avez-vous compris ?**
- Quelle est la pureté de l'état $\rho = \ket{0}\bra{0}$ ? (Réponse : 1 — c'est un état pur)
- Quelle est la pureté de $\rho = I/2$ ? (Réponse : 1/2 — c'est le mélange maximal)

---

### Section 2 : Matrice densité réduite

#### 2.1 Trace partielle

Pour un système bipartite $\rho_{AB} \in \mathcal{H}_A \otimes \mathcal{H}_B$, la matrice densité réduite de $A$ est :

$$\rho_A = \text{Tr}_B(\rho_{AB}) = \sum_i (I_A \otimes \bra{i}_B) \rho_{AB} (I_A \otimes \ket{i}_B)$$

> **Intuition :** Si vous avez un système composé AB mais que vous n'avez accès qu'à A, vous devez « moyenner » sur B. C'est exactement ce que fait la trace partielle : elle élimine le sous-système B en sommant sur tous ses états possibles.

#### 2.2 Exemple crucial : Bell state

Pour $\ket{\Phi^+} = (\ket{00} + \ket{11})/\sqrt{2}$ :

$$\rho_{\Phi^+} = \frac{1}{2} \begin{pmatrix} 1 & 0 & 0 & 1 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 1 \end{pmatrix}$$

$$\rho_A = \text{Tr}_B(\rho_{\Phi^+}) = \frac{I}{2} = \begin{pmatrix} 1/2 & 0 \\ 0 & 1/2 \end{pmatrix}$$

> **Résultat remarquable :** L'état global $\ket{\Phi^+}$ est un état PUR (parfaitement connu). Mais l'état réduit $\rho_A$ est un MÉLANGE MAXIMAL ! L'information n'est pas dans les sous-systèmes individuels — elle est dans les **corrélations** entre eux. C'est la signature de l'intrication.

```python
import qutip as qt

# --- État de Bell |Φ⁺⟩ ---
ket00 = qt.tensor(qt.basis(2,0), qt.basis(2,0))
ket11 = qt.tensor(qt.basis(2,1), qt.basis(2,1))
phi_plus = (ket00 + ket11).unit()
rho_AB = phi_plus * phi_plus.dag()

# --- Trace partielle sur B ---
# ptrace(0) garde le sous-système A (index 0) et trace sur B
rho_A = rho_AB.ptrace(0)
print("ρ_A =", rho_A)

# --- Entropie de von Neumann de ρ_A ---
# S = -Tr(ρ log ρ) = ln 2 pour un état intriqué maximal
print("S(ρ_A) =", qt.entropy_vn(rho_A))  # = 0.693 ≈ ln 2
```

**Sortie attendue :**

```
ρ_A = Quantum object: dims=[[2], [2]], shape=(2, 2), type='oper', dtype=CSR, isherm=True
Qobj data =
[[0.5 0. ]
 [0.  0.5]]
S(ρ_A) = 0.6931471805599454
```

> **Interprétation :** $S(\rho_A) = \ln 2 \approx 0.693$ est l'entropie maximale pour un qubit. Cela confirme que le sous-système A est dans l'état le plus « mélangé » possible, même si l'état global est pur.

---

### Section 3 : Entropie d'intrication

#### 3.1 Entropie de von Neumann

L'entropie de von Neumann mesure le désordre d'un état quantique :

$$S(\rho) = -\text{Tr}(\rho \log \rho) = -\sum_i \lambda_i \log \lambda_i$$

où $\lambda_i$ sont les valeurs propres de $\rho$.

> **Intuition :** C'est l'analogue quantique de l'entropie de Shannon. Si $\rho$ est un état pur, une seule valeur propre vaut 1 et les autres valent 0, donc $S = 0$ (pas de désordre). Si $\rho = I/d$ (mélange maximal), $S = \log d$ (désordre maximal).

#### 3.2 Intrication

Pour un état pur bipartite $\ket{\psi}_{AB}$, l'intrication est mesurée par :

$$E(\ket{\psi}) = S(\rho_A) = S(\rho_B)$$

- État séparable : $E = 0$
- État maximalement intriqué : $E = \log d$ (où $d = \dim \mathcal{H}_A$)

| État | $\rho_A$ | $S(\rho_A)$ |
|------|----------|-------------|
| $\ket{00}$ | $\ket{0}\bra{0}$ | $0$ |
| $\ket{\Phi^+}$ | $I/2$ | $\ln 2$ |
| $(\sqrt{0.8}\ket{00} + \sqrt{0.2}\ket{11})$ | $\begin{pmatrix}0.8&0\\0&0.2\end{pmatrix}$ | $-(0.8\log0.8 + 0.2\log0.2)$ |

> **Exemple numérique :** Pour $\sqrt{0.8}\ket{00} + \sqrt{0.2}\ket{11}$ :
> $S = -(0.8 \ln 0.8 + 0.2 \ln 0.2) = -(0.8 \times (-0.223) + 0.2 \times (-1.609)) = 0.179 + 0.322 = 0.500$
> L'intrication est intermédiaire : ni nulle, ni maximale.

```python
import numpy as np
import qutip as qt

# --- Intrication en fonction du paramètre θ ---
def entanglement_entropy(theta):
    """Calcule S(ρ_A) pour |ψ⟩ = cos(θ)|00⟩ + sin(θ)|11⟩
    
    Args:
        theta: angle paramétrant l'état (0 = séparable, π/4 = maximal)
    
    Returns:
        Entropie de von Neumann de la matrice réduite ρ_A
    """
    c, s = np.cos(theta), np.sin(theta)
    # État |ψ⟩ = cos(θ)|00⟩ + sin(θ)|11⟩
    psi = c * qt.tensor(qt.basis(2,0), qt.basis(2,0)) + s * qt.tensor(qt.basis(2,1), qt.basis(2,1))
    rho = psi * psi.dag()
    # Trace partielle sur B
    rho_A = rho.ptrace(0)
    return qt.entropy_vn(rho_A)

# --- Calcul pour différents angles ---
thetas = np.linspace(0, np.pi/2, 100)
entropies = [entanglement_entropy(t) for t in thetas]
# L'entropie est maximale à θ = π/4 (état de Bell)
```

---

### Section 4 : Mesures POVM

#### 4.1 Définition

Un **POVM** (Positive Operator-Valued Measure) est un ensemble $\{E_m\}$ tel que :
- $E_m \geq 0$ (positifs)
- $\sum_m E_m = I$

La probabilité d'obtenir $m$ est $p(m) = \text{Tr}(E_m \rho)$.

> **Intuition :** Les POVM généralisent les mesures projectives. Au lieu d'exiger que les opérateurs de mesure soient orthogonaux ($P_m P_n = \delta_{mn} P_m$), on autorise des éléments qui se « chevauchent ». C'est utile pour discriminer des états non orthogonaux.

Contrairement aux mesures projectives, les $E_m$ n'ont pas besoin d'être orthogonaux.

#### 4.2 Exemple : discrimination de 3 états

Discriminer $\ket{0}$, $\ket{+}$, $\ket{+i}$ avec une seule mesure :

```python
import qutip as qt
import numpy as np

# --- États à discriminer ---
states = [
    qt.basis(2, 0),           # |0⟩ : état de base Z
    (qt.basis(2,0) + qt.basis(2,1)).unit(),  # |+⟩ : superposition symétrique
    (qt.basis(2,0) + 1j*qt.basis(2,1)).unit() # |+i⟩ : superposition avec phase i
]

# --- Construction des éléments POVM ---
E = []
for i, s in enumerate(states):
    # Chaque élément E_m est le projecteur sur l'état correspondant
    E.append(s * s.dag())

# --- Vérification de la normalisation ---
E_sum = sum(E)  # devrait être proche de I (pas exactement I ici)

# --- Probabilités de mesure ---
# Pour chaque état d'entrée, quelle est la probabilité du résultat m=0 ?
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

> **Interprétation :** Le résultat m=0 identifie parfaitement $\ket{0}$ (probabilité 1), mais ne peut pas distinguer $\ket{+}$ de $\ket{+i}$ (probabilité 0.5 chacun). C'est une limitation fondamentale : on ne peut pas discriminer parfaitement des états non orthogonaux.

---

### Section 5 : Distinguer intrication et corrélations classiques

#### 5.1 États séparables vs intriqués

Un état $\rho_{AB}$ est **séparable** s'il peut s'écrire :

$$\rho_{AB} = \sum_i p_i \; \rho_A^{(i)} \otimes \rho_B^{(i)}$$

> **Intuition :** Un état séparable est un mélange d'états produits. Les corrélations sont purement classiques (comme deux pièces qui ont été préparées séparément). Sinon, l'état est **intriqué**.

Sinon, il est **intriqué**.

#### 5.2 Critère PPT (Peres–Horodecki)

Pour un système $2 \times 2$ ou $2 \times 3$, un état est intriqué ssi sa **transposée partielle** a une valeur propre négative.

> **Intuition :** La transposée partielle est une opération mathématique sur la matrice densité. Si le résultat a des valeurs propres négatives, c'est la signature que les corrélations sont « trop fortes » pour être classiques → intrication.

```python
import qutip as qt

# --- Test PPT pour l'état de Bell ---
ket00 = qt.tensor(qt.basis(2,0), qt.basis(2,0))
ket11 = qt.tensor(qt.basis(2,1), qt.basis(2,1))
phi_plus = (ket00 + ket11).unit()
rho_AB = phi_plus * phi_plus.dag()

# --- Transposée partielle par rapport à B ---
# partial_transpose transpose le sous-système B
rho_PT = qt.partial_transpose(rho_AB, [0, 1])

# --- Calcul des valeurs propres ---
eigvals = rho_PT.eigenenergies()
print(f"Valeurs propres de ρ^{{T_B}} : {eigvals}")

# --- Critère : une valeur propre négative = intriqué ---
print("État intriqué ?", any(v < -1e-10 for v in eigvals))
```

**Sortie attendue :**

```
Valeurs propres de ρ^{T_B} : [-0.5  0.5  0.5  0.5]
État intriqué ? True
```

> **Interprétation :** La valeur propre $-0.5$ est négative → l'état est intriqué. Pour un état séparable, toutes les valeurs propres de la transposée partielle seraient $\geq 0$.

---

## Exemple guidé

**Problème :** Calculer $\rho_A$ pour l'état $\ket{\Psi^-} = (\ket{01} - \ket{10})/\sqrt{2}$ et vérifier que $S(\rho_A) = \ln 2$.

**Étape 1 — Écrire la matrice densité complète :**

$$\rho_{AB} = \ket{\Psi^-}\bra{\Psi^-} = \frac{1}{2}(\ket{01} - \ket{10})(\bra{01} - \bra{10})$$
$$= \frac{1}{2}(\ket{01}\bra{01} - \ket{01}\bra{10} - \ket{10}\bra{01} + \ket{10}\bra{10})$$

En matrice (base $\{\ket{00}, \ket{01}, \ket{10}, \ket{11}\}$) :

$$\rho_{AB} = \frac{1}{2}\begin{pmatrix} 0 & 0 & 0 & 0 \\ 0 & 1 & -1 & 0 \\ 0 & -1 & 1 & 0 \\ 0 & 0 & 0 & 0 \end{pmatrix}$$

**Étape 2 — Trace partielle sur B :**

$$\rho_A = \text{Tr}_B(\rho_{AB}) = \bra{0}_B \rho_{AB} \ket{0}_B + \bra{1}_B \rho_{AB} \ket{1}_B$$

- $\bra{0}_B \rho_{AB} \ket{0}_B$ : on prend les éléments où B est dans l'état $\ket{0}$, c'est-à-dire les blocs $\ket{00}, \ket{10}$ :
$$= \frac{1}{2}(\ket{1}\bra{1}) = \begin{pmatrix} 0 & 0 \\ 0 & 1/2 \end{pmatrix}$$

- $\bra{1}_B \rho_{AB} \ket{1}_B$ : on prend les éléments où B est dans l'état $\ket{1}$, c'est-à-dire les blocs $\ket{01}, \ket{11}$ :
$$= \frac{1}{2}(\ket{0}\bra{0}) = \begin{pmatrix} 1/2 & 0 \\ 0 & 0 \end{pmatrix}$$

$$\rho_A = \begin{pmatrix} 1/2 & 0 \\ 0 & 1/2 \end{pmatrix} = \frac{I}{2}$$

**Étape 3 — Calculer l'entropie :**

$$S(\rho_A) = -\text{Tr}(\rho_A \log \rho_A) = -(1/2 \log(1/2) + 1/2 \log(1/2)) = -2 \times \frac{1}{2} \times (-\ln 2) = \ln 2$$

**Conclusion :** $S(\rho_A) = \ln 2$ confirme que $\ket{\Psi^-}$ est maximalement intriqué. ✓

---

## Implémentation Python

### Résumé complet en code

```python
import numpy as np
import qutip as qt

# ============================================================
# 1. MATRICE DENSITÉ : états purs vs mélanges
# ============================================================
ket0 = qt.basis(2, 0)
ket1 = qt.basis(2, 1)
ket_plus = (ket0 + ket1).unit()

# État pur |+⟩⟨+|
rho_pur = ket_plus * ket_plus.dag()
print("État pur |+⟩ :")
print(rho_pur)
print("Pureté =", (rho_pur * rho_pur).tr())  # = 1.0

# Mélange 50/50
rho_mix = 0.5 * qt.ket2dm(ket0) + 0.5 * qt.ket2dm(ket1)
print("\nMélange 50/50 :")
print(rho_mix)
print("Pureté =", (rho_mix * rho_mix).tr())  # = 0.5

# ============================================================
# 2. TRACE PARTIELLE : sous-système d'un état intriqué
# ============================================================
ket00 = qt.tensor(ket0, ket0)
ket11 = qt.tensor(ket1, ket1)
phi_plus = (ket00 + ket11).unit()
rho_AB = phi_plus * phi_plus.dag()

# ρ_A = Tr_B(ρ_AB)
rho_A = rho_AB.ptrace(0)
print("\nρ_A (état de Bell) :", rho_A)
print("S(ρ_A) =", qt.entropy_vn(rho_A), "= ln 2 (intrication maximale)")

# ============================================================
# 3. ENTROPIE D'INTRICATION en fonction du paramètre
# ============================================================
def entanglement_entropy(theta):
    """Calcule S(ρ_A) pour |ψ⟩ = cos(θ)|00⟩ + sin(θ)|11⟩"""
    c, s = np.cos(theta), np.sin(theta)
    psi = c * ket00 + s * ket11
    rho = psi * psi.dag()
    rho_A = rho.ptrace(0)
    return qt.entropy_vn(rho_A)

# Maximum à θ = π/4 (état de Bell)
print("\nEntropie à θ=0 :", entanglement_entropy(0))         # = 0 (séparable)
print("Entropie à θ=π/4 :", entanglement_entropy(np.pi/4))  # = ln 2 (maximal)
print("Entropie à θ=π/2 :", entanglement_entropy(np.pi/2))  # = 0 (séparable)

# ============================================================
# 4. CRITÈRE PPT : détection d'intrication
# ============================================================
rho_PT = qt.partial_transpose(rho_AB, [0, 1])
eigvals = rho_PT.eigenenergies()
print("\nValeurs propres de ρ^{T_B} :", eigvals)
print("Intriqué ?", any(v < -1e-10 for v in eigvals))  # True
```

---

## À retenir

1. **Matrice densité** $\rho = \sum_i p_i \ket{\psi_i}\bra{\psi_i}$ : généralise les états purs aux mélanges statistiques
2. **Pureté** $\text{Tr}(\rho^2)$ : vaut 1 pour un état pur, $< 1$ pour un mélange
3. **Trace partielle** $\rho_A = \text{Tr}_B(\rho_{AB})$ : décrit un sous-système en « moyennant » sur le reste
4. **Intrication** = état pur global mais sous-systèmes mélangés : $S(\rho_A) > 0$
5. **Entropie de von Neumann** $S(\rho) = -\text{Tr}(\rho \log \rho)$ : mesure le désordre/l'information
6. **POVM** : généralisation des mesures projectives, éléments non orthogonaux possibles
7. **Critère PPT** : transposée partielle avec valeur propre négative → intriqué

---

## Pièges à éviter

1. **Confondre superposition et mélange** — $\ket{+} = \frac{1}{\sqrt{2}}(\ket{0}+\ket{1})$ (état pur, $\text{Tr}(\rho^2)=1$) n'est PAS la même chose que 50% $\ket{0}$ + 50% $\ket{1}$ (mélange, $\text{Tr}(\rho^2)=1/2$). La différence est dans les termes hors-diagonaux.

2. **Penser que $\rho_A$ mixte implique que l'état global est mixte** — NON ! Pour un état de Bell, $\rho_{AB}$ est pur mais $\rho_A$ est totalement mixte. C'est la signature de l'intrication.

3. **Confondre les probabilités classiques $p_i$ et les amplitudes quantiques** — Les $p_i$ dans $\rho = \sum p_i \ket{\psi_i}\bra{\psi_i}$ sont des probabilités classiques (pas d'interférence entre les termes).

4. **Oublier que le critère PPT n'est suffisant que pour $2\times 2$ et $2\times 3$** — Pour des systèmes plus grands, il existe des états intriqués à transposée partielle positive (états « bound entangled »).

5. **Penser qu'un POVM donne plus d'information qu'une mesure projective** — Un POVM peut discriminer plus d'états non orthogonaux, mais ne permet jamais de discriminer parfaitement des états non orthogonaux.

---

## Exercices

### Niveau 1 — Application directe

1. Calculer $\rho_A$ pour $\ket{\Psi^-} = (\ket{01} - \ket{10})/\sqrt{2}$ et vérifier que $S(\rho_A) = \ln 2$.
   *(Suivez l'exemple guidé ci-dessus !)*

2. Montrer que $\rho = \frac{3}{4}\ket{0}\bra{0} + \frac{1}{4}\ket{1}\bra{1}$ a $\text{Tr}(\rho^2) < 1$.
   *(Indice : calculez $\rho^2$ puis sa trace)*

3. Écrire la matrice densité de l'état $\ket{+i} = \frac{1}{\sqrt{2}}(\ket{0} + i\ket{1})$ et vérifier que c'est un état pur.

### Niveau 2 — Compréhension

4. Implémenter la discrimination optimale entre $\ket{0}$ et $\ket{+}$ avec un POVM. Combien d'éléments POVM faut-il ?

5. Vérifier le critère PPT pour l'état $\rho = p\ket{\Phi^+}\bra{\Phi^+} + (1-p)I/4$ en fonction de $p$. Pour quelles valeurs de $p$ l'état est-il intriqué ?

6. Montrer que pour un état produit $\ket{\psi}_A \otimes \ket{\phi}_B$, la trace partielle donne $\rho_A = \ket{\psi}\bra{\psi}$.

### Niveau 3 — Défi

7. Calculer l'intrication de formation pour l'état de Werner à 2 qubits : $\rho_W = p\ket{\Psi^-}\bra{\Psi^-} + (1-p)I/4$.

8. Démontrer que l'entropie de von Neumann est invariante sous évolution unitaire : $S(U\rho U^\dagger) = S(\rho)$.

---

## Pour aller plus loin

- Nielsen & Chuang, Ch. 2.4 & 11.3 — Matrice densité et entropie de von Neumann
- Vidéo : [Density Matrices Explained](https://www.youtube.com/watch?v=9GWVi8WmaXQ) — Introduction visuelle
- Preskill's lecture notes, Ch. 3 — Traitement très pédagogique des systèmes composites
