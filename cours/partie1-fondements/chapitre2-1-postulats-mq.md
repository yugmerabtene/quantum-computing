# Chapitre 2.1 — Postulats de la mécanique quantique

## Ce que vous allez apprendre

- Énoncer et comprendre les 4 postulats fondamentaux de la mécanique quantique
- Maîtriser la sphère de Bloch : une représentation géométrique magnifique d'un qubit
- Décrire l'évolution unitaire d'un état quantique (équation de Schrödinger)
- Calculer les probabilités de mesure et comprendre l'effondrement du vecteur d'état
- Simuler l'évolution d'un qubit avec QuTiP et visualiser sur la sphère de Bloch

---

## Motivation

Dans le chapitre 1.2, nous avons construit la boîte à outils mathématique : vecteurs, matrices, produits tensoriels. Mais comment utilise-t-on tout ça pour décrire un vrai système physique ? Quelles sont les **règles du jeu** de la mécanique quantique ?

La réponse tient en 4 postulats. C'est tout. De ces 4 règles simples découlent toute la richesse du monde quantique : superposition, intrication, incertitude, téléportation...

Ce chapitre est le fondement absolu. Les 4 postulats seront utilisés dans **chaque** chapitre qui suit. Les maîtriser maintenant vous évitera des confusions plus tard.

---

## Idée principale

Imaginez que vous jouez à un jeu de société avec des règles très simples, mais qui produisent des comportements émergents extraordinaires (comme les échecs : 6 types de pièces, quelques règles, et une complexité infinie).

Les 4 postulats sont les règles de base du « jeu » quantique :

1. **L'état** d'un système est un vecteur de norme 1 (comme une flèche de longueur 1)
2. **L'évolution** est une rotation de cette flèche (sans la déformer)
3. **La mesure** est un instantané : la flèche « saute » sur un axe, et vous lisez le résultat
4. **Les systèmes composés** combinent leurs flèches par produit tensoriel

Le plus surprenant ? Le postulat 3. En classique, mesurer ne change rien (regarder une pomme ne la modifie pas). En quantique, mesurer **change l'état** de façon irréversible. C'est ce qui rend le quantique si différent.

---

## Contenu du cours

### Section 1 : Postulat 1 — États

> **Postulat 1 :** À tout système physique isolé est associé un espace de Hilbert $\mathcal{H}$. L'état du système est décrit par un **vecteur unitaire** $\ket{\psi} \in \mathcal{H}$ (rayon projectif).

> **Intuition :** L'état d'un système, c'est comme la « carte d'identité complète » de ce système. Pour un qubit, cette carte d'identité est un vecteur dans $\mathbb{C}^2$.

Pour un qubit : $\mathcal{H} = \mathbb{C}^2$, et tout état pur s'écrit :

$$\ket{\psi} = \alpha \ket{0} + \beta \ket{1}, \quad |\alpha|^2 + |\beta|^2 = 1$$

où $\alpha, \beta \in \mathbb{C}$ sont les amplitudes complexes avec $|\alpha|^2 + |\beta|^2 = 1$ (normalisation)

> **Exemple numérique :** L'état $\ket{\psi} = \frac{1}{\sqrt{3}}\ket{0} + \sqrt{\frac{2}{3}}\ket{1}$ est valide car :
> $$|\alpha|^2 + |\beta|^2 = \frac{1}{3} + \frac{2}{3} = 1 \quad \checkmark$$

**Remarque importante :** La phase globale n'a pas d'importance physique : $\ket{\psi}$ et $e^{i\theta}\ket{\psi}$ représentent le même état. Seule la **phase relative** entre $\alpha$ et $\beta$ est observable.

> **Pourquoi ?** Parce que toutes les probabilités de mesure font intervenir $|\alpha|^2$ et $|\beta|^2$, et $|e^{i\theta}|^2 = 1$. La phase globale s'annule.

**Avez-vous compris ?**
- L'état $\ket{\psi} = 2\ket{0} + 3\ket{1}$ est-il un état valide ? (Non : $4 + 9 = 13 \neq 1$)
- Comment le normaliser ? ($\frac{2}{\sqrt{13}}\ket{0} + \frac{3}{\sqrt{13}}\ket{1}$)

---

### Section 2 : Postulat 2 — Évolution

> **Postulat 2 :** L'évolution d'un système quantique isolé est décrite par une **transformation unitaire** :

$$\ket{\psi(t)} = U(t, t_0) \ket{\psi(t_0)}, \quad U^\dagger U = I$$

