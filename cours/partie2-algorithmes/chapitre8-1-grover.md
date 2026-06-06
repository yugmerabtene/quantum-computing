# Chapitre 8.1 — Algorithme de Grover

## Ce que vous allez apprendre

- Comprendre le mécanisme de l'**oracle** et de l'**inversion autour de la moyenne**
- Maîtriser l'**interprétation géométrique** (rotation dans un plan)
- Analyser la complexité $O(\sqrt{N})$ et la **preuve d'optimalité**
- Implémenter l'algorithme complet en **Qiskit**
- Connaître les **conditions d'application** et les limites

---

## Motivation

Imaginez que vous cherchez un nom dans un annuaire de $N$ pages, mais les pages ne sont pas triées. Classiquement, vous devez regarder en moyenne $N/2$ pages, et $N$ pages dans le pire cas. C'est frustrant : l'information est là, mais vous ne pouvez pas l'exploiter mieux.

Et si vous pouviez regarder toutes les pages en même temps et faire interférer les mauvaises réponses ? C'est exactement ce que fait l'algorithme de Grover (1996). Il trouve l'élément cible en seulement $O(\sqrt{N})$ évaluations de l'oracle. Pour un annuaire d'un million de pages, il faut environ 1000 itérations au lieu de 500 000.

Contrairement à Shor (avantage exponentiel), Grover offre un avantage **quadratique**. Mais il est **universel** : il s'applique à tout problème de recherche non structurée, et il est **prouvé optimal** — aucun algorithme quantique ne peut faire mieux. C'est l'algorithme le plus généraliste de la boîte à outils quantique.

---

## Idée principale

