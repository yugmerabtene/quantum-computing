# Chapitre 14.2 — Défis ouverts et perspectives

## Ce que vous allez apprendre

- Analyser les trois défis de scalabilité : nombre, qualité et connectivité des qubits
- Comprendre le coût réel de la correction d'erreur (overhead physique/logique)
- Évaluer les besoins en main-d'œuvre (QEC, 600→16 000 spécialistes d'ici 2030)
- Étudier la feuille de route : avantage quantique pratique 2027-2029
- Maîtriser la standardisation post-quantique (NIST) et son impact
- Implémenter un benchmark comparatif classique vs quantique

---

## Motivation

**Où en est-on vraiment ?** Les médias alternent entre « l'ordinateur quantique va tout révolutionner demain » et « c'est une arnaque, ça ne marchera jamais ». La réalité est entre les deux : des progrès spectaculaires ont eu lieu (Google Willow, Harvard/QuEra 48 qubits logiques, Microsoft Majorana 1), mais des défis immenses restent.

**Le triple défi.** Pour construire un ordinateur quantique utile, il faut résoudre simultanément trois problèmes :
1. **Quantité** : avoir assez de qubits physiques (des millions)
2. **Qualité** : avoir des qubits assez bons pour la correction d'erreur
3. **Connectivité** : pouvoir faire interagir n'importe quels qubits entre eux

**Le coût caché.** La correction d'erreur est le goulot d'étranglement principal. Pour un qubit logique fiable, il faut typiquement 1000 qubits physiques. Un algorithme utile (Shor pour RSA-2048) nécessite ~6000 qubits logiques → ~6 millions de qubits physiques. On en est à ~1000 qubits physiques en 2025.

**L'urgence post-quantique.** Même si l'ordinateur quantique universel arrive dans 10-15 ans, il cassera RSA et ECC. La migration vers la cryptographie post-quantique (NIST) doit commencer MAINTENANT, car les données chiffrées aujourd'hui avec RSA pourront être déchiffrées rétroactivement (« harvest now, decrypt later »).

---

## Idée principale

### Le problème du scaling

Imaginez construire un gratte-ciel. Vous ne pouvez pas juste empiler les étages : il faut des fondations solides, des ascenseurs, de l'électricité, de la plomberie, etc. De même, un ordinateur quantique ne se résume pas à « ajouter des qubits ». Chaque qubit supplémentaire ajoute :
- Des lignes de contrôle (câblage cryogénique)
- De la chaleur à évacuer (dans le cryostat)
- De la calibration (fréquences, amplitudes)
- De la correction d'erreur (qubits auxiliaires, décodage)

### L'overhead de la correction d'erreur

C'est le concept le plus important de ce chapitre. Pour protéger un qubit logique, on utilise un code quantique (ex: code de surface). Le code de surface de distance $d$ utilise $d^2$ qubits physiques par qubit logique.

**Analogie :** Imaginez vouloir envoyer un message important sans erreur. Vous pourriez le répéter 3 fois (code de répétition). Si un des 3 messages est corrompu, vous prenez la majorité. Mais cela triple la quantité d'information. Pour un ordinateur quantique, le facteur de multiplication est de ~1000x.

---

## Contenu du cours

### Section 1 : Scalabilité — le triple défi

#### 1.1 Nombre de qubits — croissance exponentielle

Le nombre de qubits physiques croît exponentiellement :

$$
N_{\text{phys}}(t) \approx N_0 \cdot 2^{(t-t_0)/\tau}, \quad \tau \sim 1.5\text{–}2 \text{ ans}
$$

**Signification :** Le nombre de qubits double tous les 1.5-2 ans — similaire à la loi de Moore pour les transistors. Mais le nombre de **qubits logiques** utiles croît beaucoup plus lentement à cause de l'overhead de correction :

$$
N_{\text{log}} = \frac{N_{\text{phys}}}{d^2}, \quad d \propto \log(1/\epsilon_{\text{phys}})
$$

