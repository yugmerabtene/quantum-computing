# Séance 8.2 — Applications de Grover

## Objectifs d'apprentissage

- Maîtriser le comptage quantique (Quantum Counting) comme extension de Grover
- Analyser la résolution de problèmes NP avec Grover
- Comprendre les bornes inférieures et l'optimalité
- Étudier la robustesse au bruit

---

## 1. Comptage quantique (Quantum Counting)

### Problème

Soit $f : \{0,1\}^n \to \{0,1\}$. Estimer le nombre $M = |\{x : f(x) = 1\}|$ (taille du espace de solutions) avec une accélération quantique.

### Algorithme

Le comptage quantique combine Grover et QPE. L'opérateur de Grover $G$ a pour valeurs propres :

$$e^{\pm 2i\theta}, \quad \text{où} \quad \sin\theta = \sqrt{\frac{M}{N}}$$

En appliquant QPE sur $G$, on estime $2\theta$, d'où $M = N \sin^2\theta$.

### Analyse de précision

Pour une estimation à $\epsilon$ près, le comptage quantique utilise $O(1/\epsilon)$ itérations, contre $O(1/\epsilon^2)$ classiquement.

```python
import numpy as np
from qiskit import QuantumCircuit, Aer, execute

def oracle_comptage(qc, n, solutions):
    """
    Oracle qui marque les états dans la liste 'solutions'.
    """
    target_bits = [format(s, f'0{n}b') for s in solutions]
    for target in target_bits:
        for i, bit in enumerate(target):
            if bit == '0':
                qc.x(i)

        if n == 1:
            qc.z(0)
        else:
            qc.h(n - 1)
            qc.mcx(list(range(n - 1)), n - 1)
            qc.h(n - 1)

        for i, bit in enumerate(target):
            if bit == '0':
                qc.x(i)

def diffuseur(qc, n):
    """Diffuseur de Grover standard"""
    qc.h(range(n))
    qc.x(range(n))
    if n == 1:
        qc.z(0)
    else:
        qc.h(n - 1)
        qc.mcx(list(range(n - 1)), n - 1)
        qc.h(n - 1)
    qc.x(range(n))
    qc.h(range(n))

def comptage_quantique(n, solutions, m_qpe=4):
    """
    Comptage quantique : QPE sur l'opérateur de Grover.
    n : nombre de qubits de recherche
    solutions : liste des états marqués
    m_qpe : qubits de contrôle pour QPE
    """
    qc = QuantumCircuit(m_qpe + n, m_qpe)

    # Hadamard sur tous les qubits
    qc.h(range(m_qpe))
    qc.h(range(m_qpe, m_qpe + n))

    # Application contrôlée de G^(2^j)
    for j in range(m_qpe):
        for _ in range(2**j):
            oracle_comptage(qc, n, solutions)
            diffuseur(qc, n)

    # QFT inverse
    for i in range(m_qpe // 2):
        qc.swap(i, m_qpe - 1 - i)
    for i in range(m_qpe - 1, -1, -1):
        qc.h(i)
        for j in range(i):
            angle = -2 * np.pi / (2**(i - j + 1))
            qc.cp(angle, j, i)

    qc.measure(range(m_qpe), range(m_qpe))
    return qc

def estimer_M(counts, n, m_qpe):
    """
    Estime M = nombre de solutions à partir des mesures.
    """
    N = 2**n
    estimates = []
    for bits, count in counts.items():
        theta_est = sum(int(bits[i]) / (2**(i+1)) for i in range(m_qpe)) * np.pi
        M_est = N * np.sin(theta_est)**2
        estimates.append((M_est, count))

    # Moyenne pondérée
    total = sum(count for _, count in estimates)
    M_avg = sum(M * count for M, count in estimates) / total
    return M_avg

# Test : N=16, M=3 solutions
n = 4
N = 2**n
solutions = [2, 5, 11]
print(f"Solutions : {solutions}, M={len(solutions)}")

qc_count = comptage_quantique(n, solutions, m_qpe=5)
backend = Aer.get_backend('qasm_simulator')
result = execute(qc_count, backend, shots=4096).result()
counts = result.get_counts()

M_est = estimer_M(counts, n, 5)
print(f"M estimé (comptage quantique) : {M_est:.2f}")
print(f"M réel : {len(solutions)}")
```

