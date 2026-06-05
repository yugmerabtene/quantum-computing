# Séance 8.1 — Algorithme de Grover

## Objectifs d'apprentissage

- Comprendre le mécanisme de l'oracle et de l'inversion autour de la moyenne
- Maîtriser l'analyse de complexité $O(\sqrt{N})$ et la preuve d'optimalité
- Implémenter l'algorithme en Qiskit
- Analyser les conditions d'application

---

## 1. Problème de recherche non structurée

**Problème** : Soit un espace de recherche de taille $N = 2^n$. On dispose d'une fonction $f : \{0,1\}^n \to \{0,1\}$ telle que $f(x) = 1$ ssi $x = x^*$ (l'élément cible). Trouver $x^*$.

Classiquement : $O(N)$ requêtes en moyenne. Quantiquement (Grover) : $O(\sqrt{N})$ requêtes.

C'est une **amplification d'amplitude** : on augmente l'amplitude de l'état cible et on diminue celle des autres.

## 2. Oracle de Grover

L'oracle $O$ marque l'état cible en inversant sa phase :

$$O|x\rangle = (-1)^{f(x)}|x\rangle = \begin{cases} -|x^*\rangle, & x = x^* \\ |x\rangle, & x \neq x^* \end{cases}$$

En notation matricielle, $O = I - 2|x^*\rangle\langle x^*|$.

**Implémentation** : L'oracle peut être réalisé par une porte $Z$ multi-contrôlée :

```
Pour n≥2 : O = (X⊗ⁿ) · C^{n-1}NOT · (X⊗ⁿ)
```

## 3. Opérateur de diffusion (inversion autour de la moyenne)

L'opérateur de Grover (ou de diffusion) $D$ est :

$$D = 2|s\rangle\langle s| - I = H^{\otimes n} (2|0\rangle\langle 0| - I) H^{\otimes n}$$

où $|s\rangle = \frac{1}{\sqrt{N}}\sum_{x=0}^{N-1} |x\rangle$ est la superposition uniforme.

### Interprétation géométrique

L'opérateur $D$ effectue une réflexion autour de $|s\rangle$ dans l'espace des amplitudes. Combiné avec $O$ (réflexion autour de $|x^*\rangle$), l'itération de Grover $G = D \cdot O$ est une rotation dans le plan défini par $|x^*\rangle$ et $|s\rangle$.

### Circuit de diffusion

```
|ψ⟩ — H⊗ⁿ — X⊗ⁿ — C^{n-1}Z — X⊗ⁿ — H⊗ⁿ — |ψ'⟩
```

où $C^{n-1}Z$ est la porte $Z$ multi-contrôlée.

## 4. Analyse de l'algorithme

### Définition des angles

Soit $|s\rangle = \sin\theta |x^*\rangle + \cos\theta |\psi_\perp\rangle$, où $|\psi_\perp\rangle$ est orthogonal à $|x^*\rangle$ et $\sin\theta = \frac{1}{\sqrt{N}}$.

Géométriquement, $G$ est une rotation d'angle $2\theta$ dans le plan $(|x^*\rangle, |\psi_\perp\rangle)$.

$$G^k |s\rangle = \sin((2k+1)\theta) |x^*\rangle + \cos((2k+1)\theta) |\psi_\perp\rangle$$

### Nombre d'itérations optimal

La probabilité de mesurer $x^*$ est $P = \sin^2((2k+1)\theta)$. Elle est maximale quand :

$$(2k+1)\theta \approx \frac{\pi}{2} \implies k \approx \frac{\pi}{4\theta} - \frac{1}{2}$$

Avec $\theta \approx \frac{1}{\sqrt{N}}$ pour $N$ grand :

$$k_{\text{opt}} = \left\lfloor \frac{\pi}{4} \sqrt{N} \right\rfloor$$

Soit $k_{\text{opt}} = O(\sqrt{N})$, un gain quadratique par rapport à $O(N)$ classique.

### Probabilité de succès

$$P_{\text{succès}} \geq 1 - \frac{1}{N}$$

pour le nombre optimal d'itérations.

```python
import numpy as np
import matplotlib.pyplot as plt

def grover_analyse(N=256):
    """Analyse de la probabilité de succès en fonction du nombre d'itérations"""
    theta = np.arcsin(1 / np.sqrt(N))
    k_opt = int(np.pi / (4 * theta) - 0.5)

    ks = np.arange(0, 3 * k_opt)
    probs = np.sin((2 * ks + 1) * theta)**2

    print(f"N={N}, √N={np.sqrt(N):.1f}, θ={theta:.4f}")
    print(f"Nombre optimal d'itérations : k_opt = {k_opt}")
    print(f"Probabilité maximale : {probs[k_opt]:.4f}")

    # Tableau des premières valeurs
    print("\nk\tP(succès)")
    for k in range(max(1, k_opt - 2), min(len(ks), k_opt + 3)):
        print(f"{k}\t{probs[k]:.4f}")

    return k_opt, probs

# Analyse pour différentes tailles
for N in [16, 64, 256, 1024]:
    print(f"\n{'='*40}")
    grover_analyse(N)
    print()
```