| Année | Qubits physiques | Qubits logiques (d=7) | Qubits logiques (d=17) |
|-------|-----------------|----------------------|-----------------------|
| 2024 | 105 (Willow) | 2 | 0 |
| 2026 | 1000 | 20 | 3 |
| 2028 | 10000 | 200 | 35 |
| 2030 | 100000 | 2000 | 350 |

> **Exemple numérique :** Avec 10 000 qubits physiques et un code de surface de distance $d = 7$ : $N_{\text{log}} = 10000/49 \approx 204$ qubits logiques. Pour $d = 17$ : $N_{\text{log}} = 10000/289 \approx 34$. Plus la distance est grande, plus les qubits logiques sont fiables, mais moins on en a.

#### 1.2 Qualité des qubits

La métrique clé est le rapport $T_2/T_{\text{gate}}$ et le taux d'erreur par porte :

$$
Q = \left( \frac{T_2}{T_{\text{gate}}} \right)^{-1} \cdot \frac{1}{\epsilon_{\text{2Q}}}
$$

| Architecture | $\epsilon_{\text{1Q}}$ | $\epsilon_{\text{2Q}}$ | $T_2$ | $Q$ |
|-------------|----------------------|----------------------|-------|-----|
| Supraconducteur | $10^{-4}$ | $10^{-3}$ | $100\,\mu$s | $10^3$ |
| Atomes neutres | $10^{-5}$ | $5 \times 10^{-3}$ | $1$ s | $10^5$ |
| Ions piégés | $10^{-5}$ | $10^{-4}$ | $10$ s | $10^7$ |
| Topologique | $10^{-7}$ | — | Protection | $\infty$ (théorique) |

**Signification :** $Q$ est un facteur de qualité global. Plus $Q$ est grand, moins l'overhead de correction est important. Les ions piégés ont le meilleur $Q$, mais le scaling est limité. Les supraconducteurs ont un $Q$ modeste mais excellent à grande échelle.

#### 1.3 Connectivité

La connectivité est limitée par la topologie physique :
- Grille 2D : degré moyen ~3-4 (supraconducteurs)
- Atomes neutres : degré variable (reconfigurable)
- Photonique : degré élevé (réseau)

Le **coût de routage** pour les opérations non-locales :

$$
\text{Cost}_{\text{SWAP}} = O(\text{diamètre du graphe}) \quad \text{portes SWAP}
$$

**Signification :** Sur une grille 2D de $N$ qubits, le diamètre est $O(\sqrt{N})$. Pour faire interagir deux qubits aux opposés d'une grille de 1000 qubits, il faut ~30 SWAP — chaque SWAP ajoutant des erreurs.

---

### Section 2 : Coût de la correction d'erreur

#### 2.1 Overhead physique/logique

Le ratio $r = N_{\text{phys}} / N_{\text{log}}$ dépend du code et du taux d'erreur :

$$
r_{\text{surface}} = \left( \frac{2\log(1/\epsilon_{\text{log}})}{\log(1/\epsilon_{\text{phys}}) - \log(p_{\text{th}})} \right)^2
$$

**Signification physique :**
- $\epsilon_{\text{phys}}$ = taux d'erreur physique par porte
- $\epsilon_{\text{log}}$ = taux d'erreur logique souhaité
- $p_{\text{th}}$ = seuil de correction d'erreur (~1% pour le code de surface)
- Plus $\epsilon_{\text{phys}}$ est petit (meilleurs qubits), moins on a besoin de qubits physiques par qubit logique

#### 2.2 Budget de ressources pour des algorithmes concrets

| Ressource | RSA-2048 (Shor) | Grover 256-bit | VQE (100 spins) |
|-----------|-----------------|----------------|-----------------|
| Qubits logiques | $6144$ | $256$ | $100$ |
| Portes logiques | $1.5 \times 10^{12}$ | $10^8$ | $10^6$ |
| Qubits physiques (surface, $p=10^{-3}$) | $1.5 \times 10^8$ | $4096$ | $900$ |
| Temps d'exécution | ~$10^6$ s (~12 jours) | ~20 s | ~0.15 s |
| Énergie | ~10 MW | ~1 kW | ~100 W |

