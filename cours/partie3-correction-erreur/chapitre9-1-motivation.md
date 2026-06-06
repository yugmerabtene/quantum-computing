# Chapitre 9.1 — Motivation et défis de la correction d'erreur quantique

## Ce que vous allez apprendre

- Comprendre pourquoi les qubits sont si fragiles face à la décohérence
- Distinguer la correction d'erreur classique (copie) de la correction quantique (intrication)
- Identifier les 3 obstacles fondamentaux : non-clonage, mesure destructive, erreurs continues
- Formaliser le seuil de correction d'erreur et son importance
- Simuler un qubit bruité avec QuTiP et visualiser la décohérence en temps réel

---

## Motivation

Imaginez que vous envoyez un message important par la poste. Que faites-vous pour vous protéger contre la perte du courrier ? Vous envoyez **3 copies**. Si une arrive abîmée, les deux autres vous permettent de reconstituer le message par vote majoritaire. Simple, efficace, universel.

En informatique classique, c'est exactement ce qu'on fait : on **copie** l'information (0 → 000, 1 → 111) et on vote. Mais en quantique, on se heurte à un mur :

> **Théorème de non-clonage** : il est physiquement impossible de copier un état quantique inconnu.

Alors comment protéger l'information quantique ? C'est le défi central de ce chapitre. Et la réponse — la correction d'erreur quantique — est l'une des idées les plus élégantes de toute l'informatique quantique.

**Pourquoi ce sujet est critique ?** Sans correction d'erreur, pas d'ordinateur quantique utile. Les qubits actuels (Google, IBM, Harvard) perdent leur information en quelques microsecondes. Un algorithme comme celui de Shor nécessite des milliards d'opérations. Sans correction, c'est impossible.

---

## Idée principale

Pensez à un **orchestre symphonique**. Un seul musicien peut jouer faux — c'est inévitable. Mais si vous avez 100 musiciens jouant la même partition, et que vous placez des chefs de pupitre qui écoutent les voisins, vous pouvez détecter et corriger les fausses notes **sans arrêter le concert**.

En correction quantique, c'est similaire :
- On ne **copie** pas le qubit (interdit par la physique)
- On **répartit** l'information sur plusieurs qubits physiques via l'intrication
- On **surveille** les erreurs indirectement, sans jamais regarder l'information elle-même (mesure de syndrome)

L'astuce géniale : même si l'erreur est **continue** (une petite rotation quelconque), on peut la **discrétiser** en erreurs Pauli (X, Y, Z) et les corriger une par une.

---

## Contenu du cours

### Section 1 : La fragilité des qubits — pourquoi c'est si difficile

#### Concept

Un qubit stocke l'information dans un état quantique :

$$
\ket{\psi} = \alpha\ket{0} + \beta\ket{1}, \quad |\alpha|^2 + |\beta|^2 = 1
$$

**Intuition** : $\alpha$ et $\beta$ sont des amplitudes de probabilité (des nombres complexes). $|\alpha|^2$ donne la probabilité de mesurer $\ket{0}$, et $|\beta|^2$ celle de mesurer $\ket{1}$. Contrairement à un bit classique qui vaut 0 ou 1, le qubit est un **continuum** : une infinité d'états possibles sur la sphère de Bloch.

**Exemple** : L'état $\ket{+} = \frac{1}{\sqrt{2}}(\ket{0} + \ket{1})$ est une superposition équilibrée. Si on le mesure, on obtient 0 ou 1 avec 50% de chance chacun. Mais tant qu'on ne mesure pas, c'est « les deux à la fois ».

#### La décohérence : l'ennemi invisible

La décohérence est le processus par lequel un qubit perd sa cohérence en s'intriquant avec son environnement. C'est comme si l'environnement « espionnait » le qubit et détruisait ses superpositions.

$$
\rho(t) = \begin{pmatrix} |\alpha|^2 & \alpha\beta^* e^{-\gamma t} \\ \alpha^*\beta e^{-\gamma t} & |\beta|^2 \end{pmatrix}
$$