## 5. Implémentation Qiskit

```python
import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram

def oracle_grover(qc, n, target):
    """
    Oracle de Grover : marque l'état target avec une phase de -1.
    """
    # Phase flip sur l'état cible
    # On applique X pour amener |target⟩ → |11...1⟩, puis C^{n-1}Z, puis X⁻¹
    target_bits = format(target, f'0{n}b')

    for i, bit in enumerate(target_bits):
        if bit == '0':
            qc.x(i)

    # Porte multi-contrôlée Z
    if n == 1:
        qc.z(0)
    else:
        qc.h(n - 1)
        qc.mcx(list(range(n - 1)), n - 1)  # multi-control Toffoli
        qc.h(n - 1)

    for i, bit in enumerate(target_bits):
        if bit == '0':
            qc.x(i)

def diffuseur_grover(qc, n):
    """
    Opérateur de diffusion : inversion autour de la moyenne.
    """
    # H⊗ⁿ
    qc.h(range(n))

    # X⊗ⁿ
    qc.x(range(n))

    # C^{n-1}Z multi-contrôlée
    if n == 1:
        qc.z(0)
    else:
        qc.h(n - 1)
        qc.mcx(list(range(n - 1)), n - 1)
        qc.h(n - 1)

    # X⊗ⁿ
    qc.x(range(n))

    # H⊗ⁿ
    qc.h(range(n))

def grover_algorithm(n, target):
    """
    Algorithme de Grover complet.
    n : nombre de qubits
    target : élément cible (entier)
    """
    N = 2**n
    k_opt = int(np.pi / 4 * np.sqrt(N) - 0.5) + 1

    qc = QuantumCircuit(n, n)

    # Superposition uniforme
    qc.h(range(n))

    # Itérations de Grover
    for _ in range(k_opt):
        oracle_grover(qc, n, target)
        diffuseur_grover(qc, n)

    # Mesure
    qc.measure(range(n), range(n))

    return qc, k_opt

# Test avec n=4 qubits, cible=5
n = 4
target = 5
qc_grover, k = grover_algorithm(n, target)

print(f"Circuit Grover (n={n}, cible={target}, itérations={k}) :")
print(qc_grover.draw())

# Simulation
backend = Aer.get_backend('qasm_simulator')
result = execute(qc_grover, backend, shots=4096).result()
counts = result.get_counts()

print(f"\nDistribution des mesures (k={k} itérations) :")
for state, count in sorted(counts.items(), key=lambda x: int(x[0])):
    prob = count / 4096
    is_target = "← cible" if int(state, 2) == target else ""
    if prob > 0.01:
        print(f"  |{state}⟩ : {prob:.3f} {is_target}")

# Vérification
target_count = counts.get(format(target, f'0{n}b'), 0)
print(f"\nProbabilité de l'état cible : {target_count / 4096:.3f}")
```

```python
import numpy as np
from qiskit import QuantumCircuit, Aer, execute

def grover_n_iterations(n, target, iterations):
    """
    Grover avec un nombre d'itérations spécifié.
    """
    qc = QuantumCircuit(n, n)
    qc.h(range(n))

    for _ in range(iterations):
        oracle_grover(qc, n, target)
        diffuseur_grover(qc, n)

    qc.measure(range(n), range(n))

    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend, shots=2048).result()
    counts = result.get_counts()
    prob_target = counts.get(format(target, f'0{n}b'), 0) / 2048

    return prob_target

def analyse_iterations(n=6):
    """Analyse la probabilité en fonction du nombre d'itérations"""
    N = 2**n
    target = np.random.randint(N)
    k_opt = int(np.pi / 4 * np.sqrt(N) - 0.5) + 1

    print(f"Analyse pour n={n}, N={N}, cible={target}")
    print(f"k_opt théorique ≈ {k_opt}")
    print("-" * 40)

    # Test de 0 à 2*k_opt itérations
    for k in range(0, 2 * k_opt + 2, max(1, k_opt // 4)):
        prob = grover_n_iterations(n, target, k)
        theta = np.arcsin(1 / np.sqrt(N))
        prob_theo = np.sin((2 * k + 1) * theta)**2
        print(f"  k={k:2d} : P={prob:.4f} (théorique={prob_theo:.4f})")

analyse_iterations(n=6)
```

## 6. Preuve d'optimalité

### Théorème (Bennett et al.)