## 2. Résolution de problèmes NP avec Grover

### SAT (Satisfiability)

Pour une formule CNF à $n$ variables, l'espace de recherche est $N = 2^n$.

**Approche naïve** : Utiliser Grover avec un oracle qui vérifie la formule.

$$k_{\text{opt}} = \frac{\pi}{4} \sqrt{2^n}$$

### Complexité

$$O(\sqrt{2^n} \cdot \text{taille de l'oracle})$$

L'oracle pour une clause $l_1 \lor l_2 \lor \cdots \lor l_k$ utilise $O(k)$ portes.

Pour une formule CNF à $m$ clauses : oracle de taille $O(m \cdot n)$.

### Comparaison classique vs quantique

| Problème | Classique | Quantique (Grover) |
|----------|-----------|-------------------|
| 3-SAT | $O(1.307^n)$ | $O(2^{n/2})$ |
| Recherche | $O(N)$ | $O(\sqrt{N})$ |
| Max-Cut | $O(2^n)$ | $O(2^{n/2})$ |

```python
import numpy as np

def oracle_sat_3(qc, n, clauses):
    """
    Oracle pour 3-SAT.
    clauses : liste de triplets (var1, var2, var3, signes)
    Exemple : (0, 1, 2, (True, False, True)) → x₀ ∨ ¬x₁ ∨ x₂
    """
    # Pour chaque clause, on utilise un qubit auxiliaire
    # et une porte multi-contrôlée
    n_aux = len(clauses)
    # Note : en pratique, on utilise un registre auxiliaire

    for clause_idx, (v1, v2, v3, signs) in enumerate(clauses):
        aux = n + clause_idx

        # Appliquer X si signe négatif
        for var, sign in [(v1, signs[0]), (v2, signs[1]), (v3, signs[2])]:
            if not sign:
                qc.x(var)

        # Vérification : clause satisfaite si au moins une variable est 1
        # On utilise une porte CCX (Toffoli) avec qubit auxiliaire
        # Clause = l₁ ∨ l₂ ∨ l₃  ⇔  ¬(¬l₁ ∧ ¬l₂ ∧ ¬l₃)
        # On marque quand la clause est FALSE
        qc.ccx(v1, v2, aux)
        qc.cx(aux, v3)
        qc.ccx(v1, v2, aux)

def grover_sat(n, clauses, target_assignment=None):
    """
    Grover pour résoudre une instance SAT.
    """
    N = 2**n
    k_opt = int(np.pi / 4 * np.sqrt(N) - 0.5) + 1

    qc = QuantumCircuit(n, n)
    qc.h(range(n))

    for _ in range(k_opt):
        oracle_sat_3(qc, n, clauses)
        diffuseur(qc, n)

    qc.measure(range(n), range(n))
    return qc
```

## 3. Bornes inférieures

### Optimalité de Grover (rappel)

**Théorème** : Tout algorithme quantique pour la recherche non structurée nécessite $\Omega(\sqrt{N})$ requêtes.

### Bornes pour d'autres problèmes

| Problème | Borne inférieure | Atteinte |
|----------|-----------------|----------|
| Recherche | $\Omega(\sqrt{N})$ | Grover |
| Comptage (précision $\epsilon$) | $\Omega(1/\epsilon)$ | Comptage quantique |
| Collision | $\Omega(N^{1/3})$ | BHT |
| Élément distinct | $\Omega(N^{2/3})$ | — |

### Méthode de la borne polynomiale (polynomial method)

Les amplitudes après $k$ requêtes sont des polynômes de degré $k$ sur les bits de l'oracle. Pour distinguer $N$ oracles différents, le polynôme doit avoir $\Omega(\sqrt{N})$ oscillations.

```python
import numpy as np

def borne_inferieure_polynomiale():
    """
    Illustration de la méthode polynomiale pour la borne inférieure.
    """
    print("=== Méthode polynomiale (Beals et al.) ===")
    print()
    print("Principe : Après k appels à l'oracle, la probabilité P(x)")
    print("est un polynôme de degré ≤ 2k sur f(0), f(1), ..., f(N-1).")
    print()

    # Pour la recherche, P(x*) = 1 pour exactement un oracle
    # Un polynôme de degré d qui vaut 1 en un point et 0 ailleurs
    # doit avoir d = Ω(N) → k = Ω(√N)
    for N in [16, 32, 64, 128]:
        k_inf = int(np.sqrt(N) / 2)  # Borne inférieure
        print(f"N={N} : k ≥ {k_inf} (borne inférieure)")

    print()
    print("Limitations :")
    print("  - Ne donne pas exactement π√N/4 mais Ω(√N)")
    print("  - Constante (π/4) obtenue par analyse géométrique")

borne_inferieure_polynomiale()
```

## 4. Robustesse au bruit

### Canal de déphasage (dephasing)

L'opération de Grover applique $G = D \cdot O$ qui dépend de la cohérence du système. Le canal de déphasage :

$$\mathcal{E}(\rho) = (1-p)\rho + p \, Z\rho Z$$

détruit la cohérence dans la base $\{|0\rangle, |1\rangle\}$.

### Probabilité de succès avec bruit

```python
import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.providers.aer.noise import NoiseModel, phase_damping_error

def grover_avec_bruit(n, target, p_bruit):
    """
    Grover avec bruit de déphasage.
    """
    # Modèle de bruit
    error = phase_damping_error(p_bruit)
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(error, ['h', 'cx', 'x', 'z'])

    N = 2**n
    k_opt = int(np.pi / 4 * np.sqrt(N) - 0.5) + 1

    qc = QuantumCircuit(n, n)
    qc.h(range(n))

    for _ in range(k_opt):
        oracle_grover(qc, n, target)
        diffuseur_grover(qc, n)

    qc.measure(range(n), range(n))

    # Simulation avec bruit
    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend, shots=4096,
                     noise_model=noise_model).result()
    counts = result.get_counts()
    prob_target = counts.get(format(target, f'0{n}b'), 0) / 4096

    return prob_target

def robustesse_bruit():
    """Analyse de la robustesse en fonction du bruit."""
    n = 4
    target = 7
    bruits = [0.0, 0.001, 0.005, 0.01, 0.02, 0.05, 0.1]

    print("=== Robustesse de Grover au bruit de déphasage ===")
    print(f"n={n}, cible={target}")
    print("-" * 50)
    print(f"{'Bruit':<10} {'P(succès)':<15} {'Efficace ?':<15}")
    print("-" * 50)

    for p in bruits:
        prob = grover_avec_bruit(n, target, p)
        efficace = "Oui" if prob > 0.5 else "Non"
        print(f"{p:<10.4f} {prob:<15.4f} {efficace:<15}")

robustesse_bruit()
```

### Seuil de tolérance

L'algorithme de Grover reste efficace tant que :

$$p < \frac{1}{k_{\text{opt}}} \approx \frac{4}{\pi\sqrt{N}}$$

Pour $n=10$ : $p < 0.04$ environ.

```python
import numpy as np

def seuil_tolerance():
    """Calcule le seuil de tolérance au bruit pour Grover."""
    print("=== Seuil de tolérance au bruit ===")
    print(f"{'n':<5} {'N':<8} {'k_opt':<8} {'Seuil p':<10}")
    print("-" * 35)

    for n in range(2, 12):
        N = 2**n
        k_opt = int(np.pi / 4 * np.sqrt(N) - 0.5) + 1
        seuil = 1.0 / k_opt if k_opt > 0 else 1.0
        print(f"{n:<5} {N:<8} {k_opt:<8} {seuil:<10.6f}")

seuil_tolerance()
```

## 5. Applications avancées

### Minimum quantique (Durr-Hoyer)

Trouver le minimum d'une liste non triée en $O(\sqrt{N})$ requêtes.

**Algorithme** :
1. Choisir un seuil aléatoire $y$
2. Recherche de Grover pour $x$ tel que $f(x) < y$
3. Mettre à jour $y$ et répéter

### Estimation de moyenne

L'estimation de la valeur moyenne d'une fonction $f: \{0,1\}^n \to [0,1]$ peut être accélérée quadratiquement par rapport à l'échantillonnage classique.

```python
import numpy as np

def durr_hoyer_minimum(liste):
    """
    Algorithme de Durr-Hoyer pour trouver le minimum.
    Version simulée (classique) pour illustration.
    """
    n = len(liste)
    N = 2**int(np.ceil(np.log2(n)))

    idx_seuil = np.random.randint(n)
    seuil = liste[idx_seuil]

    iterations = 0
    while True:
        iterations += 1
        # Recherche de Grover pour x tq liste[x] < seuil
        # En pratique, cela prend O(√N) requêtes
        candidats = [i for i in range(n) if liste[i] < seuil]
        if not candidats:
            break
        idx_seuil = np.random.choice(candidats)
        seuil = liste[idx_seuil]

    print(f"Minimum trouvé : {seuil} à l'index {idx_seuil}")
    print(f"Itérations : {iterations}")
    return idx_seuil, seuil

# Test
liste = np.random.randint(0, 1000, 50)
print("Liste :", liste[:10], "...")
print(f"Min réel : {np.min(liste)} à {np.argmin(liste)}")
idx, val = durr_hoyer_minimum(liste)
```

## 6. Exercices

### Exercice 1 : Comptage quantique pour SAT
Utilisez le comptage quantique pour estimer le nombre de solutions satisfaisant une formule 2-SAT avec $n=8$ variables. Comparez avec l'énumération exhaustive.

### Exercice 2 : Grover adaptatif pour plusieurs cibles
Implémentez Grover lorsque $M$ est inconnu (algorithme de Boyer et al.). Utilisez un nombre d'itérations aléatoire.

```python
def grover_boyer(n, oracle, max_iter=100):
    """
    Algorithme de Boyer et al. : Grover avec M inconnu.
    """
    for _ in range(max_iter):
        k = np.random.randint(1, int(np.sqrt(2**n)))
        # Appliquer k itérations de Grover
        # Mesurer et vérifier
        pass
```

### Exercice 3 : Bornes inférieures — collision
Montrez que la recherche de collision nécessite $\Omega(N^{1/3})$ requêtes quantiques. Implémentez l'algorithme BHT.

### Exercice 4 : Robustesse — canal dépolarisant
Comparez l'effet du canal dépolarisant vs déphasage sur Grover pour $n=6$. Quel canal est le plus nuisible ?

### Exercice 5 : Application — résolution de Maze
Utilisez Grover pour trouver un chemin dans un labyrinthe $4 \times 4$. Construisez un oracle qui vérifie la validité du chemin.

### Exercice 6 : Quantum Walk — extension de Grover
Montrez que Grover est un cas particulier de marche quantique (Quantum Walk) sur un graphe complet. Implémentez la marche quantique correspondante.

```python
import numpy as np
import qutip as qt

def quantum_walk_grover(n):
    """
    Marche quantique sur graphe complet = itération de Grover.
    """
    N = 2**n
    # Opérateur de coin : Hadamard
    # Opérateur de déplacement : oracle
    # Une itération de marche = G (Grover)
    pass
```

---

## Références

- Brassard, G., Høyer, P. & Tapp, A. (1998). "Quantum Counting". *Proc. 25th ICALP*, 820–831.
- Boyer, M. et al. (1998). "Tight bounds on quantum searching". *Fortsch. Phys.*, 46(4-5), 493–505.
- Dürr, C. & Høyer, P. (1996). "A quantum algorithm for finding the minimum". *arXiv:quant-ph/9607014*.
- Beals, R. et al. (2001). "Quantum lower bounds by polynomials". *J. ACM*, 48(4), 778–797.
- Ambainis, A. (2004). "Quantum search algorithms". *ACM SIGACT News*, 35(2), 22–35.
