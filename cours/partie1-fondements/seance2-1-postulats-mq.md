# Séance 2.1 — Postulats de la mécanique quantique

## Objectifs

- Énoncer et comprendre les 4 postulats de la MQ
- Maîtriser la sphère de Bloch
- Savoir décrire l'évolution unitaire et la mesure projective

---

## 1. Postulat 1 — États

> À tout système physique isolé est associé un espace de Hilbert $\mathcal{H}$. L'état du système est décrit par un **vecteur unitaire** $\ket{\psi} \in \mathcal{H}$ (rayon projectif).

Pour un qubit : $\mathcal{H} = \mathbb{C}^2$, et tout état pur s'écrit :

$$
\ket{\psi} = \alpha \ket{0} + \beta \ket{1}, \quad |\alpha|^2 + |\beta|^2 = 1
$$

**Remarque :** La phase globale n'a pas d'importance physique : $\ket{\psi}$ et $e^{i\theta}\ket{\psi}$ représentent le même état. Seule la **phase relative** entre $\alpha$ et $\beta$ est observable.

---

## 2. Postulat 2 — Évolution

> L'évolution d'un système quantique isolé est décrite par une **transformation unitaire** :

$$
\ket{\psi(t)} = U(t, t_0) \ket{\psi(t_0)}, \quad U^\dagger U = I
$$

L'évolution continue est régie par l'**équation de Schrödinger** :

$$
i\hbar \frac{d}{dt} \ket{\psi(t)} = H \ket{\psi(t)}
$$

où $H$ est l'opérateur **Hamiltonien** (observable d'énergie).

Pour un Hamiltonien indépendant du temps :

$$
U(t) = e^{-iHt/\hbar}
$$

### 2.1 Exemple : Hamiltonien d'un qubit

Pour un qubit dans un champ magnétique suivant $z$ :

$$
H = \frac{\hbar\omega}{2} \sigma_z = \frac{\hbar\omega}{2} \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}
$$

L'évolution est :

$$
U(t) = e^{-i\omega t \sigma_z/2} = \begin{pmatrix} e^{-i\omega t/2} & 0 \\ 0 & e^{i\omega t/2} \end{pmatrix}
$$

Un état $\ket{\psi(0)} = \alpha\ket{0} + \beta\ket{1}$ évolue en :

$$
\ket{\psi(t)} = \alpha e^{-i\omega t/2}\ket{0} + \beta e^{i\omega t/2}\ket{1}
$$

---

## 3. Postulat 3 — Mesure (projective)

> Une **mesure projective** est décrite par un ensemble d'opérateurs de projection $\{P_m\}$ tels que $\sum_m P_m = I$. La probabilité d'obtenir le résultat $m$ est :

$$
p(m) = \bra{\psi} P_m \ket{\psi}
$$

> Après la mesure, l'état du système est **projeté** :

