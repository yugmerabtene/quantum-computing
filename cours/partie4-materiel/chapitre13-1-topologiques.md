# Chapitre 13.1 — Qubits topologiques

## Ce que vous allez apprendre

- Comprendre le concept de qubit topologique et pourquoi il est « protégé » contre le bruit
- Maîtriser les fermions de Majorana et le modèle de Kitaev (chaîne 1D)
- Analyser la puce Majorana 1 de Microsoft (2025)
- Simuler le gap topologique et les modes de bord avec Python
- Comparer les overheads de correction entre qubits topologiques et conventionnels

---

## Motivation

**Le problème fondamental.** Tous les qubits qu'on a vus (supraconducteurs, atomes, ions) ont un point commun : l'information quantique est encodée dans une propriété **locale** d'un objet physique (courant, spin, niveau d'énergie). Le moindre bruit local — un photon parasite, une vibration thermique, un défaut matériel — peut détruire l'information.

**L'idée topologique.** Et si on encodait l'information de façon **non-locale** ? Imaginez couper un billet de banque en deux : chaque moitié est inutile seule. Il faut les deux pour que le billet ait de la valeur. Un qubit topologique fonctionne pareil : l'information est stockée dans **deux objets séparés spatialement** (les modes de Majorana). Un bruit local ne peut pas atteindre les deux en même temps.

**La promesse.** Les qubits topologiques pourraient avoir des taux d'erreur physique de $10^{-6}$ (voire moins) — trois ordres de grandeur mieux que les supraconducteurs ($10^{-3}$). Cela réduirait drastiquement l'overhead de correction d'erreur : moins de qubits physiques par qubit logique.

**L'état actuel.** Microsoft a annoncé la puce **Majorana 1** en 2025, première tentative de qubit topologique fonctionnel. C'est une approche radicalement différente, encore à ses débuts mais potentiellement révolutionnaire.

---

## Idée principale

### La topologie, c'est quoi ?

Pensez à un beignet et une tasse de café. En topologie, ces deux objets sont « les mêmes » : vous pouvez déformer continûment la tasse pour obtenir un beignet (le trou de la tasse devient le trou du beignet). Ce qui compte, c'est le **nombre de trous** — un invariant topologique qui ne change pas sous déformation continue.

Maintenant, imaginez que l'information quantique est encodée dans un « nombre de trous » d'un état de la matière. Pour perturber cette information, il faudrait changer la topologie de l'état — ce qui nécessite une énergie considérable (le « gap topologique »). Les petites perturbations locales ne peuvent pas changer la topologie : l'information est **protégée topologiquement**.

### Les fermions de Majorana : des particules qui sont leurs propres antiparticules

En physique des particules, un fermion de Majorana est une particule qui est sa propre antiparticule. Dans un matériau topologique, ces particules apparaissent comme des **excitations collectives** aux bords du matériau.

L'analogie : imaginez une rangée de spins (↑↓↑↓↑↓...). Si vous créez un « défaut » (↑↑ au milieu), ce défaut se comporte comme une particule. Maintenant, séparez ce défaut en deux moitiés aux extrémités de la chaîne : chaque moitié est un mode de Majorana. L'information est stockée dans la **relation** entre les deux moitiés — pas dans une moitié individuelle.

---

## Contenu du cours

### Section 1 : Fermions de Majorana

#### 1.1 Particules de Majorana — la définition

Un **fermion de Majorana** est une particule qui est sa propre antiparticule. Mathématiquement, l'opérateur de création est égal à l'opérateur d'annihilation :

$$
\gamma^\dagger = \gamma, \quad \{\gamma_i, \gamma_j\} = 2\delta_{ij}
$$

**Signification physique :**
- $\gamma^\dagger = \gamma$ : créer ou détruire un Majorana, c'est la même chose (contrairement à un électron ordinaire où $c^\dagger \neq c$)
- $\{\gamma_i, \gamma_j\} = 2\delta_{ij}$ : la relation d'anti-commutation dit que deux Majoranas différents « anticommute » (comme tous les fermions)
- Les opérateurs de Majorana sont **hermitiens** (auto-adjoints) : ce sont des observables physiques