Pensez à un lac calme. Jetez un caillou (l'oracle marque la cible en inversant sa phase). L'onde se propage, puis vous jetez un deuxième caillou au bon moment (l'inversion autour de la moyenne). Les ondes interfèrent constructivement vers la cible et destructivement ailleurs. À chaque itération, l'amplitude de la cible grossit.

Géométriquement, l'état quantique tourne dans un plan. L'état initial $|s\rangle$ est presque orthogonal à la cible $|x^*\rangle$ (angle $\theta \approx 1/\sqrt{N}$). Chaque itération de Grover (oracle + diffusion) fait tourner l'état de $2\theta$. Après $k \approx \pi/(4\theta) \approx \frac{\pi}{4}\sqrt{N}$ itérations, l'état est aligné avec $|x^*\rangle$.

---

## Contenu du cours

### Section 1 : Le problème de recherche non structurée

**Problème** : Espace de recherche de taille $N = 2^n$. Fonction $f : \{0,1\}^n \to \{0,1\}$ telle que $f(x) = 1$ ssi $x = x^*$. Trouver $x^*$.

**Classique** : $O(N)$ requêtes en moyenne ($N/2$ exactement).
**Quantique (Grover)** : $O(\sqrt{N})$ requêtes.

**Intuition** : c'est une **amplification d'amplitude**. On part d'une superposition uniforme où chaque état a une amplitude $1/\sqrt{N}$. À chaque itération, on augmente l'amplitude de $|x^*\rangle$ et on diminue celle des autres.

### Section 2 : L'oracle de Grover

L'oracle $O$ marque l'état cible en inversant sa phase :

$$O|x\rangle = (-1)^{f(x)}|x\rangle = \begin{cases} -|x^*\rangle, & x = x^* \\ |x\rangle, & x \neq x^* \end{cases}$$

**Intuition** : l'oracle ne « trouve » pas la cible — il la « marque » d'un signe moins. C'est comme mettre un post-it négatif sur la bonne réponse.

En notation matricielle : $O = I - 2|x^*\rangle\langle x^*|$.

**Implémentation** : pour $x^* = 11\ldots1$, l'oracle est une porte $Z$ multi-contrôlée. Pour un $x^*$ arbitraire, on entoure de portes $X$ pour amener $|x^*\rangle \to |11\ldots1\rangle$ :

```
Pour n≥2 : O = (X⊗ⁿ) · C^{n-1}Z · (X⊗ⁿ)
```

**Exemple** : $n = 2$, $x^* = 10$. On applique $X$ sur le qubit 1 (pour transformer $|10\rangle \to |11\rangle$), puis $CZ$, puis $X$ sur le qubit 1.

### Section 3 : L'opérateur de diffusion (inversion autour de la moyenne)

L'opérateur de diffusion $D$ est :

$$D = 2|s\rangle\langle s| - I = H^{\otimes n} (2|0\rangle\langle 0| - I) H^{\otimes n}$$

où $|s\rangle = \frac{1}{\sqrt{N}}\sum_{x=0}^{N-1} |x\rangle$ est la superposition uniforme.

**Intuition** : $D$ effectue une « inversion autour de la moyenne ». Si les amplitudes sont $(a_0, a_1, \ldots, a_{N-1})$ avec moyenne $\bar{a}$, alors $D$ transforme chaque amplitude $a_i \to 2\bar{a} - a_i$.

**Pourquoi ça amplifie la cible ?** Après l'oracle, la cible a une amplitude négative et les autres sont positives. La moyenne est légèrement positive (car la cible ne pèse pas lourd). L'inversion autour de cette moyenne fait grandir l'amplitude de la cible (de négative à positive, au-dessus de la moyenne) et réduit les autres.

**Circuit de diffusion** :
```
|ψ⟩ — H⊗ⁿ — X⊗ⁿ — C^{n-1}Z — X⊗ⁿ — H⊗ⁿ — |ψ'⟩
```

### Section 4 : Interprétation géométrique

```
    Plan ⟨|x*⟩, |ψ⊥⟩⟩
    
            |x*⟩
              •  (état cible)
             ╱│
            ╱ │
           ╱  │ θ
          ╱   │
         ╱    │  État initial |s⟩ :
        ╱     │  = sin θ |x*⟩ + cos θ |ψ⊥⟩
       ╱      │
      ╱       •  |s⟩
     ╱  2θ     │
    ╱  ─────►  │     Itération de Grover = rotation
   ╱           │     d'angle 2θ dans ce plan
  •────────────•  |ψ⊥⟩
```

L'état initial $|s\rangle$ fait un angle $\theta$ avec $|\psi_\perp\rangle$, où $\sin\theta = 1/\sqrt{N}$.

Chaque itération de Grover $G = D \cdot O$ est une **rotation de $2\theta$** dans le plan $(|x^*\rangle, |\psi_\perp\rangle)$.

Après $k$ itérations :
$$G^k |s\rangle = \sin((2k+1)\theta) |x^*\rangle + \cos((2k+1)\theta) |\psi_\perp\rangle$$

### Section 5 : Nombre d'itérations optimal

La probabilité de mesurer $x^*$ est $P = \sin^2((2k+1)\theta)$. Elle est maximale quand :

$$(2k+1)\theta \approx \frac{\pi}{2} \implies k \approx \frac{\pi}{4\theta} - \frac{1}{2}$$

Avec $\theta \approx 1/\sqrt{N}$ pour $N$ grand :

$$k_{\text{opt}} = \left\lfloor \frac{\pi}{4} \sqrt{N} \right\rfloor$$

**Exemple numérique** : $N = 256$ ($n = 8$), $\theta = \arcsin(1/16) \approx 0.0625$.
$k_{\text{opt}} = \lfloor \pi/(4 \times 0.0625) - 0.5 \rfloor = \lfloor 12.07 \rfloor = 12$.
$P_{\text{succès}} = \sin^2(25 \times 0.0625) = \sin^2(1.5625) \approx 0.9999$.

---

## Exemple guidé

Prenons $n = 2$ qubits, $N = 4$, cible $x^* = 11$ (donc $|x^*\rangle = |3\rangle$).

$\theta = \arcsin(1/2) = \pi/6$. $k_{\text{opt}} = \lfloor \pi/(4 \times \pi/6) - 0.5 \rfloor = \lfloor 1 \rfloor = 1$.

**État initial** :
$$|s\rangle = \frac{1}{2}(|0\rangle + |1\rangle + |2\rangle + |3\rangle)$$

Amplitudes : $(1/2, 1/2, 1/2, 1/2)$.

**Itération 1 — Oracle** : marquer $|3\rangle$ avec un signe moins.
Amplitudes : $(1/2, 1/2, 1/2, -1/2)$.

Moyenne : $\bar{a} = (1/2 + 1/2 + 1/2 - 1/2)/4 = 1/8$.

**Itération 1 — Diffusion** : inversion autour de la moyenne.
- $a_0 \to 2(1/8) - 1/2 = -1/4$
- $a_1 \to 2(1/8) - 1/2 = -1/4$
- $a_2 \to 2(1/8) - 1/2 = -1/4$
- $a_3 \to 2(1/8) - (-1/2) = 5/8$

Amplitudes après 1 itération : $(-1/4, -1/4, -1/4, 5/8)$.

Probabilité de mesurer $|3\rangle$ : $(5/8)^2 = 25/64 \approx 0.39$.

Hmm, pas encore très bon. Vérifions avec la formule : $P = \sin^2(3\theta) = \sin^2(3\pi/6) = \sin^2(\pi/2) = 1$.

Attendez — recalculons. $\sin\theta = 1/\sqrt{4} = 1/2$, donc $\theta = \pi/6$.
$P = \sin^2((2 \times 1 + 1) \times \pi/6) = \sin^2(\pi/2) = 1$.

Il y a une erreur dans mon calcul manuel. Recalculons la diffusion.

Moyenne : $\bar{a} = (1/2 + 1/2 + 1/2 - 1/2)/4 = 1/8$.

Inversion : $a_i \to 2\bar{a} - a_i$.
- $a_0 = 1/2 \to 2/8 - 1/2 = 1/4 - 1/2 = -1/4$
- $a_3 = -1/2 \to 1/4 + 1/2 = 3/4$

Amplitudes : $(-1/4, -1/4, -1/4, 3/4)$.

Probabilité de $|3\rangle$ : $(3/4)^2 = 9/16 = 0.5625$.

Encore un écart. Le problème est que pour $N = 4$, l'approximation $\theta \approx 1/\sqrt{N}$ n'est pas exacte. En fait, $\sin\theta = 1/2$ donne $\theta = \pi/6$, et $\sin(3\pi/6) = \sin(\pi/2) = 1$.

Vérifions directement : l'état après 1 itération devrait être $|3\rangle$ avec probabilité 1. Recalculons en utilisant les matrices.

$O = I - 2|3\rangle\langle 3| = \text{diag}(1, 1, 1, -1)$.

$D = 2|s\rangle\langle s| - I$. $|s\rangle = \frac{1}{2}(1,1,1,1)^T$.

$|s\rangle\langle s| = \frac{1}{4}\begin{pmatrix} 1&1&1&1 \\ 1&1&1&1 \\ 1&1&1&1 \\ 1&1&1&1 \end{pmatrix}$

$D = \frac{1}{2}\begin{pmatrix} 1&1&1&1 \\ 1&1&1&1 \\ 1&1&1&1 \\ 1&1&1&1 \end{pmatrix} - I = \frac{1}{2}\begin{pmatrix} -1&1&1&1 \\ 1&-1&1&1 \\ 1&1&-1&1 \\ 1&1&1&-1 \end{pmatrix}$

$G = D \cdot O = \frac{1}{2}\begin{pmatrix} -1&1&1&-1 \\ 1&-1&1&-1 \\ 1&1&-1&-1 \\ 1&1&1&1 \end{pmatrix}$

$G|s\rangle = \frac{1}{2} \cdot \frac{1}{2}\begin{pmatrix} -1+1+1-1 \\ 1-1+1-1 \\ 1+1-1-1 \\ 1+1+1+1 \end{pmatrix} = \frac{1}{4}\begin{pmatrix} 0 \\ 0 \\ 0 \\ 4 \end{pmatrix} = |3\rangle$

Probabilité = 1. ✓ Mon calcul d'inversion autour de la moyenne était incorrect — la formule $a_i \to 2\bar{a} - a_i$ s'applique aux amplitudes, mais il faut utiliser la bonne moyenne.

---

## Implémentation Python

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# --- Oracle de Grover ---
def oracle_grover(qc, n, target):
    """
    Oracle de Grover : marque l'état 'target' avec une phase de -1.
    Stratégie : amener |target⟩ → |11...1⟩ avec des X,
    appliquer une porte Z multi-contrôlée, puis remettre les X.
    """
    target_bits = format(target, f'0{n}b')

    # Appliquer X sur les qubits qui sont à 0 dans target
    for i, bit in enumerate(target_bits):
        if bit == '0':
            qc.x(i)

    # Porte multi-contrôlée Z (via H + MCX + H)
    if n == 1:
        qc.z(0)
    else:
        qc.h(n - 1)                          # H sur le dernier qubit
        qc.mcx(list(range(n - 1)), n - 1)    # Toffoli multi-contrôlé
        qc.h(n - 1)                          # H pour restaurer

    # Remettre les X
    for i, bit in enumerate(target_bits):
        if bit == '0':
            qc.x(i)

# --- Opérateur de diffusion ---
def diffuseur_grover(qc, n):
    """
    Opérateur de diffusion : inversion autour de la moyenne.
    Circuit : H⊗ⁿ — X⊗ⁿ — C^{n-1}Z — X⊗ⁿ — H⊗ⁿ
    """
    qc.h(range(n))       # Hadamard
    qc.x(range(n))       # X sur tous les qubits

    # Z multi-contrôlée
    if n == 1:
        qc.z(0)
    else:
        qc.h(n - 1)
        qc.mcx(list(range(n - 1)), n - 1)
        qc.h(n - 1)

    qc.x(range(n))       # X pour restaurer
    qc.h(range(n))       # Hadamard

# --- Algorithme de Grover complet ---
def grover_algorithm(n, target):
    """
    Algorithme de Grover complet.
    n : nombre de qubits
    target : élément cible (entier)
    Retourne le circuit et le nombre d'itérations optimal.
    """
    N = 2**n
    k_opt = int(np.pi / 4 * np.sqrt(N) - 0.5) + 1

    qc = QuantumCircuit(n, n)

    # Superposition uniforme
    qc.h(range(n))

    # k_opt itérations de Grover (oracle + diffusion)
    for _ in range(k_opt):
        oracle_grover(qc, n, target)
        diffuseur_grover(qc, n)

    # Mesure
    qc.measure(range(n), range(n))

    return qc, k_opt

# --- Test : n=4 qubits, cible=5 ---
n = 4
target = 5
qc_grover, k = grover_algorithm(n, target)

print(f"Circuit Grover (n={n}, cible={target}, itérations={k}) :")
print(qc_grover.draw())

# Simulation
backend = AerSimulator()
result = backend.run(qc_grover, shots=4096).result()
counts = result.get_counts()

print(f"\nDistribution des mesures (k={k} itérations) :")
for state, count in sorted(counts.items(), key=lambda x: int(x[0])):
    prob = count / 4096
    is_target = "← cible" if int(state, 2) == target else ""
    if prob > 0.01:
        print(f"  |{state}⟩ : {prob:.3f} {is_target}")

target_count = counts.get(format(target, f'0{n}b'), 0)
print(f"\nProbabilité de l'état cible : {target_count / 4096:.3f}")
```

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# --- Analyse du nombre d'itérations ---
def grover_analyse(N=256):
    """
    Analyse la probabilité de succès en fonction du nombre d'itérations.
    Montre que la probabilité oscille (il ne faut pas trop itérer !).
    """
    theta = np.arcsin(1 / np.sqrt(N))
    k_opt = int(np.pi / (4 * theta) - 0.5)

    ks = np.arange(0, 3 * k_opt)
    probs = np.sin((2 * ks + 1) * theta)**2

    print(f"N={N}, √N={np.sqrt(N):.1f}, θ={theta:.4f}")
    print(f"Nombre optimal d'itérations : k_opt = {k_opt}")
    print(f"Probabilité maximale : {probs[k_opt]:.4f}")

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

**Sortie attendue :**

```
========================================
N=16, √N=4.0, θ=0.2527
Nombre optimal d'itérations : k_opt = 2
Probabilité maximale : 0.9084

k	P(succès)
1	0.4727
2	0.9084
3	0.9613
4	0.5817

========================================
N=64, √N=8.0, θ=0.1253
Nombre optimal d'itérations : k_opt = 5
Probabilité maximale : 0.9635

k	P(succès)
3	0.5914
4	0.8164
5	0.9635
6	0.9966
7	0.9074

========================================
N=256, √N=16.0, θ=0.0625
Nombre optimal d'itérations : k_opt = 12
Probabilité maximale : 0.9999

k	P(succès)
10	0.9352
11	0.9826
12	0.9999
13	0.9862
14	0.9422

========================================
N=1024, √N=32.0, θ=0.0313
Nombre optimal d'itérations : k_opt = 24
Probabilité maximale : 0.9985

k	P(succès)
22	0.9732
23	0.9897
24	0.9985
25	0.9995
26	0.9927
```

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# --- Grover avec nombre d'itérations variable ---
def grover_n_iterations(n, target, iterations):
    """
    Grover avec un nombre d'itérations spécifié.
    Permet d'étudier l'oscillation de la probabilité.
    """
    qc = QuantumCircuit(n, n)
    qc.h(range(n))

    for _ in range(iterations):
        oracle_grover(qc, n, target)
        diffuseur_grover(qc, n)

    qc.measure(range(n), range(n))

    backend = AerSimulator()
    result = backend.run(qc, shots=2048).result()
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

    for k in range(0, 2 * k_opt + 2, max(1, k_opt // 4)):
        prob = grover_n_iterations(n, target, k)
        theta = np.arcsin(1 / np.sqrt(N))
        prob_theo = np.sin((2 * k + 1) * theta)**2
        print(f"  k={k:2d} : P={prob:.4f} (théorique={prob_theo:.4f})")

analyse_iterations(n=6)
```

---

## Complexité et avantage quantique

| Approche | Requêtes | Type d'avantage |
|----------|----------|-----------------|
| Classique (moyenne) | $N/2$ | — |
| Classique (pire cas) | $N$ | — |
| **Grover** | $\frac{\pi}{4}\sqrt{N}$ | **Quadratique** |

**Pourquoi Grover est-il plus rapide ?** Classiquement, chaque requête ne donne qu'un bit d'information (« c'est ça » ou « c'est pas ça »). Grover exploite le parallélisme quantique pour évaluer l'oracle sur toutes les entrées en superposition, puis utilise les interférences pour amplifier l'amplitude de la cible.

**Preuve d'optimalité (Bennett et al., 1997)** : Tout algorithme quantique de recherche non structurée nécessite $\Omega(\sqrt{N})$ évaluations de l'oracle. Grover est donc optimal à une constante près.

**Intuition de la preuve** : après $k$ appels à l'oracle, l'état quantique ne peut s'être « éloigné » de l'état initial que d'une distance proportionnelle à $k/\sqrt{N}$. Pour distinguer $N$ cibles possibles, il faut une distance $\Omega(1)$, donc $k = \Omega(\sqrt{N})$.

---

## À retenir

1. Grover cherche un élément marqué dans une base de données non triée en $O(\sqrt{N})$ requêtes
2. L'**oracle** marque la cible en inversant sa phase : $O = I - 2|x^*\rangle\langle x^*|$
3. Le **diffuseur** effectue une inversion autour de la moyenne : $D = 2|s\rangle\langle s| - I$
4. Géométriquement, chaque itération est une **rotation de $2\theta$** dans le plan $(|x^*\rangle, |\psi_\perp\rangle)$
5. Le nombre optimal d'itérations est $k_{\text{opt}} \approx \frac{\pi}{4}\sqrt{N}$
6. Grover est **prouvé optimal** : aucun algorithme quantique ne peut faire mieux
7. L'avantage est **quadratique** (pas exponentiel comme Shor), mais universel

---

## Pièges à éviter

1. **Trop itérer** : la probabilité oscille ! Au-delà de $k_{\text{opt}}$, elle redescend
2. **Confondre oracle et calcul** : l'oracle ne « calcule » pas $f$, il marque la phase
3. **Penser que Grover accélère tout** : il faut que le problème soit une recherche non structurée avec un oracle efficace
4. **Négliger le coût de l'oracle** : si l'oracle est coûteux, l'avantage peut être réduit
5. **Oublier que $N = 2^n$** : le nombre de qubits est $n = \log_2 N$, pas $N$

---

## Exercices

### Niveau 1 — Application directe

**Exercice 1** : Concevez l'oracle de Grover pour marquer $x^* = 10110$ (5 qubits) sans utiliser de porte multi-contrôlée, uniquement des portes Toffoli.

**Exercice 2** : Simulez l'itération de Grover avec QuTiP :

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

    # Itération G = D · O
    G = D * O

    # État initial = superposition uniforme
    psi = s.copy()

    # Appliquer k_opt fois
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

### Niveau 2 — Compréhension

**Exercice 3** : Généralisez Grover au cas de $M$ cibles ($1 \leq M \leq N$). Montrez que $k_{\text{opt}} = \frac{\pi}{4}\sqrt{N/M}$.

**Exercice 4** : Implémentez Grover en Cirq pour $n=4$ qubits avec un oracle arbitraire.

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

### Niveau 3 — Défi

**Exercice 5** : Ajoutez un canal de déphasage sur chaque qubit et étudiez la dégradation de la probabilité de succès. Pour quel taux de bruit l'algorithme devient-il inefficace ?

**Exercice 6** : Utilisez Grover pour résoudre un Sudoku 2×2. Construisez l'oracle qui vérifie les contraintes.

---

## Pour aller plus loin

- **Amplitude Amplification** : généralisation de Grover à tout algorithme randomisé
- **Quantum Counting** (chapitre 8.2) : combine Grover et QPE pour estimer le nombre de solutions
- **Minimum quantique** (Dürr-Høyer) : trouver le minimum d'une liste en $O(\sqrt{N})$

---

## Références

- Grover, L. K. (1996). "A fast quantum mechanical algorithm for database search". *Proc. 28th STOC*, 212–219.
- Bennett, C. H. et al. (1997). "Strengths and Weaknesses of Quantum Computing". *SIAM J. Comput.*, 26(5), 1510–1523.
- Nielsen, M. A. & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*.
- Zalka, C. (1999). "Grover's quantum searching algorithm is optimal". *Phys. Rev. A*, 60, 2746–2751.
