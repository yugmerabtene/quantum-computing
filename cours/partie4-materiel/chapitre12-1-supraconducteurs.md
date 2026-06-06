# Chapitre 12.1 — Qubits supraconducteurs

## Ce que vous allez apprendre

- Comprendre pourquoi un circuit électrique refroidi à -273°C peut se comporter comme un qubit
- Maîtriser l'Hamiltonien d'un transmon et le concept crucial d'anharmonicité
- Analyser l'architecture de grille de couplage des processeurs IBM Condor (433 qubits) et Google Willow (105 qubits)
- Simuler un transmon réaliste avec QuTiP et extraire ses fréquences de résonance
- Identifier les trois ennemis mortels : décohérence, diaphonie (crosstalk) et leakage

---

## Motivation

**Le problème concret.** Dans un fil de cuivre ordinaire, les électrons bumpent contre les atomes du métal : c'est la résistance électrique, qui produit de la chaleur. Imaginez maintenant un métal refroidi à -273.1°C (quelques millikelvins au-dessus du zéro absolu). Soudain, les électrons se mettent à former des **paires de Cooper** et circulent sans aucune résistance : c'est la **supraconductivité**.

**Le lien avec les qubits.** Un circuit LC classique (inductance + condensateur) oscille à une fréquence bien définie, mais ses niveaux d'énergie sont **équidistants** — comme les barreaux d'une échelle régulière. Impossible d'isoler deux niveaux pour en faire un qubit : si vous envoyez une impulsion pour faire $|0\rangle \to |1\rangle$, vous excitez aussi $|1\rangle \to |2\rangle$, $|2\rangle \to |3\rangle$, etc.

**La solution.** Remplacer l'inductance classique par une **jonction Josephson** — un isolant ultra-fin entre deux supraconducteurs. Cet élément introduit une **non-linéarité** : les barreaux de l'échelle ne sont plus réguliers. On peut alors isoler les deux premiers barreaux ($|0\rangle$ et $|1\rangle$) pour former un qubit.

**Comparaison avec les autres plateformes.** Les supraconducteurs sont les qubits les plus matures industriellement (IBM, Google, Rigetti). Leur force : fabrication avec des techniques de micro-électronique éprouvées. Leur faiblesse : des temps de cohérence courts ($T_2 \sim 100$ µs) comparés aux ions piégés ($T_2 > 10$ s).

---

## Idée principale

Imaginez une balançoire. Si vous la poussez toujours au bon moment (sa fréquence de résonance), l'amplitude augmente. Un circuit LC, c'est pareil : il oscille à sa fréquence $\omega_0 = 1/\sqrt{LC}$.

Mais cette balançoire est **parfaitement régulière** : chaque oscillation prend exactement le même temps, peu importe l'amplitude. Les niveaux d'énergie sont donc régulièrement espacés.

Maintenant, remplacez la chaîne de la balançoire par un **élastique non-linéaire** : plus vous tirez fort, plus l'élastique se raidit (ou se relâche). La fréquence dépend maintenant de l'amplitude ! C'est exactement ce que fait la jonction Josephson : elle rend la fréquence dépendante du niveau d'énergie. La transition $|0\rangle \to |1\rangle$ a une fréquence légèrement différente de $|1\rangle \to |2\rangle$. Cette différence s'appelle l'**anharmonicité** $\alpha$, et c'est elle qui permet de cibler sélectivement la transition $|0\rangle \leftrightarrow |1\rangle$.

---

## Contenu du cours

### Section 1 : Du circuit LC au transmon

#### 1.1 Circuit LC quantique — l'oscillateur harmonique

Un circuit LC (inductance $L$, capacité $C$) est l'analogue électrique d'un ressort mécanique. L'énergie se balance entre le condensateur (énergie électrique) et l'inductance (énergie magnétique), exactement comme un pendule balance entre énergie cinétique et potentielle.

En mécanique quantique, ce circuit devient un **oscillateur harmonique quantique** :

$$
H_{\text{LC}} = \frac{Q^2}{2C} + \frac{\Phi^2}{2L}, \quad [\Phi, Q] = i\hbar
$$

**Signification physique :**
- $Q$ = charge électrique sur le condensateur (analogue de la quantité de mouvement $p$)
- $\Phi$ = flux magnétique à travers l'inductance (analogue de la position $x$)
- Le commutateur $[\Phi, Q] = i\hbar$ dit que charge et flux sont des variables conjuguées, comme $x$ et $p$

**Conséquence :** Les niveaux d'énergie sont $E_n = \hbar\omega_0(n + 1/2)$ avec $\omega_0 = 1/\sqrt{LC}$. Ils sont **équidistants** : $E_1 - E_0 = E_2 - E_1 = \hbar\omega_0$.

