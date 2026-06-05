# Chapitre 14.2 — Défis ouverts et perspectives

## Objectifs

- Analyser les défis de scalabilité (nombre de qubits, qualité, connectivité)
- Comprendre le coût de la correction d'erreur (overhead physique/logique)
- Évaluer les besoins en main-d'œuvre (QEC, 600–16000 spécialistes d'ici 2030)
- Étudier la feuille de route : avantage quantique pratique 2027–2029
- Maîtriser la standardisation post-quantique (NIST)
- Implémenter un benchmark comparatif de simulation classique vs quantique

---

## 1. Scalabilité : le triple défi

### 1.1 Nombre de qubits

Le nombre de qubits physiques a connu une croissance exponentielle :

$$
N_{\text{phys}}(t) \approx N_0 \cdot 2^{(t-t_0)/\tau}, \quad \tau \sim 1.5\text{–}2 \text{ ans}
$$

Cependant, le nombre de **qubits logiques** utiles suit une courbe plus lente :

$$
N_{\text{log}} = \frac{N_{\text{phys}}}{d^2}, \quad d \propto \log(1/\epsilon_{\text{phys}})
$$

| Année | Qubits physiques | Qubits logiques (d=7) | Qubits logiques (d=17) |
|-------|-----------------|----------------------|-----------------------|
| 2024 | 105 (Willow) | 2 | 0 |
| 2026 | 1000 | 20 | 3 |
| 2028 | 10000 | 200 | 35 |
| 2030 | 100000 | 2000 | 350 |

### 1.2 Qualité des qubits

La métrique clé est le **taux d'erreur par porte** $\epsilon$ et le **rapport $T_2/T_{\text{gate}}$** :

$$
Q = \left( \frac{T_2}{T_{\text{gate}}} \right)^{-1} \cdot \frac{1}{\epsilon_{\text{2Q}}}
$$

| Architecture | $\epsilon_{\text{1Q}}$ | $\epsilon_{\text{2Q}}$ | $T_2$ | $Q$ |
|-------------|----------------------|----------------------|-------|-----|
| Supraconducteur | $10^{-4}$ | $10^{-3}$ | $100\,\mu$s | $10^3$ |
| Atomes neutres | $10^{-5}$ | $5 \times 10^{-3}$ | $1$ s | $10^5$ |
| Ions piégés | $10^{-5}$ | $10^{-4}$ | $10$ s | $10^7$ |
| Topologique | $10^{-7}$ | — | Protection | $\infty$ (théorique) |

### 1.3 Connectivité

La connectivité est limitée par la topologie physique :

- Grille 2D : degré moyen $\sim 3$–4
- Atomes neutres : degré variable (reconfigurable)
- Photonique : degré élevé (réseau)

Le **coût de routage** des qubits entre opérations non-locales est :

$$
\text{Cost}_{\text{SWAP}} = O(\text{diamètre du graphe}) \quad \text{portes SWAP}
$$

---

## 2. Coût de la correction d'erreur

### 2.1 Overhead physique/logique

Le ratio $r = N_{\text{phys}} / N_{\text{log}}$ dépend du code et du taux d'erreur :

$$
r_{\text{surface}} = \left( \frac{2\log(1/\epsilon_{\text{log}})}{\log(1/\epsilon_{\text{phys}}) - \log(p_{\text{th}})} \right)^2
$$

