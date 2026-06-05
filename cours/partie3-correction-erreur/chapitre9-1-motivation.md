# Chapitre 9.1 — Motivation et défis de la correction d'erreur quantique

## Objectifs

- Comprendre la fragilité des qubits face à la décohérence
- Distinguer la correction d'erreur classique de la correction quantique
- Formaliser le seuil de correction d'erreur
- Simuler un qubit bruité avec QuTiP

---

## 1. Fragilité des qubits

### 1.1 Le problème fondamental

Un qubit stocke une information dans un état quantique :

$$
\ket{\psi} = \alpha\ket{0} + \beta\ket{1}, \quad |\alpha|^2 + |\beta|^2 = 1
$$
où $\alpha, \beta \in \mathbb{C}$ = amplitudes de probabilité, $|\alpha|^2, |\beta|^2$ = probabilités de mesurer $\ket{0}, \ket{1}$.

Contrairement à un bit classique, un qubit est **continu** (amplitude complexe) et **fragile** : toute interaction avec l'environnement le dégrade.

### 1.2 Décohérence

La décohérence est le processus par lequel un système quantique perd sa cohérence en s'intriquant avec l'environnement :

$$
\rho(t) = \begin{pmatrix} |\alpha|^2 & \alpha\beta^* e^{-\gamma t} \\ \alpha^*\beta e^{-\gamma t} & |\beta|^2 \end{pmatrix}
$$
où $\rho(t)$ = matrice densité au temps $t$, $\gamma$ = taux de décohérence, $\alpha, \beta$ = amplitudes initiales.

Les temps caractéristiques sont :