$$
\ket{\psi'} = \frac{P_m \ket{\psi}}{\sqrt{p(m)}}
$$

### 3.1 Mesure dans la base $Z$

Les projecteurs sont $P_0 = \ket{0}\bra{0}$, $P_1 = \ket{1}\bra{1}$.

Pour $\ket{\psi} = \alpha\ket{0} + \beta\ket{1}$ :

- $p(0) = |\alpha|^2$, l'état devient $\ket{0}$
- $p(1) = |\beta|^2$, l'état devient $\ket{1}$

### 3.2 Principe de Born

> La probabilité de mesurer un état $\ket{\psi}$ dans l'état $\ket{\phi}$ est $|\braket{\phi}{\psi}|^2$.

---

## 4. Postulat 4 — Systèmes composites

> L'espace d'état d'un système composé est le **produit tensoriel** des espaces de ses sous-systèmes :

$$
\mathcal{H}_{AB} = \mathcal{H}_A \otimes \mathcal{H}_B
$$

Pour un système à $n$ qubits : $\dim(\mathcal{H}) = 2^n$.

---

## 5. La sphère de Bloch

### 5.1 Paramétrisation

Tout état pur à un qubit peut s'écrire :

$$
\ket{\psi} = \cos\frac{\theta}{2} \ket{0} + e^{i\phi} \sin\frac{\theta}{2} \ket{1}
$$

avec :
- $0 \leq \theta \leq \pi$ (colatitude)
- $0 \leq \phi < 2\pi$ (longitude)

Le vecteur de Bloch associé est :

$$
\vec{r} = (\sin\theta\cos\phi,\; \sin\theta\sin\phi,\; \cos\theta)
$$

### 5.2 Points remarquables

| État | $\theta$ | $\phi$ | Vecteur de Bloch |
|------|----------|--------|-------------------|
| $\ket{0}$ | $0$ | — | $(0,0,1)$ |
| $\ket{1}$ | $\pi$ | — | $(0,0,-1)$ |
| $\ket{+} = (\ket{0}+\ket{1})/\sqrt{2}$ | $\pi/2$ | $0$ | $(1,0,0)$ |
| $\ket{-} = (\ket{0}-\ket{1})/\sqrt{2}$ | $\pi/2$ | $\pi$ | $(-1,0,0)$ |
| $\ket{+i} = (\ket{0}+i\ket{1})/\sqrt{2}$ | $\pi/2$ | $\pi/2$ | $(0,1,0)$ |

### 5.3 Visualisation QuTiP

```python
import qutip as qt
import matplotlib.pyplot as plt

# États sur la sphère de Bloch
bloch = qt.Bloch()

# États à visualiser
ket0 = qt.basis(2, 0)
ket1 = qt.basis(2, 1)
ket_plus = (ket0 + ket1).unit()
ket_minus = (ket0 - ket1).unit()
ket_plus_i = (ket0 + 1j * ket1).unit()

for state, label, color in [
    (ket0, "|0⟩", "r"),
    (ket1, "|1⟩", "b"),
    (ket_plus, "|+⟩", "g"),
    (ket_minus, "|-⟩", "orange"),
    (ket_plus_i, "|+i⟩", "purple"),
]:
    bloch.add_states(state)

bloch.show()
```

---

## 6. Évolution unitaire sur la sphère de Bloch

### 6.1 Rotation autour d'un axe

La porte $R_x(\theta) = e^{-i\theta X/2}$ fait tourner l'état d'un angle $\theta$ autour de l'axe $x$.

```python
import numpy as np

# Porte de rotation autour de x
theta = np.pi / 2
Rx = (-1j * theta * qt.sigmax() / 2).expm()

# État initial |0⟩
psi0 = qt.basis(2, 0)
psi_final = Rx * psi0
print("Rx(π/2)|0⟩ =", psi_final)
```

### 6.2 Code complet

```python
import numpy as np
import qutip as qt

# Simulation de l'évolution sous H = ω σ_z / 2
omega = 1.0
H = omega / 2 * qt.sigmaz()
psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()  # |+⟩

tlist = np.linspace(0, 4 * np.pi, 100)
result = qt.sesolve(H, psi0, tlist)

# Visualisation
bloch = qt.Bloch()
bloch.add_states(result.states[::10])
bloch.show()

# Probabilité de mesurer |+⟩ en fonction du temps
p_plus = [abs((psi_plus.dag() * state).full()[0, 0]) ** 2
          for state in result.states]
```

---

## 7. Résumé des postulats

| Postulat | Énoncé | Formule |
|----------|--------|---------|
| **1. État** | Vecteur unitaire dans $\mathcal{H}$ | $\|\ket{\psi}\| = 1$ |
| **2. Évolution** | Transformation unitaire | $\ket{\psi(t)} = U\ket{\psi_0}$ |
| **3. Mesure** | Projection probabiliste | $p(m) = \bra{\psi}P_m\ket{\psi}$ |
| **4. Composition** | Produit tensoriel | $\mathcal{H}_{AB} = \mathcal{H}_A \otimes \mathcal{H}_B$ |

---

## Exercices

1. Soit $\ket{\psi} = \frac{1}{\sqrt{3}}\ket{0} + \sqrt{\frac{2}{3}}\ket{1}$. Quelles sont les probabilités de mesurer $0$ et $1$ dans la base $Z$ ?
2. Montrer que $\ket{+} = (\ket{0}+\ket{1})/\sqrt{2}$ est un état propre de $X$ avec valeur propre $+1$.
3. Calculer la probabilité de mesurer $\ket{+}$ pour l'état $\ket{\psi} = \sqrt{0.8}\ket{0} + \sqrt{0.2}\ket{1}$.
4. Implémenter l'évolution d'un qubit sous $H = \omega(\sigma_x + \sigma_z)/2$ et visualiser la trajectoire sur la sphère de Bloch.
5. Démontrer que la mesure projective est idempotente : $P_m^2 = P_m$.