> **Exemple :** Pour Shor RSA-2048 avec $p_{\text{phys}} = 10^{-3}$ : il faut 6144 qubits logiques, chacun nécessitant ~25 qubits physiques (distance $d=5$), soit ~150 000 qubits physiques. Le temps d'exécution est ~$10^5$ secondes. C'est faisable en principe, mais pas avant 2035+.

---

### Section 3 : Main-d'œuvre et formation

#### 3.1 État des lieux (2026)

- **600-700 spécialistes mondiaux** en correction d'erreur quantique
- Demande projetée : **5000-16 000 d'ici 2030**
- Croissance >50% par an

$$
\text{Spécialistes 2030} = \text{Spécialistes 2026} \times \left(1 + r_{\text{croissance}}\right)^{\Delta t}
$$

avec $r_{\text{croissance}} \sim 0.5$-$0.7$ par an. Pour $r = 0.6$ : $650 \times 1.6^4 \approx 650 \times 6.55 \approx 4260$.

#### 3.2 Compétences requises

| Domaine | Compétence | Priorité |
|---------|-----------|----------|
| Théorie | Codes stabilisateurs, QEC, décodeurs | Critique |
| Simulation | Stim, QuTiP, Qiskit | Élevée |
| Hardware | Compréhension du bruit physique | Élevée |
| Algorithmique | Circuits quantiques, optimisation | Moyenne |
| Software | Python, C++, parallélisation | Moyenne |

---

### Section 4 : Feuille de route 2026-2035

#### 4.1 Jalons clés

| Année | Jalon | Architecture probable |
|-------|-------|----------------------|
| 2026 | 1000 qubits physiques, QEC robuste | Supra, atomes neutres |
| 2027 | Premier qubit logique topologique | Topologique (MS) |
| 2028 | 100 qubits logiques (multi-codes) | Atomes neutres + QLDPC |
| 2029 | Avantage quantique pratique (optimisation) | Hybride |
| 2030 | 10 000 qubits physiques, 1000 logiques | Multi-plateforme |
| 2032 | Calculateur quantique modulaire | Photonique + réseau |
| 2035 | 1 million de qubits logiques | Intégration hétérogène |

$$
\text{Avantage} = \begin{cases}
\text{Démontré (simulation)} & 2025\text{–}2027 \\
\text{Pratique (niche)} & 2027\text{–}2029 \\
\text{Industriel} & 2029\text{–}2032 \\
\text{Généralisé} & 2032\text{–}2035
\end{cases}
$$

---

### Section 5 : Standardisation post-quantique (NIST)

#### 5.1 Le problème

Les ordinateurs quantiques de demain briseront RSA et ECC :

$$
\text{RSA-2048} \xrightarrow{\text{Shor}} O(10^8) \text{ portes logiques}
$$

**Signification :** Un ordinateur quantique avec ~6000 qubits logiques peut factoriser RSA-2048 en ~8 heures. Cela casserait la majorité du chiffrement Internet (HTTPS, emails, signatures électroniques).

**Menace « Harvest Now, Decrypt Later » :** Des adversaires stockent dès maintenant des communications chiffrées avec RSA. Dans 10-15 ans, quand l'ordinateur quantique sera disponible, ils pourront les déchiffrer rétroactivement. D'où l'urgence de migrer MAINTENANT.

#### 5.2 Algorithmes NIST standardisés (2024)