> **Exemple numérique :** Pour $L = 10$ nH et $C = 1 pF$ : $\omega_0/(2\pi) = 1/(2\pi\sqrt{LC}) \approx 5.03$ GHz. C'est typiquement la fréquence de travail d'un qubit supraconducteur.

#### 1.2 La jonction Josephson — la non-linéarité magique

La jonction Josephson est une sandwich : supraconducteur / isolant ultra-fin (~2 nm) / supraconducteur. Les paires de Cooper traversent l'isolant par effet tunnel.

Les deux **relations de Josephson** gouvernent ce composant :

$$
I = I_c \sin\delta, \quad V = \frac{\hbar}{2e} \frac{d\delta}{dt}
$$

**Signification physique :**
- $\delta$ = différence de phase supraconductrice entre les deux côtés de la jonction
- $I_c$ = courant critique : le courant maximum que la jonction peut supporter sans dissiper
- La première équation dit que le courant dépend **sinusoïdalement** de la phase — c'est cette non-linéarité qui nous intéresse !

L'énergie stockée dans la jonction est :

$$
E_J = -E_J^0 \cos\delta, \quad E_J^0 = \frac{\hbar I_c}{2e}
$$

**Signification physique :** $E_J^0$ est l'échelle d'énergie de la jonction. Contrairement à l'inductance qui stocke l'énergie de façon quadratique ($\Phi^2/2L$), la jonction la stocke de façon **cosinusoïdale** — d'où la non-linéarité.

> **Exemple numérique :** Pour $I_c = 100$ nA : $E_J^0/(2\pi\hbar) = I_c \cdot \Phi_0/(2\pi) \approx 20$ GHz, où $\Phi_0 = h/(2e)$ est le quantum de flux.

#### 1.3 Le transmon : le qubit supraconducteur moderne

Le **transmon** (Koch et al., 2007) est le design dominant aujourd'hui. L'idée : rendre $E_J \gg E_C$ pour protéger le qubit du bruit de charge.

L'Hamiltonien complet s'écrit :

$$
H = 4E_C \hat{n}^2 - E_J \cos\hat{\delta}
$$

**Signification physique :**
- $\hat{n}$ = opérateur nombre de paires de Cooper (combien de paires ont traversé la jonction)
- $E_C = e^2/(2C_\Sigma)$ = énergie capacitive : le coût énergétique d'ajouter une paire de Cooper
- Le premier terme ($4E_C \hat{n}^2$) est l'énergie électrique du condensateur
- Le second terme ($-E_J \cos\hat{\delta}$) est l'énergie non-linéaire de la jonction

En développant le cosinus au second ordre (approximation proche du fond du puits), on obtient un oscillateur harmonique + correction :

$$
H \approx \hbar\omega_q a^\dagger a + \frac{\alpha}{2} a^\dagger a^\dagger a a
$$

avec :
- Fréquence du qubit : $\omega_q = \sqrt{8E_C E_J}/\hbar$
- Anharmonicité : $\alpha = -E_C$ (toujours négative !)

**Signification physique de l'anharmonicité :**

$$
\alpha = (E_{12} - E_{01}) / \hbar
$$

- $E_{01}$ = énergie pour passer de $|0\rangle$ à $|1\rangle$
- $E_{12}$ = énergie pour passer de $|1\rangle$ à $|2\rangle$
- $\alpha < 0$ signifie que $E_{12} < E_{01}$ : la transition vers $|2\rangle$ est à **plus basse fréquence** que $|0\rangle \to |1\rangle$

> **Exemple numérique :** Avec $E_J/(2\pi\hbar) = 15$ GHz et $E_C/(2\pi\hbar) = 300$ MHz :
> - $\omega_q/(2\pi) = \sqrt{8 \times 300 \times 15000} \approx 5.48$ GHz
> - $\alpha/(2\pi) = -300$ MHz
> - La transition $|1\rangle \to |2\rangle$ est à $5.48 - 0.30 = 5.18$ GHz
> - Un pulse micro-onde à 5.48 GHz excite $|0\rangle \to |1\rangle$ sans exciter $|1\rangle \to |2\rangle$ (car 300 MHz de séparation)

---

### Section 2 : Architectures de processeurs réels

#### 2.1 IBM Condor (433 qubits, 2023)

IBM Condor utilise une **grille heavy-hexagonale** — un motif en nid d'abeille où chaque qubit a au plus 3 voisins.

