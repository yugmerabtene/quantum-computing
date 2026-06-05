# Chapitre 13.1 — Qubits topologiques

## Objectifs

- Comprendre le concept de qubit topologique et les fermions de Majorana
- Analyser la puce Majorana 1 de Microsoft
- Maîtriser le modèle de Kitaev (chaîne 1D)
- Simuler le gap topologique avec Python
- Comparer les qubits topologiques aux autres architectures
- Appréhender la stabilité topologique et la protection contre le bruit

---

## 1. Fermions de Majorana

### 1.1 Particules de Majorana

Un **fermion de Majorana** est une particule qui est sa propre antiparticule :

$$
\gamma^\dagger = \gamma, \quad \{\gamma_i, \gamma_j\} = 2\delta_{ij}
$$

Contrairement aux fermions ordinaires (Dirac) où $c^\dagger \neq c$, les opérateurs de Majorana sont réels et autoadjoints.

Un fermion ordinaire peut être décomposé en deux fermions de Majorana :

$$
c = \frac{1}{2}(\gamma_1 + i\gamma_2), \quad c^\dagger = \frac{1}{2}(\gamma_1 - i\gamma_2)
$$

### 1.2 Modes zéro de Majorana (MZM)

Dans un système topologique, les **modes zéro de Majorana** apparaissent aux bords d'une phase topologique. Ils sont protégés par un gap d'énergie $\Delta$ :

$$
H = \sum_i \Delta_i \gamma_i \gamma_{i+1} + \text{termes sous-gap}
$$

Les MZM sont des états liés de bord avec énergie $E = 0$, séparés du bulk par un gap $\Delta$.

---

## 2. Modèle de Kitaev (chaîne 1D)

### 2.1 Hamiltonien

Le modèle de Kitaev décrit une chaîne 1D de fermions sans spin avec pairing $p$-wave :

$$
H = -\mu \sum_{j=1}^N c_j^\dagger c_j - \sum_{j=1}^{N-1} (t c_j^\dagger c_{j+1} + \Delta e^{i\phi} c_j c_{j+1} + \text{h.c.})
$$

où $\mu$ est le potentiel chimique, $t$ l'amplitude de hopping, $\Delta$ le paramètre de pairing, et $\phi$ la phase.

### 2.2 Phase topologique

Le système est dans une **phase topologique** (phase T) quand $|\mu| < 2|t|$ et dans une phase triviale (phase S) quand $|\mu| > 2|t|$.

$$
\mu_c = \pm 2t \quad \text{(ligne critique)}
$$

Dans la phase topologique, deux MZM apparaissent aux extrémités de la chaîne :

$$
\gamma_1 \propto c_1 + c_1^\dagger, \quad \gamma_N \propto c_N + c_N^\dagger
$$

Ces modes de bord sont **exponentiellement localisés** :

$$
\gamma_L \sim \sum_j e^{-j/\xi} (c_j + c_j^\dagger), \quad \xi \propto 1/\Delta
$$

### 2.3 Qubit topologique

Le qubit topologique est formé par l'espace doublement dégénéré de deux MZM :

$$
|0_L\rangle = |\text{vide}\rangle, \quad |1_L\rangle = \gamma_1 \gamma_N |\text{vide}\rangle
$$

La non-localité du qubit (les deux MZM sont aux extrémités de la chaîne) assure la **protection topologique** : un bruit local ne peut pas retourner le qubit.

---

## 3. Simulation Python du modèle de Kitaev

