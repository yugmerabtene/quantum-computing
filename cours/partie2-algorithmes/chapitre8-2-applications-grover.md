# Chapitre 8.2 — Applications de Grover

## Ce que vous allez apprendre

- Maîtriser le **comptage quantique** (Quantum Counting) comme extension de Grover + QPE
- Comprendre comment Grover résout des **problèmes NP** (SAT, coloriage, etc.)
- Connaître les **bornes inférieures** et l'optimalité de Grover
- Étudier la **robustesse au bruit** et les seuils de tolérance
- Découvrir les **applications avancées** : minimum quantique, marche quantique

---

## Motivation

L'algorithme de Grover (chapitre 8.1) trouve un élément marqué parmi $N$ en $O(\sqrt{N})$ requêtes. Mais que peut-on en faire d'autre ?

D'abord, on peut **compter** le nombre de solutions sans les énumérer toutes — c'est le comptage quantique, qui combine Grover et la QPE (chapitre 6.2). Ensuite, Grover s'applique à tout problème de recherche : résoudre un Sudoku, trouver un chemin dans un labyrinthe, optimiser une fonction. Même si l'accélération n'est que quadratique, elle est **universelle** et s'applique à des problèmes pratiques.

Enfin, comprendre les limites de Grover (bornes inférieures, robustesse au bruit) est essentiel pour savoir quand l'algorithme est vraiment utile sur du hardware réel.

---

## Idée principale

Grover est un « couteau suisse » quantique. Si vous avez un problème qui peut s'énoncer comme « trouver $x$ tel que $f(x) = 1$ », Grover peut vous aider, même si $f$ est un algorithme complexe qui vérifie des contraintes.

Le comptage quantique va plus loin : au lieu de trouver UNE solution, il estime COMBIEN il y en a. C'est comme passer de « il y a au moins un trésor sur cette île » à « il y a environ 42 trésors ».

Et quand on ne connaît pas le nombre de solutions ? L'algorithme de Boyer et al. utilise un nombre d'itérations aléatoire pour s'adapter automatiquement.

---

## Contenu du cours

### Section 1 : Comptage quantique (Quantum Counting)

**Problème** : Soit $f : \{0,1\}^n \to \{0,1\}$. Estimer $M = |\{x : f(x) = 1\}|$ (nombre de solutions).

**Classique** : $O(N)$ évaluations pour compter exactement, $O(N/\epsilon^2)$ pour estimer à $\epsilon N$ près.

**Quantique** : $O(\sqrt{N}/\epsilon)$ évaluations.

**Algorithme** : Le comptage quantique combine Grover et QPE. L'opérateur de Grover $G = D \cdot O$ a pour valeurs propres :

$$e^{\pm 2i\theta}, \quad \text{où} \quad \sin\theta = \sqrt{\frac{M}{N}}$$

**Intuition** : l'angle de rotation $\theta$ dans le plan de Grover dépend du nombre de solutions $M$. Plus il y a de solutions, plus $\theta$ est grand. En estimant $\theta$ par QPE, on déduit $M = N \sin^2\theta$.

**Exemple** : $N = 16$, $M = 3$. $\sin\theta = \sqrt{3/16} \approx 0.433$, $\theta \approx 0.448$ rad. QPE estime $\theta$, puis on calcule $M = 16 \sin^2\theta \approx 3$.

### Section 2 : Résolution de problèmes NP avec Grover

**SAT (Satisfiabilité)** : Pour une formule CNF à $n$ variables, l'espace de recherche est $N = 2^n$.

**Approche** : Utiliser Grover avec un oracle qui vérifie la formule. L'oracle évalue la formule sur l'entrée et marque si elle est satisfaite.

$$k_{\text{opt}} = \frac{\pi}{4} \sqrt{2^n}$$

