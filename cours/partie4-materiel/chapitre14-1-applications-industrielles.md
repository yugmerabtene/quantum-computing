# Chapitre 14.1 — Applications industrielles du calcul quantique

## Objectifs

- Comprendre le potentiel de la chimie quantique (simulation moléculaire, drug discovery)
- Maîtriser l'optimisation quantique (finance, logistique, QAOA, QUBO)
- Introduire le Quantum Machine Learning (QML)
- Analyser les projections de marché (McKinsey 72 G$ d'ici 2035)
- Implémenter une classification simple avec QNN (PennyLane)
- Identifier les secteurs à fort impact

---

## 1. Chimie quantique

### 1.1 Simulation moléculaire

Le problème fondamental : résoudre l'équation de Schrödinger pour une molécule de $M$ électrons :

$$
H\Psi = E\Psi, \quad H = -\sum_i \frac{\hbar^2}{2m_e}\nabla_i^2 - \sum_{i,I} \frac{Z_I e^2}{|\mathbf{r}_i - \mathbf{R}_I|} + \sum_{i<j} \frac{e^2}{|\mathbf{r}_i - \mathbf{r}_j|}
$$

La dimension de l'espace de Hilbert croît exponentiellement avec $M$. Les méthodes classiques (DFT, Hartree-Fock) sont approximatives.

### 1.2 VQE (Variational Quantum Eigensolver)

Le VQE combine un circuit paramétré $U(\theta)$ avec un optimiseur classique :

$$
E(\theta) = \langle 0 | U^\dagger(\theta) H U(\theta) | 0 \rangle, \quad \theta^* = \arg\min_\theta E(\theta)
$$

L'avantage quantique apparaît pour des systèmes de $> 50$ électrons corrélés.

### 1.3 Applications pharmaceutiques

| Application | Impact | Horizon |
|------------|--------|---------|
| Docking moléculaire | $10^6\times$ accélération | 2027–2030 |
| Simulation de métalloenzymes | New catalysts | 2028–2032 |
| Drug discovery (small molecules) | R&D réduit de 50% | 2030–2035 |
| Protéines (folding) | Médecine personnalisée | 2030+ |

---

## 2. Optimisation quantique

### 2.1 Problèmes QUBO

Le format QUBO (Quadratic Unconstrained Binary Optimization) est central :

$$
\min_{x \in \{0,1\}^n} x^T Q x + c^T x
$$

où $Q$ est une matrice $n \times n$ de coefficients de couplage.

### 2.2 QAOA (Quantum Approximate Optimization Algorithm)

Le QAOA utilise $p$ couches de portes :

$$
|\gamma, \beta\rangle = e^{-i\beta_p H_B} e^{-i\gamma_p H_C} \cdots e^{-i\beta_1 H_B} e^{-i\gamma_1 H_C} |+\rangle^{\otimes n}
$$

où $H_C = \sum_i Q_{ij} Z_i Z_j$ et $H_B = \sum_i X_i$.

La performance s'améliore avec $p$ :

$$
F_p = \frac{\langle \gamma, \beta | H_C | \gamma, \beta \rangle}{E_{\text{min}}}, \quad \lim_{p\to\infty} F_p = 1
$$

### 2.3 Finance et logistique

| Secteur | Problème | Algorithme |
|---------|----------|------------|
| Finance | Portfolio optimization | QAOA, VQE |
| Finance | Risk analysis, VaR | Amplitude estimation |
| Logistique | Vehicle routing | QUBO, QAOA |
| Logistique | Supply chain optimization | Hybrid quantum-classical |
| Énergie | Grid optimization | QAOA |
| Transport | Traffic flow | QUBO |

---

## 3. Quantum Machine Learning (QML)

### 3.1 Quantum Kernels

Les cartes de caractéristiques quantiques (quantum feature maps) projettent les données dans un espace de Hilbert :

$$
\Phi(x) = U_{\phi(x)} |0\rangle^{\otimes n}, \quad K(x_i, x_j) = |\langle \Phi(x_i) | \Phi(x_j) \rangle|^2
$$

### 3.2 Quantum Neural Networks (QNN)

Un QNN alterne couches de portes paramétrées et mesures :

$$
f(x; \theta) = \langle 0 | U^\dagger(x) V^\dagger(\theta) M V(\theta) U(x) | 0 \rangle
$$

### 3.3 Avantage quantique en QML

L'avantage potentiel vient de :

- **Expressivité** : l'espace de Hilbert permet des séparations non-linéaires impossibles classiquement
- **Concentration** : les données peuvent être encodées dans un espace de dimension $2^n$

Cependant, la **malédiction de la mesure** (shot noise) limite l'avantage pratique.

---

## 4. Classification avec PennyLane (QNN)

```python
import pennylane as qml
import numpy as np

n_qubits = 4
n_layers = 3

dev = qml.device("default.qubit", wires=n_qubits)

def feature_map(x, wires):
    for i, w in enumerate(wires):
        qml.RX(x[i % len(x)], wires=w)

def variational_layer(params, wires):
    n = len(wires)
    for i in range(n):
        qml.RY(params[i], wires=wires[i])
    for i in range(n - 1):
        qml.CNOT(wires=[wires[i], wires[i + 1]])
    qml.CNOT(wires=[wires[-1], wires[0]])

@qml.qnode(dev)
def qnn_circuit(x, params):
    feature_map(x, wires=range(n_qubits))

    for l in range(n_layers):
        variational_layer(params[l], wires=range(n_qubits))

    return [qml.expval(qml.PauliZ(i)) for i in range(n_qubits)]

def qnn_predict(x, params):
    outputs = qnn_circuit(x, params)
    return np.sign(np.sum(outputs))

np.random.seed(42)
X = np.random.randn(100, 2)
y = np.array([1 if x[0]**2 + x[1]**2 < 1.0 else -1 for x in X])

params = np.random.randn(n_layers, n_qubits) * 0.1

def square_loss(pred, target):
    return np.mean((pred - target) ** 2)

def accuracy(preds, targets):
    return np.mean(preds == targets)

preds_classical = []
for x in X[:20]:
    preds_classical.append(qnn_predict(x, params))

preds_classical = np.array(preds_classical)
acc_before = accuracy(preds_classical, y[:20])
print(f"Accuracy avant entrainement: {acc_before:.3f}")

def cost_fn(params):
    preds = []
    for x in X[:30]:
        outputs = qnn_circuit(x, params)
        pred = np.sign(np.sum(outputs))
        preds.append(pred)
    return square_loss(np.array(preds), y[:30])

opt = qml.AdamOptimizer(stepsize=0.1)

for step in range(50):
    params = opt.step(lambda p: cost_fn(p), params)
    if step % 10 == 0:
        cost_val = cost_fn(params)
        print(f"Step {step:3d}: cost = {cost_val:.4f}")

preds_trained = []
for x in X[30:50]:
    preds_trained.append(qnn_predict(x, params))

preds_trained = np.array(preds_trained)
acc_after = accuracy(preds_trained, y[30:50])
print(f"Accuracy apres entrainement: {acc_after:.3f}")
```

---

## 5. Marché et projections

### 5.1 McKinsey (2025) : 72 G$ d'ici 2035

| Secteur | Valeur 2035 (G$) | Maturité |
|---------|-----------------|----------|
| Chimie et matériaux | 15–25 | 2027–2030 |
| Pharmaceutique | 12–20 | 2028–2032 |
| Finance | 8–15 | 2027–2030 |
| Logistique | 6–10 | 2028–2033 |
| Énergie | 5–8 | 2028–2032 |
| Cybersécurité | 3–6 | 2027–2030 |
| IA/ML | 4–8 | 2027–2032 |
| **Total** | **53–92** | **2027–2035** |

### 5.2 Niveaux d'avantage quantique

$$
\text{Avantage} = \frac{T_{\text{classique}}}{T_{\text{quantique}}}
$$

| Niveau | Rapport | Exemple |
|--------|---------|---------|
| Faible | $10^1-10^3$ | VQE molécules simples |
| Moyen | $10^3-10^6$ | Optimisation logistique |
| Fort | $10^6-10^9$ | Catalyse, matériaux |
| Révolutionnaire | $> 10^9$ | Drug discovery complet |

### 5.3 Simulation VQE pour H2 avec PennyLane

```python
import pennylane as qml
from pennylane import numpy as np

H2_hamiltonian = qml.qchem.molecular_hamiltonian(
    ["H", "H"],
    np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.74]),
    basis="sto-3g",
    active_electrons=2
)[0]

dev_vqe = qml.device("default.qubit", wires=4)

def ansatz(params, wires):
    qml.BasisState(np.array([1, 1, 0, 0]), wires=wires)
    for i in range(4):
        qml.RY(params[i], wires=wires[i])
    qml.CNOT(wires=[0, 1])
    qml.CNOT(wires=[2, 3])
    for i in range(4):
        qml.RY(params[4+i], wires=wires[i])

@qml.qnode(dev_vqe)
def cost_fn(params):
    ansatz(params, range(4))
    return qml.expval(H2_hamiltonian)

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

### 5.4 Quantum Approximate Optimization Algorithm (QAOA)

#### Formalisme détaillé

Le QAOA approxime la solution d'un problème d'optimisation combinatoire en alternant l'évolution sous $H_C$ (problème) et $H_B$ (mélangeur) :

$$
| \gamma, \beta \rangle = e^{-i\beta_p H_B} e^{-i\gamma_p H_C} \cdots e^{-i\beta_1 H_B} e^{-i\gamma_1 H_C} | + \rangle^{\otimes n}
$$

$$
H_C = \sum_{\langle i,j \rangle} w_{ij} Z_i Z_j + \sum_i h_i Z_i, \quad H_B = \sum_i X_i
$$

La performance est mesurée par le ratio d'approximation :

$$
r_p = \frac{\langle \gamma^*, \beta^* | H_C | \gamma^*, \beta^* \rangle}{C_{\text{max}}}
$$

où $C_{\text{max}}$ est la valeur optimale.

### 5.5 Implémentation QAOA pour MaxCut

```python
import pennylane as qml
from pennylane import numpy as np

edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
n_nodes_qaoa = 4

def qaoa_layer(gamma, beta, wires):
    for (u, v) in edges:
        qml.CNOT(wires=[wires[u], wires[v]])
        qml.RZ(2 * gamma, wires=wires[v])
        qml.CNOT(wires=[wires[u], wires[v]])
    for w in wires:
        qml.RX(2 * beta, wires=w)

@qml.qnode(dev_vqe)
def qaoa_circuit(params, wires):
    n_layers = len(params) // 2
    for w in wires:
        qml.Hadamard(wires=w)
    for l in range(n_layers):
        qaoa_layer(params[l], params[n_layers + l], wires)
    return [qml.expval(qml.PauliZ(w)) for w in wires]

def maxcut_cost(params, wires):
    z = qaoa_circuit(params, wires)
    cost = 0.0
    for (u, v) in edges:
        cost += 0.5 * (1 - z[u] * z[v])
    return -cost

params_qaoa = np.random.randn(4) * 0.1
opt_qaoa = qml.GradientDescentOptimizer(stepsize=0.5)

for step in range(50):
    params_qaoa = opt_qaoa.step(lambda p: maxcut_cost(p, range(n_nodes_qaoa)), params_qaoa)
    if step % 10 == 0:
        cost_val = maxcut_cost(params_qaoa, range(n_nodes_qaoa))
        print(f"QAOA step {step}: cost = {-cost_val:.4f}")
```

### 5.5 Quantum Kernel Method

```python
import pennylane as qml
from pennylane import numpy as np

n_qubits_kernel = 2
dev_kernel = qml.device("default.qubit", wires=n_qubits_kernel)

@qml.qnode(dev_kernel)
def kernel_circuit(x1, x2):
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
    probs = kernel_circuit(x1, x2)
    return probs[0] + probs[3]

X_train_k = np.random.randn(20, 2)
y_train_k = np.array([1 if x[0]*x[1] > 0 else -1 for x in X_train_k])

K_matrix = np.zeros((len(X_train_k), len(X_train_k)))
for i in range(len(X_train_k)):
    for j in range(i, len(X_train_k)):
        k_val = quantum_kernel(X_train_k[i], X_train_k[j])
        K_matrix[i, j] = k_val
        K_matrix[j, i] = k_val

print(f"Matrice de kernel quantique: {K_matrix.shape}")
print(f"Valeurs propres du kernel: {np.sort(np.linalg.eigvalsh(K_matrix))[:5]}")

alpha_k = np.linalg.solve(K_matrix + 0.01 * np.eye(len(X_train_k)), y_train_k)
pred_k = np.sign(K_matrix @ alpha_k)
acc_k = np.mean(pred_k == y_train_k)
print(f"Accuracy du kernel quantique: {acc_k:.3f}")
```

### 5.6 Roadmap Consulting

| Période | Jalon |
|---------|-------|
| 2025–2027 | Avantage démontré en simulation quantique |
| 2027–2029 | Premier avantage pratique (optimisation, chimie) |
| 2029–2032 | Déploiement industriel limité |
| 2032–2035 | Adoption massive, 72 G$ de marché |

---

## 6. Exercices

1. **VQE moléculaire** : Implémenter un VQE pour la molécule $H_2$ avec PennyLane. Utiliser l'Hamiltonien dans la base STO-3G. Trouver l'énergie de l'état fondamental.

2. **QAOA MaxCut** : Implémenter QAOA pour MaxCut sur un graphe à 6 nœuds. Tracer la performance $F_p$ en fonction du nombre de couches $p = 1, 2, 3, 5, 10$.

3. **QNN classification** : Comparer la performance d'un QNN (noyau quantique) vs SVM classique sur un jeu de données synthétique non-linéaire (toy dataset).

4. **Portfolio optimization** : Formuler un problème de sélection de portefeuille (10 actifs) en QUBO. Résoudre avec QAOA et comparer avec un solveur classique (scipy.optimize).

5. **Analyse de marché** : Pour un secteur au choix (finance, pharma, logistique), construire un argumentaire détaillé sur l'apport du calcul quantique, incluant les métriques attendues et l'horizon temporel.

---

## Références

- **McKinsey & Company** (2025). "Quantum computing: An emerging ecosystem and industry use cases." *McKinsey Digital*. [McK25]
- **Consentino, M.** et al. (2022). "Quantum computing for finance: A review." *Nature Reviews Physics*, 4, 421–433. [Con22]
- **Peruzzo, A.** et al. (2014). "A variational eigenvalue solver on a photonic quantum processor." *Nature Communications*, 5, 4213.
- **Farhi, E., Goldstone, J. & Gutmann, S.** (2014). "A Quantum Approximate Optimization Algorithm." *arXiv:1411.4028*.
- **Havlíček, V.** et al. (2019). "Supervised learning with quantum-enhanced feature spaces." *Nature*, 567, 209–212.
- **Cerezo, M.** et al. (2021). "Variational quantum algorithms." *Nature Reviews Physics*, 3, 625–644.