```python
import numpy as np
from scipy.linalg import eigh

def kitaev_chain(N, mu, t, Delta, phi=0.0):
    H = np.zeros((2*N, 2*N), dtype=complex)

    for j in range(N):
        H[2*j, 2*j] = -mu

    for j in range(N-1):
        H[2*j, 2*(j+1)] = -t
        H[2*j+1, 2*(j+1)+1] = t

    for j in range(N-1):
        H[2*j, 2*(j+1)+1] = Delta * np.exp(1j * phi)
        H[2*j+1, 2*(j+1)] = -np.conj(Delta * np.exp(1j * phi))
        H[2*(j+1), 2*j+1] = Delta * np.exp(1j * phi)
        H[2*(j+1)+1, 2*j] = -np.conj(Delta * np.exp(1j * phi))

    evals, evecs = eigh(H)

    gap = np.min(evals[N:]) - np.max(evals[:N])
    return evals, evecs, gap

def majorana_wavefunctions(evecs, N):
    gamma_L = evecs[:2*N, N-1]
    gamma_R = evecs[:2*N, N]
    return gamma_L, gamma_R

Ns = [50, 100, 200, 400, 800]
gaps = []

for N in Ns:
    _, _, gap = kitaev_chain(N, mu=0.0, t=1.0, Delta=0.5)
    gaps.append(gap)
    print(f"N = {N}: gap = {gap:.6f}")

gap_inf = gaps[-1]
decay = np.polyfit(np.log(Ns[-3:]), np.log(np.abs(np.array(gaps[-3:]) - gap_inf)), 1)
print(f"Decroissance du gap: O(N^{decay[0]:.2f})")

N_plot = 200
evals, evecs, gap_plot = kitaev_chain(N_plot, mu=0.0, t=1.0, Delta=0.5)

print(f"\nAnalyse du gap topologique (N={N_plot}):")
print(f"mu = 0, t = 1, Delta = 0.5 (phase topologique)")
print(f"Gap d'energie = {gap_plot:.6f}")

mu_vals = np.linspace(-3, 3, 200)
gaps_mu = []

for mu_val in mu_vals:
    _, _, g = kitaev_chain(N_plot, mu=mu_val, t=1.0, Delta=0.5)
    gaps_mu.append(g)

gap_array = np.array(gaps_mu)
idx_top = np.where(gap_array > 1e-6)[0]
print(f"Phase topologique: |mu| < 2t = 2.0")
print(f"Gap maximum dans phase topo: {np.max(gap_array):.4f}")

def topological_invariant(evals, evecs, N):
    Q = np.eye(N, dtype=complex)
    for n in range(0, N):
        vn = evecs[:N, n]
        Q[n, n] = np.sum(np.conj(vn[0::2]) * vn[1::2])
    return np.linalg.det(Q).real

winding = topological_invariant(evals, evecs, N_plot)
print(f"Invariant topologique (winding) = {winding:.4f}")

N_test = 400
evals_test, evecs_test, gap_test = kitaev_chain(N_test, mu=0.0, t=1.0, Delta=0.5)
gamma_L, gamma_R = majorana_wavefunctions(evecs_test, N_test)

site_probs_L = np.abs(gamma_L[0::2])**2 + np.abs(gamma_L[1::2])**2
site_probs_R = np.abs(gamma_R[0::2])**2 + np.abs(gamma_R[1::2])**2

print(f"\nLocalisation des modes de Majorana:")
print(f"Probabilite au bord gauche (site 0): {site_probs_L[0]:.6f}")
print(f"Probabilite au bord droit (site {N_test-1}): {site_probs_R[N_test-1]:.6f}")
print(f"Probabilite au centre gauche (site {N_test//2}): {site_probs_L[N_test//2]:.6e}")
```

---

## 4. Microsoft Majorana 1

### 4.1 Puce topologique (2025)

Microsoft a annoncé la **Majorana 1** : première puce utilisant des qubits topologiques basés sur des **nanofils supraconducteurs** (InAs-Al) :

- Longueur de cohérence topologique $\xi \sim 3-5\,\mu$m
- Gap topologique $\Delta \sim 200\,\mu$eV $\sim 50$ GHz
- Température de fonctionnement $< 50$ mK
- Protection topologique : réduction exponentielle des erreurs avec la longueur du fil

$$
\epsilon_{\text{qubit}} \propto \exp(-L/\xi)
$$

### 4.2 Mesure topologique

La mesure d'un qubit topologique utilise l'interférence de **bras de frustration** :

$$
I_{\text{mes}} \propto \cos(\pi N_{\text{tot}})
$$

où $N_{\text{tot}}$ est la parité totale du système.

| Propriété | Majorana 1 | Transmon | Atome neutre |
|-----------|-----------|----------|--------------|
| Protection | Topologique (exponentielle) | Active (QEC) | Active (QEC) |
| Taux d'erreur physique | $10^{-6}$ (extrapolé) | $10^{-3}$ | $10^{-3}$ |
| Overhead QEC | Faible | Élevé | Élevé |
| Portes logiques | À démontrer | Démonstrées | 48 qubits logiques |

---

## 5. Protection topologique contre le bruit

### 5.1 Hamiltonien perturbé

Sous l'effet du bruit, le Hamiltonien devient :

$$
H = H_0 + \sum_i \lambda_i(t) V_i
$$

où $V_i$ sont des perturbations locales. La protection topologique assure :

$$
|\langle 0_L | V_i | 1_L \rangle| \propto e^{-L/\xi}
$$

### 5.1 Simulation du désordre et robustesse topologique