```python
import numpy as np

def compute_overhead(epsilon_phys, epsilon_log, p_th=0.01):
    d = np.ceil(2 * np.log(1/epsilon_log) / np.log(1/epsilon_phys / p_th))
    return int(d ** 2), int(d)

targets = [1e-6, 1e-10, 1e-15]
phys_rates = [1e-3, 1e-4, 1e-5]

print("Overhead N_phys/N_log pour code de surface:")
print(f"{'eps_phys':>10} {'eps_log':>10} {'d':>5} {'N_phys/N_log':>15}")
for eps_p in phys_rates:
    for eps_l in targets:
        if eps_p < 0.01:
            n_phys, d = compute_overhead(eps_p, eps_l)
            print(f"{eps_p:>10.0e} {eps_l:>10.0e} {d:>5} {n_phys:>15d}")

def qldpc_overhead(epsilon_log, n_data=1000):
    rate = 0.2
    n_log = int(n_data * rate)
    return n_data, n_log

for eps_l in targets:
    n_phys, n_log = qldpc_overhead(eps_l, 1000)
    print(f"QLDPC (n=1000, rate=0.2) pour eps_log={eps_l:.0e}: {n_phys} physiques -> {n_log} logiques")

epsilon_phys_real = 1e-3
n_logical_target = 100
eps_logical_target = 1e-12

n_phys_per_log, d_real = compute_overhead(epsilon_phys_real, eps_logical_target)
total_physical = n_phys_per_log * n_logical_target
print(f"\nPour {n_logical_target} qubits logiques a {eps_logical_target:.0e}:")
print(f"  Distance requise: d = {d_real}")
print(f"  Qubits physiques/logique: {n_phys_per_log}")
print(f"  Total qubits physiques: {total_physical}")
```

**Sortie attendue :**

```
Overhead N_phys/N_log pour code de surface:
  eps_phys    eps_log     d    N_phys/N_log
     1e-03      1e-06     3               9
     1e-03      1e-10     4              16
     1e-03      1e-15     6              36
     1e-04      1e-06     2               4
     1e-04      1e-10     4              16
     1e-04      1e-15     5              25
     1e-05      1e-06     2               4
     1e-05      1e-10     3               9
     1e-05      1e-15     5              25
QLDPC (n=1000, rate=0.2) pour eps_log=1e-06: 1000 physiques -> 200 logiques
QLDPC (n=1000, rate=0.2) pour eps_log=1e-10: 1000 physiques -> 200 logiques
QLDPC (n=1000, rate=0.2) pour eps_log=1e-15: 1000 physiques -> 200 logiques
Pour 100 qubits logiques a 1e-12:
  Distance requise: d = 5
  Qubits physiques/logique: 25
  Total qubits physiques: 2500
```

### 2.2 Budget de ressources

Pour exécuter un algorithme pratique (e.g. factorisation RSA-2048) :

| Ressource | Estimation |
|-----------|-----------|
| Qubits logiques | $O(10^4)$ |
| Portes logiques | $O(10^{12})$ |
| Portes physiques (surface) | $O(10^{16})$ |
| Temps d'exécution | $O(10^6)$ secondes |
| Énergie | $O(10)$ MW |

---

## 3. Main-d'œuvre et formation

### 3.1 État des lieux (2026)

- **600–700 spécialistes mondiaux** en correction d'erreur quantique
- Demande projetée : **5000–16000 d'ici 2030**
- Croissance $> 50\%$ par an

### 3.2 Compétences requises

| Domaine | Compétence | Priorité |
|---------|-----------|----------|
| Théorie | Codes stabilisateurs, QEC, décodeurs | Critique |
| Simulation | Stim, QuTiP, Qiskit | Élevée |
| Hardware | Compréhension du bruit physique | Élevée |
| Algorithmique | Circuits quantiques, optimisation | Moyenne |
| Software | Python, C++, parallélisation | Moyenne |

### 3.3 Formation recommandée

$$
\text{Spécialistes 2030} = \text{Spécialistes 2026} \times \left(1 + r_{\text{croissance}}\right)^{\Delta t}
$$

avec $r_{\text{croissance}} \sim 0.5$–$0.7$ par an.

---

## 4. Feuille de route 2026–2035

### 4.1 Jalons clés

$$
\text{Avantage} = \begin{cases}
\text{Démontré (simulation)} & 2025–2027 \\
\text{Pratique (niche)} & 2027–2029 \\
\text{Industriel} & 2029–2032 \\
\text{Généralisé} & 2032–2035
\end{cases}
$$

| Année | Jalon | Architecture probable |
|-------|-------|----------------------|
| 2026 | 1000 qubits physiques, démonstration QEC robuste | Supra, atomes neutres |
| 2027 | Premier qubit logique topologique fonctionnel | Topologique (MS) |
| 2028 | 100 qubits logiques (multi-codes) | Atomes neutres + QLDPC |
| 2029 | Avantage quantique pratique en optimisation | Hybride |
| 2030 | 10000 qubits physiques, 1000 logiques | Multi-plateforme |
| 2032 | Calculateur quantique modulaire | Photonique + réseau |
| 2035 | 1 million de qubits logiques | Intégration hétérogène |

