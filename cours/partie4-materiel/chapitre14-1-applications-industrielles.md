# Chapitre 14.1 — Applications industrielles du calcul quantique

## Ce que vous allez apprendre

- Comprendre le potentiel de la chimie quantique (simulation moléculaire, drug discovery)
- Maîtriser l'optimisation quantique (QAOA, QUBO) pour la finance et la logistique
- Introduire le Quantum Machine Learning (QML) et les réseaux de neurones quantiques
- Analyser les projections de marché (McKinsey : 72 G$ d'ici 2035)
- Implémenter un VQE pour H₂ et une classification QNN avec PennyLane

---

## Motivation

**La question que tout le monde pose.** « Le calcul quantique, c'est bien beau en théorie, mais ça sert à quoi concrètement ? » Ce chapitre répond à cette question en passant en revue les applications les plus prometteuses.

**Le constat.** Les ordinateurs quantiques ne remplaceront PAS les ordinateurs classiques. Ils sont spécialisés pour trois types de problèmes :
1. **Simuler la nature** : les molécules, les matériaux, les réactions chimiques obéissent aux lois quantiques — un ordinateur quantique les simule naturellement
2. **Optimiser** : trouver le meilleur arrangement parmi un nombre exponentiel de possibilités (logistique, finance, planification)
3. **Apprendre** : certains problèmes de machine learning pourraient bénéficier de l'espace de Hilbert exponentiellement grand

**L'état actuel.** On est en 2026. Les ordinateurs quantiques sont encore en phase NISQ (Noisy Intermediate-Scale Quantum). Les applications pratiques à grande échelle nécessiteront des qubits corrigés (fault-tolerant), probablement à partir de 2029-2032. Mais des avantages de niche sont possibles dès 2027.

**Le marché.** McKinsey projette un marché de 53-92 G$ d'ici 2035, avec la chimie/pharma en tête (27-45 G$), suivies de la finance (8-15 G$) et la logistique (6-10 G$).

---

## Idée principale

### Pourquoi un ordinateur quantique pour la chimie ?

Imaginez vouloir simuler une molécule de caféine (C₈H₁₀N₄O₂) avec 24 atomes. Elle a ~150 électrons. En mécanique quantique, chaque électron peut être dans une superposition d'états. L'espace de Hilbert croît comme $2^N$ où $N$ est le nombre d'orbitales. Pour la caféine : $N \sim 100$ orbitales → $2^{100} \approx 10^{30}$ dimensions. Aucun ordinateur classique ne peut stocker un vecteur dans cet espace.

Mais un ordinateur quantique de 100 qubits vit naturellement dans un espace de $2^{100}$ dimensions ! Il peut **être** la molécule, pas juste la simuler. C'est l'idée de Feynman (1982) : utiliser un système quantique pour en simuler un autre.

### L'optimisation : trouver l'aiguille dans la botte de foin

Un problème de logistique (livrer 100 colis dans 100 villes) a $100! \approx 10^{158}$ arrangements possibles. Un QAOA (Quantum Approximate Optimization Algorithm) explore ces possibilités en superposition et utilise l'interférence quantique pour amplifier les bonnes solutions.

**Analogie :** Classiquement, c'est comme envoyer 1000 livreurs explorer 1000 chemins différents. Quantiquement, c'est comme envoyer un seul livreur qui emprunte TOUS les chemins en même temps (superposition) et dont les copies sur les mauvais chemins s'annulent (interférence destructive).

---

## Contenu du cours

### Section 1 : Chimie quantique — simuler les molécules

#### 1.1 Le problème fondamental

Résoudre l'équation de Schrödinger pour une molécule de $M$ électrons :

$$
H\Psi = E\Psi, \quad H = -\sum_i \frac{\hbar^2}{2m_e}\nabla_i^2 - \sum_{i,I} \frac{Z_I e^2}{|\mathbf{r}_i - \mathbf{R}_I|} + \sum_{i<j} \frac{e^2}{|\mathbf{r}_i - \mathbf{r}_j|}
$$

**Signification physique des trois termes :**
1. $-\frac{\hbar^2}{2m_e}\nabla_i^2$ = énergie cinétique de l'électron $i$ (il bouge)
2. $-\frac{Z_I e^2}{|\mathbf{r}_i - \mathbf{R}_I|}$ = attraction entre l'électron $i$ et le noyau $I$ (Coulomb)
3. $+\frac{e^2}{|\mathbf{r}_i - \mathbf{r}_j|}$ = répulsion entre électrons $i$ et $j$ (le terme qui rend le problème difficile !)

Le 3ème terme couple tous les électrons entre eux : on ne peut pas les traiter indépendamment. La dimension de l'espace de Hilbert croît exponentiellement avec $M$.

> **Exemple :** La molécule de H₂ (2 électrons) est triviale. FeMoco (catalyseur de fixation d'azote, ~100 électrons corrélés) est impossible classiquement — et c'est un problème industriel énorme (les engrais azotés consomment 2% de l'énergie mondiale).

#### 1.2 VQE — Variational Quantum Eigensolver

Le VQE est l'algorithme phare pour la chimie quantique sur les machines NISQ :

$$
E(\theta) = \langle 0 | U^\dagger(\theta) H U(\theta) | 0 \rangle, \quad \theta^* = \arg\min_\theta E(\theta)
$$

**Signification physique :**
- $U(\theta)$ = circuit quantique paramétré (l'« ansatz ») — il prépare un état candidat
- $H$ = Hamiltonien moléculaire (encodé en opérateurs de Pauli via transformation Jordan-Wigner)
- On mesure l'énergie moyenne $\langle H \rangle$ sur le processeur quantique
- Un optimiseur classique ajuste $\theta$ pour minimiser l'énergie
- Le théorème variationnel garantit : $E(\theta) \geq E_0$ (l'énergie trouvée est toujours une borne supérieure)

**Analogie :** C'est comme chercher le point le plus bas d'une vallée. Le circuit quantique évalue l'altitude pour une position donnée ($\theta$), et l'optimiseur classique décide où aller ensuite.

> **Exemple :** Pour H₂ (base STO-3G) : 4 qubits, ~10 termes de Pauli dans $H$. L'énergie exacte est -1.137 Ha. Le VQE converge en ~50 itérations.

#### 1.3 Applications pharmaceutiques

| Application | Impact | Horizon |
|------------|--------|---------|
| Docking moléculaire | $10^6\times$ accélération | 2027–2030 |
| Simulation de métalloenzymes | Nouveaux catalyseurs | 2028–2032 |
| Drug discovery (small molecules) | R&D réduit de 50% | 2030–2035 |
| Protéines (folding) | Médecine personnalisée | 2030+ |

---

### Section 2 : Optimisation quantique

#### 2.1 Problèmes QUBO

Le format QUBO (Quadratic Unconstrained Binary Optimization) est central en optimisation quantique :

$$
\min_{x \in \{0,1\}^n} x^T Q x + c^T x
$$

**Signification :** $x$ est un vecteur de $n$ variables binaires (0 ou 1). $Q$ est une matrice de coûts d'interaction. $c$ est un vecteur de coûts individuels. Le problème : trouver la configuration $x$ qui minimise le coût total.

> **Exemple :** MaxCut — partitionner un graphe en deux groupes pour maximiser les arêtes entre groupes. $x_i = 0$ ou $1$ selon le groupe. $Q_{ij} = -1$ si $i,j$ sont connectés.

#### 2.2 QAOA — Quantum Approximate Optimization Algorithm

Le QAOA utilise $p$ couches alternant deux Hamiltoniens :

$$
|\gamma, \beta\rangle = e^{-i\beta_p H_B} e^{-i\gamma_p H_C} \cdots e^{-i\beta_1 H_B} e^{-i\gamma_1 H_C} |+\rangle^{\otimes n}
$$

avec :
- $H_C = \sum_{\langle i,j \rangle} w_{ij} Z_i Z_j$ : encode le problème (coût)
- $H_B = \sum_i X_i$ : le « mélangeur » (exploration)

**Signification physique :**
- $H_C$ est appliqué pendant un temps $\gamma$ : il encode le paysage de coût dans la phase
- $H_B$ est appliqué pendant un temps $\beta$ : il fait « tunnel » entre les configurations
- L'alternance crée des interférences constructives vers les bonnes solutions
- Pour $p \to \infty$, le QAOA converge vers la solution optimale

$$
F_p = \frac{\langle \gamma, \beta | H_C | \gamma, \beta \rangle}{E_{\text{min}}}, \quad \lim_{p\to\infty} F_p = 1
$$

> **Exemple numérique :** MaxCut sur un cycle à 4 nœuds avec $p = 1$ : le QAOA trouve un ratio d'approximation de 0.69 (meilleur que le classique glouton 0.5). Avec $p = 5$ : >0.95.

#### 2.3 Applications sectorielles

| Secteur | Problème | Algorithme |
|---------|----------|------------|
| Finance | Portfolio optimization | QAOA, VQE |
| Finance | Risk analysis, VaR | Amplitude estimation |
| Logistique | Vehicle routing | QUBO, QAOA |
| Logistique | Supply chain optimization | Hybride quantique-classique |
| Énergie | Grid optimization | QAOA |
| Transport | Traffic flow | QUBO |

---

### Section 3 : Quantum Machine Learning (QML)

#### 3.1 Quantum Kernels

Les cartes de caractéristiques quantiques projettent les données dans un espace de Hilbert :

$$
\Phi(x) = U_{\phi(x)} |0\rangle^{\otimes n}, \quad K(x_i, x_j) = |\langle \Phi(x_i) | \Phi(x_j) \rangle|^2
$$

**Signification :** Le circuit $U_{\phi(x)}$ encode les données $x$ dans un état quantique. Le kernel $K$ mesure la « similarité quantique » entre deux points de données. L'espace de Hilbert de dimension $2^n$ permet des séparations non-linéaires impossibles classiquement.

#### 3.2 Quantum Neural Networks (QNN)

Un QNN alterne encodage des données et couches variationnelles :

$$
f(x; \theta) = \langle 0 | U^\dagger(x) V^\dagger(\theta) M V(\theta) U(x) | 0 \rangle
$$

**Signification :**
- $U(x)$ : encode les données d'entrée dans l'état quantique
- $V(\theta)$ : couches de portes paramétrées (comme les poids d'un réseau de neurones classique)
- $M$ : mesure (observable de Pauli Z typiquement)
- On entraîne $\theta$ par descente de gradient pour minimiser une fonction de coût

#### 3.3 Avantage quantique en QML — mythe et réalité

L'avantage potentiel vient de :
- **Expressivité** : l'espace de Hilbert de dimension $2^n$ permet des frontières de décision très complexes
- **Concentration** : les données peuvent être encodées dans un espace exponentiellement grand

**Mais** la « malédiction de la mesure » (shot noise) limite l'avantage pratique : il faut un nombre de mesures (shots) qui croît avec la précision souhaitée.

---

## Exemple guidé

**Problème :** Trouver l'énergie de l'état fondamental de H₂ avec le VQE.

**Étape 1 — Hamiltonien moléculaire :**
Dans la base STO-3G, après transformation Jordan-Wigner, l'Hamiltonien de H₂ s'écrit comme somme de termes de Pauli :
$$H = c_0 I + c_1 Z_0 + c_2 Z_1 + c_3 Z_0 Z_1 + c_4 X_0 X_1 + c_5 Y_0 Y_1$$
avec des coefficients $c_i$ qui dépendent de la distance interatomique (0.74 Å à l'équilibre).

**Étape 2 — Ansatz :**
On choisit un ansatz simple (UCCSD à 1 paramètre) :
$$U(\theta) = e^{\theta(X_0 Y_1 - Y_0 X_1)/2}$$

**Étape 3 — Mesure :**
Pour chaque $\theta$, on prépare $U(\theta)|00\rangle$ et on mesure $\langle H \rangle$ (moyenne de nombreuses mesures).

**Étape 4 — Optimisation :**
L'optimiseur classique (gradient descent, Adam) ajuste $\theta$ pour minimiser $\langle H \rangle$.

**Résultat attendu :** $E_{\text{VQE}} \approx -1.136$ Ha (énergie exacte dans STO-3G).

---

## Implémentation Python

### Classification avec PennyLane (QNN)

```python
# ============================================================
# Réseau de neurones quantique (QNN) pour classification
# Implémentation avec PennyLane
# ============================================================
import pennylane as qml
import numpy as np

# --- Architecture du QNN ---
n_qubits = 4     # Nombre de qubits (détermine la dimension de l'espace de features)
n_layers = 3     # Nombre de couches variationnelles

# Device PennyLane : simulateur quantique par défaut
dev = qml.device("default.qubit", wires=n_qubits)

def feature_map(x, wires):
    """
    Encode les données x dans l'état quantique.
    Chaque feature est encodée comme une rotation RX sur un qubit.
    """
    for i, w in enumerate(wires):
        qml.RX(x[i % len(x)], wires=w)

def variational_layer(params, wires):
    """
    Couche variationnelle : rotations RY + CNOT en anneau.
    C'est l'équivalent quantique d'une couche dense dans un réseau classique.
    """
    n = len(wires)
    # Rotation individuelle sur chaque qubit
    for i in range(n):
        qml.RY(params[i], wires=wires[i])
    # CNOT en anneau : intrique les qubits voisins
    for i in range(n - 1):
        qml.CNOT(wires=[wires[i], wires[i + 1]])
    qml.CNOT(wires=[wires[-1], wires[0]])  # Ferme l'anneau

@qml.qnode(dev)
def qnn_circuit(x, params):
    """Circuit complet du QNN : encodage + couches variationnelles + mesure."""
    feature_map(x, wires=range(n_qubits))
    for l in range(n_layers):
        variational_layer(params[l], wires=range(n_qubits))
    # Mesure de l'espérance de Z sur chaque qubit
    return [qml.expval(qml.PauliZ(i)) for i in range(n_qubits)]

def qnn_predict(x, params):
    """Prédiction : somme des attentes de Z, puis signe."""
    outputs = qnn_circuit(x, params)
    return np.sign(np.sum(outputs))

# --- Génération de données : classification circulaire ---
np.random.seed(42)
X = np.random.randn(100, 2)  # 100 points en 2D
# Labels : +1 si dans le cercle unité, -1 sinon
y = np.array([1 if x[0]**2 + x[1]**2 < 1.0 else -1 for x in X])

# Paramètres initiaux (petits, aléatoires)
params = np.random.randn(n_layers, n_qubits) * 0.1

def square_loss(pred, target):
    """Fonction de coût : erreur quadratique moyenne."""
    return np.mean((pred - target) ** 2)

def accuracy(preds, targets):
    """Fraction de prédictions correctes."""
    return np.mean(preds == targets)

# --- Évaluation avant entraînement ---
preds_classical = []
for x in X[:20]:
    preds_classical.append(qnn_predict(x, params))

preds_classical = np.array(preds_classical)
acc_before = accuracy(preds_classical, y[:20])
print(f"Accuracy avant entrainement: {acc_before:.3f}")

# --- Fonction de coût pour l'optimisation ---
def cost_fn(params):
    preds = []
    for x in X[:30]:
        outputs = qnn_circuit(x, params)
        pred = np.sign(np.sum(outputs))
        preds.append(pred)
    return square_loss(np.array(preds), y[:30])

# --- Entraînement ---
opt = qml.AdamOptimizer(stepsize=0.1)

for step in range(50):
    params = opt.step(lambda p: cost_fn(p), params)
    if step % 10 == 0:
        cost_val = cost_fn(params)
        print(f"Step {step:3d}: cost = {cost_val:.4f}")

# --- Évaluation après entraînement ---
preds_trained = []
for x in X[30:50]:
    preds_trained.append(qnn_predict(x, params))

preds_trained = np.array(preds_trained)
acc_after = accuracy(preds_trained, y[30:50])
print(f"Accuracy apres entrainement: {acc_after:.3f}")
```

### VQE pour H₂ avec PennyLane

```python
# ============================================================
# VQE pour la molécule H₂ (hydrogène diatomique)
# Trouver l'énergie de l'état fondamental
# ============================================================
import pennylane as qml
from pennylane import numpy as np

# --- Construction de l'Hamiltonien moléculaire ---
# H₂ à la distance d'équilibre (0.74 Å = 1.4 Bohr)
# Base STO-3G : 2 orbitales spatiales → 4 qubits (spin-up + spin-down)
H2_hamiltonian = qml.qchem.molecular_hamiltonian(
    ["H", "H"],
    np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.74]),  # Coordonnées des atomes
    basis="sto-3g",
    active_electrons=2
)[0]

# Device : 4 qubits
dev_vqe = qml.device("default.qubit", wires=4)

# --- Ansatz : UCCSD simplifié ---
def ansatz(params, wires):
    """
    Ansatz de type UCCSD (Unitary Coupled Cluster).
    1. État de référence Hartree-Fock : |1100> (2 électrons dans les 2 premières orbitales)
    2. Rotations RY pour mixer les configurations
    3. CNOT pour intriquer
    """
    qml.BasisState(np.array([1, 1, 0, 0]), wires=wires)  # État HF
    # Première couche de rotations
    for i in range(4):
        qml.RY(params[i], wires=wires[i])
    # Intrication
    qml.CNOT(wires=[0, 1])
    qml.CNOT(wires=[2, 3])
    # Deuxième couche de rotations
    for i in range(4):
        qml.RY(params[4+i], wires=wires[i])

@qml.qnode(dev_vqe)
def cost_fn(params):
    """Coût VQE : énergie attendue <H> pour les paramètres theta."""
    ansatz(params, range(4))
    return qml.expval(H2_hamiltonian)

# --- Optimisation ---
params_init = np.random.randn(8) * 0.1

opt_vqe = qml.GradientDescentOptimizer(stepsize=0.4)
energy_hist = []

for step in range(100):
    params_init, energy = opt_vqe.step_and_cost(lambda p: cost_fn(p), params_init)
    energy_hist.append(energy)
    if step % 20 == 0:
        print(f"Step {step:3d}: energy = {energy:.6f} Ha")

print(f"\nEnergie finale VQE H2: {energy:.6f} Ha")
print(f"Energie exacte attendue: -1.136 Ha (approx)")
print(f"Erreur: {abs(energy - (-1.136)):.6f} Ha")
```

### QAOA pour MaxCut

```python
# ============================================================
# QAOA pour le problème MaxCut
# Partitionner un graphe en 2 groupes pour maximiser les arêtes coupées
# ============================================================
import pennylane as qml
from pennylane import numpy as np

# Graphe : cycle à 4 nœuds + diagonale
edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
n_nodes_qaoa = 4

def qaoa_layer(gamma, beta, wires):
    """
    Une couche QAOA :
    1. Evolution sous H_C (problème) pendant temps gamma
    2. Evolution sous H_B (mélangeur) pendant temps beta
    """
    # H_C : pour chaque arête, CNOT + RZ(2*gamma) + CNOT
    for (u, v) in edges:
        qml.CNOT(wires=[wires[u], wires[v]])
        qml.RZ(2 * gamma, wires=wires[v])
        qml.CNOT(wires=[wires[u], wires[v]])
    # H_B : rotation RX sur chaque qubit
    for w in wires:
        qml.RX(2 * beta, wires=w)

@qml.qnode(dev_vqe)
def qaoa_circuit(params, wires):
    """Circuit QAOA complet avec p couches."""
    n_layers = len(params) // 2
    # État initial : superposition uniforme |+>^n
    for w in wires:
        qml.Hadamard(wires=w)
    # Couches QAOA alternées
    for l in range(n_layers):
        qaoa_layer(params[l], params[n_layers + l], wires)
    return [qml.expval(qml.PauliZ(w)) for w in wires]

def maxcut_cost(params, wires):
    """
    Coût MaxCut : pour chaque arête (u,v), contribution = 0.5*(1 - Z_u*Z_v).
    On maximise le nombre d'arêtes coupées.
    """
    z = qaoa_circuit(params, wires)
    cost = 0.0
    for (u, v) in edges:
        cost += 0.5 * (1 - z[u] * z[v])
    return -cost  # Négatif car on minimise

# --- Optimisation ---
params_qaoa = np.random.randn(4) * 0.1  # p=2 couches
opt_qaoa = qml.GradientDescentOptimizer(stepsize=0.5)

for step in range(50):
    params_qaoa = opt_qaoa.step(lambda p: maxcut_cost(p, range(n_nodes_qaoa)), params_qaoa)
    if step % 10 == 0:
        cost_val = maxcut_cost(params_qaoa, range(n_nodes_qaoa))
        print(f"QAOA step {step}: cost = {-cost_val:.4f}")
```

### Quantum Kernel Method

```python
# ============================================================
# Méthode des noyaux quantiques (Quantum Kernel)
# Classification via une matrice de similarité quantique
# ============================================================
import pennylane as qml
from pennylane import numpy as np

n_qubits_kernel = 2
dev_kernel = qml.device("default.qubit", wires=n_qubits_kernel)

@qml.qnode(dev_kernel)
def kernel_circuit(x1, x2):
    """
    Circuit de kernel : encode x1 et x2, puis mesure la probabilité
    de revenir à |00>. Plus c'est élevé, plus x1 et x2 sont similaires.
    """
    for i in range(n_qubits_kernel):
        qml.Hadamard(wires=i)
        qml.RX(x1[i], wires=i)
        qml.RZ(x2[i], wires=i)
    qml.CNOT(wires=[0, 1])
    for i in range(n_qubits_kernel):
        qml.RX(x2[i], wires=i)
        qml.RZ(x1[i], wires=i)
    return qml.probs(wires=[0, 1])

def quantum_kernel(x1, x2):
    """Kernel quantique : somme des probabilités |00> et |11>."""
    probs = kernel_circuit(x1, x2)
    return probs[0] + probs[3]

# --- Données d'entraînement ---
X_train_k = np.random.randn(20, 2)
y_train_k = np.array([1 if x[0]*x[1] > 0 else -1 for x in X_train_k])

# --- Construction de la matrice de kernel ---
K_matrix = np.zeros((len(X_train_k), len(X_train_k)))
for i in range(len(X_train_k)):
    for j in range(i, len(X_train_k)):
        k_val = quantum_kernel(X_train_k[i], X_train_k[j])
        K_matrix[i, j] = k_val
        K_matrix[j, i] = k_val

print(f"Matrice de kernel quantique: {K_matrix.shape}")
print(f"Valeurs propres du kernel: {np.sort(np.linalg.eigvalsh(K_matrix))[:5]}")

# --- Classification par kernel ---
alpha_k = np.linalg.solve(K_matrix + 0.01 * np.eye(len(X_train_k)), y_train_k)
pred_k = np.sign(K_matrix @ alpha_k)
acc_k = np.mean(pred_k == y_train_k)
print(f"Accuracy du kernel quantique: {acc_k:.3f}")
```

---

## Comparaison des technologies pour les applications

| Application | Meilleure plateforme | Horizon | Qubits nécessaires |
|------------|---------------------|---------|-------------------|
| Chimie (H₂, LiH) | Supraconducteurs, Photonique | 2025-2027 | 10-50 |
| Chimie (FeMoco) | Topologique, Supraconducteurs | 2030-2035 | 10 000+ |
| Optimisation (MaxCut, TSP) | Supraconducteurs, Atomes neutres | 2027-2030 | 100-1000 |
| Finance (portfolio) | Supraconducteurs | 2027-2030 | 100-500 |
| QML (classification) | Photonique, Supraconducteurs | 2026-2028 | 10-100 |
| Cryptanalyse (Shor) | Topologique, Supraconducteurs | 2035+ | 10⁶+ |

---

## À retenir

1. **Le VQE** est l'algorithme roi pour la chimie quantique NISQ. Il combine un circuit quantique (prépare l'état) avec un optimiseur classique (minimise l'énergie). Le théorème variationnel garantit de converger vers l'énergie fondamentale.

2. **Le QAOA** est l'algorithme principal pour l'optimisation combinatoire. Il alterne evolution sous le problème ($H_C$) et le mélangeur ($H_B$). La performance s'améliore avec le nombre de couches $p$.

3. **Le QML** exploite l'espace de Hilbert exponentiel pour des features quantiques. Les quantum kernels peuvent capturer des patterns non-linéaires impossibles classiquement, mais l'avantage pratique reste à démontrer.

4. **Le marché** est projeté à 53-92 G$ d'ici 2035 (McKinsey), dominé par la chimie/pharma et la finance.

5. **L'avantage quantique pratique** (utile industriellement) est attendu entre 2027 et 2032, selon les secteurs. La chimie sera probablement le premier domaine touché.

6. **Les algorithmes hybrides** (quantique-classique comme VQE, QAOA) sont les seuls viables en phase NISQ. Les algorithmes purement quantiques (Shor, QPE) nécessitent des qubits fault-tolerant.

---

## Pièges à éviter

1. **Confondre avantage quantique « suprématie » et « utilité »** : La suprématie quantique (Google, 2019) montre qu'un QC peut faire quelque chose d'impossible classiquement — mais d'aucune utilité pratique. L'utilité quantique signifie résoudre un problème industriellement pertinent plus vite.

2. **Penser que le QAOA bat toujours les classiques** : Pour beaucoup de problèmes d'optimisation, les algorithmes classiques (recuit simulé, algorithmes génétiques) sont très compétitifs. Le QAOA n'a d'avantage que pour des problèmes spécifiques et avec suffisamment de couches.

3. **Surenchérir les capacités du QML** : Les QNN ne sont PAS des réseaux de neurones classiques plus puissants. Ils ont des propriétés différentes (expressivité, barrens plateaus) mais pas nécessairement un avantage systématique.

4. **Oublier le bruit** : En phase NISQ, le bruit limite sévèrement la profondeur des circuits. Un VQE avec un ansatz trop profond donnera des résultats inutilisables sur du hardware réel.

5. **Confondre qubits logiques et physiques** : Les projections de marché supposent des qubits logiques (corrigés). Le passage de 1000 qubits physiques à 1 qubit logique fiable nécessite encore des années de développement.

---

## Exercices

### Niveau 1 — Application directe

1. **VQE H₂** : Implémenter un VQE pour H₂ avec PennyLane. Utiliser l'Hamiltonien STO-3G. Trouver l'énergie de l'état fondamental et comparer avec la valeur exacte (-1.136 Ha).

2. **Exécuter le QNN** : Reproduire la classification circulaire avec le QNN PennyLane. Tracer la frontière de décision apprise.

3. **QAOA MaxCut basique** : Implémenter QAOA pour MaxCut sur un graphe complet à 4 nœuds ($K_4$). Quel est le nombre maximum d'arêtes coupables ?

### Niveau 2 — Compréhension

4. **QAOA convergence** : Tracer la performance $F_p$ en fonction du nombre de couches $p = 1, 2, 3, 5, 10$ pour MaxCut sur un graphe aléatoire à 6 nœuds.

5. **QNN vs SVM** : Comparer la performance d'un QNN (kernel quantique) vs un SVM classique sur un dataset synthétique non-linéaire (moons, circles).

6. **Portfolio optimization** : Formuler un problème de sélection de portefeuille (10 actifs, contrainte de budget) en QUBO. Résoudre avec QAOA et comparer avec scipy.optimize.

### Niveau 3 — Défi

7. **VQE avec bruit** : Simuler l'effet du bruit (dépolarisation, amortissement) sur la convergence du VQE pour H₂. À partir de quel taux d'erreur les résultats deviennent-ils inutilisables ?

8. **Scaling QAOA** : Pour MaxCut sur des graphes aléatoires de 10 à 100 nœuds, comparer le ratio d'approximation du QAOA ($p=1,3$) avec un algorithme classique glouton.

9. **Analyse de marché** : Pour le secteur pharmaceutique, construire un argumentaire détaillé sur l'apport du calcul quantique, incluant les molécules cibles, les métriques attendues et l'horizon temporel.

---

## Pour aller plus loin

- **McKinsey & Company** (2025). "Quantum computing: An emerging ecosystem and industry use cases." — Analyse de marché complète.
- **Consentino, M.** et al. (2022). "Quantum computing for finance: A review." *Nature Reviews Physics*, 4, 421–433.
- **Peruzzo, A.** et al. (2014). "A variational eigenvalue solver on a photonic quantum processor." *Nature Communications*, 5, 4213. — L'article fondateur du VQE.
- **Farhi, E., Goldstone, J. & Gutmann, S.** (2014). "A Quantum Approximate Optimization Algorithm." *arXiv:1411.4028*. — L'article fondateur du QAOA.
- **Havlíček, V.** et al. (2019). "Supervised learning with quantum-enhanced feature spaces." *Nature*, 567, 209–212.
- **Cerezo, M.** et al. (2021). "Variational quantum algorithms." *Nature Reviews Physics*, 3, 625–644. — Revue complète et pédagogique.