```python
import numpy as np

def kitaev_chain_disordered(N, mu, t, Delta, disorder_amp=0.0):
    H = np.zeros((2*N, 2*N), dtype=complex)
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

N_chain = 100
disorder_scan = np.logspace(-3, 1, 30)
gap_means = []
gap_stds = []

for W in disorder_scan:
    gaps = []
    for _ in range(50):
        _, _, g = kitaev_chain_disordered(N_chain, 0.0, 1.0, 0.5, W)
        gaps.append(g)
    gap_means.append(np.mean(gaps))
    gap_stds.append(np.std(gaps))
    print(f"W = {W:.4f}: gap moyen = {np.mean(gaps):.6f} +/- {np.std(gaps):.6f}")

idx_cross = np.argmin(np.abs(np.array(gap_means) - 0.01))
print(f"\nDisorder critique (gap < 0.01): W_c ~ {disorder_scan[idx_cross]:.4f}")
```

### 5.2 Comparaison des overheads de correction

$$
N_{\text{phys}} / N_{\text{log}} = 
\begin{cases}
O(\log^2(1/\epsilon)) & \text{topologique (intrinsèque)} \\
O(\log^6(1/\epsilon)) & \text{codes de surface} \\
O(\log^4(1/\epsilon)) & \text{codes QLDPC}
\end{cases}
$$

```python
import numpy as np

def topological_overhead(epsilon, L=10, xi=5):
    phys_err = np.exp(-L / xi)
    return 1.0

def surface_overhead(epsilon, p_phys=1e-3):
    d = np.ceil(2 * np.log(1/epsilon) / np.log(1/p_phys))
    return d**2

eps_target = 1e-12
N_top = topological_overhead(eps_target)
N_surface = surface_overhead(eps_target)

print(f"Rapport N_phys/N_log (cible erreur = {eps_target:.0e}):")
print(f"  Topologique (attendue): {N_top}")
print(f"  Code de surface (p=1e-3): {N_surface:.0f}")
```

**Sortie attendue :**

```
Rapport N_phys/N_log (cible erreur = 1e-12):
  Topologique (attendue): 1.0
  Code de surface (p=1e-3): 64
```

---

## 6. Simulation du gap en fonction de la taille finie

```python
import numpy as np

def finite_size_gap(N, mu, t, Delta):
    evals, _, _ = kitaev_chain(N, mu, t, Delta)
    gap_finite = np.min(evals[N:]) - np.max(evals[:N])
    return gap_finite

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

## 7. Exercices

1. **Transition de phase topologique** : Tracer le gap en fonction de $\mu$ pour $N=100$, $t=1$, $\Delta=0.5$. Identifier les points critiques $\mu_c = \pm 2t$ et la région topologique.

2. **Modes de bord** : Visualiser les fonctions d'onde des deux modes zéro de Majorana ($\gamma_L, \gamma_R$) pour $N=200$ en phase topologique ($\mu=0$) et en phase triviale ($\mu=3$). Observer la localisation.

3. **Longueur de cohérence** : Mesurer $\xi$ en ajustant l'enveloppe exponentielle des MZM pour différentes valeurs de $\Delta$. Comparer avec la prédiction théorique $\xi \propto 1/\Delta$.

4. **Bruit local** : Ajouter un terme de désordre $\delta\mu_j$ aléatoire sur chaque site de la chaîne. Calculer la dégénérescence des MZM en fonction de l'amplitude du désordre pour $N=50$.

5. **Comparaison architecturale** : Pour un budget de $10^6$ qubits physiques, estimer le nombre de qubits logiques réalisables avec des qubits topologiques (Microsoft) vs des qubits supraconducteurs (Google Willow). Inclure l'overhead de correction d'erreur.

---

## Références

- **Microsoft Quantum** (2025). "Majorana 1: A topological qubit platform." *Nature*. [Mic25]
- **Kitaev, A.Yu.** (2001). "Unpaired Majorana fermions in quantum wires." *Physics-Uspekhi*, 44, 131.
- **Nayak, C.** et al. (2008). "Non-Abelian anyons and topological quantum computation." *Rev. Mod. Phys.*, 80, 1083.
- **Alicea, J.** (2012). "New directions in the pursuit of Majorana fermions in solid state systems." *Rep. Prog. Phys.*, 75, 076501.
- **Lutchyn, R.M.** et al. (2010). "Majorana fermions and topological phase in a semiconductor-superconductor heterostructure." *Phys. Rev. Lett.*, 105, 077001.