Tout algorithme quantique de recherche non structurée nécessite $\Omega(\sqrt{N})$ évaluations de l'oracle.

### Idée de la preuve

Soit $U_k$ l'état après $k$ appels à l'oracle. On montre que pour tout algorithme :

$$\max_{x^*} \|U_k - V_k\| \leq \frac{2k}{\sqrt{N}}$$

où $V_k$ est l'état sans l'oracle (toutes les phases sont $+1$).

Or, pour distinguer $N$ possibilités, il faut $\|U_k - V_k\| \geq \Omega(1)$. Donc $k = \Omega(\sqrt{N})$.

```python
import numpy as np

def preuve_optimalite(N=1024):
    """
    Illustration de la borne inférieure de Grover.
    """
    print("=== Preuve d'optimalité de Grover ===")
    print(f"N = {N}, √N = {np.sqrt(N):.1f}")
    print()

    # Bornes
    k_classical = N / 2  # Recherche classique moyenne
    k_quantum = np.pi / 4 * np.sqrt(N)  # Grover

    print(f"Classique (moyenne) : {k_classical:.0f} requêtes")
    print(f"Grover (optimal)    : {k_quantum:.1f} requêtes")
    print(f"Rapport            : {k_classical / k_quantum:.0f}×")
    print()

    # Théorème : k ≥ c·√N pour tout algorithme quantique
    c = 0.5  # Constante de la borne inférieure
    borne_inf = c * np.sqrt(N)
    print(f"Borne inférieure    : k ≥ {c}·√N ≈ {borne_inf:.1f}")
    print(f"Grover atteint     : {k_quantum:.1f} ≈ {np.pi/4:.4f}·√N")
    print(f"Ratio optimal      : {k_quantum / borne_inf:.2f} (optimal à constante près)")

preuve_optimalite(1024)
```

## 7. Exercices

### Exercice 1 : Implémentation de l'oracle
Concevez l'oracle de Grover pour marquer $x^* = 10110$ (5 qubits) sans utiliser de porte multi-contrôlée, uniquement des portes Toffoli.

### Exercice 2 : Simulation QuTiP de l'itération
Simulez l'itération de Grover avec QuTiP :

```python
import qutip as qt
import numpy as np

def grover_iteration_qutip(n, target):
    """Itération de Grover avec matrices QuTiP"""
    N = 2**n

    # Superposition uniforme
    s = qt.basis(N, 0)
    for i in range(N):
        s += qt.basis(N, i)
    s = s.unit()

    # Oracle : I - 2|target⟩⟨target|
    O = qt.qeye(N) - 2 * qt.basis(N, target) * qt.basis(N, target).dag()

    # Diffuseur : 2|s⟩⟨s| - I
    D = 2 * s * s.dag() - qt.qeye(N)

    # Itération
    G = D * O

    # État initial
    psi = s.copy()

    # Appliquer k fois
    k_opt = int(np.pi / 4 * np.sqrt(N))
    psi_k = (G**k_opt) * psi

    prob_target = abs((qt.basis(N, target).dag() * psi_k)[0, 0])**2
    return prob_target

# Test
for n in range(2, 8):
    target = 1
    prob = grover_iteration_qutip(n, target)
    print(f"n={n}, N={2**n}, P(cible)={prob:.4f}")
```

### Exercice 3 : Recherche avec plusieurs cibles
Généralisez Grover au cas de $M$ cibles ($1 \leq M \leq N$). Montrez que $k_{\text{opt}} = \frac{\pi}{4}\sqrt{N/M}$.

### Exercice 4 : Implémentation Cirq
Implémentez Grover en Cirq pour $n=4$ qubits avec un oracle arbitraire.

```python
import cirq
import numpy as np

def grover_cirq(n, target):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    circuit.append(cirq.H.on_each(*qubits))

    # Oracle
    # ... à compléter ...

    return circuit
```

### Exercice 5 : Recherche sans oracle — analyse du bruit
Ajoutez un canal de déphasage sur chaque qubit et étudiez la dégradation de la probabilité de succès. Pour quel taux de bruit l'algorithme devient-il inefficace ?

### Exercice 6 : Applications — résolution de Sudoku
Utilisez Grover pour résoudre un Sudoku 2×2. Construisez l'oracle qui vérifie les contraintes.

---

## Références

- Grover, L. K. (1996). "A fast quantum mechanical algorithm for database search". *Proc. 28th STOC*, 212–219.
- Bennett, C. H. et al. (1997). "Strengths and Weaknesses of Quantum Computing". *SIAM J. Comput.*, 26(5), 1510–1523.
- Nielsen, M. A. & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*.
- Zalka, C. (1999). "Grover's quantum searching algorithm is optimal". *Phys. Rev. A*, 60, 2746–2751.