> **Intuition :** L'évolution, c'est comme faire tourner une flèche dans l'espace. La rotation préserve la longueur (unitarité = conservation des probabilités). C'est réversible : si vous connaissez l'état final, vous pouvez retrouver l'état initial.

L'évolution continue est régie par l'**équation de Schrödinger** :

$$i\hbar \frac{d}{dt} \ket{\psi(t)} = H \ket{\psi(t)}$$

où $H$ est l'opérateur **Hamiltonien** (observable d'énergie).

> **Intuition :** L'Hamiltonien $H$ est au quantique ce que l'énergie est au classique : il dicte comment le système évolue dans le temps. C'est le « moteur » de l'évolution.

Pour un Hamiltonien indépendant du temps :

$$U(t) = e^{-iHt/\hbar}$$

#### Exemple : Hamiltonien d'un qubit

Pour un qubit dans un champ magnétique suivant $z$ :

$$H = \frac{\hbar\omega}{2} \sigma_z = \frac{\hbar\omega}{2} \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$$

> **Intuition :** C'est comme une toupie qui précesse autour d'un axe magnétique. La fréquence $\omega$ contrôle la vitesse de rotation.

L'évolution est :

$$U(t) = e^{-i\omega t \sigma_z/2} = \begin{pmatrix} e^{-i\omega t/2} & 0 \\ 0 & e^{i\omega t/2} \end{pmatrix}$$

> **Exemple numérique :** Pour $\omega = 1$, $t = \pi$ :
> $$U(\pi) = \begin{pmatrix} e^{-i\pi/2} & 0 \\ 0 & e^{i\pi/2} \end{pmatrix} = \begin{pmatrix} -i & 0 \\ 0 & i \end{pmatrix}$$

Un état $\ket{\psi(0)} = \alpha\ket{0} + \beta\ket{1}$ évolue en :

$$\ket{\psi(t)} = \alpha e^{-i\omega t/2}\ket{0} + \beta e^{i\omega t/2}\ket{1}$$

> **Exemple :** Si $\ket{\psi(0)} = \ket{+} = \frac{1}{\sqrt{2}}(\ket{0} + \ket{1})$, alors à $t = \pi/\omega$ :
> $$\ket{\psi(\pi/\omega)} = \frac{1}{\sqrt{2}}(e^{-i\pi/2}\ket{0} + e^{i\pi/2}\ket{1}) = \frac{1}{\sqrt{2}}(-i\ket{0} + i\ket{1}) = \frac{-i}{\sqrt{2}}(\ket{0} - \ket{1}) = -i\ket{-}$$
> À un facteur de phase globale près, l'état est devenu $\ket{-}$ !

---

### Section 3 : Postulat 3 — Mesure (projective)

> **Postulat 3 :** Une **mesure projective** est décrite par un ensemble d'opérateurs de projection $\{P_m\}$ tels que $\sum_m P_m = I$. La probabilité d'obtenir le résultat $m$ est :

$$p(m) = \bra{\psi} P_m \ket{\psi}$$

> **Intuition :** Mesurer, c'est poser une question au système. Les projecteurs $P_m$ sont les « questions possibles ». La probabilité de chaque réponse dépend de l'état actuel.

> **Et après la mesure, l'état du système est projeté :**

$$\ket{\psi'} = \frac{P_m \ket{\psi}}{\sqrt{p(m)}}$$

> **Intuition :** Après la mesure, le système « oublie » sa superposition et se retrouve dans l'état correspondant au résultat. C'est l'effondrement du vecteur d'état.

#### 3.1 Mesure dans la base $Z$

Les projecteurs sont $P_0 = \ket{0}\bra{0}$, $P_1 = \ket{1}\bra{1}$.

Pour $\ket{\psi} = \alpha\ket{0} + \beta\ket{1}$ :

- $p(0) = |\alpha|^2$, l'état devient $\ket{0}$
- $p(1) = |\beta|^2$, l'état devient $\ket{1}$

> **Exemple numérique :** Pour $\ket{\psi} = \frac{1}{\sqrt{3}}\ket{0} + \sqrt{\frac{2}{3}}\ket{1}$ :
> - $p(0) = |\frac{1}{\sqrt{3}}|^2 = \frac{1}{3} \approx 33\%$
> - $p(1) = |\sqrt{\frac{2}{3}}|^2 = \frac{2}{3} \approx 67\%$
> Si on mesure 1, l'état devient $\ket{1}$ (plus de superposition !).

#### 3.2 Principe de Born

> La probabilité de mesurer un état $\ket{\psi}$ dans l'état $\ket{\phi}$ est $|\braket{\phi}{\psi}|^2$.

> **Exemple :** Probabilité de mesurer $\ket{+}$ pour l'état $\ket{\psi} = \ket{0}$ :
> $$|\braket{+}{0}|^2 = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2}$$