### 4.2 Gates et milestones

```python
import numpy as np

def extrapolate_qubits(years, n0=105, t0=2024, tau=1.8):
    return n0 * 2 ** ((years - t0) / tau)

def extrapolate_logical(years, n0=2, t0=2024, tau_log=2.5):
    return n0 * 2 ** ((years - t0) / tau_log)

years = np.arange(2024, 2036)

print("Feuille de route - Qubits physiques et logiques:")
print(f"{'Annee':>6} {'Physiques':>12} {'Logiques (estim)':>16}")
for y in years:
    n_phys = extrapolate_qubits(y)
    n_log = extrapolate_logical(y)
    print(f"{y:>6d} {n_phys:>12.0f} {n_log:>16.1f}")

def quantum_advantage_gate_count(N, eps_phys=1e-3, d=7):
    n_log = N / (d ** 2)
    gate_depth = 1000
    err_per_gate = eps_phys * d
    prob_success = (1 - err_per_gate) ** (n_log * gate_depth)
    return prob_success

for N in [1000, 10000, 100000]:
    prob = quantum_advantage_gate_count(N)
    print(f"N_phys={N:>6d}: probabilite de succes d'un circuit de 1000 portes = {prob:.4f}")
```

---

## 5. Standardisation post-quantique (NIST)

### 5.1 Problème

Les ordinateurs quantiques de demain briseront RSA et ECC :

$$
\text{RSA-2048} \xrightarrow{\text{Shor}} O(10^8) \text{ portes logiques}
$$

### 5.2 Algorithmes NIST standardisés (2024)

| Algorithme | Type | Clé publique | Signature |
|-----------|------|-------------|-----------|
| CRYSTALS-Kyber | Lattice-based | Oui | Non |
| CRYSTALS-Dilithium | Lattice-based | Non | Oui |
| FALCON | Lattice-based (hash) | Non | Oui |
| SPHINCS+ | Hash-based | Non | Oui |

Contrainte : les tailles de clé et signatures sont $10\times$ à $100\times$ plus grandes que RSA/ECC.

---

## 5.1 Analyse des besoins en correction d'erreur par algorithme

```python
import numpy as np

algorithms = {
    "Shor RSA-2048": {"n_log": 6144, "n_gates": 1.5e12},
    "Grover 256-bit": {"n_log": 256, "n_gates": 1.0e8},
    "VQE (100 spins)": {"n_log": 100, "n_gates": 1.0e6},
    "QAOA MaxCut (100n)": {"n_log": 100, "n_gates": 1.0e5},
    "QPE (10 bits)": {"n_log": 20, "n_gates": 1.0e8},
}

p_phys = 1e-3
p_th = 0.01
d_min = 3

print("Besoins en ressources par algorithme:")
print(f"{'Algorithme':>25} {'n_log':>8} {'n_portes':>12} {'d_min':>6} {'n_phys':>10} {'t_exec(s)':>10}")

for name, params in algorithms.items():
    n_log = params["n_log"]
    n_gates = params["n_gates"]

    eps_gate = 1.0 / n_gates
    d = max(d_min, int(np.ceil(2 * np.log(1/eps_gate) / np.log(1/p_phys / p_th))))
    n_phys = n_log * d ** 2

    t_gate_phys = 50e-9
    t_exec = n_gates * t_gate_phys * d

    print(f"{name:>25} {n_log:>8d} {n_gates:>12.0e} {d:>6d} {n_phys:>10d} {t_exec:>10.2e}")
```

**Sortie attendue :**

```
Besoins en ressources par algorithme:
               Algorithme    n_log     n_portes  d_min     n_phys  t_exec(s)
            Shor RSA-2048     6144        2e+12      5     153600   3.75e+05
           Grover 256-bit      256        1e+08      4       4096   2.00e+01
          VQE (100 spins)      100        1e+06      3        900   1.50e-01
       QAOA MaxCut (100n)      100        1e+05      3        900   1.50e-02
            QPE (10 bits)       20        1e+08      4        320   2.00e+01
```