| Algorithme | Type | Sécurité basée sur | Taille clé |
|-----------|------|-------------------|-----------|
| CRYSTALS-Kyber (ML-KEM) | Encapsulation clé | Lattice (LWE) | 800-1568 bytes |
| CRYSTALS-Dilithium (ML-DSA) | Signature | Lattice (LWE) | 1300-2500 bytes |
| FALCON (FN-DSA) | Signature | Lattice (NTRU) | 600-1300 bytes |
| SPHINCS+ (SLH-DSA) | Signature | Hash functions | 8000-50000 bytes |

**Contrainte :** Les tailles de clé et signatures sont $10\times$ à $100\times$ plus grandes que RSA/ECC. Cela impacte les protocoles réseau (TLS, IPsec) et les systèmes embarqués.

---

## Exemple guidé

**Problème :** Pour $p_{\text{phys}} = 10^{-3}$ et $\epsilon_{\text{log}} = 10^{-12}$, calculer l'overhead du code de surface.

**Étape 1 — Distance du code :**
$$d = \left\lceil \frac{2\log(1/\epsilon_{\text{log}})}{\log(1/p_{\text{phys}}) - \log(p_{\text{th}})} \right\rceil = \left\lceil \frac{2 \times 12}{3 - (-2)} \right\rceil = \left\lceil \frac{24}{5} \right\rceil = 5$$

**Étape 2 — Qubits physiques par qubit logique :**
$$N_{\text{phys/log}} = d^2 = 25$$

**Étape 3 — Pour 100 qubits logiques :**
$$N_{\text{phys}} = 100 \times 25 = 2500 \text{ qubits physiques}$$

**Étape 4 — Pour Shor RSA-2048 (6144 qubits logiques) :**
$$N_{\text{phys}} = 6144 \times 25 = 153\,600 \text{ qubits physiques}$$

**Conclusion :** Avec 150 000 qubits physiques de qualité $10^{-3}$, on peut lancer Shor RSA-2048. C'est réalisable vers 2033-2035 selon les feuilles de route.

---

## Implémentation Python

### Calcul de l'overhead de correction d'erreur

```python
# ============================================================
# Calcul de l'overhead N_phys/N_log pour différents codes
# ============================================================
import numpy as np

def compute_overhead(epsilon_phys, epsilon_log, p_th=0.01):
    """
    Calcule le nombre de qubits physiques par qubit logique
    pour un code de surface.
    
    Paramètres :
    - epsilon_phys : taux d'erreur physique par porte
    - epsilon_log : taux d'erreur logique souhaité
    - p_th : seuil de correction d'erreur du code
    
    Retourne :
    - n_phys : nombre de qubits physiques par qubit logique
    - d : distance du code
    """
    d = np.ceil(2 * np.log(1/epsilon_log) / np.log(1/epsilon_phys / p_th))
    return int(d ** 2), int(d)

# --- Balayage des paramètres ---
targets = [1e-6, 1e-10, 1e-15]      # Erreurs logiques cibles
phys_rates = [1e-3, 1e-4, 1e-5]     # Taux d'erreur physique

print("Overhead N_phys/N_log pour code de surface:")
print(f"{'eps_phys':>10} {'eps_log':>10} {'d':>5} {'N_phys/N_log':>15}")
for eps_p in phys_rates:
    for eps_l in targets:
        if eps_p < 0.01:
            n_phys, d = compute_overhead(eps_p, eps_l)
            print(f"{eps_p:>10.0e} {eps_l:>10.0e} {d:>5} {n_phys:>15d}")

# --- Overhead QLDPC (taux de code fixe) ---
def qldpc_overhead(epsilon_log, n_data=1000):
    """Pour un QLDPC avec taux de code k/n = 0.2."""
    rate = 0.2
    n_log = int(n_data * rate)
    return n_data, n_log

for eps_l in targets:
    n_phys, n_log = qldpc_overhead(eps_l, 1000)
    print(f"QLDPC (n=1000, rate=0.2) pour eps_log={eps_l:.0e}: {n_phys} physiques -> {n_log} logiques")

# --- Cas concret : 100 qubits logiques pour un algorithme utile ---
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

### Besoins en ressources par algorithme

```python
# ============================================================
# Estimation des ressources quantiques pour différents algorithmes
# ============================================================
import numpy as np