**Complexité** : $O(\sqrt{2^n} \cdot \text{taille de l'oracle})$. L'oracle pour une clause $l_1 \lor l_2 \lor \cdots \lor l_k$ utilise $O(k)$ portes.

**Intuition** : Grover ne résout pas P = NP. Il accélère la recherche exhaustive de $O(2^n)$ à $O(2^{n/2})$, mais ça reste exponentiel. C'est comme passer de 1 an à 1 heure pour un problème de 40 variables.

**Comparaison classique vs quantique** :

| Problème | Classique | Quantique (Grover) |
|----------|-----------|-------------------|
| 3-SAT | $O(1.307^n)$ | $O(2^{n/2})$ |
| Recherche | $O(N)$ | $O(\sqrt{N})$ |
| Max-Cut | $O(2^n)$ | $O(2^{n/2})$ |

### Section 3 : Bornes inférieures

**Optimalité de Grover** (rappel) : Tout algorithme quantique pour la recherche non structurée nécessite $\Omega(\sqrt{N})$ requêtes.

**Autres problèmes** :

| Problème | Borne inférieure | Algorithme |
|----------|-----------------|------------|
| Recherche | $\Omega(\sqrt{N})$ | Grover |
| Comptage (précision $\epsilon$) | $\Omega(1/\epsilon)$ | Comptage quantique |
| Collision | $\Omega(N^{1/3})$ | BHT |
| Élément distinct | $\Omega(N^{2/3})$ | — |

**Méthode polynomiale** : Les amplitudes après $k$ requêtes sont des polynômes de degré $k$ sur les bits de l'oracle. Pour distinguer $N$ oracles différents, le polynôme doit avoir $\Omega(\sqrt{N})$ oscillations, donc $k = \Omega(\sqrt{N})$.

### Section 4 : Robustesse au bruit

**Canal de déphasage** : $\mathcal{E}(\rho) = (1-p)\rho + p \, Z\rho Z$

L'algorithme de Grover dépend de la **cohérence** des qubits. Le bruit de déphasage détruit cette cohérence et réduit la probabilité de succès.

**Seuil de tolérance** : Grover reste efficace tant que :

$$p < \frac{1}{k_{\text{opt}}} \approx \frac{4}{\pi\sqrt{N}}$$

**Intuition** : chaque itération accumule un peu de bruit. Après $k_{\text{opt}}$ itérations, le bruit total doit rester petit. Plus $N$ est grand, plus $k_{\text{opt}}$ est grand, plus le seuil de tolérance est bas.

**Exemple** : $n = 10$ ($N = 1024$), $k_{\text{opt}} = 25$. Seuil : $p < 1/25 = 0.04$. Si le taux de bruit par porte dépasse 4%, Grover devient inefficace.

---

## Exemple guidé

**Comptage quantique** : $N = 16$ ($n = 4$), solutions = $\{2, 5, 11\}$, donc $M = 3$.

$\sin\theta = \sqrt{3/16} \approx 0.433$. $\theta \approx 0.448$ rad.

L'opérateur de Grover $G$ a pour valeurs propres $e^{\pm 2i\theta} = e^{\pm 0.896i}$.

Avec $m = 5$ qubits de contrôle pour la QPE, on estime $2\theta/(2\pi) \approx 0.143$.

Mesure attendue : $k \approx 0.143 \times 32 \approx 4.6$, donc $k = 4$ ou $5$.

Si $k = 5$ : $\theta_{\text{est}} = 5\pi/32 \approx 0.491$. $M_{\text{est}} = 16 \sin^2(0.491) \approx 3.6$.

Si $k = 4$ : $\theta_{\text{est}} = 4\pi/32 = 0.393$. $M_{\text{est}} = 16 \sin^2(0.393) \approx 2.4$.

La moyenne donne $M \approx 3$. ✓

---

## Implémentation Python

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# --- Oracle qui marque plusieurs solutions ---
def oracle_comptage(qc, n, solutions):
    """
    Oracle qui marque les états dans la liste 'solutions'.
    Pour chaque solution, on applique un phase flip.
    """
    target_bits = [format(s, f'0{n}b') for s in solutions]
    for target in target_bits:
        # Amener |target⟩ → |11...1⟩
        for i, bit in enumerate(target):
            if bit == '0':
                qc.x(i)

        # Phase flip sur |11...1⟩
        if n == 1:
            qc.z(0)
        else:
            qc.h(n - 1)
            qc.mcx(list(range(n - 1)), n - 1)
            qc.h(n - 1)

        # Restaurer
        for i, bit in enumerate(target):
            if bit == '0':
                qc.x(i)

# --- Diffuseur de Grover ---
def diffuseur(qc, n):
    """Diffuseur standard : inversion autour de la moyenne"""
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

# --- Comptage quantique : QPE sur l'opérateur de Grover ---
def comptage_quantique(n, solutions, m_qpe=4):
    """
    Comptage quantique.
    n : nombre de qubits de recherche
    solutions : liste des états marqués
    m_qpe : qubits de contrôle pour QPE
    """
    qc = QuantumCircuit(m_qpe + n, m_qpe)

    # Hadamard sur tous les qubits
    qc.h(range(m_qpe))              # Superposition des contrôles
    qc.h(range(m_qpe, m_qpe + n))   # Superposition de recherche

    # Application contrôlée de G^(2^j)
    for j in range(m_qpe):
        for _ in range(2**j):
            oracle_comptage(qc, n, solutions)
            diffuseur(qc, n)

    # QFT inverse sur les qubits de contrôle
    for i in range(m_qpe // 2):
        qc.swap(i, m_qpe - 1 - i)
    for i in range(m_qpe - 1, -1, -1):
        qc.h(i)
        for j in range(i):
            angle = -2 * np.pi / (2**(i - j + 1))
            qc.cp(angle, j, i)

    qc.measure(range(m_qpe), range(m_qpe))
    return qc

# --- Estimation de M à partir des mesures ---
def estimer_M(counts, n, m_qpe):
    """
    Estime M = nombre de solutions à partir des mesures QPE.
    """
    N = 2**n
    estimates = []
    for bits, count in counts.items():
        # Convertir les bits en estimation de θ
        theta_est = sum(int(bits[i]) / (2**(i+1)) for i in range(m_qpe)) * np.pi
        M_est = N * np.sin(theta_est)**2
        estimates.append((M_est, count))

    # Moyenne pondérée
    total = sum(count for _, count in estimates)
    M_avg = sum(M * count for M, count in estimates) / total
    return M_avg

# --- Test : N=16, M=3 solutions ---
n = 4
N = 2**n
solutions = [2, 5, 11]
print(f"Solutions : {solutions}, M={len(solutions)}")

qc_count = comptage_quantique(n, solutions, m_qpe=5)
backend = AerSimulator()
result = backend.run(qc_count, shots=4096).result()
counts = result.get_counts()

M_est = estimer_M(counts, n, 5)
print(f"M estimé (comptage quantique) : {M_est:.2f}")
print(f"M réel : {len(solutions)}")
```

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.providers.aer.noise import NoiseModel, phase_damping_error

# --- Grover avec bruit de déphasage ---
def oracle_grover(qc, n, target):
    """Oracle de Grover (même code que chapitre 8.1)"""
    target_bits = format(target, f'0{n}b')
    for i, bit in enumerate(target_bits):
        if bit == '0':
            qc.x(i)
    if n == 1:
        qc.z(0)
    else:
        qc.h(n - 1)
        qc.mcx(list(range(n - 1)), n - 1)
        qc.h(n - 1)
    for i, bit in enumerate(target_bits):
        if bit == '0':
            qc.x(i)

def diffuseur_grover(qc, n):
    """Diffuseur de Grover (même code que chapitre 8.1)"""
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

def grover_avec_bruit(n, target, p_bruit):
    """
    Grover avec bruit de déphasage.
    p_bruit : probabilité de déphasage par porte
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

    backend = AerSimulator()
    result = backend.run(qc, shots=4096,
                     noise_model=noise_model).result()
    counts = result.get_counts()
    prob_target = counts.get(format(target, f'0{n}b'), 0) / 4096

    return prob_target

# --- Analyse de la robustesse ---
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

```python
import numpy as np

# --- Seuil de tolérance au bruit ---
def seuil_tolerance():
    """
    Calcule le seuil de tolérance au bruit pour Grover.
    Au-delà de ce seuil, Grover n'est plus efficace.
    """
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

**Sortie attendue :**

```
=== Seuil de tolérance au bruit ===
n     N        k_opt    Seuil p   
-----------------------------------
2     4        2        0.500000  
3     8        2        0.500000  
4     16       3        0.333333  
5     32       4        0.250000  
6     64       6        0.166667  
7     128      9        0.111111  
8     256      13       0.076923  
9     512      18       0.055556  
10    1024     25       0.040000  
11    2048     36       0.027778  
```

```python
import numpy as np

# --- Algorithme de Durr-Hoyer pour le minimum ---
def durr_hoyer_minimum(liste):
    """
    Algorithme de Durr-Hoyer pour trouver le minimum d'une liste.
    Complexité : O(√N) requêtes quantiques.
    Version simulée (classique) pour illustration.
    """
    n = len(liste)
    N = 2**int(np.ceil(np.log2(n)))

    # Choisir un seuil initial aléatoire
    idx_seuil = np.random.randint(n)
    seuil = liste[idx_seuil]

    iterations = 0
    while True:
        iterations += 1
        # Recherche de Grover pour x tq liste[x] < seuil
        candidats = [i for i in range(n) if liste[i] < seuil]
        if not candidats:
            break
        # Mettre à jour le seuil
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

```python
import numpy as np

# --- Méthode polynomiale pour les bornes inférieures ---
def borne_inferieure_polynomiale():
    """
    Illustration de la méthode polynomiale (Beals et al.).
    """
    print("=== Méthode polynomiale (Beals et al.) ===")
    print()
    print("Principe : Après k appels à l'oracle, la probabilité P(x)")
    print("est un polynôme de degré ≤ 2k sur f(0), f(1), ..., f(N-1).")
    print()

    for N in [16, 32, 64, 128]:
        k_inf = int(np.sqrt(N) / 2)
        print(f"N={N} : k ≥ {k_inf} (borne inférieure)")

    print()
    print("Limitations :")
    print("  - Ne donne pas exactement π√N/4 mais Ω(√N)")
    print("  - Constante (π/4) obtenue par analyse géométrique")

borne_inferieure_polynomiale()
```

**Sortie attendue :**

```
=== Méthode polynomiale (Beals et al.) ===

Principe : Après k appels à l'oracle, la probabilité P(x)
est un polynôme de degré ≤ 2k sur f(0), f(1), ..., f(N-1).

N=16 : k ≥ 2 (borne inférieure)
N=32 : k ≥ 2 (borne inférieure)
N=64 : k ≥ 4 (borne inférieure)
N=128 : k ≥ 5 (borne inférieure)

Limitations :
  - Ne donne pas exactement π√N/4 mais Ω(√N)
  - Constante (π/4) obtenue par analyse géométrique
```

---

## Complexité et avantage quantique

| Problème | Classique | Quantique | Avantage |
|----------|-----------|-----------|----------|
| Recherche (1 solution) | $O(N)$ | $O(\sqrt{N})$ | Quadratique |
| Comptage (précision $\epsilon$) | $O(1/\epsilon^2)$ | $O(1/\epsilon)$ | Quadratique |
| Collision | $O(N^{1/2})$ | $O(N^{1/3})$ | Polynomial |
| Minimum | $O(N)$ | $O(\sqrt{N})$ | Quadratique |
| SAT ($n$ variables) | $O(1.307^n)$ | $O(2^{n/2})$ | Quadratique en $2^n$ |

**Pourquoi ces accélérations ?** Grover exploite le parallélisme quantique pour évaluer l'oracle sur toutes les entrées en superposition, puis utilise les interférences pour amplifier les solutions. Le comptage quantique ajoute la QPE pour estimer l'angle de rotation, qui encode le nombre de solutions.

---

## À retenir

1. Le **comptage quantique** combine Grover + QPE pour estimer le nombre de solutions $M$
2. Grover résout les problèmes **NP** en $O(\sqrt{2^n})$ au lieu de $O(2^n)$, mais ça reste exponentiel
3. Grover est **optimal** : $\Omega(\sqrt{N})$ est une borne inférieure pour la recherche
4. Le **bruit** limite l'efficacité : seuil $p < 1/k_{\text{opt}} \approx 4/(\pi\sqrt{N})$
5. L'algorithme de **Dürr-Høyer** trouve le minimum en $O(\sqrt{N})$
6. L'algorithme de **Boyer et al.** s'adapte quand le nombre de solutions $M$ est inconnu
7. Grover est un cas particulier de **marche quantique** sur un graphe complet

---

## Pièges à éviter

1. **Penser que Grover résout NP en polynomial** : $O(\sqrt{2^n}) = O(2^{n/2})$ reste exponentiel
2. **Oublier que le comptage est une estimation** : il donne $M$ avec une certaine précision, pas exactement
3. **Négliger le bruit** : pour $n > 10$, le seuil de tolérance est très bas (< 4%)
4. **Confondre recherche structurée et non structurée** : si le problème a de la structure, des algorithmes classiques peuvent être meilleurs
5. **Utiliser trop d'itérations** : si $M$ est inconnu, il faut l'algorithme de Boyer et al.

---

## Exercices

### Niveau 1 — Application directe

**Exercice 1** : Utilisez le comptage quantique pour estimer le nombre de solutions d'une formule 2-SAT avec $n=8$ variables. Comparez avec l'énumération exhaustive.

**Exercice 2** : Implémentez Grover lorsque $M$ est inconnu (algorithme de Boyer et al.). Utilisez un nombre d'itérations aléatoire.

```python
def grover_boyer(n, oracle, max_iter=100):
    """
    Algorithme de Boyer et al. : Grover avec M inconnu.
    À chaque essai, on choisit un nombre d'itérations aléatoire,
    on mesure, et on vérifie si c'est une solution.
    """
    for _ in range(max_iter):
        k = np.random.randint(1, int(np.sqrt(2**n)))
        # Appliquer k itérations de Grover
        # Mesurer et vérifier
        pass
```

### Niveau 2 — Compréhension

**Exercice 3** : Montrez que la recherche de collision nécessite $\Omega(N^{1/3})$ requêtes quantiques. Implémentez l'algorithme BHT.

**Exercice 4** : Comparez l'effet du canal dépolarisant vs déphasage sur Grover pour $n=6$. Quel canal est le plus nuisible ?

### Niveau 3 — Défi

**Exercice 5** : Utilisez Grover pour trouver un chemin dans un labyrinthe $4 \times 4$. Construisez un oracle qui vérifie la validité du chemin.

**Exercice 6** : Montrez que Grover est un cas particulier de marche quantique (Quantum Walk) sur un graphe complet. Implémentez la marche quantique correspondante.

```python
import numpy as np
import qutip as qt

def quantum_walk_grover(n):
    """
    Marche quantique sur graphe complet = itération de Grover.
    L'opérateur de coin = Hadamard, l'opérateur de déplacement = oracle.
    """
    N = 2**n
    # Complétez...
    pass
```

---

## Pour aller plus loin

- Les **marches quantiques** (Quantum Walks) généralisent Grover à des graphes non complets
- L'**algorithme d'Ambainis** pour le problème de l'élément distinct utilise une marche quantique en $O(N^{2/3})$
- L'**amplitude estimation** est utilisée en finance quantique pour estimer des valeurs attendues

---

## Références

- Brassard, G., Høyer, P. & Tapp, A. (1998). "Quantum Counting". *Proc. 25th ICALP*, 820–831.
- Boyer, M. et al. (1998). "Tight bounds on quantum searching". *Fortsch. Phys.*, 46(4-5), 493–505.
- Dürr, C. & Høyer, P. (1996). "A quantum algorithm for finding the minimum". *arXiv:quant-ph/9607014*.
- Beals, R. et al. (2001). "Quantum lower bounds by polynomials". *J. ACM*, 48(4), 778–797.
- Ambainis, A. (2004). "Quantum search algorithms". *ACM SIGACT News*, 35(2), 22–35.