**Avez-vous compris ?**
- Si $\ket{\psi} = \ket{1}$, quelle est la probabilité de mesurer 0 dans la base Z ? (Réponse : 0)
- Si on mesure $\ket{1}$ et qu'on obtient 1, quel est le nouvel état ? (Réponse : $\ket{1}$ — il ne change pas)

---

### Section 4 : Postulat 4 — Systèmes composites

> **Postulat 4 :** L'espace d'état d'un système composé est le **produit tensoriel** des espaces de ses sous-systèmes :

$$\mathcal{H}_{AB} = \mathcal{H}_A \otimes \mathcal{H}_B$$

Pour un système à $n$ qubits : $\dim(\mathcal{H}) = 2^n$.

> **Intuition :** Si Alice a un qubit ($\dim = 2$) et Bob a un qubit ($\dim = 2$), ensemble ils ont un espace de dimension $2 \times 2 = 4$. Pour 10 qubits : $2^{10} = 1024$. C'est cette croissance exponentielle qui donne sa puissance au quantique.

---

### Section 5 : La sphère de Bloch

#### 5.1 Paramétrisation

Tout état pur à un qubit peut s'écrire :

$$\ket{\psi} = \cos\frac{\theta}{2} \ket{0} + e^{i\phi} \sin\frac{\theta}{2} \ket{1}$$

avec :
- $0 \leq \theta \leq \pi$ (colatitude)
- $0 \leq \phi < 2\pi$ (longitude)

> **Intuition :** Au lieu de 2 nombres complexes ($\alpha, \beta$) avec une contrainte, on utilise 2 angles réels ($\theta, \phi$). L'état du qubit devient un **point sur une sphère** — la sphère de Bloch. C'est magnifique et très utile visuellement.

Le vecteur de Bloch associé est :

$$\vec{r} = (\sin\theta\cos\phi,\; \sin\theta\sin\phi,\; \cos\theta)$$

#### 5.2 Points remarquables

| État | $\theta$ | $\phi$ | Vecteur de Bloch |
|------|----------|--------|-------------------|
| $\ket{0}$ | $0$ | — | $(0,0,1)$ |
| $\ket{1}$ | $\pi$ | — | $(0,0,-1)$ |
| $\ket{+} = (\ket{0}+\ket{1})/\sqrt{2}$ | $\pi/2$ | $0$ | $(1,0,0)$ |
| $\ket{-} = (\ket{0}-\ket{1})/\sqrt{2}$ | $\pi/2$ | $\pi$ | $(-1,0,0)$ |
| $\ket{+i} = (\ket{0}+i\ket{1})/\sqrt{2}$ | $\pi/2$ | $\pi/2$ | $(0,1,0)$ |

> **Exemple :** L'état $\ket{+}$ correspond à $\theta = \pi/2, \phi = 0$ :
> $$\ket{+} = \cos(\pi/4)\ket{0} + e^{i \cdot 0}\sin(\pi/4)\ket{1} = \frac{1}{\sqrt{2}}\ket{0} + \frac{1}{\sqrt{2}}\ket{1} \quad \checkmark$$

```
                    SPHÈRE DE BLOCH
                 ═══════════════════════

                       |0⟩  (nord)
                         •
                       ╱ │ ╲
                      ╱  │  ╲
                     ╱   │   ╲
                    ╱    │    ╲
                   ╱     │     ╲
        |+⟩  •───────────┼─────────── •  |−⟩
                   ╲     │     ╱
                    ╲    │    ╱
                     ╲   │   ╱
                      ╲  │  ╱
                       ╲ │ ╱
                         •
                       |1⟩  (sud)

         θ = angle polaire (0 à π)
         φ = angle azimutal (0 à 2π)
```

#### 5.3 Visualisation QuTiP