# Dictionnaire des algorithmes avec leurs besoins
algorithms = {
    "Shor RSA-2048": {"n_log": 6144, "n_gates": 1.5e12},
    "Grover 256-bit": {"n_log": 256, "n_gates": 1.0e8},
    "VQE (100 spins)": {"n_log": 100, "n_gates": 1.0e6},
    "QAOA MaxCut (100n)": {"n_log": 100, "n_gates": 1.0e5},
    "QPE (10 bits)": {"n_log": 20, "n_gates": 1.0e8},
}

p_phys = 1e-3    # Taux d'erreur physique
p_th = 0.01      # Seuil de correction
d_min = 3        # Distance minimale

print("Besoins en ressources par algorithme:")
print(f"{'Algorithme':>25} {'n_log':>8} {'n_portes':>12} {'d_min':>6} {'n_phys':>10} {'t_exec(s)':>10}")

for name, params in algorithms.items():
    n_log = params["n_log"]
    n_gates = params["n_gates"]

    # Distance nécessaire pour que l'erreur par porte logique soit < 1/n_gates
    eps_gate = 1.0 / n_gates
    d = max(d_min, int(np.ceil(2 * np.log(1/eps_gate) / np.log(1/p_phys / p_th))))
    n_phys = n_log * d ** 2  # Qubits physiques totaux

    # Temps d'exécution : n_gates * temps par porte physique * overhead de distance
    t_gate_phys = 50e-9  # 50 ns par porte physique (supraconducteur)
    t_exec = n_gates * t_gate_phys * d

    print(f"{name:>25} {n_log:>8d} {n_gates:>12.0e} {d:>6d} {n_phys:>10d} {t_exec:>10.2e}")
```

### Benchmark classique vs quantique

```python
# ============================================================
# Benchmark : simulation classique exacte vs estimation quantique
# À partir de combien de spins l'ordinateur quantique gagne-t-il ?
# ============================================================
import numpy as np
import time

def classical_simulation(n_spins, method='exact'):
    """
    Simule un système de n_spins classiquement.
    La dimension de l'espace de Hilbert est 2^n_spins.
    Au-delà de ~20 spins, la diagonalisation exacte devient très lente.
    """
    if method == 'exact':
        dim = 2 ** n_spins
        if dim > 2**20:  # Au-delà de 20 spins : trop de mémoire
            return None, dim
        start = time.time()
        # Construction d'une matrice Hamiltonienne aléatoire
        H = np.random.randn(dim, dim)
        H = (H + H.T) / 2  # Symétrique (Hermitienne)
        evals = np.linalg.eigvalsh(H)  # Diagonalisation
        elapsed = time.time() - start
        return elapsed, dim
    return None, 2**n_spins

def quantum_gate_estimate(n_spins, gate_fidelity=0.999, n_shots=1000):
    """
    Estime le temps et la probabilité de succès d'une simulation quantique.
    Le nombre de portes nécessaires croît comme 4^n (estimation conservative).
    """
    n_gates = 4 ** n_spins
    t_gate = 50e-9  # 50 ns par porte
    total_time = n_gates * t_gate * n_shots
    success_prob = gate_fidelity ** n_gates
    return total_time, success_prob

# --- Comparaison pour différentes tailles ---
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

# --- Point de croisement ---
def crossover_point(max_n=60):
    """Trouve le nombre de spins où le quantique devient plus rapide."""
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

### Projection de la feuille de route