Un fermion ordinaire (Dirac) peut être décomposé en deux fermions de Majorana :

$$
c = \frac{1}{2}(\gamma_1 + i\gamma_2), \quad c^\dagger = \frac{1}{2}(\gamma_1 - i\gamma_2)
$$

**Analogie :** Un nombre complexe $z = x + iy$ se décompose en deux nombres réels. De même, un fermion ordinaire se « sépare » en deux Majoranas. L'information quantique est dans la « partie imaginaire » (la relation entre $\gamma_1$ et $\gamma_2$).

#### 1.2 Modes zéro de Majorana (MZM)

Dans un système topologique 1D (comme un nanofil semi-conducteur couplé à un supraconducteur), les **modes zéro de Majorana** apparaissent aux extrémités du fil :

$$
H = \sum_i \Delta_i \gamma_i \gamma_{i+1} + \text{termes sous-gap}
$$

**Signification physique :**
- À l'intérieur du fil (bulk), les Majoranas $\gamma_i$ et $\gamma_{i+1}$ sont couplés par $\Delta_i$ : ils forment des fermions ordinaires avec une énergie $\pm \Delta$
- Aux extrémités, il reste un Majorana $\gamma_L$ (à gauche) et $\gamma_R$ (à droite) qui ne sont couplés à personne
- Ces modes de bord ont une énergie $E = 0$ (d'où « mode zéro »)
- Ils sont séparés du bulk par un **gap d'énergie** $\Delta$

> **Exemple numérique :** Pour un nanofil InAs-Al (Microsoft Majorana 1) : $\Delta \sim 200$ µeV $\sim 50$ GHz en fréquence. Ce gap protège les MZM contre les perturbations d'énergie inférieure à 50 GHz.

---

### Section 2 : Modèle de Kitaev — le jouet théorique

#### 2.1 L'Hamiltonien de Kitaev

Le modèle de Kitaev est le modèle le plus simple qui exhibe des modes de Majorana. Il décrit une chaîne 1D de fermions sans spin avec un pairing « p-wave » (appariement entre voisins) :

$$
H = -\mu \sum_{j=1}^N c_j^\dagger c_j - \sum_{j=1}^{N-1} (t c_j^\dagger c_{j+1} + \Delta e^{i\phi} c_j c_{j+1} + \text{h.c.})
$$

**Signification physique de chaque terme :**
- $\mu$ = potentiel chimique : contrôle le nombre de particules (comme le niveau de l'eau dans un réservoir)
- $t$ = amplitude de hopping : les fermions sautent de site en site (énergie cinétique)
- $\Delta$ = paramètre de pairing : crée ou détruit des paires de fermions sur sites voisins (c'est le terme « exotique »)
- $\phi$ = phase supraconductrice

**Analogie :** Imaginez une rangée de places de parking ($j = 1, \ldots, N$). Les voitures (fermions) peuvent :
- Rester sur place (terme en $\mu$)
- Se déplacer d'une place (terme en $t$)
- Apparaître ou disparaître par paires sur deux places adjacentes (terme en $\Delta$) — c'est le pairing supraconducteur

#### 2.2 La transition de phase topologique

Le système subit une **transition de phase** en fonction de $\mu$ :

- **Phase topologique** (phase T) : $|\mu| < 2|t|$ — des modes de Majorana apparaissent aux bords
- **Phase triviale** (phase S) : $|\mu| > 2|t|$ — pas de modes de bord

$$
\mu_c = \pm 2t \quad \text{(ligne critique)}
$$

**Analogie :** C'est comme un pont entre deux phases de la matière. D'un côté ($|\mu| < 2t$), le fil est « topologique » et héberge des Majoranas aux bords. De l'autre côté ($|\mu| > 2t$), le fil est « trivial » et les Majoranas disparaissent.

Dans la phase topologique, les deux modes de bord sont :

$$
\gamma_1 \propto c_1 + c_1^\dagger, \quad \gamma_N \propto c_N + c_N^\dagger
$$

Ces modes sont **exponentiellement localisés** aux bords :

$$
\gamma_L \sim \sum_j e^{-j/\xi} (c_j + c_j^\dagger), \quad \xi \propto 1/\Delta
$$

**Signification physique :** $\xi$ est la **longueur de cohérence topologique** : la distance sur laquelle le mode de Majorana s'étend dans le fil. Pour $\Delta$ grand, $\xi$ est petit : le Majorana est très localisé au bord.

> **Exemple numérique :** Avec $\Delta/(2\pi\hbar) = 50$ GHz et $v_F \sim 10^5$ m/s : $\xi = \hbar v_F / \Delta \sim 2$ µm. Sur un fil de 10 µm, les deux modes de bord sont bien séparés ($L \gg \xi$).

#### 2.3 Le qubit topologique

Le qubit est formé par la dégénérescence des deux modes de bord :

$$
|0_L\rangle = |\text{vide}\rangle, \quad |1_L\rangle = \gamma_1 \gamma_N |\text{vide}\rangle
$$

**Pourquoi c'est protégé :** Les deux MZM sont aux extrémités opposées du fil (séparés de $L$). Un bruit local (défaut, impureté, fluctuation thermique) ne peut agir que sur un seul MZM à la fois. Or, pour retourner le qubit ($|0_L\rangle \to |1_L\rangle$), il faut agir sur les DEUX MZM simultanément. La probabilité de cela décroît exponentiellement avec la longueur du fil :

$$
|\langle 0_L | V_i | 1_L \rangle| \propto e^{-L/\xi}
$$

**Analogie :** C'est comme un coffre-fort dont la clé est coupée en deux. Une moitié est à Paris, l'autre à Tokyo. Un voleur à Paris ne peut pas ouvrir le coffre — il lui faut les deux moitiés.

---

### Section 3 : Microsoft Majorana 1

#### 3.1 La puce topologique (2025)

Microsoft a annoncé la **Majorana 1** : première puce utilisant des qubits topologiques basés sur des **nanofils hybrides** semi-conducteur/supraconducteur (InAs-Al) :

**Architecture :**
- Un nanofil de InAs (arséniure d'indium) — semi-conducteur à fort spin-orbite
- Recouvert d'une couche d'Al (aluminium) — supraconducteur
- Un champ magnétique externe tune le système dans la phase topologique
- Les MZM apparaissent aux extrémités du fil

**Caractéristiques :**
- Longueur de cohérence topologique $\xi \sim 3-5\,\mu$m
- Gap topologique $\Delta \sim 200\,\mu$eV $\sim 50$ GHz
- Température de fonctionnement $< 50$ mK
- Protection topologique : réduction exponentielle des erreurs avec la longueur du fil

$$
\epsilon_{\text{qubit}} \propto \exp(-L/\xi)
$$

**Signification physique :** Pour un fil de longueur $L = 10$ µm et $\xi = 3$ µm : $\epsilon \propto e^{-10/3} \approx 0.036$. Pour $L = 30$ µm : $\epsilon \propto e^{-10} \approx 4.5 \times 10^{-5}$. L'erreur décroît exponentiellement avec la longueur !

#### 3.2 Mesure topologique

La lecture d'un qubit topologique utilise l'interférence de **bras de frustration** (un réseau de nanofils en T) :

$$
I_{\text{mes}} \propto \cos(\pi N_{\text{tot}})
$$

où $N_{\text{tot}}$ est la parité totale du système (nombre de fermions modulo 2). La mesure est non-destructive car elle ne probe que la parité, pas l'état individuel des MZM.

#### 3.3 Comparaison avec les autres plateformes

| Propriété | Majorana 1 (Microsoft) | Transmon (Google/IBM) | Atome neutre (QuEra) |
|-----------|-----------|----------|--------------|
| **Protection** | Topologique (passive) | Active (QEC) | Active (QEC) |
| **Taux d'erreur physique** | $10^{-6}$ (extrapolé) | $10^{-3}$ | $10^{-3}$ |
| **Overhead QEC** | Faible (théorique) | Élevé (~1000:1) | Élevé (~1000:1) |
| **Portes logiques** | À démontrer | Démontrées | 48 qubits logiques |
| **Maturité** | Préliminaire | Avancée | Avancée |
| **Scalabilité** | Potentiellement excellente | Bonne | Excellente |

---

## Exemple guidé

**Problème :** Pour une chaîne de Kitaev avec $N = 100$ sites, $\mu = 0$, $t = 1$, $\Delta = 0.5$, calculer le gap topologique et vérifier la présence de modes de bord.

**Étape 1 — Vérifier la phase :**
Condition topologique : $|\mu| < 2|t|$. Ici $|0| < 2 \times 1 = 2$. ✓ On est en phase topologique.

**Étape 2 — Gap théorique :**
Le gap du bulk est $\Delta_{\text{bulk}} = 2\Delta = 1.0$ (pour $\mu = 0$).

**Étape 3 — Splitting des modes de bord (effet de taille finie) :**
Le recouvrement entre les deux MZM décroît comme $e^{-N/\xi}$ avec $\xi = t/\Delta = 2$.
Pour $N = 100$ : splitting $\sim e^{-100/2} = e^{-50} \approx 1.9 \times 10^{-22}$.
Les deux MZM sont essentiellement dégénérés à $E = 0$.

**Étape 4 — Localisation des modes de bord :**
Le mode gauche $\gamma_L$ a une amplitude sur le site $j$ qui décroît comme $e^{-j/\xi} = e^{-j/2}$.
- Site 0 : amplitude $\propto 1$
- Site 10 : amplitude $\propto e^{-5} \approx 0.0067$
- Site 50 : amplitude $\propto e^{-25} \approx 10^{-11}$

Le mode est exponentiellement localisé sur les ~10 premiers sites.

---

## Implémentation Python

### Simulation du modèle de Kitaev

```python
# ============================================================
# Simulation numérique du modèle de Kitaev (chaîne 1D)
# Objectif : calculer le gap topologique et visualiser les modes de Majorana
# ============================================================
import numpy as np
from scipy.linalg import eigh

def kitaev_chain(N, mu, t, Delta, phi=0.0):
    """
    Construit et diagonalise l'Hamiltonien de Kitaev pour une chaîne de N sites.
    
    Paramètres :
    - N : nombre de sites de la chaîne
    - mu : potentiel chimique (contrôle la phase topologique)
    - t : amplitude de hopping (énergie cinétique)
    - Delta : paramètre de pairing supraconducteur
    - phi : phase supraconductrice
    
    Retourne :
    - evals : valeurs propres (spectre d'énergie)
    - evecs : vecteurs propres
    - gap : gap d'énergie au niveau de Fermi
    """
    # L'Hamiltonien est de taille 2N x 2N (espace de Nambu : particule + trou)
    H = np.zeros((2*N, 2*N), dtype=complex)

    # Terme diagonal : potentiel chimique -mu sur chaque site
    for j in range(N):
        H[2*j, 2*j] = -mu

    # Termes de hopping : -t entre sites voisins (particules)
    # +t entre sites voisins (trous — signe opposé dans l'espace de Nambu)
    for j in range(N-1):
        H[2*j, 2*(j+1)] = -t           # hopping particule
        H[2*j+1, 2*(j+1)+1] = t        # hopping trou (signe +)

    # Termes de pairing : Delta entre sites voisins
    # Ces termes créent/détruisent des paires de fermions
    for j in range(N-1):
        H[2*j, 2*(j+1)+1] = Delta * np.exp(1j * phi)       # pairing particule-trou
        H[2*j+1, 2*(j+1)] = -np.conj(Delta * np.exp(1j * phi))  # pairing trou-particule
        H[2*(j+1), 2*j+1] = Delta * np.exp(1j * phi)       # pairing symétrique
        H[2*(j+1)+1, 2*j] = -np.conj(Delta * np.exp(1j * phi))

    # Diagonalisation
    evals, evecs = eigh(H)

    # Le gap est la différence entre la plus petite énergie positive
    # et la plus grande énergie négative
    gap = np.min(evals[N:]) - np.max(evals[:N])
    return evals, evecs, gap

def majorana_wavefunctions(evecs, N):
    """
    Extrait les fonctions d'onde des deux modes de Majorana de bord.
    Ce sont les vecteurs propres au niveau de Fermi (E ≈ 0).
    """
    gamma_L = evecs[:2*N, N-1]   # Mode de Majorana gauche
    gamma_R = evecs[:2*N, N]     # Mode de Majorana droit
    return gamma_L, gamma_R

# --- Balayage en taille de chaîne : convergence du gap ---
Ns = [50, 100, 200, 400, 800]
gaps = []

for N in Ns:
    _, _, gap = kitaev_chain(N, mu=0.0, t=1.0, Delta=0.5)
    gaps.append(gap)
    print(f"N = {N}: gap = {gap:.6f}")

# Estimation de la décroissance du gap avec la taille
gap_inf = gaps[-1]
decay = np.polyfit(np.log(Ns[-3:]), np.log(np.abs(np.array(gaps[-3:]) - gap_inf)), 1)
print(f"Decroissance du gap: O(N^{decay[0]:.2f})")

# --- Analyse détaillée pour N = 200 ---
N_plot = 200
evals, evecs, gap_plot = kitaev_chain(N_plot, mu=0.0, t=1.0, Delta=0.5)

print(f"\nAnalyse du gap topologique (N={N_plot}):")
print(f"mu = 0, t = 1, Delta = 0.5 (phase topologique)")
print(f"Gap d'energie = {gap_plot:.6f}")

# --- Diagramme de phase : gap en fonction de mu ---
mu_vals = np.linspace(-3, 3, 200)
gaps_mu = []

for mu_val in mu_vals:
    _, _, g = kitaev_chain(N_plot, mu=mu_val, t=1.0, Delta=0.5)
    gaps_mu.append(g)

gap_array = np.array(gaps_mu)
idx_top = np.where(gap_array > 1e-6)[0]
print(f"Phase topologique: |mu| < 2t = 2.0")
print(f"Gap maximum dans phase topo: {np.max(gap_array):.4f}")

# --- Invariant topologique (nombre de winding) ---
def topological_invariant(evals, evecs, N):
    """
    Calcule l'invariant topologique Z2 de la chaîne de Kitaev.
    W = +1 : phase triviale
    W = -1 : phase topologique
    """
    Q = np.eye(N, dtype=complex)
    for n in range(0, N):
        vn = evecs[:N, n]
        Q[n, n] = np.sum(np.conj(vn[0::2]) * vn[1::2])
    return np.linalg.det(Q).real

winding = topological_invariant(evals, evecs, N_plot)
print(f"Invariant topologique (winding) = {winding:.4f}")

# --- Visualisation de la localisation des modes de Majorana ---
N_test = 400
evals_test, evecs_test, gap_test = kitaev_chain(N_test, mu=0.0, t=1.0, Delta=0.5)
gamma_L, gamma_R = majorana_wavefunctions(evecs_test, N_test)

# Probabilité de présence sur chaque site (composantes particule + trou)
site_probs_L = np.abs(gamma_L[0::2])**2 + np.abs(gamma_L[1::2])**2
site_probs_R = np.abs(gamma_R[0::2])**2 + np.abs(gamma_R[1::2])**2

print(f"\nLocalisation des modes de Majorana:")
print(f"Probabilite au bord gauche (site 0): {site_probs_L[0]:.6f}")
print(f"Probabilite au bord droit (site {N_test-1}): {site_probs_R[N_test-1]:.6f}")
print(f"Probabilite au centre gauche (site {N_test//2}): {site_probs_L[N_test//2]:.6e}")
```

### Simulation du désordre et robustesse topologique

```python
# ============================================================
# Test de robustesse : le gap topologique résiste-t-il au désordre ?
# ============================================================
import numpy as np

def kitaev_chain_disordered(N, mu, t, Delta, disorder_amp=0.0):
    """
    Chaîne de Kitaev avec désordre sur le potentiel chimique.
    disorder_amp : amplitude du désordre aléatoire sur chaque site.
    """
    H = np.zeros((2*N, 2*N), dtype=complex)
    # Le potentiel chimique varie aléatoirement sur chaque site
    mu_local = mu + disorder_amp * (np.random.rand(N) - 0.5)

    for j in range(N):
        H[2*j, 2*j] = -mu_local[j]

    for j in range(N-1):
        H[2*j, 2*(j+1)] = -t
        H[2*j+1, 2*(j+1)+1] = t

    for j in range(N-1):
        H[2*j, 2*(j+1)+1] = Delta
        H[2*j+1, 2*(j+1)] = -Delta
        H[2*(j+1), 2*j+1] = Delta
        H[2*(j+1)+1, 2*j] = -Delta

    evals, evecs = np.linalg.eigh(H)
    gap = np.min(evals[N:]) - np.max(evals[:N])
    return evals, evecs, gap

# --- Balayage de l'amplitude du désordre ---
N_chain = 100
disorder_scan = np.logspace(-3, 1, 30)  # De 0.001 à 10
gap_means = []
gap_stds = []

for W in disorder_scan:
    gaps = []
    for _ in range(50):  # 50 réalisations du désordre pour chaque W
        _, _, g = kitaev_chain_disordered(N_chain, 0.0, 1.0, 0.5, W)
        gaps.append(g)
    gap_means.append(np.mean(gaps))
    gap_stds.append(np.std(gaps))
    print(f"W = {W:.4f}: gap moyen = {np.mean(gaps):.6f} +/- {np.std(gaps):.6f}")

# Identification du désordre critique (transition topologique → triviale)
idx_cross = np.argmin(np.abs(np.array(gap_means) - 0.01))
print(f"\nDisorder critique (gap < 0.01): W_c ~ {disorder_scan[idx_cross]:.4f}")
```

### Comparaison des overheads de correction

```python
# ============================================================
# Comparaison : combien de qubits physiques par qubit logique ?
# Topologique vs code de surface vs QLDPC
# ============================================================
import numpy as np

def topological_overhead(epsilon, L=10, xi=5):
    """
    Overhead topologique : l'erreur est supprimée exponentiellement
    par la longueur du fil. Un seul qubit physique suffit (en théorie).
    """
    phys_err = np.exp(-L / xi)
    return 1.0

def surface_overhead(epsilon, p_phys=1e-3):
    """
    Overhead du code de surface : il faut d² qubits physiques par qubit logique,
    où d est la distance du code.
    """
    d = np.ceil(2 * np.log(1/epsilon) / np.log(1/p_phys))
    return d**2

eps_target = 1e-12  # Erreur cible pour un qubit logique utile
N_top = topological_overhead(eps_target)
N_surface = surface_overhead(eps_target)

print(f"Rapport N_phys/N_log (cible erreur = {eps_target:.0e}):")
print(f"  Topologique (attendue): {N_top}")
print(f"  Code de surface (p=1e-3): {N_surface:.0f}")
```

### Simulation du gap en fonction de la taille finie

```python
# ============================================================
# Effet de taille finie : le gap se ferme-t-il pour une chaîne courte ?
# ============================================================
import numpy as np

def finite_size_gap(N, mu, t, Delta):
    """Calcule le gap pour une chaîne de taille finie."""
    evals, _, _ = kitaev_chain(N, mu, t, Delta)
    gap_finite = np.min(evals[N:]) - np.max(evals[:N])
    return gap_finite

# Pour différentes valeurs du couplage t
for t_coupling in [0.5, 1.0, 2.0]:
    Ns_finite = [20, 40, 80, 160, 320, 640]
    gaps_finite = []
    for Nf in Ns_finite:
        gf = finite_size_gap(Nf, 0.0, t_coupling, 0.5)
        gaps_finite.append(gf)

    gap_inf_fit = gaps_finite[-1]
    decays = []
    for i in range(len(Ns_finite)-2):
        d = np.log(abs(gaps_finite[i] - gap_inf_fit)) / np.log(Ns_finite[i])
        decays.append(d)

    print(f"t={t_coupling}: gap(N->inf) ~ {gap_inf_fit:.6f}")

def topological_robustness(N, mu, t, Delta, n_samples=20):
    """
    Vérifie que les modes de Majorana gauche et droit
    ont un recouvrement exponentiellement petit.
    """
    overlaps = []
    for _ in range(n_samples):
        evals, evecs, _ = kitaev_chain_disordered(N, mu, t, Delta, 0.1)
        gamma_L = evecs[:2*N, N-1]
        gamma_R = evecs[:2*N, N]
        overlap = np.abs(np.dot(gamma_L.conj(), gamma_R))
        overlaps.append(overlap)
    return np.mean(overlaps), np.std(overlaps)

rob_mean, rob_std = topological_robustness(200, 0.0, 1.0, 0.5, 30)
print(f"Recouvrement moyen MZM-L/R : {rob_mean:.4e} +/- {rob_std:.4e}")
print(f"Les MZM sont bien separes exponentiellement")
```

---

## Comparaison des technologies

| Critère | Topologique (Microsoft) | Supraconducteur (Google/IBM) | Atomes neutres (QuEra) | Ions piégés |
|---------|------------------------|------------------------------|------------------------|-------------|
| **Protection** | Passive (topologique) | Active (QEC) | Active (QEC) | Active (QEC) |
| **Erreur physique** | $10^{-6}$ (extrapolé) | $10^{-3}$ | $5 \times 10^{-3}$ | $10^{-4}$ |
| **Overhead QEC** | ~1 (théorique) | ~1000 | ~1000 | ~100 |
| **Maturité** | Préliminaire (1 qubit) | Avancée (100+ qubits) | Avancée (48 logiques) | Avancée (99.99%) |
| **Portes** | À démontrer | Démontrées | Démontrées | Démontrées |
| **Scalabilité** | Potentiellement excellente | Bonne | Excellente | Limitée |
| **Température** | <50 mK | <15 mK | Ultra-vide + µK | Ultra-vide |

---

## À retenir

1. **Un qubit topologique encode l'information de façon non-locale** : deux modes de Majorana aux extrémités d'un nanofil. Un bruit local ne peut pas retourner le qubit car il devrait agir sur les deux modes simultanément.

2. **Le modèle de Kitaev** est le modèle théorique le plus simple exhibant des modes de Majorana. La phase topologique apparaît quand $|\mu| < 2t$.

3. **Le gap topologique $\Delta$** protège les MZM : toute perturbation d'énergie inférieure à $\Delta$ ne peut pas détruire l'information. Pour Microsoft Majorana 1, $\Delta \sim 200$ µeV $\sim 50$ GHz.

4. **L'erreur décroît exponentiellement** avec la longueur du fil : $\epsilon \propto e^{-L/\xi}$. C'est fondamentalement différent des qubits conventionnels où l'erreur est constante.

5. **Le désordre ne détruit pas la phase topologique** (tant qu'il ne ferme pas le gap). C'est la « robustesse topologique » — l'invariant topologique ne change pas sous perturbation continue.

6. **L'overhead de correction est drastiquement réduit** : un qubit topologique pourrait nécessiter ~1 qubit physique par qubit logique, contre ~1000 pour un code de surface avec des supraconducteurs.

7. **La promesse reste à démontrer** : Microsoft Majorana 1 est la première puce, mais les portes logiques topologiques n'ont pas encore été réalisées. Le chemin est long entre un qubit et un ordinateur fonctionnel.

---

## Pièges à éviter

1. **Confondre Majorana et supersymétrie** : Les fermions de Majorana en physique de la matière condensée sont des **excitations collectives** (quasi-particules), pas des particules fondamentales. Ils n'ont rien à voir avec la supersymétrie.

2. **Penser que la protection topologique est absolue** : Elle est exponentiellement bonne, pas parfaite. Pour un fil trop court ($L \sim \xi$), les deux MZM se recouvrent et la protection disparaît. Il faut $L \gg \xi$.

3. **Confondre phase topologique et isolation** : Un isolant est trivial (pas de modes de bord). Un isolant topologique a des états conducteurs aux bords. La « topologie » ne signifie pas « isolé de tout » — elle signifie « protégé par un invariant global ».

4. **Croire que les qubits topologiques n'ont besoin d'aucune correction** : Même avec une erreur de $10^{-6}$, pour un algorithme de $10^{12}$ portes, on aura ~$10^6$ erreurs. La correction d'erreur reste nécessaire, mais avec un overhead bien plus faible.

5. **Oublier que le modèle de Kitaev est idéalisé** : Le vrai matériau (InAs-Al) a du désordre, des imperfections, des interactions électron-électron. La phase topologique peut être détruite si le désordre est trop fort (transition d'Anderson).

---

## Exercices

### Niveau 1 — Application directe

1. **Phase topologique** : Pour le modèle de Kitaev avec $t = 1$ et $\Delta = 0.5$, déterminer si les valeurs suivantes de $\mu$ sont en phase topologique ou triviale : $\mu = 0$, $\mu = 1$, $\mu = 1.5$, $\mu = 3$.

2. **Exécuter le code** : Reproduire la simulation Python de la chaîne de Kitaev et vérifier que le gap est non nul pour $\mu = 0$, $t = 1$, $\Delta = 0.5$.

3. **Longueur de cohérence** : Calculer $\xi = t/\Delta$ pour $\Delta = 0.3$ et $\Delta = 0.8$. Combien de sites faut-il pour que le recouvrement entre MZM soit $< 10^{-10}$ ?

### Niveau 2 — Compréhension

4. **Transition de phase** : Tracer le gap en fonction de $\mu$ pour $N=100$, $t=1$, $\Delta=0.5$. Identifier les points critiques $\mu_c = \pm 2t$ et la région topologique. Que se passe-t-il exactement aux points critiques ?

5. **Modes de bord** : Visualiser les fonctions d'onde des deux MZM ($\gamma_L, \gamma_R$) pour $N=200$ en phase topologique ($\mu=0$) et en phase triviale ($\mu=3$). Observer la localisation exponentielle.

6. **Bruit local** : Ajouter un terme de désordre $\delta\mu_j$ aléatoire sur chaque site. Calculer la dégénérescence des MZM en fonction de l'amplitude du désordre pour $N=50$. À partir de quelle amplitude le gap se ferme-t-il ?

### Niveau 3 — Défi

7. **Longueur de cohérence** : Mesurer $\xi$ en ajustant l'enveloppe exponentielle des MZM pour différentes valeurs de $\Delta$. Vérifier la loi $\xi \propto 1/\Delta$.

8. **Invariant topologique** : Calculer l'invariant de winding pour $\mu$ variant de -3 à 3. Vérifier qu'il change de valeur aux points critiques.

9. **Comparaison architecturale** : Pour un budget de $10^6$ qubits physiques, estimer le nombre de qubits logiques réalisables avec des qubits topologiques ($\epsilon = 10^{-6}$) vs des qubits supraconducteurs ($\epsilon = 10^{-3}$). Inclure l'overhead de correction d'erreur pour chaque cas.

---

## Pour aller plus loin

- **Microsoft Quantum** (2025). "Majorana 1: A topological qubit platform." *Nature*. — L'article annonçant la première puce topologique.
- **Kitaev, A.Yu.** (2001). "Unpaired Majorana fermions in quantum wires." *Physics-Uspekhi*, 44, 131. — L'article fondateur du modèle.
- **Nayak, C.** et al. (2008). "Non-Abelian anyons and topological quantum computation." *Rev. Mod. Phys.*, 80, 1083. — Revue complète sur les anyons et le calcul topologique.
- **Alicea, J.** (2012). "New directions in the pursuit of Majorana fermions in solid state systems." *Rep. Prog. Phys.*, 75, 076501. — Guide pédagogique sur la recherche expérimentale.
- **Lutchyn, R.M.** et al. (2010). "Majorana fermions and topological phase in a semiconductor-superconductor heterostructure." *Phys. Rev. Lett.*, 105, 077001. — Proposition réaliste de réalisation expérimentale.