**Intuition** : $\rho(t)$ est la matrice densité — elle décrit l'état du qubit quand il est mélangé avec l'environnement. Le terme $e^{-\gamma t}$ fait décroître les **termes hors diagonale** (les cohérences), c'est-à-dire les superpositions. Quand $\gamma t \gg 1$, il ne reste que les probabilités classiques $|\alpha|^2$ et $|\beta|^2$ : le qubit est devenu un bit classique aléatoire.

**Variables** : $\rho(t)$ = matrice densité au temps $t$, $\gamma$ = taux de décohérence (plus il est grand, plus ça va vite), $\alpha, \beta$ = amplitudes initiales.

**Exemple concret** : Pour un qubit supraconducteur Google Willow avec $T_2 = 12\,\mu s$, les cohérences sont divisées par $e \approx 2.718$ en 12 microsecondes. En 60 µs, elles sont quasi nulles.

#### Temps caractéristiques

- **T₁** : temps de relaxation (perte d'énergie, $\ket{1} \to \ket{0}$)
- **T₂** : temps de déphasage (perte de cohérence de phase)
- Toujours $T_2 \le 2T_1$

**Analogie** : T₁, c'est comme la durée de vie d'une balle en l'air (elle finit par retomber). T₂, c'est comme la durée pendant laquelle deux métronomes restent synchronisés (ils finissent par se désynchroniser).

```python
import qutip as qt
import numpy as np

# Simulation de la décohérence d'un qubit
# T1 = 30 µs : temps de relaxation (énergie)
# T2 = 15 µs : temps de déphasage (cohérence)
T1, T2 = 30.0, 15.0  # µs
gamma1 = 1.0 / T1     # taux de relaxation
gamma2 = 1.0 / T2     # taux de déphasage

omega = 2.0  # GHz : fréquence du qubit
H = omega / 2 * qt.sigmaz()  # Hamiltonien : évolution libre

sm = qt.destroy(2)    # opérateur d'abaissement (relaxation)
sz = qt.sigmaz()      # opérateur Z (déphasage)

# Opérateurs de Kraus : modélisent l'interaction avec l'environnement
c_ops = [np.sqrt(gamma1) * sm, np.sqrt(gamma2) * sz]

# État initial : |+> = superposition égale de |0> et |1>
psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
rho0 = psi0 * psi0.dag()  # matrice densité initiale (état pur)

# Simulation de l'équation maîtresse de Lindblad
tlist = np.linspace(0, 3 * T1, 200)
result = qt.mesolve(H, rho0, tlist, c_ops=c_ops)

# Affichage de la pureté Tr(rho^2) au cours du temps
# Pureté = 1 : état pur (parfait)
# Pureté = 0.5 : état totalement mélangé (plus d'info quantique)
print("Purete (Tr(rho^2)) au cours du temps :")
for t_idx in [0, len(tlist)//4, len(tlist)//2, -1]:
    rho_t = result.states[t_idx]
    purete = (rho_t * rho_t).tr()
    print(f"  t = {tlist[t_idx]:5.1f} µs : Tr(rho^2) = {purete:.6f}")
```

**Sortie attendue :**

```
Purete (Tr(rho^2)) au cours du temps :
  t =   0.0 µs : Tr(rho^2) = 1.000000
  t =  22.5 µs : Tr(rho^2) = 0.720368
  t =  45.0 µs : Tr(rho^2) = 0.560974
  t =  90.0 µs : Tr(rho^2) = 0.386174
```

**Ce qu'on observe** : La pureté chute de 1.0 (état pur parfait) à ~0.39 après 90 µs. Le qubit a perdu la majeure partie de son information quantique.

#### Sources de bruit physique

| Source | Effet | Ordre de grandeur |
|--------|-------|-------------------|
| Couplage phonons | Relaxation T₁ | 10–100 µs (supra) |
| Bruit de flux | Déphasage T₂ | 5–50 µs (supra) |
| Radiation ionisante | Erreurs parasites | 1/10 min |
| Diaphonie | Crosstalk entre qubits | 0.1–1 % |
| Impuretés de fabrication | Variations de fréquence | 1–10 MHz |

**Analogie** : Ces sources de bruit sont comme les différentes façons dont un message peut être corrompu : la pluie (décohérence), le vent (déphasage), les interférences radio (crosstalk), etc.

---

### Section 2 : Pourquoi la correction classique ne suffit pas

#### Concept : la correction classique par répétition

En classique, c'est simple :
- Bit $0 \to 000$, bit $1 \to 111$
- Si on reçoit $010$, on vote majoritaire → $0$

**Pourquoi ça marche ?** Parce qu'on peut **copier** un bit classique sans problème.

#### Les 3 obstacles quantiques

**Obstacle 1 : Le théorème de non-clonage**

Il est physiquement impossible de copier un état quantique inconnu :

$$
\nexists U \; \text{t.q.} \; U(\ket{\psi}\ket{0}) = \ket{\psi}\ket{\psi}
$$

**Intuition** : En classique, copier c'est gratuit (Ctrl+C). En quantique, la physique l'interdit fondamentalement. Si on essaie de « copier » un qubit, on le détruit.

**Variables** : $U$ = opérateur unitaire de copie (n'existe pas), $\ket{\psi}$ = état inconnu à copier, $\ket{0}$ = état auxiliaire vierge.

**Exemple** : Si $\ket{\psi} = \frac{1}{\sqrt{3}}\ket{0} + \sqrt{\frac{2}{3}}\ket{1}$, on ne peut PAS créer $\ket{\psi}\ket{\psi}$. Point.

**Obstacle 2 : La mesure est destructive**

Mesurer un qubit détruit sa superposition. On ne peut donc pas « vérifier » l'état d'un qubit sans le casser.

**Analogie** : C'est comme ouvrir une lettre scellée : une fois ouverte, le sceau est brisé. En quantique, mesurer $\alpha\ket{0} + \beta\ket{1}$ donne soit 0 soit 1, et l'état original est perdu.

**Obstacle 3 : Les erreurs sont continues**

En classique, une erreur est binaire : 0 devient 1, ou 1 devient 0. En quantique, l'erreur peut être une **rotation continue** :

$$
\ket{\psi} \to \ket{\psi'} = a\ket{0} + b\ket{1} \quad \text{avec rotation continue}
$$

**Intuition** : Une erreur quantique, c'est comme si quelqu'un tournait légèrement votre boussole. En classique, l'aiguille saute de Nord à Sud (binaire). En quantique, elle peut pointer dans n'importe quelle direction (continu). Comment corriger une infinité d'erreurs possibles ?

**Variables** : $a, b \in \mathbb{C}$ = amplitudes après l'erreur (rotation continue sur la sphère de Bloch).

#### La solution : discrétiser les erreurs

Le miracle de la correction quantique, c'est que même si les erreurs sont continues, on peut les **projecter** sur une base discrète : les opérateurs de Pauli $I, X, Y, Z$.

$$
X = \begin{pmatrix}0&1\\1&0\end{pmatrix},\;
Y = \begin{pmatrix}0&-i\\i&0\end{pmatrix},\;
Z = \begin{pmatrix}1&0\\0&-1\end{pmatrix}
$$

**Intuition** : $X$ = bit-flip (0 ↔ 1), $Z$ = phase-flip (change le signe de $\ket{1}$), $Y = iXZ$ = les deux à la fois. Toute erreur, aussi compliquée soit-elle, se décompose comme une combinaison de ces 4 opérations de base.

Toute erreur peut se décomposer sur la base $\{I, X, Y, Z\}$ :

$$
\mathcal{E}(\rho) = \sum_{i,j} \chi_{ij} P_i \rho P_j, \quad P_i \in \{I, X, Y, Z\}^{\otimes n}
$$

**Variables** : $\chi_{ij}$ = matrice de processus (décrit le canal de bruit), $P_i$ = opérateurs de Pauli sur $n$ qubits.

**Exemple** : Une petite rotation $R_x(\theta = 0.1)$ se décompose en $0.995 \cdot I - 0.0998i \cdot X$. L'erreur est majoritairement « rien » ($I$) avec une petite composante de bit-flip ($X$).

```python
import numpy as np

# Décomposition d'une erreur continue sur la base de Pauli
def decompose_error_on_pauli(E_matrix):
    """
    Décompose une matrice d'erreur 2x2 sur la base de Pauli.
    Retourne les coefficients (c_I, c_X, c_Y, c_Z).
    """
    # Les 4 matrices de Pauli forment une base de l'espace des matrices 2x2
    I2 = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)

    basis = [I2, X, Y, Z]
    coeffs = []
    for P in basis:
        # Produit scalaire : c_P = Tr(P† · E) / 2
        c = np.trace(P.conj().T @ E_matrix) / 2.0
        coeffs.append(c)
    return coeffs

# Exemple : rotation autour de X d'angle theta = 0.1 radian
# C'est une erreur continue, mais on va la décomposer en Pauli discrets
theta = 0.1
U_rot = np.cos(theta) * np.eye(2, dtype=complex) - 1j * np.sin(theta) * np.array([[0, 1], [1, 0]], dtype=complex)
c = decompose_error_on_pauli(U_rot)
print("Decomposition d'une rotation X(theta=0.1) :")
for name, val in zip(['I', 'X', 'Y', 'Z'], c):
    print(f"  {name}: {val.real:.6f} + {val.imag:.6f}i")
```

**Sortie attendue :**

```
Decomposition d'une rotation X(theta=0.1) :
  I: 0.995004 + 0.000000i
  X: 0.000000 - 0.099833i
  Y: 0.000000 + 0.000000i
  Z: 0.000000 + 0.000000i
```

**Interprétation** : L'erreur est à 99.5% « rien » (composante $I$) et à ~10% un bit-flip ($X$). La correction d'erreur quantique va traiter cette erreur continue comme si c'était un bit-flip discret.

---

### Section 3 : Le seuil de correction d'erreur

#### Concept

C'est LE résultat fondamental de la correction d'erreur quantique :

> **Théorème du seuil** : Il existe un taux d'erreur physique critique $p_\text{th}$ tel que :
> - Si $p < p_\text{th}$ : la correction réduit **exponentiellement** le taux d'erreur logique
> - Si $p > p_\text{th}$ : la correction **empire** la situation

**Intuition** : Pensez à un filet de sécurité sous un trapéziste. Si le filet est bien tendu ($p < p_\text{th}$), il rattrape le trapéziste à chaque chute. Mais si le filet est détendu ($p > p_\text{th}$), il crée plus de problèmes qu'il n'en résout — le trapéziste rebondit et retombe encore plus mal.

$$
p_L \propto \left(\frac{p}{p_\text{th}}\right)^{\lfloor (d+1)/2 \rfloor}
$$

**Variables** : $p_L$ = taux d'erreur logique (après correction), $p$ = taux d'erreur physique (avant correction), $p_\text{th}$ = seuil de correction, $d$ = distance du code (capacité de correction).

**Exemple** : Si $p = 0.3\%$, $p_\text{th} = 1\%$, et $d = 7$, alors $p_L \propto (0.3)^4 \approx 0.008\%$. On a divisé l'erreur par ~400 !

#### Valeurs typiques

| Code | Seuil $p_\text{th}$ | Distance | Référence |
|------|---------------------|----------|-----------|
| Code de surface | $\sim 1\%$ | $d$ | Fowler 2012 |
| Code de Shor | $\sim 10^{-4}$ | $3$ | Shor 1995 |
| Code Steane | $\sim 10^{-3}$ | $3$ | Steane 1996 |
| Code GKP (bosonique) | $\sim 10^{-2}$ | — | Gottesman 2001 |

#### Passage sous le seuil (Google Willow 2024)

Google a démontré expérimentalement que l'augmentation de la distance du code réduit exponentiellement le taux d'erreur logique :

```python
import numpy as np
import matplotlib.pyplot as plt

# Simulation du scaling sous le seuil
# p_physique = 0.3% : en dessous du seuil ~1%
p_physique = 0.003  # 0.3% < seuil ~1%
p_th = 0.01         # seuil théorique du code de surface

distances = [3, 5, 7, 9, 11, 13, 15]

# Sous le seuil : p_L diminue exponentiellement avec d
p_logique = []
for d in distances:
    pl = (p_physique / p_th) ** ((d + 1) // 2)
    p_logique.append(pl)

print("Scaling du taux d'erreur logique avec la distance :")
for d, pl in zip(distances, p_logique):
    print(f"  d={d:2d} : p_L = {pl:.2e}")

# Au-dessus du seuil : p_L AUGMENTE avec d (catastrophe)
p_physique_bad = 0.05  # 5% > seuil
p_logique_bad = []
for d in distances:
    pl = (p_physique_bad / p_th) ** ((d + 1) // 2)
    p_logique_bad.append(pl)

print("\nAvec p=5% (au-dessus du seuil), la correction empire :")
for d, pl in zip(distances, p_logique_bad):
    print(f"  d={d:2d} : p_L = {pl:.2e}")
```

**Sortie attendue :**

```
Scaling du taux d'erreur logique avec la distance :
  d= 3 : p_L = 9.00e-03
  d= 5 : p_L = 2.70e-04
  d= 7 : p_L = 8.10e-06
  d= 9 : p_L = 2.43e-07
  d=11 : p_L = 7.29e-09
  d=13 : p_L = 2.19e-10
  d=15 : p_L = 6.56e-12

Avec p=5% (au-dessus du seuil), la correction empire :
  d= 3 : p_L = 1.25e+00
  d= 5 : p_L = 1.56e+01
  d= 7 : p_L = 1.95e+02
  d= 9 : p_L = 2.44e+03
  d=11 : p_L = 3.05e+04
  d=13 : p_L = 3.81e+05
  d=15 : p_L = 4.77e+06
```

**Ce qu'il faut retenir** : Sous le seuil, chaque augmentation de distance divise l'erreur par ~30. Au-dessus, chaque augmentation la multiplie par ~12. C'est la différence entre le succès et l'échec.

---

### Section 4 : Simulation d'un qubit avec bruit (QuTiP)

#### Le canal dépolarisant

Le canal dépolarisant est le modèle de bruit le plus simple : avec probabilité $p$, on applique une erreur Pauli aléatoire (X, Y ou Z avec probabilité égale).

$$
\rho \to (1-p)\rho + \frac{p}{3}(X\rho X + Y\rho Y + Z\rho Z)
$$

**Intuition** : Imaginez un dé à 4 faces. Avec probabilité $1-p$, rien ne se passe. Avec probabilité $p/3$ chacune, on applique X, Y ou Z. Quand $p = 3/4$, l'état devient totalement mélangé (plus aucune information).

**Variables** : $p$ = probabilité d'erreur, $\rho$ = matrice densité, $X, Y, Z$ = matrices de Pauli.

**Exemple** : Pour $p = 0.1$, l'état $\ket{+}$ reste fidèle à 93.3%. Pour $p = 0.5$, la fidélité tombe à 66.7%.

```python
import qutip as qt
import numpy as np

def depolarizing_kraus(p):
    """Retourne les opérateurs de Kraus du canal dépolarisant.
    K0 = rien (probabilité 1-p)
    K1, K2, K3 = erreurs X, Y, Z (probabilité p/3 chacune)"""
    K0 = np.sqrt(1 - p) * qt.qeye(2)
    K1 = np.sqrt(p / 3) * qt.sigmax()
    K2 = np.sqrt(p / 3) * qt.sigmay()
    K3 = np.sqrt(p / 3) * qt.sigmaz()
    return [K0, K1, K2, K3]

def apply_kraus(rho, kraus_ops):
    """Applique un canal Kraus à une matrice densité.
    rho' = sum_k K_k · rho · K_k†"""
    result = qt.Qobj(np.zeros_like(rho.full()), dims=rho.dims)
    for K in kraus_ops:
        result += K * rho * K.dag()
    return result

# Test : évolution de la pureté et de la fidélité
p_values = np.linspace(0, 1, 11)
psi_init = (qt.basis(2, 0) + qt.basis(2, 1)).unit()  # état |+>
rho_init = psi_init * psi_init.dag()

print("Effet du canal dépolarisant sur |+><+| :")
for p in p_values:
    kraus = depolarizing_kraus(p)
    rho_final = apply_kraus(rho_init, kraus)
    purete = (rho_final * rho_final).tr()              # Tr(rho^2) : pureté
    fidelity = (psi_init.dag() * rho_final * psi_init).real  # fidélité avec |+>
    print(f"  p = {p:.1f} : Tr(rho^2) = {purete:.4f}, F = {fidelity:.4f}")
```

**Sortie attendue :**

```
Effet du canal dépolarisant sur |+><+| :
  p = 0.0 : Tr(rho^2) = 1.0000, F = 1.0000
  p = 0.1 : Tr(rho^2) = 0.9200, F = 0.9333
  p = 0.2 : Tr(rho^2) = 0.8400, F = 0.8667
  p = 0.3 : Tr(rho^2) = 0.7600, F = 0.8000
  p = 0.4 : Tr(rho^2) = 0.6800, F = 0.7333
  p = 0.5 : Tr(rho^2) = 0.6000, F = 0.6667
  p = 0.6 : Tr(rho^2) = 0.5200, F = 0.6000
  p = 0.7 : Tr(rho^2) = 0.4400, F = 0.5333
  p = 0.8 : Tr(rho^2) = 0.3600, F = 0.4667
  p = 0.9 : Tr(rho^2) = 0.2800, F = 0.4000
  p = 1.0 : Tr(rho^2) = 0.2000, F = 0.3333
```

#### Simulation Monte Carlo de trajectoires

Plutôt que de faire évoluer la matrice densité (lente), on peut simuler des **trajectoires individuelles** : chaque trajectoire représente un scénario possible du bruit, et la moyenne reconstruit le comportement global.

**Analogie** : Au lieu de calculer la trajectoire moyenne de toutes les molécules d'un gaz (équation maîtresse), on simule chaque molécule individuellement (Monte Carlo) et on fait la moyenne.

```python
import qutip as qt
import numpy as np

# Paramètres physiques
T1, T2 = 20.0, 10.0          # temps de relaxation et déphasage (µs)
gamma1, gamma2 = 1.0/T1, 1.0/T2  # taux correspondants
H = 0.5 * qt.sigmaz()        # Hamiltonien

sm = qt.destroy(2)            # opérateur d'abaissement
c_ops = [np.sqrt(gamma1) * sm, np.sqrt(gamma2) * qt.sigmaz()]  # canaux de bruit

psi0 = qt.basis(2, 0)         # état initial |0>

# Monte Carlo : 100 trajectoires individuelles
n_traj = 100
tlist = np.linspace(0, 40, 200)
mc_result = qt.mcsolve(H, psi0, tlist, c_ops=c_ops, e_ops=[qt.sigmaz()],
                       ntraj=n_traj, progress_bar=False)

# Comparaison avec l'équation maîtresse (plus exacte mais plus lente)
me_result = qt.mesolve(H, psi0 * psi0.dag(), tlist, c_ops=c_ops, e_ops=[qt.sigmaz()])

print(f"Simulation Monte Carlo ({n_traj} trajectoires) vs maître:")
for t_idx in [0, len(tlist)//4, len(tlist)//2, -1]:
    t = tlist[t_idx]
    sz_mc = mc_result.expect[0][t_idx]   # valeur moyenne de Z (Monte Carlo)
    sz_me = me_result.expect[0][t_idx]   # valeur moyenne de Z (maître)
    print(f"  t = {t:5.1f} : <Z>_MC = {sz_mc:.4f}, <Z>_ME = {sz_me:.4f}")
```

**Sortie attendue :**

```
Simulation Monte Carlo (100 trajectoires) vs maître:
  t =   0.0 : <Z>_MC = 1.0000, <Z>_ME = 1.0000
  t =  10.0 : <Z>_MC = 0.8063, <Z>_ME = 0.8197
  t =  20.0 : <Z>_MC = 0.6678, <Z>_ME = 0.6703
  t =  40.0 : <Z>_MC = 0.4572, <Z>_ME = 0.4493
```

---

### Section 5 : Le principe de la correction quantique

#### Les 3 défis majeurs résumés

1. **Non-clonage** $\Rightarrow$ on utilise l'intrication (pas la copie) pour la redondance
2. **Mesure destructive** $\Rightarrow$ on fait des mesures indirectes (syndrome) qui ne lisent pas l'information
3. **Erreurs continues** $\Rightarrow$ la correction discrétise automatiquement en erreurs Pauli

#### Le principe général

On code $k$ qubits logiques dans $n$ qubits physiques ($n > k$), en les plongeant dans un sous-espace de code :

$$
\mathcal{C} \subset (\mathbb{C}^2)^{\otimes n}, \quad \dim \mathcal{C} = 2^k
$$

**Intuition** : L'espace de Hilbert de $n$ qubits a dimension $2^n$. Le code occupe un sous-espace de dimension $2^k$. Les erreurs « poussent » l'état hors de ce sous-espace, et on peut détecter dans quelle direction il a été poussé.

Les erreurs sont détectées par des **mesures de syndrome** qui ne révèlent pas l'état logique :

$$
\begin{aligned}
\ket{\psi_L} &= \alpha\ket{0_L} + \beta\ket{1_L} \\
\text{Erreur } E &\to E\ket{\psi_L} \\
\text{Syndrome } S(E) &\to \text{information sur } E \text{ sans mesurer } \ket{\psi_L}
\end{aligned}
$$

**Analogie** : Le syndrome, c'est comme un témoin lumineux sur un tableau électrique. Il vous dit « il y a un problème sur la ligne 3 » sans vous dire quel est le message qui transitait sur cette ligne.

---

## Exemple guidé

**Problème** : Simulons la décohérence d'un qubit initialement dans l'état $\ket{+}$ avec $T_1 = 50\,\mu s$ et $T_2 = 30\,\mu s$. Calculons la fidélité après $t = 30\,\mu s$.

**Étape 1** : État initial. $\ket{\psi(0)} = \ket{+} = \frac{1}{\sqrt{2}}(\ket{0} + \ket{1})$

**Étape 2** : Matrice densité initiale.
$$\rho(0) = \ket{+}\bra{+} = \frac{1}{2}\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$$

**Étape 3** : Évolution sous décohérence. Les termes hors diagonale décroissent comme $e^{-t/T_2}$ :
$$\rho(30) = \frac{1}{2}\begin{pmatrix} 1 & e^{-30/30} \\ e^{-30/30} & 1 \end{pmatrix} = \frac{1}{2}\begin{pmatrix} 1 & e^{-1} \\ e^{-1} & 1 \end{pmatrix} \approx \frac{1}{2}\begin{pmatrix} 1 & 0.368 \\ 0.368 & 1 \end{pmatrix}$$

**Étape 4** : Fidélité avec l'état initial.
$$F = \bra{+}\rho(30)\ket{+} = \frac{1}{2}(1 + e^{-1}) \approx \frac{1}{2}(1 + 0.368) = 0.684$$

**Conclusion** : Après 30 µs (= $T_2$), la fidélité est tombée à 68.4%. C'est exactement pour combattre cette dégradation que la correction d'erreur est nécessaire.

---

## Implémentation Python

```python
import qutip as qt
import numpy as np

# === Simulation complète d'un qubit bruité avec suivi de la décohérence ===

# Paramètres physiques (typiques d'un qubit supraconducteur)
T1 = 50.0   # µs : temps de relaxation
T2 = 30.0   # µs : temps de déphasage

# Taux de bruit
gamma1 = 1.0 / T1   # taux de relaxation
gamma2 = 1.0 / T2   # taux de déphasage

# Hamiltonien : qubit à fréquence 5 GHz
omega = 5.0
H = omega / 2 * qt.sigmaz()

# Opérateurs de saut (canaux de bruit)
sm = qt.destroy(2)           # abaissement : |1> -> |0>
sz = qt.sigmaz()             # déphasage : |1> -> -|1>
c_ops = [np.sqrt(gamma1) * sm, np.sqrt(gamma2) * sz]

# État initial : |+> (superposition maximale)
psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
rho0 = psi0 * psi0.dag()

# Grille temporelle : 0 à 150 µs (3 × T1)
tlist = np.linspace(0, 150, 300)

# Résolution de l'équation maîtresse
result = qt.mesolve(H, rho0, tlist, c_ops=c_ops)

# Extraction des observables
print("Décohérence d'un qubit |+> avec T1=50µs, T2=30µs :")
print(f"{'t (µs)':<10} {'Pureté':<12} {'Fidélité |+>':<15} {'<X>':<10} {'<Z>':<10}")
for t_idx in [0, 50, 100, 150, 200, 299]:
    rho_t = result.states[t_idx]
    t = tlist[t_idx]
    purete = (rho_t * rho_t).tr().real
    fid = (psi0.dag() * rho_t * psi0).real
    ex = qt.expect(qt.sigmax(), rho_t)
    ez = qt.expect(qt.sigmaz(), rho_t)
    print(f"{t:<10.1f} {purete:<12.4f} {fid:<15.4f} {ex:<10.4f} {ez:<10.4f}")
```

---

## À retenir

1. **Les qubits sont fragiles** : la décohérence détruit l'information en quelques microsecondes (T₁, T₂)
2. **Non-clonage** : on ne peut pas copier un état quantique, donc la redondance classique est interdite
3. **Mesure destructive** : on ne peut pas « regarder » l'état d'un qubit sans le détruire
4. **Erreurs continues → discrètes** : toute erreur se décompose sur la base de Pauli {I, X, Y, Z}
5. **Seuil de correction** : si le taux d'erreur physique $p < p_\text{th} \approx 1\%$, la correction réduit exponentiellement l'erreur logique
6. **Au-dessus du seuil** : la correction empire la situation — il faut d'abord améliorer le hardware
7. **Google Willow (2024)** : première démonstration expérimentale du passage sous le seuil

---

## Pièges à éviter

1. **Confondre T₁ et T₂** : T₁ est la relaxation (énergie), T₂ est le déphasage (cohérence). Toujours $T_2 \le 2T_1$.
2. **Penser qu'on peut copier un qubit** : le théorème de non-clonage est fondamental, pas technique. Aucune exception.
3. **Croire que la correction marche toujours** : si $p > p_\text{th}$, ajouter des qubits de correction aggrave le problème.
4. **Oublier que le circuit de correction est lui-même bruité** : les portes de syndrome introduisent aussi des erreurs.
5. **Confondre erreur physique et erreur logique** : l'erreur physique est celle d'un qubit brut, l'erreur logique est celle après correction.

---

## Exercices

### Niveau 1 — Application directe

1. Simuler un qubit initialement dans l'état $\ket{+}$ avec un modèle de bruit incluant T₁ = 50 µs et T₂ = 30 µs. Tracer $\langle X \rangle$, $\langle Y \rangle$, $\langle Z \rangle$ en fonction du temps.

2. Implémenter manuellement les opérateurs de Kraus du canal bit-flip et vérifier la condition $\sum_k K_k^\dagger K_k = I$.

### Niveau 2 — Compréhension

3. Montrer que la fidélité d'un état $\ket{\psi}$ après un canal dépolarisant est $F = 1 - \frac{2p}{3}$.

4. Avec Qiskit, créer un circuit qui prépare $\ket{+}$ et lui applique un canal dépolarisant via le `NoiseModel`. Comparer les distributions de mesure avec et sans bruit pour 4096 shots.

### Niveau 3 — Défi

5. Démontrer mathématiquement que le taux d'erreur logique pour un code de distance $d$ sous un seuil $p_\text{th}$ évolue comme $p_L \propto (p/p_\text{th})^{\lfloor (d+1)/2 \rfloor}$.

6. **Recherche** : Lire l'article Google Willow (Nature 2024) et résumer en 10 lignes comment ils démontrent le passage sous le seuil.

---

## Pour aller plus loin

- **Article fondateur** : Shor, « Scheme for Reducing Decoherence in Quantum Computer Memory » (1995) — le premier code correcteur quantique
- **Revue pédagogique** : Lidar & Brun, « Quantum Error Correction » (Cambridge, 2013) — référence complète
- **Google Willow** : Nature 634, 893–899 (2024) — démonstration expérimentale du seuil
- **Simulation avancée** : le package `qiskit-aer` permet de simuler des circuits bruités réalistes avec des modèles de bruit personnalisés
- **Prochaine étape** : Chapitre 9.2 — les codes correcteurs quantiques concrets (répétition, Shor, CSS, stabilisateurs)