## 6. Benchmark comparatif classique vs quantique

```python
import numpy as np
import time

def classical_simulation(n_spins, method='exact'):
    if method == 'exact':
        dim = 2 ** n_spins
        if dim > 2**20:
            return None, dim
        start = time.time()
        H = np.random.randn(dim, dim)
        H = (H + H.T) / 2
        evals = np.linalg.eigvalsh(H)
        elapsed = time.time() - start
        return elapsed, dim
    return None, 2**n_spins

def quantum_gate_estimate(n_spins, gate_fidelity=0.999, n_shots=1000):
    n_gates = 4 ** n_spins
    t_gate = 50e-9
    total_time = n_gates * t_gate * n_shots
    success_prob = gate_fidelity ** n_gates
    return total_time, success_prob

n_range = [10, 15, 20, 25, 30, 35, 40]

print("Benchmark: Simulation classique vs estimation quantique")
print(f"{'n_spins':>8} {'Classique (s)':>15} {'Dim':>12} {'Quantique (s)':>15} {'Succès':>12}")

for n in n_range:
    t_class, dim = classical_simulation(n)
    t_quant, prob = quantum_gate_estimate(n)

    t_class_str = f"{t_class:.2e}" if t_class is not None else "N/A"
    dim_str = f"{dim:.0e}" if dim is not None else "N/A"
    t_quant_str = f"{t_quant:.2e}" if t_quant is not None else "N/A"
    prob_str = f"{prob:.2e}" if prob is not None else "N/A"

    print(f"{n:>8d} {t_class_str:>15} {dim_str:>12} {t_quant_str:>15} {prob_str:>12}")

def crossover_point(max_n=60):
    for n in range(10, max_n + 1):
        _, dim = classical_simulation(n, 'exact')
        if dim is None or dim > 2**25:
            t_class = 1e6
        else:
            t_class, _ = classical_simulation(n, 'exact')

        t_quant, prob = quantum_gate_estimate(n, 0.999, 100)

        if t_quant < t_class and prob > 0.01:
            return n

n_cross = crossover_point(60)
print(f"\nPoint de croisement estime : n = {n_cross} spins")
```

---

## 7. Exercices

1. **Overhead de correction** : Pour un taux d'erreur physique $p = 10^{-3}$, tracer $N_{\text{phys}}/N_{\text{log}}$ en fonction de $\epsilon_{\text{log}}$ entre $10^{-3}$ et $10^{-15}$. Inclure les courbes pour les codes de surface et QLDPC.

2. **Budget de ressources** : Estimer le nombre de qubits et le temps nécessaire pour un circuit de $10^{12}$ portes logiques sur une architecture à 10000 qubits physiques avec $\epsilon_{\text{phys}} = 10^{-3}$.

3. **Besoins en main-d'œuvre** : En supposant une croissance de 60% par an, calculer le nombre de spécialistes QEC nécessaires en 2027, 2028, 2029 et 2030. Discuter des implications pour la formation.

4. **Benchmark** : Comparer le temps d'exécution classique vs quantique attendu pour la simulation d'un modèle de Heisenberg à $n$ spins ($n=10$ à $n=100$). Identifier le point de croisement pour une fidélité de porte de $99.9\%$.

5. **Analyse de standardisation** : Comparer les tailles de clé et signatures des algorithmes post-quantiques NIST avec RSA-2048. Discuter de l'impact sur les protocoles réseau actuels.

---

## Références

- **Google Quantum AI** (2024). "Quantum error correction below the surface code threshold." *Nature*, 636, 74–79.
- **Bluvstein, D.** et al. (2025). "Logical quantum processor with 48 logical qubits." *Nature*.
- **Microsoft Quantum** (2025). "Majorana 1: A topological qubit platform." *Nature*.
- **NIST** (2024). "Post-Quantum Cryptography: Selected Algorithms 2024." *NIST IR 8413*.
- **McKinsey & Company** (2025). "Quantum computing: An emerging ecosystem and industry use cases."
- **Preskill, J.** (2018). "Quantum Computing in the NISQ era and beyond." *Quantum*, 2, 79.