```python
import qutip as qt
import matplotlib.pyplot as plt

# --- Création de la sphère de Bloch ---
bloch = qt.Bloch()

# --- Définition des états à visualiser ---
ket0 = qt.basis(2, 0)           # |0⟩ : pôle nord
ket1 = qt.basis(2, 1)           # |1⟩ : pôle sud
ket_plus = (ket0 + ket1).unit() # |+⟩ : sur l'axe x positif
ket_minus = (ket0 - ket1).unit()# |-⟩ : sur l'axe x négatif
ket_plus_i = (ket0 + 1j * ket1).unit()  # |+i⟩ : sur l'axe y positif

# --- Ajout de chaque état avec sa couleur ---
for state, label, color in [
    (ket0, "|0⟩", "r"),
    (ket1, "|1⟩", "b"),
    (ket_plus, "|+⟩", "g"),
    (ket_minus, "|-⟩", "orange"),
    (ket_plus_i, "|+i⟩", "purple"),
]:
    bloch.add_states(state)

# --- Affichage ---
bloch.show()
```

---

### Section 6 : Évolution unitaire sur la sphère de Bloch

#### 6.1 Rotation autour d'un axe

La porte $R_x(\theta) = e^{-i\theta X/2}$ fait tourner l'état d'un angle $\theta$ autour de l'axe $x$.

> **Intuition :** Sur la sphère de Bloch, appliquer une porte quantique = faire tourner le point représentant l'état. $R_x(\theta)$ est une rotation d'angle $\theta$ autour de l'axe horizontal $x$.

```python
import numpy as np
import qutip as qt

# --- Porte de rotation autour de l'axe x d'angle θ = π/2 ---
theta = np.pi / 2
# expm() calcule l'exponentielle de matrice : e^(-iθX/2)
Rx = (-1j * theta * qt.sigmax() / 2).expm()

# --- État initial |0⟩ (pôle nord) ---
psi0 = qt.basis(2, 0)

# --- Application de la rotation ---
psi_final = Rx * psi0
print("Rx(π/2)|0⟩ =", psi_final)
```

**Sortie attendue :**

```
Rx(π/2)|0⟩ = Quantum object: dims=[[2], [1]], shape=(2, 1), type='ket', dtype=Dense
Qobj data =
[[0.70710678+0.j        ]
 [0.        -0.70710678j]]
```

> **Interprétation :** $R_x(\pi/2)$ appliqué à $\ket{0}$ (pôle nord) donne un état sur l'équateur de la sphère de Bloch — un état avec des amplitudes égales en module mais avec une phase relative.

#### 6.2 Simulation complète de l'évolution

```python
import numpy as np
import qutip as qt

# --- Paramètres de l'Hamiltonien ---
# H = ω σ_z / 2 : qubit dans un champ magnétique selon z
omega = 1.0
H = omega / 2 * qt.sigmaz()

# --- État initial |+⟩ (sur l'axe x) ---
psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()  # |+⟩

# --- Grille de temps : de 0 à 4π, 100 points ---
tlist = np.linspace(0, 4 * np.pi, 100)

# --- Résolution de l'équation de Schrödinger ---
result = qt.sesolve(H, psi0, tlist)

# --- Visualisation sur la sphère de Bloch ---
# On affiche un point tous les 10 pas de temps
bloch = qt.Bloch()
bloch.add_states(result.states[::10])
bloch.show()

# --- Probabilité de mesurer |+⟩ en fonction du temps ---
psi_plus = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
p_plus = [abs((psi_plus.dag() * state).full()[0, 0]) ** 2
          for state in result.states]
```

> **Ce que fait ce code :**
> - Lignes 5-6 : on définit l'Hamiltonien $H = \frac{\omega}{2}\sigma_z$
> - Ligne 9 : l'état initial est $\ket{+}$, situé sur l'axe $x$ de la sphère
> - Lignes 12-13 : on résout l'équation de Schrödinger
> - Lignes 16-18 : on visualise la trajectoire sur la sphère de Bloch
> - Lignes 21-23 : on calcule la probabilité de retrouver $\ket{+}$ au cours du temps
>
> **Résultat physique :** Le vecteur de Bloch précesse autour de l'axe $z$, comme une toupie. La probabilité $p_+(t)$ oscille — ce sont les **oscillations de Rabi**.

---

## Exemple guidé

**Problème :** Un qubit est dans l'état $\ket{\psi} = \frac{1}{\sqrt{3}}\ket{0} + \sqrt{\frac{2}{3}}\ket{1}$.

**(a)** Quelles sont les probabilités de mesurer 0 et 1 dans la base Z ?