```python
# ============================================================
# Extrapolation du nombre de qubits physiques et logiques
# ============================================================
import numpy as np

def extrapolate_qubits(years, n0=105, t0=2024, tau=1.8):
    """Extrapolation exponentielle des qubits physiques."""
    return n0 * 2 ** ((years - t0) / tau)

def extrapolate_logical(years, n0=2, t0=2024, tau_log=2.5):
    """Extrapolation des qubits logiques (croissance plus lente)."""
    return n0 * 2 ** ((years - t0) / tau_log)

years = np.arange(2024, 2036)

print("Feuille de route - Qubits physiques et logiques:")
print(f"{'Annee':>6} {'Physiques':>12} {'Logiques (estim)':>16}")
for y in years:
    n_phys = extrapolate_qubits(y)
    n_log = extrapolate_logical(y)
    print(f"{y:>6d} {n_phys:>12.0f} {n_log:>16.1f}")

# --- Probabilité de succès d'un circuit profond ---
def quantum_advantage_gate_count(N, eps_phys=1e-3, d=7):
    """
    Estime la probabilité de succès d'un circuit de 1000 portes
    sur N qubits physiques avec correction d'erreur.
    """
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

## Comparaison des technologies — état des lieux et perspectives

| Critère | Supraconducteurs | Atomes neutres | Ions piégés | Topologiques | Photonique |
|---------|-----------------|----------------|-------------|-------------|-----------|
| **Qubits physiques (2025)** | 433 (IBM Condor) | 1000+ (QuEra) | ~50 | 1 (MS Majorana 1) | ~100 logiques |
| **Qubits logiques** | 2 (Willow) | 48 (Harvard) | Démontrés | 0 | 100+ |
| **Feuille de route 2030** | 100 000 phys. | 10 000+ phys. | 200 phys. | 1000 phys. | 10 000+ |
| **Avantage pratique** | 2028-2030 | 2027-2029 | 2029-2032 | 2030+ | 2028-2030 |
| **Principal défi** | Cohérence, crosstalk | Portes 2Q | Scaling | Maturité | Portes déterministes |
| **Investissement** | Très élevé (IBM, Google) | Élevé (QuEra, Pascal) | Modéré (IonQ, Oxford) | Élevé (Microsoft) | Élevé (Photonic) |

---

## À retenir

1. **Le triple défi du scaling** : nombre de qubits (quantité), qualité des portes (fidélité), et connectivité. Les trois doivent progresser simultanément.

2. **L'overhead de correction d'erreur est le goulot principal** : typiquement 1000 qubits physiques par qubit logique pour le code de surface. Les QLDPC réduisent cet overhead à ~5-10x.

3. **La loi de Moore quantique** : le nombre de qubits physiques double tous les 1.5-2 ans. À ce rythme, 100 000 qubits physiques sont attendus vers 2030-2031.

4. **L'avantage quantique pratique** (résoudre un problème industriel plus vite/moins cher que le classique) est attendu entre 2027 et 2029 pour des cas de niche (simulation quantique, optimisation).

5. **La cryptographie post-quantique est urgente** : les algorithmes NIST (Kyber, Dilithium) doivent être déployés maintenant car la menace « harvest now, decrypt later » est réelle.

6. **La main-d'œuvre est le facteur limitant caché** : seulement 600-700 spécialistes QEC au monde en 2026, pour un besoin de 5000-16 000 d'ici 2030. La formation est un enjeu stratégique.

7. **Aucune plateforme ne domine toutes les autres** : chaque technologie a ses forces. L'avenir sera probablement hétérogène (supraconducteurs pour le calcul, photonique pour le réseau, ions pour la haute fidélité).

---

## Pièges à éviter

1. **Confondre qubits physiques et logiques** : 1000 qubits physiques ≠ 1000 qubits logiques. Avec le code de surface (d=7), 1000 qubits physiques donnent ~20 qubits logiques. Les annonces « 1000 qubits ! » sont toujours en qubits physiques.

2. **Sous-estimer l'overhead classique** : Le décodage d'un code de surface nécessite un calcul classique en temps réel (µs). Pour un million de qubits, le décodeur doit traiter ~10⁹ syndromes par seconde — un défi informatique en soi.

3. **Penser que la correction d'erreur résout tout** : La QEC protège contre les erreurs, mais introduit son propre overhead (qubits auxiliaires, mesures, décodage). Si l'erreur physique est trop haute ($> p_{\text{th}}$), la QEC empire la situation au lieu de l'améliorer.

4. **Confondre « avantage quantique » et « utilité quantique »** : L'avantage quantique = faire quelque chose d'impossible classiquement (même inutile). L'utilité quantique = faire quelque chose d'utile plus vite/mieux. On vise la seconde.

5. **Oublier le coût énergétique** : Un cryostat à 15 mK consomme ~25 kW. Un ordinateur de 1 million de qubits logiques pourrait nécessiter ~10 MW — l'équivalent d'un petit réacteur nucléaire. L'efficacité énergétique est un enjeu réel.

---

## Exercices

### Niveau 1 — Application directe

1. **Overhead de base** : Pour $p_{\text{phys}} = 10^{-3}$, calculer la distance $d$ nécessaire pour obtenir $\epsilon_{\text{log}} = 10^{-6}$, $10^{-10}$, $10^{-15}$. En déduire le nombre de qubits physiques par qubit logique.

2. **Exécuter le code** : Reproduire le calcul d'overhead et le benchmark classique/quantique. Identifier le point de croisement.

3. **Projection simple** : Si le nombre de qubits double tous les 2 ans, combien de qubits physiques en 2030 ? En 2035 ? (Base : 105 en 2024.)

### Niveau 2 — Compréhension

4. **Budget de ressources** : Estimer le nombre de qubits et le temps nécessaire pour un circuit de $10^{12}$ portes logiques sur une architecture à 10 000 qubits physiques avec $\epsilon_{\text{phys}} = 10^{-3}$.

5. **Besoins en main-d'œuvre** : En supposant une croissance de 60% par an, calculer le nombre de spécialistes QEC nécessaires en 2027, 2028, 2029 et 2030. Discuter des implications pour la formation.

6. **Benchmark Heisenberg** : Comparer le temps d'exécution classique vs quantique pour la simulation d'un modèle de Heisenberg à $n$ spins ($n=10$ à $n=100$). Identifier le point de croisement pour une fidélité de porte de 99.9%.

### Niveau 3 — Défi

7. **Overhead QLDPC vs surface** : Tracer $N_{\text{phys}}/N_{\text{log}}$ en fonction de $\epsilon_{\text{log}}$ entre $10^{-3}$ et $10^{-15}$ pour les codes de surface et QLDPC. À partir de quel $\epsilon_{\text{log}}$ le QLDPC devient-il plus avantageux ?

8. **Analyse post-quantique** : Comparer les tailles de clé et signatures des algorithmes NIST (Kyber, Dilithium, FALCON, SPHINCS+) avec RSA-2048. Discuter de l'impact sur TLS 1.3 et les protocoles IoT.

9. **Feuille de route personnalisée** : Pour un algorithme de votre choix (VQE, QAOA, Shor, Grover), construire une feuille de route détaillée : nombre de qubits nécessaires, qualité requise, année estimée de réalisation, plateforme la plus adaptée.

---

## Pour aller plus loin

- **Google Quantum AI** (2024). "Quantum error correction below the surface code threshold." *Nature*, 636, 74–79. — Démonstration historique de la QEC sous le seuil.
- **Bluvstein, D.** et al. (2025). "Logical quantum processor with 48 logical qubits." *Nature*. — Record de qubits logiques.
- **Microsoft Quantum** (2025). "Majorana 1: A topological qubit platform." *Nature*. — Première puce topologique.
- **NIST** (2024). "Post-Quantum Cryptography: Selected Algorithms 2024." *NIST IR 8413*. — Standards post-quantiques.
- **McKinsey & Company** (2025). "Quantum computing: An emerging ecosystem and industry use cases." — Analyse de marché.
- **Preskill, J.** (2018). "Quantum Computing in the NISQ era and beyond." *Quantum*, 2, 79. — Article fondateur sur l'ère NISQ.