**Pourquoi cette géométrie bizarre ?** Dans une grille carrée, chaque qubit a 4 voisins. Le problème : les qubits non-adjacents mais proches subissent de la **diaphonie** (crosstalk). La grille hexagonale réduit le nombre de voisins et donc la diaphonie.

Caractéristiques réelles :
- Fréquence de travail : 4–5 GHz
- $T_1 \sim 200\,\mu$s (temps de relaxation énergétique)
- $T_2 \sim 100\,\mu$s (temps de décohérence)
- Fidélité porte 1 qubit : $> 99.9\%$
- Fidélité porte 2 qubits : $> 99\%$

#### 2.2 Google Willow (105 qubits, 2024)

Google Willow utilise une **grille rectangulaire** avec une innovation majeure : les **coupleurs accordables** (tunable couplers).

**L'analogie :** Imaginez deux pendules reliés par un ressort. Si le ressort est rigide, les pendules échangent toujours de l'énergie. Si vous pouvez **ajuster la raideur du ressort** en temps réel (le rendre mou ou rigide), vous contrôlez quand les pendules interagissent. C'est exactement ce que fait un coupleur accordable : il permet de connecter/déconnecter dynamiquement deux qubits.

Résultats remarquables :
- $T_1 \sim 350\,\mu$s (record pour des qubits de grille)
- Fidélité porte 2 qubits : $99.97\%$
- Lecture : $99.9\%$ en $1\,\mu$s
- **Démonstration historique** : réduction exponentielle des erreurs sous le seuil de correction

$$
\text{Erreur logique} \propto \left(\frac{p}{p_{\text{th}}}\right)^{\lfloor d/2 \rfloor}
$$

**Signification physique :**
- $p$ = taux d'erreur physique par porte
- $p_{\text{th}}$ = seuil de correction d'erreur (typiquement ~1%)
- $d$ = distance du code de surface
- Quand $p < p_{\text{th}}$, l'erreur logique décroît **exponentiellement** avec la distance du code

> **Exemple numérique :** Si $p = 0.1\%$, $p_{\text{th}} = 1\%$, $d = 5$ : Erreur logique $\propto (0.1)^{2} = 0.01$. Avec $d = 7$ : $(0.1)^3 = 0.001$. Chaque incrément de $d$ divise l'erreur par 10.

---

### Section 3 : Grille de couplage et diaphonie

#### 3.1 Hamiltonien de la grille

Pour un processeur à $N$ qubits couplés à leurs voisins :

$$
H = \sum_{i=1}^N \hbar\omega_i a_i^\dagger a_i + \sum_{\langle i,j \rangle} g_{ij}(a_i^\dagger a_j + a_i a_j^\dagger)
$$

**Signification physique :**
- Premier terme : chaque qubit oscille à sa propre fréquence $\omega_i$
- Second terme : les qubits voisins échangent des excitations avec une force $g_{ij}$
- $a_i^\dagger a_j$ = « détruire une excitation sur le qubit $j$ et la créer sur le qubit $i$ » — c'est un échange d'énergie

#### 3.2 La diaphonie (crosstalk) — le problème n°1

La diaphonie, c'est quand une opération destinée à un qubit affecte accidentellement ses voisins. Il y en a trois types :

- **ZZ-crosstalk** : l'état d'un qubit décale la fréquence de son voisin (comme deux pendules couplés qui modifient mutuellement leur fréquence)
- **Readout crosstalk** : la mesure d'un qubit perturbe ses voisins
- **Control crosstalk** : un pulse micro-onde destiné à un qubit « déborde » sur ses voisins

$$
\Delta\omega_i = \sum_{j \neq i} \zeta_{ij} \langle Z_j \rangle
$$

**Signification physique :** $\zeta_{ij}$ est le coefficient de diaphonie entre qubits $i$ et $j$. Typiquement 10–100 kHz. $\langle Z_j \rangle = \pm 1$ selon que le qubit voisin est dans $|0\rangle$ ou $|1\rangle$.

> **Exemple numérique :** Si $\zeta_{12} = 20$ kHz et le qubit 2 est dans $|1\rangle$ ($\langle Z_2 \rangle = -1$), la fréquence du qubit 1 est décalée de $-20$ kHz. Sur un pulse de 50 ns, cela accumule une erreur de phase de $2\pi \times 20 \times 10^3 \times 50 \times 10^{-9} \approx 0.006$ rad — petit mais non négligeable sur des milliers de portes.

---

## Exemple guidé

**Problème :** Calculer les propriétés d'un transmon avec $E_J/(2\pi\hbar) = 15$ GHz et $E_C/(2\pi\hbar) = 300$ MHz.