**Étape 1 :** Identifier les amplitudes : $\alpha = \frac{1}{\sqrt{3}}$, $\beta = \sqrt{\frac{2}{3}}$

**Étape 2 :** Vérifier la normalisation : $|\alpha|^2 + |\beta|^2 = \frac{1}{3} + \frac{2}{3} = 1$ ✓

**Étape 3 :** Calculer les probabilités :
- $p(0) = |\alpha|^2 = \frac{1}{3} \approx 33.3\%$
- $p(1) = |\beta|^2 = \frac{2}{3} \approx 66.7\%$

**(b)** Si on mesure et qu'on obtient 1, quel est le nouvel état ?

**Réponse :** L'état est projeté sur $\ket{1}$. Si on remesure immédiatement dans la base Z, on obtient 1 avec certitude (probabilité 100%).

**(c)** Représenter cet état sur la sphère de Bloch.

**Étape 1 :** Identifier $\theta$ : $\cos(\theta/2) = \frac{1}{\sqrt{3}}$, donc $\theta/2 = \arccos(1/\sqrt{3}) \approx 0.955$ rad, soit $\theta \approx 1.91$ rad ($\approx 109.5°$)

**Étape 2 :** Identifier $\phi$ : ici $\alpha$ et $\beta$ sont réels positifs, donc $\phi = 0$.

**Étape 3 :** Vecteur de Bloch : $\vec{r} = (\sin\theta, 0, \cos\theta) \approx (0.943, 0, -0.333)$

---

## Implémentation Python

### Résumé des postulats en code

```python
import numpy as np
import qutip as qt

# ============================================================
# POSTULAT 1 : État = vecteur unitaire dans H
# ============================================================
# Créer un état normalisé
alpha, beta = 1/np.sqrt(3), np.sqrt(2/3)
psi = alpha * qt.basis(2, 0) + beta * qt.basis(2, 1)
print("Postulat 1 - État |ψ⟩ :", psi)
print("  Norme =", psi.norm())  # Doit valoir 1.0

# ============================================================
# POSTULAT 2 : Évolution = transformation unitaire
# ============================================================
# Hamiltonien H = (ω/2) σ_z
omega = 1.0
H = omega / 2 * qt.sigmaz()
t = 2.0  # temps

# Calcul de U(t) = exp(-iHt/ℏ) avec ℏ = 1
U = (-1j * H * t).expm()
psi_evolved = U * psi
print("\nPostulat 2 - État après évolution :", psi_evolved)
print("  Norme =", psi_evolved.norm())  # Toujours 1.0 !

# ============================================================
# POSTULAT 3 : Mesure = projection probabiliste
# ============================================================
# Mesure dans la base Z : projecteurs P0 = |0⟩⟨0|, P1 = |1⟩⟨1|
P0 = qt.basis(2, 0) * qt.basis(2, 0).dag()
P1 = qt.basis(2, 1) * qt.basis(2, 1).dag()

# Probabilités
p0 = (psi.dag() * P0 * psi).real
p1 = (psi.dag() * P1 * psi).real
print(f"\nPostulat 3 - Probabilités : p(0) = {p0:.4f}, p(1) = {p1:.4f}")

# Après mesure (si résultat = 1)
psi_after = P1 * psi / np.sqrt(p1)
print("  État après mesure (résultat=1) :", psi_after)

# ============================================================
# POSTULAT 4 : Systèmes composites = produit tensoriel
# ============================================================
psi_A = qt.basis(2, 0)  # Qubit A dans |0⟩
psi_B = qt.basis(2, 1)  # Qubit B dans |1⟩
psi_AB = qt.tensor(psi_A, psi_B)  # État composite |01⟩
print("\nPostulat 4 - État composite |01⟩ :", psi_AB)
print("  Dimension :", psi_AB.shape)  # (4, 1)
```

**Sortie attendue :**

```
Postulat 1 - État |ψ⟩ : ...
  Norme = 1.0

Postulat 2 - État après évolution : ...
  Norme = 1.0

Postulat 3 - Probabilités : p(0) = 0.3333, p(1) = 0.6667
  État après mesure (résultat=1) : ...

Postulat 4 - État composite |01⟩ : ...
  Dimension : (4, 1)
```

---

## À retenir