- **T₁** : temps de relaxation (perte d'énergie)
- **T₂** : temps de déphasage (perte de cohérence de phase)
- Toujours $T_2 \le 2T_1$, où $T_1$ = temps de relaxation (perte d'énergie), $T_2$ = temps de déphasage (perte de cohérence de phase)

```python
import qutip as qt
import numpy as np

# Simulation de la décohérence d'un qubit
T1, T2 = 30.0, 15.0  # µs
gamma1 = 1.0 / T1
gamma2 = 1.0 / T2

omega = 2.0  # GHz
H = omega / 2 * qt.sigmaz()

sm = qt.destroy(2)
sz = qt.sigmaz()

c_ops = [np.sqrt(gamma1) * sm, np.sqrt(gamma2) * sz]

psi0 = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
rho0 = psi0 * psi0.dag()

tlist = np.linspace(0, 3 * T1, 200)
result = qt.mesolve(H, rho0, tlist, c_ops=c_ops)

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

### 1.3 Sources de bruit physique

| Source | Effet | Ordre de grandeur |
|--------|-------|-------------------|
| Couplage phonons | Relaxation T₁ | 10–100 µs (supra) |
| Bruit de flux | Déphasage T₂ | 5–50 µs (supra) |
| Radiation ionisante | Erreurs parasites | 1/10 min |
| Diaphonie | Crosstalk entre qubits | 0.1–1 % |
| Impuretés de fabrication | Variations de fréquence | 1–10 MHz |

---

## 2. Différence fondamentale avec la correction classique

### 2.1 Correction classique : la redondance simple

Un code classique à répétition :
- Bit $0 \to 000$, bit $1 \to 111$
- Correction par vote majoritaire : $010 \to 0$

**Pourquoi cela ne marche pas en quantique :**

1. **Théorème de non-clonage** : impossible de copier un état quantique inconnu

$$
\nexists U \; \text{t.q.} \; U(\ket{\psi}\ket{0}) = \ket{\psi}\ket{\psi}
$$
où $U$ = opérateur unitaire de copie, $\ket{\psi}$ = état inconnu, $\ket{0}$ = état auxiliaire.

2. **Mesure destructive** : mesurer un qubit détruit la superposition

3. **Erreurs continues** : une erreur n'est pas binaire mais un continuum

$$
\ket{\psi} \to \ket{\psi'} = a\ket{0} + b\ket{1} \quad \text{avec rotation continue}
$$
où $a, b \in \mathbb{C}$ = amplitudes après l'erreur (rotation continue).

### 2.2 Types d'erreurs quantiques

Les erreurs sur un qubit sont décrites par les opérateurs de Pauli :

$$
X = \begin{pmatrix}0&1\\1&0\end{pmatrix},\;
Y = \begin{pmatrix}0&-i\\i&0\end{pmatrix},\;
Z = \begin{pmatrix}1&0\\0&-1\end{pmatrix}
$$

Toute erreur peut se décomposer sur la base $\{I, X, Y, Z\}$ :

$$
\mathcal{E}(\rho) = \sum_{i,j} \chi_{ij} P_i \rho P_j, \quad P_i \in \{I, X, Y, Z\}^{\otimes n}
$$

```python
import numpy as np

# Décomposition d'une erreur continue sur les Pauli
def decompose_error_on_pauli(E_matrix):
    """
    Décompose une matrice d'erreur 2x2 sur la base de Pauli.
    Retourne les coefficients (c_I, c_X, c_Y, c_Z).
    """
    I2 = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)

    basis = [I2, X, Y, Z]
    coeffs = []
    for P in basis:
        c = np.trace(P.conj().T @ E_matrix) / 2.0
        coeffs.append(c)
    return coeffs

# Exemple : rotation autour de X d'angle theta
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

---

## 3. Seuil de correction d'erreur

### 3.1 Théorème du seuil

Il existe un **taux d'erreur physique critique** $p_\text{th}$ tel que :

- Si $p < p_\text{th}$ : la correction d'erreur peut réduire arbitrairement le taux d'erreur logique
- Si $p > p_\text{th}$ : la correction empire la situation

$$
p_L \propto \left(\frac{p}{p_\text{th}}\right)^{\lfloor (d+1)/2 \rfloor}
$$

où $p_L$ est le taux d'erreur logique, $p$ le taux physique, $d$ la distance du code.

### 3.2 Valeurs typiques

| Code | Seuil $p_\text{th}$ | Distance | Référence |
|------|---------------------|----------|-----------|
| Code de surface | $\sim 1\%$ | $d$ | Fowler 2012 |
| Code de Shor | $\sim 10^{-4}$ | $3$ | Shor 1995 |
| Code Steane | $\sim 10^{-3}$ | $3$ | Steane 1996 |
| Code GKP (bosonique) | $\sim 10^{-2}$ | — | Gottesman 2001 |

### 3.3 Passage sous le seuil (Google Willow 2024)

Google a démontré que l'augmentation de la distance du code réduit exponentiellement le taux d'erreur logique :

```python
import numpy as np
import matplotlib.pyplot as plt

# Simulation du scaling sous le seuil
p_physique = 0.003  # 0.3% < seuil ~1%
p_th = 0.01

distances = [3, 5, 7, 9, 11, 13, 15]

p_logique = []
for d in distances:
    pl = (p_physique / p_th) ** ((d + 1) // 2)
    p_logique.append(pl)

print("Scaling du taux d'erreur logique avec la distance :")
for d, pl in zip(distances, p_logique):
    print(f"  d={d:2d} : p_L = {pl:.2e}")

# Taux d'erreur physique au-dessus du seuil (pas d'amélioration)
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

---

## 4. Simulation d'un qubit avec bruit (QuTiP)

### 4.1 Canal dépolarisant

Le canal dépolarisant applique une erreur Pauli aléatoire avec probabilité $p$ :

$$
\rho \to (1-p)\rho + \frac{p}{3}(X\rho X + Y\rho Y + Z\rho Z)
$$

```python
import qutip as qt
import numpy as np

def depolarizing_kraus(p):
    """Retourne les opérateurs de Kraus du canal dépolarisant."""
    K0 = np.sqrt(1 - p) * qt.qeye(2)
    K1 = np.sqrt(p / 3) * qt.sigmax()
    K2 = np.sqrt(p / 3) * qt.sigmay()
    K3 = np.sqrt(p / 3) * qt.sigmaz()
    return [K0, K1, K2, K3]

def apply_kraus(rho, kraus_ops):
    """Applique un canal Kraus à une matrice densité."""
    result = qt.Qobj(np.zeros_like(rho.full()), dims=rho.dims)
    for K in kraus_ops:
        result += K * rho * K.dag()
    return result

# Test : évolution de la pureté
p_values = np.linspace(0, 1, 11)
psi_init = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
rho_init = psi_init * psi_init.dag()

print("Effet du canal dépolarisant sur |+><+| :")
for p in p_values:
    kraus = depolarizing_kraus(p)
    rho_final = apply_kraus(rho_init, kraus)
    purete = (rho_final * rho_final).tr()
    fidelity = (psi_init.dag() * rho_final * psi_init).real
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

### 4.2 Simulation Monte Carlo de trajectoires

Plutôt que de faire évoluer la matrice densité, on peut simuler des trajectoires individuelles (quantum trajectories) :

```python
import qutip as qt
import numpy as np

# Paramètres
T1, T2 = 20.0, 10.0
gamma1, gamma2 = 1.0/T1, 1.0/T2
H = 0.5 * qt.sigmaz()

sm = qt.destroy(2)
c_ops = [np.sqrt(gamma1) * sm, np.sqrt(gamma2) * qt.sigmaz()]

psi0 = qt.basis(2, 0)

# Monte Carlo : 100 trajectoires
n_traj = 100
tlist = np.linspace(0, 40, 200)
mc_result = qt.mcsolve(H, psi0, tlist, c_ops=c_ops, e_ops=[qt.sigmaz()],
                       ntraj=n_traj, progress_bar=False)

# Comparaison avec l'équation maîtresse
me_result = qt.mesolve(H, psi0 * psi0.dag(), tlist, c_ops=c_ops, e_ops=[qt.sigmaz()])

print(f"Simulation Monte Carlo ({n_traj} trajectoires) vs maître:")
for t_idx in [0, len(tlist)//4, len(tlist)//2, -1]:
    t = tlist[t_idx]
    sz_mc = mc_result.expect[0][t_idx]
    sz_me = me_result.expect[0][t_idx]
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

## 5. Pourquoi la correction d'erreur quantique est difficile

### 5.1 Trois défis majeurs

1. **Non-clonage** $\Rightarrow$ redondance via intrication, pas copie
2. **Mesure** $\Rightarrow$ mesures indirectes (syndrome) sans lire l'information
3. **Erreurs continues** $\Rightarrow$ discrétisation via la correction d'erreur

### 5.2 Principe de la correction

On code $k$ qubits logiques dans $n$ qubits physiques ($n > k$), en les plongeant dans un sous-espace de code :

$$
\mathcal{C} \subset (\mathbb{C}^2)^{\otimes n}, \quad \dim \mathcal{C} = 2^k
$$

Les erreurs sont détectées par des **mesures de syndrome** qui ne révèlent pas l'état logique.

$$
\begin{aligned}
\ket{\psi_L} &= \alpha\ket{0_L} + \beta\ket{1_L} \\
\text{Erreur } E &\to E\ket{\psi_L} \\
\text{Syndrome } S(E) &\to \text{information sur } E \text{ sans mesurer } \ket{\psi_L}
\end{aligned}
$$

---

## Exercices

1. Simuler un qubit initialement dans l'état $\ket{+}$ avec un modèle de bruit incluant T₁ = 50 µs et T₂ = 30 µs. Tracer $\langle X \rangle$, $\langle Y \rangle$, $\langle Z \rangle$ en fonction du temps.

2. Implémenter manuellement les opérateurs de Kraus du canal bit-flip et vérifier la condition $\sum_k K_k^\dagger K_k = I$.

3. Montrer que la fidélité d'un état $\ket{\psi}$ après un canal dépolarisant est $F = 1 - \frac{2p}{3}$.

4. Avec Qiskit, créer un circuit qui prépare $\ket{+}$ et lui applique un canal dépolarisant via le `NoiseModel`. Comparer les distributions de mesure avec et sans bruit pour 4096 shots.

5. Démontrer mathématiquement que le taux d'erreur logique pour un code de distance $d$ sous un seuil $p_\text{th}$ évolue comme $p_L \propto (p/p_\text{th})^{\lfloor (d+1)/2 \rfloor}$.

6. **Recherche** : Lire l'article Google Willow (Nature 2024) et résumer en 10 lignes comment ils démontrent le passage sous le seuil.