**Étape 1 — Fréquence du qubit :**
$$\omega_q/(2\pi) = \sqrt{8 \times E_C \times E_J}/(2\pi\hbar) = \sqrt{8 \times 0.3 \times 15} = \sqrt{36} = 6.0 \text{ GHz}$$

**Étape 2 — Anharmonicité :**
$$\alpha/(2\pi) = -E_C/(2\pi\hbar) = -300 \text{ MHz}$$

**Étape 3 — Fréquences de transition :**
- $|0\rangle \to |1\rangle$ : $\nu_{01} = 6.0$ GHz
- $|1\rangle \to |2\rangle$ : $\nu_{12} = 6.0 - 0.3 = 5.7$ GHz

**Étape 4 — Rapport $E_J/E_C$ :**
$$E_J/E_C = 15000/300 = 50$$

Ce rapport est typique d'un transmon (gamme 20–100). Plus il est grand, plus le qubit est protégé du bruit de charge, mais plus l'anharmonicité est petite (difficile d'adresser sélectivement).

**Étape 5 — Durée d'un pulse $\pi$ :**
Avec une amplitude de drive $\Omega/(2\pi) = 10$ MHz :
$$T_\pi = \pi/\Omega = 1/(2 \times 10 \text{ MHz}) = 50 \text{ ns}$$

---

## Implémentation Python

```python
# ============================================================
# Simulation QuTiP d'un transmon supraconducteur
# ============================================================
import numpy as np
import qutip as qt

# --- Paramètres physiques du transmon ---
E_J = 20.0   # Énergie de Josephson (GHz) : contrôle la non-linéarité
E_C = 0.25   # Énergie capacitive (GHz) : coût d'ajouter une paire de Cooper
# Rapport E_J/E_C = 80 : régime transmon (bien protégé du bruit de charge)
N = 6        # Nombre de niveaux conservés dans la troncature

# --- Opérateurs de base ---
n = qt.num(N)       # Opérateur nombre : compte les paires de Cooper
a = qt.destroy(N)   # Opérateur d'annihilation : détruit un quantum d'oscillation
adag = qt.create(N) # Opérateur de création : crée un quantum d'oscillation

# --- Hamiltonien du circuit LC (oscillateur harmonique) ---
# H_lin = 4*E_C*(n + 1/2) - E_J*cos(delta) ≈ quadratique en delta
# C'est l'approximation harmonique (sans anharmonicité)
H_lin = 4.0 * E_C * (adag * a + 0.5) - E_J * (a + adag) / 2.0

# --- Hamiltonien complet du transmon ---
# phi est l'opérateur de phase supraconductrice (sans dimension)
# phi = (a + a†) * (8*E_C/E_J)^(1/4) / sqrt(2)
# Le facteur (8*E_C/E_J)^(1/4) vient de la diagonalisation de l'oscillateur
phi = (a + adag) * (8.0 * E_C / E_J) ** 0.25 / np.sqrt(2.0)

# Développement du cosinus : cos(phi) ≈ 1 - phi²/2 + phi⁴/24 - ...
# On garde jusqu'à phi⁴ pour capturer la non-linéarité
H_transmon = 4.0 * E_C * n**2 - E_J * (1.0 - phi**2 / 2.0 + phi**4 / 24.0)

# On soustrait l'énergie du fond de puits pour normaliser
H_transmon = H_transmon - H_transmon[0, 0] * qt.identity(N)

# --- Diagonalisation : extraction des niveaux d'énergie ---
evals = H_transmon.eigenenergies()

# Fréquence du qubit : différence E_1 - E_0
omega_q = evals[1] - evals[0]

# Anharmonicité : différence entre (E_2 - E_1) et (E_1 - E_0)
# Si alpha < 0, la transition |1>→|2> est à plus basse fréquence que |0>→|1>
anharmonicity = (evals[2] - evals[1]) - (evals[1] - evals[0])

print(f"Frequence qubit omega_q/(2pi) = {omega_q / (2*np.pi):.4f}")
print(f"Anharmonicite alpha/(2pi) = {anharmonicity / (2*np.pi):.4f}")

# --- Spectre de résonance : on balaye la fréquence de drive ---
w = np.linspace(0.5 * omega_q, 1.5 * omega_q, 500)
H0 = H_transmon

# État initial : le qubit dans son état fondamental |0>
psi0 = qt.basis(N, 0)
d = qt.destroy(N)

# Pour chaque fréquence de drive, on simule l'évolution et on regarde
# si le qubit absorbe l'énergie (résonance)
spectrum = []
for wi in w:
    # Drive micro-onde : terme de couplage avec le champ externe
    H_drive = H0 + 0.01 * (d * np.exp(-1j * wi * 0.0) + adag * np.exp(1j * wi * 0.0))
    H_drive = H0 + 0.01 * (d + adag)
    # Simulation de l'évolution temporelle
    tlist = np.linspace(0, 200.0 / omega_q, 500)
    result = qt.mesolve(H0 + 0.01 * (d + adag), psi0, tlist, c_ops=[], e_ops=[d + adag])
    # La probabilité d'excitation est liée à l'amplitude <d + d†>
    prob = np.abs(result.expect[0]) ** 2
    spectrum.append(np.max(prob))

spectrum = np.array(spectrum)

# Détection des pics de résonance dans le spectre
from scipy.signal import find_peaks
peaks, _ = find_peaks(spectrum, height=0.5)
if len(peaks) > 0:
    print(f"Resonance ω/(2π) ≈ {w[peaks[0]] / (2*np.pi):.4f}")

print(f"Rapport E_J/E_C = {E_J/E_C:.1f}")
print(f"Taille du sous-espace : {N} niveaux")
```

### Simulation de la diaphonie sur une grille de 4 qubits

```python
# ============================================================
# Simulation de la diaphonie (crosstalk) sur 4 qubits couplés
# ============================================================
import numpy as np

N_qubits = 4
# Fréquences individuelles des 4 qubits (légèrement différentes pour les distinguer)
omega = np.array([5.0, 5.1, 4.9, 5.05])
g = 0.05  # Force de couplage entre voisins (GHz)

# Construction de la matrice Hamiltonienne de la grille
# Diagonale : fréquences propres de chaque qubit
H_qubits = np.diag(omega)
# Couplage entre qubits adjacents (chaîne linéaire ici)
for i in range(N_qubits - 1):
    H_qubits[i, i+1] = g    # Terme de couplage super-diagonal
    H_qubits[i+1, i] = g    # Terme de couplage sous-diagonal

# Diagonalisation pour trouver les modes propres du système couplé
evals, evecs = np.linalg.eigh(H_qubits)
print("Modes du systeme couple :")
for i in range(N_qubits):
    print(f"  ω_{i}/(2π) = {evals[i]:.4f} GHz")

# --- Matrice de coefficients de diaphonie ZZ ---
# zeta[i,j] = décalage de fréquence du qubit i causé par le qubit j
# Valeurs typiques : 5-20 MHz (ici en GHz)
zeta = np.array([
    [0.0, 0.02, 0.01, 0.005],
    [0.02, 0.0, 0.015, 0.008],
    [0.01, 0.015, 0.0, 0.012],
    [0.005, 0.008, 0.012, 0.0]
])

# États des qubits : +1 pour |0>, -1 pour |1> (valeurs propres de Z)
Z_states = np.array([[1], [-1], [-1], [1]])

# Calcul du décalage de fréquence pour chaque qubit
for i in range(N_qubits):
    shift = np.sum(zeta[i] * Z_states.flatten())
    print(f"ZZ-decalage qubit {i} : {shift:.4f} GHz")
```

### Simulation d'une porte iSWAP entre deux transmons

```python
# ============================================================
# Simulation d'une porte à deux qubits (iSWAP) avec QuTiP
# ============================================================
import numpy as np
import qutip as qt

# Dimensions des sous-espaces pour chaque transmon (troncature à 4 niveaux)
N1, N2 = 4, 4

# Opérateurs annihilation pour chaque qubit dans l'espace produit tensoriel
a1 = qt.tensor(qt.destroy(N1), qt.identity(N2))  # a ⊗ I
a2 = qt.tensor(qt.identity(N1), qt.destroy(N2))  # I ⊗ a

# --- Paramètres des deux transmons ---
omega1 = 5.0      # Fréquence du qubit 1 (GHz)
omega2 = 5.1      # Fréquence du qubit 2 (GHz) — légèrement différent
alpha1 = -0.3     # Anharmonicité du qubit 1 (GHz)
alpha2 = -0.3     # Anharmonicité du qubit 2 (GHz)
g_cpl = 0.05      # Force de couplage entre les deux qubits (GHz)

# Hamiltonien individuel de chaque transmon (oscillateur + anharmonicité)
H_single = omega1 * a1.dag() * a1 + alpha1/2 * a1.dag() * a1.dag() * a1 * a1
H_single += omega2 * a2.dag() * a2 + alpha2/2 * a2.dag() * a2.dag() * a2 * a2

# Hamiltonien de couplage : échange d'excitations entre qubits
# a1† a2 + a1 a2† = « swap » d'un quantum d'oscillation
H_cpl = g_cpl * (a1.dag() * a2 + a1 * a2.dag())
H_total = H_single + H_cpl

# État initial : |01> (qubit 1 dans |0>, qubit 2 dans |1>)
psi0 = qt.tensor(qt.basis(N1, 0), qt.basis(N2, 1))
tlist = np.linspace(0, 500, 1000)  # Temps de simulation (ns)

# On mesure la probabilité de trouver le système dans |10>
# C'est la porte iSWAP : |01> → |10>
result_swap = qt.mesolve(H_total, psi0, tlist, c_ops=[], e_ops=[
    qt.tensor(qt.projection(N1, 1, 1), qt.projection(N2, 0, 0))
])

P_swap = result_swap.expect[0]
t_opt = tlist[np.argmax(P_swap)]  # Temps optimal pour le swap complet
print(f"Temps optimal pour iSWAP : {t_opt:.2f} ns")
print(f"Probabilité max de swap : {np.max(P_swap):.4f}")

# --- Calcul de la fidélité de la porte iSWAP ---
def swap_fidelity(t, H, psi_t, target_state):
    # Évolution unitaire : U = exp(-iHt)
    U = (-1j * H * t).expm()
    psi_f = U * psi_t
    # Fidélité = |<cible|psi_final>|²
    return (target_state.dag() * psi_f).real

# État cible : |10> (l'excitation a été transférée)
target = qt.tensor(qt.basis(N1, 1), qt.basis(N2, 0))
fid_max = swap_fidelity(t_opt, H_total, psi0, target)
print(f"Fidélité de l'iSWAP au temps optimal : {fid_max:.6f}")

# --- Balayage de la force de couplage g ---
g_vals = np.linspace(0.01, 0.2, 20)
fidelities = []
for gtest in g_vals:
    Htest = H_single + gtest * (a1.dag() * a2 + a1 * a2.dag())
    evals = Htest.eigenenergies()
    gap = evals[1] - evals[0]
    t_swap_test = np.pi / (2 * gap)  # Temps de swap optimal = π/(2*gap)
    fid_test = swap_fidelity(t_swap_test, Htest, psi0, target)
    fidelities.append(fid_test)

for gv, fv in zip(g_vals, fidelities):
    print(f"g = {gv:.3f} : fidelite = {fv:.6f}")
```

### Simulation de la relaxation T1

```python
# ============================================================
# Simulation de la relaxation T1 d'un transmon
# T1 = temps caractéristique de décroissance |1> → |0>
# ============================================================
import numpy as np
import qutip as qt

N = 3           # 3 niveaux : |0>, |1>, |2>
a = qt.destroy(N)

# Hamiltonien du transmon : oscillateur + anharmonicité
H = 5.0 * a.dag() * a - 0.15 * a.dag() * a.dag() * a * a

T1 = 100.0  # Temps de relaxation T1 (en unités de temps arbitraires, typiquement ns)

# Opérateur de Lindblad pour la relaxation : sqrt(1/T1) * a
# Cela modélise la perte d'énergie vers l'environnement
c_ops = [np.sqrt(1.0 / T1) * a]

# État initial : |1> (premier état excité)
psi1 = qt.basis(N, 1)
rho1 = psi1 * psi1.dag()  # Matrice densité associée
tlist = np.linspace(0, 500, 200)

# Simulation de l'équation maîtresse de Lindblad
# On mesure les populations de |0>, |1>, |2> au cours du temps
result = qt.mesolve(H, rho1, tlist, c_ops=c_ops, e_ops=[
    qt.projection(N, 0, 0),  # Projecteur sur |0>
    qt.projection(N, 1, 1),  # Projecteur sur |1>
    qt.projection(N, 2, 2)   # Projecteur sur |2>
])

P0, P1, P2 = result.expect
print(f"Population |0> a t=0 : {P0[0]:.4f}")
print(f"Population |0> a t=T1 : {P0[np.argmin(np.abs(tlist - T1))]:.4f}")
print(f"T1 extrait : {tlist[np.argmin(np.abs(P1 - 0.5))]:.2f}")
```

### Simulation du leakage vers |2>

```python
# ============================================================
# Simulation du leakage : la population qui fuit vers |2>
# ============================================================
import numpy as np
import qutip as qt

N = 4              # 4 niveaux pour capturer le leakage vers |2> et au-delà
a = qt.destroy(N)
adag = a.dag()

# Hamiltonien du transmon
H0 = 5.0 * adag * a - 0.15 * adag * adag * a * a

# État initial : |1> (on veut faire une rotation vers |0>)
psi0 = qt.basis(N, 1)
Omega_drive = 0.1   # Amplitude du drive micro-onde (GHz)
omega_drive = 4.85  # Fréquence du drive (proche de la transition |0>→|1>)
T_gate = 50.0       # Durée de la porte (ns)
tlist = np.linspace(0, T_gate, 500)

# Drive micro-onde : oscillation à la fréquence omega_drive
H_drive_func = lambda t, args: Omega_drive * (a * np.exp(1j * omega_drive * t) + adag * np.exp(-1j * omega_drive * t))

# Simulation sans dissipation pour voir le leakage pur
result_drive = qt.mesolve(H0, psi0, tlist, c_ops=[], e_ops=[
    qt.projection(N, 0, 0),  # Population de |0>
    qt.projection(N, 1, 1),  # Population de |1>
    qt.projection(N, 2, 2)   # Population de |2> (leakage !)
], args={})

P0_d, P1_d, P2_d = result_drive.expect
leakage_max = np.max(P2_d)
print(f"Leakage maximal vers |2> : {leakage_max:.4f}")

# Balayage de la fréquence de drive pour trouver les zones de leakage
omega_scan = np.linspace(4.5, 5.5, 100)
leakages = []
for wd in omega_scan:
    # Drive à fréquence fixe (approximation)
    H_drive = H0 + Omega_drive * (a * np.exp(1j * wd * 0) + adag * np.exp(-1j * wd * 0))
    r = qt.mesolve(H_drive, psi0, tlist, c_ops=[], e_ops=[qt.projection(N, 2, 2)])
    leakages.append(np.max(r.expect[0]))

print(f"Leakage minimal : {np.min(leakages):.4f} a ω_drive = {omega_scan[np.argmin(leakages)]:.3f}")
```

---

## Comparaison des technologies supraconducteurs

| Critère | IBM Condor | Google Willow | Rigetti Ankaa-2 |
|---------|-----------|--------------|-----------------|
| **Nombre de qubits** | 433 | 105 | 84 |
| **Topologie** | Heavy-hex | Grille rectangulaire | Grille octagonale |
| **Couplage** | Fixe | Accordable (tunable) | Fixe |
| **T1** | ~200 µs | ~350 µs | ~50 µs |
| **T2** | ~100 µs | ~350 µs | ~30 µs |
| **Fidélité 1Q** | >99.9% | >99.9% | >99.5% |
| **Fidélité 2Q** | >99% | 99.97% | >99% |
| **Connectivité** | 3 voisins | 4 voisins | 3 voisins |
| **Point fort** | Scale, écosystème | Correction d'erreur | Accès cloud |
| **Point faible** | Crosstalk, T1 limité | Peu de qubits | Cohérence courte |

---

## À retenir

1. **Un transmon est un oscillateur non-linéaire** : la jonction Josephson remplace l'inductance et introduit l'anharmonicité nécessaire pour isoler deux niveaux.

2. **L'anharmonicité $\alpha = -E_C$** est le paramètre clé : elle permet d'adresser sélectivement la transition $|0\rangle \leftrightarrow |1\rangle$. Plus $E_J/E_C$ est grand, plus le qubit est protégé du bruit de charge, mais plus $\alpha$ est petit.

3. **Le compromis fondamental** : $E_J/E_C \sim 50$ est un bon équilibre entre protection contre le bruit (grand $E_J/E_C$) et adressabilité (grande anharmonicité).

4. **La diaphonie (crosstalk)** est l'ennemi n°1 des processeurs denses. Les coupleurs accordables (Google Willow) permettent de la réduire en déconnectant les qubits quand ils n'interagissent pas.

5. **Le leakage** vers $|2\rangle$ est une source d'erreur spécifique aux supraconducteurs : le transmon n'est pas un vrai système à 2 niveaux. Les pulses de forme optimisée (DRAG) réduisent ce problème.

6. **Le scaling** est le défi majeur : IBM vise >100 000 qubits physiques d'ici 2033, mais le câblage, la dissipation thermique et la calibration deviennent exponentiellement difficiles.

7. **La correction d'erreur** avec les codes de surface nécessite typiquement 1000 qubits physiques par qubit logique — d'où l'objectif de >1 million de qubits physiques pour un calculateur utile.

---

## Pièges à éviter

1. **Confondre $T_1$ et $T_2$** : $T_1$ est le temps de relaxation énergétique ($|1\rangle \to |0\rangle$), $T_2$ est le temps de décohérence de phase. On a toujours $T_2 \leq 2T_1$. Un qubit peut avoir $T_1$ long mais $T_2$ court si le bruit de phase domine.

2. **Penser que l'anharmonicité est positive** : $\alpha = -E_C < 0$. La transition $|1\rangle \to |2\rangle$ est à PLUS BASSE fréquence que $|0\rangle \to |1\rangle$. C'est l'inverse d'un oscillateur mécanique durci.

3. **Confondre fréquence du qubit et fréquence de résonance du circuit** : $\omega_q = \sqrt{8E_C E_J}/\hbar$ n'est PAS la même chose que $\omega_0 = 1/\sqrt{LC}$. Le transmon a une fréquence modifiée par la non-linéarité.

4. **Oublier que le transmon a plus de 2 niveaux** : En simulation, tronquer à 2 niveaux donne des résultats incorrects pour les portes rapides ou les drives forts. Toujours garder au moins 3-4 niveaux.

5. **Croire que la fidélité de porte 2Q de 99.97% est « parfaite »** : Cela signifie 3 erreurs pour 10 000 portes. Pour un algorithme de 1 million de portes, cela fait 300 erreurs — d'où la nécessité absolue de la correction d'erreur.

---

## Exercices

### Niveau 1 — Application directe

1. **Transmon basique** : Calculer $\omega_q/(2\pi)$ et $\alpha/(2\pi)$ pour un transmon avec $E_J/(2\pi\hbar) = 20$ GHz et $E_C/(2\pi\hbar) = 250$ MHz. En déduire les fréquences des transitions $|0\rangle \to |1\rangle$ et $|1\rangle \to |2\rangle$.

2. **Temps de porte** : Un pulse micro-onde a une amplitude $\Omega/(2\pi) = 20$ MHz. Calculer la durée d'un pulse $\pi$ et d'un pulse $\pi/2$. Combien de portes peut-on enchaîner avant $T_2 = 100$ µs ?

3. **Exécuter le code QuTiP** : Reproduire la simulation du transmon et vérifier que les valeurs numériques sont cohérentes avec les formules analytiques.

### Niveau 2 — Compréhension

4. **Budget d'erreur** : Pour IBM Condor, construire un budget d'erreur détaillé incluant : erreurs de porte 1Q ($10^{-4}$), erreurs de porte 2Q ($10^{-3}$), leakage ($10^{-3}$), crosstalk ($10^{-3}$), erreur de lecture ($10^{-2}$). Estimer le nombre de portes correctes avant qu'une erreur ne survienne avec certitude.

5. **Porte iSWAP** : Simuler une porte iSWAP entre deux transmons couplés avec QuTiP. Tracer la fidélité en fonction du couplage $g$ et du temps d'interaction. Quel est le temps optimal ?

6. **Analyse de crosstalk** : Sur un réseau $3\times3$ avec ZZ-crosstalk réaliste ($\zeta \sim 20$ kHz), simuler l'erreur cumulée lors d'une séquence de 1000 portes sur un qubit central.

### Niveau 3 — Défi

7. **Optimisation DRAG** : Implémenter un pulse DRAG (Derivative Removal by Adiabatic Gate) pour réduire le leakage vers $|2\rangle$. Comparer la fidélité avec et sans correction DRAG pour un pulse $\pi$ de 20 ns.

8. **Comparaison d'architectures** : Comparer les architectures heavy-hexagonal (IBM) et grille rectangulaire (Google) en termes de : diamètre du graphe, nombre de SWAP nécessaires pour une porte CNOT entre qubits distants de 5, tolérance au crosstalk.

9. **Scaling du QEC** : Pour un code de surface de distance $d$ avec $p_{\text{phys}} = 10^{-3}$, calculer le nombre de qubits physiques nécessaires pour obtenir 100 qubits logiques avec une erreur logique $< 10^{-12}$. Combien de temps prend un calcul de $10^{12}$ portes logiques ?

---

## Pour aller plus loin

- **Koch, J.** et al. (2007). "Charge-insensitive qubit design derived from the Cooper pair box." *Phys. Rev. A*, 76, 042319. — L'article fondateur du transmon.
- **IBM Quantum** (2023). "IBM Quantum Condor: 433-qubit processor." *IBM Research*. — Spécifications du processeur Condor.
- **Google Quantum AI** (2024). "Quantum error correction below the surface code threshold." *Nature*, 636, 74–79. — Démonstration historique de la correction d'erreur sous le seuil avec Willow.
- **Kjaergaard, M.** et al. (2020). "Superconducting qubits: Current state of play." *Annual Review of Condensed Matter Physics*, 11, 369–395. — Revue complète et pédagogique.
- **Blais, A.** et al. (2021). "Circuit quantum electrodynamics." *Rev. Mod. Phys.*, 93, 025005. — La référence théorique sur le couplage circuit-QED.