1. **Postulat 1 (État)** : Un système quantique est décrit par un vecteur unitaire $\ket{\psi}$ dans un espace de Hilbert $\mathcal{H}$
2. **Postulat 2 (Évolution)** : L'évolution est unitaire : $\ket{\psi(t)} = U\ket{\psi_0}$ avec $U = e^{-iHt/\hbar}$
3. **Postulat 3 (Mesure)** : La mesure est projective et probabiliste : $p(m) = \bra{\psi}P_m\ket{\psi}$, et l'état s'effondre
4. **Postulat 4 (Composition)** : Les systèmes composites vivent dans un produit tensoriel : $\mathcal{H}_{AB} = \mathcal{H}_A \otimes \mathcal{H}_B$
5. **Sphère de Bloch** : Tout état d'un qubit correspond à un point sur une sphère, paramétré par $(\theta, \phi)$
6. **Phase globale** : $e^{i\theta}\ket{\psi}$ et $\ket{\psi}$ représentent le même état physique
7. **Mesure = irréversible** : Contrairement à l'évolution unitaire, la mesure ne peut pas être « défaite »

---

## Pièges à éviter

1. **Confondre évolution unitaire et mesure** — L'évolution (postulat 2) est réversible, déterministe, et préserve les superpositions. La mesure (postulat 3) est irréversible, probabiliste, et détruit les superpositions.

2. **Penser que $\theta$ va de 0 à $2\pi$** — Sur la sphère de Bloch, $\theta$ va de 0 à $\pi$ (pas $2\pi$), car le facteur $\theta/2$ dans $\cos(\theta/2)$ couvre déjà tous les états.

3. **Oublier le facteur $\frac{1}{2}$ dans les rotations** — $R_x(\theta) = e^{-i\theta X/2}$, pas $e^{-i\theta X}$. Il faut $4\pi$ (pas $2\pi$) pour revenir à l'identité !

4. **Croire que la mesure révèle un état préexistant** — Non ! Avant la mesure, le qubit n'est « ni 0 ni 1 ». C'est la mesure qui force le système à « choisir ».

5. **Confondre phase globale et phase relative** — La phase globale ($e^{i\theta}\ket{\psi}$) n'a aucun effet observable. La phase relative (entre $\alpha$ et $\beta$) est cruciale.

---

## Exercices

### Niveau 1 — Application directe

1. Soit $\ket{\psi} = \frac{1}{\sqrt{3}}\ket{0} + \sqrt{\frac{2}{3}}\ket{1}$. Quelles sont les probabilités de mesurer $0$ et $1$ dans la base $Z$ ?

2. Montrer que $\ket{+} = (\ket{0}+\ket{1})/\sqrt{2}$ est un état propre de $X$ avec valeur propre $+1$.
   *(Indice : calculez $X\ket{+}$ et vérifiez que c'est égal à $+1 \cdot \ket{+}$)*

3. Calculer la probabilité de mesurer $\ket{+}$ pour l'état $\ket{\psi} = \sqrt{0.8}\ket{0} + \sqrt{0.2}\ket{1}$.
   *(Indice : utilisez le principe de Born $|\braket{+}{\psi}|^2$)*

### Niveau 2 — Compréhension

4. Un qubit évolue sous $H = \frac{\hbar\omega}{2}\sigma_z$. Si l'état initial est $\ket{0}$, décrire l'état à tout instant $t$. Que remarquez-vous ?
   *(Indice : $\ket{0}$ est un état propre de $H$...)*

5. Montrer que la mesure projective est idempotente : $P_m^2 = P_m$.
   *(Indice : utilisez $P_m = \ket{m}\bra{m}$ et $\braket{m}{m} = 1$)*

6. Sur la sphère de Bloch, quelle porte correspond à une rotation de $\pi$ autour de l'axe $z$ ? Quel est son effet sur $\ket{+}$ ?

### Niveau 3 — Défi

7. Implémenter l'évolution d'un qubit sous $H = \omega(\sigma_x + \sigma_z)/2$ et visualiser la trajectoire sur la sphère de Bloch. Autour de quel axe le vecteur de Bloch précesse-t-il ?

8. Démontrer que deux mesures successives identiques donnent toujours le même résultat. (Formalisez avec les projecteurs.)

---

## Pour aller plus loin

- Nielsen & Chuang, *Quantum Computation and Quantum Information*, Ch. 2.2 — Les postulats en détail
- Video : [Bloch Sphere Explained](https://www.youtube.com/watch?v=OmvbqgKbDjk) — Visualisation intuitive
- QuTiP documentation : [Time evolution](https://qutip.org/docs/latest/guide/dynamics/dynamics.html) — Pour simuler des évolutions
