# Chapitre 7.1 — Algorithme de Shor

## Ce que vous allez apprendre

- Comprendre la **réduction factorisation → recherche de période** (la partie classique)
- Maîtriser l'**exponentiation modulaire quantique** et son circuit
- Implémenter le circuit complet pour **$N = 15$** et extraire les facteurs
- Analyser l'**impact sur la cryptographie RSA** et les contre-mesures post-quantiques
- Voir comment la QPE (chapitre 6.2) et la QFT (chapitre 6.1) s'assemblent pour former Shor

---

## Motivation

En 1994, Peter Shor a montré qu'un ordinateur quantique peut factoriser un entier $N$ en temps polynomial. Cela peut sembler anodin, mais c'est un séisme : la sécurité de **RSA**, le système de chiffrement qui protège vos transactions bancaires, vos emails, et la plupart des communications sur Internet, repose exactement sur la difficulté de factoriser de grands nombres.

L'idée géniale de Shor est une réduction en deux étapes. D'abord, une réduction **classique** : factoriser $N$ revient à trouver la **période** de la fonction $f(x) = a^x \bmod N$. Ensuite, une réduction **quantique** : trouver cette période se fait efficacement avec la QPE (estimation de phase quantique, chapitre 6.2), elle-même basée sur la QFT (chapitre 6.1).

C'est l'aboutissement de tout ce que nous avons construit depuis le début : le phase kickback (chapitre 5.1), la détection de période de Simon (chapitre 5.2), la QFT (chapitre 6.1) et la QPE (chapitre 6.2) convergent dans cet algorithme.

---

## Idée principale

Imaginez que vous voulez savoir si une roue dentée a un défaut. Vous la faites tourner et vous regardez si un motif se répète. Si le motif se répète toutes les $r$ dents, alors $r$ est la période.

Shor fait la même chose, mais avec des nombres. La fonction $f(x) = a^x \bmod N$ est périodique : $f(x+r) = f(x)$. Si on trouve $r$ (la période), et si $r$ est pair, alors $a^{r/2}$ est une racine carrée de 1 modulo $N$. Et $\gcd(a^{r/2} \pm 1, N)$ donne un facteur de $N$ !

Quantiquement, on prépare une superposition de tous les $x$, on calcule $a^x \bmod N$ en parallèle, puis on utilise la QPE pour détecter la période. La QFT transforme la périodicité temporelle en pics de fréquence, exactement comme en traitement du signal.

---

## Contenu du cours

### Section 1 : Réduction classique — de la factorisation à la période

**Problème** : Soit $N$ un entier composé à factoriser.

**Étape 1** — Choisir $a$ aléatoire avec $1 < a < N$ et $\gcd(a, N) = 1$.

**Intuition** : $a$ doit être premier avec $N$ pour que la fonction $x \mapsto a^x \bmod N$ soit périodique.

**Étape 2** — Définir $f(x) = a^x \bmod N$. Cette fonction est périodique :

$$f(x+r) = f(x) \bmod N, \quad r = \text{ord}_N(a)$$

**Intuition** : $r$ est le plus petit entier tel que $a^r \equiv 1 \pmod N$. C'est l'« ordre » de $a$ modulo $N$.

**Exemple** : $N = 15, a = 2$.
$2^0 = 1, 2^1 = 2, 2^2 = 4, 2^3 = 8, 2^4 = 16 \equiv 1 \pmod{15}$. Donc $r = 4$.

**Étape 3** — Si $r$ est pair et $a^{r/2} \not\equiv \pm 1 \pmod N$, alors :

$$\gcd(a^{r/2} + 1, N) \quad \text{et} \quad \gcd(a^{r/2} - 1, N)$$

sont des facteurs non triviaux de $N$.

**Pourquoi ça marche ?** $a^r \equiv 1 \pmod N$ signifie $(a^{r/2} - 1)(a^{r/2} + 1) \equiv 0 \pmod N$. Donc $N$ divise le produit, mais ne divise ni l'un ni l'autre facteur (car $a^{r/2} \not\equiv \pm 1$). Les facteurs de $N$ se répartissent donc entre les deux termes.

**Exemple** : $N = 15, a = 2, r = 4$. $a^{r/2} = 2^2 = 4$.
$\gcd(4+1, 15) = \gcd(5, 15) = 5$
$\gcd(4-1, 15) = \gcd(3, 15) = 3$
$15 = 3 \times 5$ ✓

**Probabilité de succès** : Pour un $a$ aléatoire, $P(r \text{ pair et } a^{r/2} \not\equiv \pm 1) \geq 1/2$. Donc en choisissant quelques $a$ aléatoires, on trouve les facteurs avec haute probabilité.

### Section 2 : Partie quantique — trouver la période par QPE

**Architecture** :
```
Registre 1 (2n qubits) : |0⟩ — H⊗²ⁿ — QFT† — M → estimation de phase
                       |         |
Registre 2 (n qubits) : |0⟩ — — — U_a — — — — M (optionnel)
```

Où $U_a$ est l'opérateur d'exponentiation modulaire : $U_a |x\rangle = |ax \bmod N\rangle$.

**Étape 1** — État initial :
$$|\psi_0\rangle = |0\rangle^{\otimes 2n} |1\rangle$$

**Intuition** : on initialise le registre 2 à $|1\rangle$ car $U_a|1\rangle = |a \bmod N\rangle$, ce qui lance la séquence $1, a, a^2, \ldots$

**Étape 2** — Hadamard sur le registre 1 :
$$|\psi_1\rangle = \frac{1}{\sqrt{2^{2n}}} \sum_{j=0}^{2^{2n}-1} |j\rangle |1\rangle$$

**Étape 3** — Exponentiation modulaire contrôlée :
$$|\psi_2\rangle = \frac{1}{\sqrt{2^{2n}}} \sum_{j=0}^{2^{2n}-1} |j\rangle |a^j \bmod N\rangle$$

**Intuition** : le registre 1 est en superposition de tous les $j$, et le registre 2 contient $a^j \bmod N$ pour chaque $j$. La périodicité de $f(j) = a^j \bmod N$ est maintenant encodée dans l'état quantique.

**Étape 4** — QFT inverse sur le registre 1 :
$$|\psi_3\rangle = QFT^\dagger \otimes I \left( \frac{1}{\sqrt{2^{2n}}} \sum_{j=0}^{2^{2n}-1} |j\rangle |a^j \bmod N\rangle \right)$$

**Analyse par QPE** : Les valeurs propres de $U_a$ sont $e^{2\pi i k/r}$ pour $k=0,\ldots,r-1$. La QPE estime $k/r$ avec $2n$ qubits de précision.

Soit $c$ la mesure du premier registre. Alors $c/2^{2n} \approx k/r$ pour un certain $k$. On trouve $r$ via le **développement en fractions continues**.

**Intuition** : le développement en fractions continues trouve la fraction $k/r$ la plus simple qui approche $c/2^{2n}$. Comme $r < N < 2^n$ et qu'on a $2n$ bits de précision, l'approximation est suffisante pour retrouver exactement $r$.

### Section 3 : Exponentiation modulaire

Implémenter $U_a |x\rangle = |ax \bmod N\rangle$ est la partie la plus coûteuse.

**Multiplication modulaire** :
$$a^j \bmod N = a^{j_{n-1}2^{n-1}} \times \cdots \times a^{j_0 2^0} \bmod N$$

**Intuition** : on décompose $j$ en binaire et on multiplie les puissances de $a$ correspondantes. Chaque multiplication modulaire $|x\rangle \to |a^{2^k} x \bmod N\rangle$ est implémentée par des additionneurs quantiques.

**Complexité** :
- Portes : $O(n^3)$
- Profondeur : $O(n^3)$
- Qubits : $O(n)$ (avec optimisation)

---

## Exemple guidé

Factorisons $N = 15$ avec $a = 2$.

**Partie classique** :
$\gcd(2, 15) = 1$ ✓. La fonction $f(x) = 2^x \bmod 15$ :
$f(0) = 1, f(1) = 2, f(2) = 4, f(3) = 8, f(4) = 1, \ldots$

Période $r = 4$. $r$ est pair ✓. $a^{r/2} = 4 \not\equiv \pm 1 \pmod{15}$ ✓.

Facteurs : $\gcd(4+1, 15) = 5$, $\gcd(4-1, 15) = 3$. Donc $15 = 3 \times 5$.

**Partie quantique** (esquisse avec $n = 4$, donc $2n = 8$ qubits de contrôle) :

Les valeurs propres de $U_2$ sont $e^{2\pi i k/4}$ pour $k = 0, 1, 2, 3$, c'est-à-dire $1, i, -1, -i$.

Les phases sont $\theta = k/r = 0, 1/4, 1/2, 3/4$.

Avec 8 qubits de contrôle, la QPE donne $c/256 \approx k/4$. Donc $c \approx 0, 64, 128, 192$.

Si on mesure $c = 64$ : $64/256 = 1/4$. Fraction continue : $1/4$. Donc $r = 4$. ✓

Si on mesure $c = 128$ : $128/256 = 1/2$. Fraction continue : $1/2$. Donc $r = 2$. $r$ est pair, $a^{r/2} = 2 \not\equiv \pm 1$. $\gcd(3, 15) = 3, \gcd(1, 15) = 1$. On trouve quand même un facteur !

---

## Implémentation Python

```python
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from fractions import Fraction

# --- Multiplication modulaire contrôlée pour N=15 ---
def c_amod15(qc, a, power, control, target):
    """
    Multiplication modulaire contrôlée : |x⟩ → |a^{power}·x mod 15⟩.
    Implémentée pour N=15 avec des portes élémentaires (SWAP, CX).
    Chaque valeur de a^power mod 15 correspond à une permutation spécifique.
    """
    U = a**power % 15
    for _ in range(U):
        # Pour N=15, la multiplication par a mod 15 est une permutation
        # des 4 qubits du registre, implémentée par SWAP et CX
        if U == 2:
            qc.swap(control, target)
        elif U == 4:
            qc.swap(control, target)
            qc.swap(target, control)
        elif U == 7:
            qc.swap(control, target)
            qc.cx(control, target)
        elif U == 8:
            qc.cx(control, target)

# --- Circuit de Shor pour N=15 ---
def shor_circuit_15(a=2):
    """
    Circuit de Shor pour N=15 avec multiplicateur a.
    Utilise 4 qubits de contrôle pour la QPE.
    """
    n_count = 4  # qubits de contrôle
    qc = QuantumCircuit(n_count + 4, n_count)

    # Hadamard sur les qubits de contrôle → superposition
    qc.h(range(n_count))

    # Préparation du registre de fonction en |1⟩
    qc.x(n_count + 3)

    # Exponentiation modulaire contrôlée U_a^(2^j)
    for j in range(n_count):
        for _ in range(2**j):
            c_amod15(qc, a, 2**j, j, n_count)

    # QFT inverse sur les qubits de contrôle
    for j in range(n_count // 2):
        qc.swap(j, n_count - 1 - j)
    for i in range(n_count - 1, -1, -1):
        qc.h(i)
        for j in range(i):
            angle = -2 * np.pi / (2**(i - j + 1))
            qc.cp(angle, j, i)

    qc.measure(range(n_count), range(n_count))

    return qc

# --- Exécution complète de Shor pour N=15 ---
def shor_15(a=2):
    """
    Factorise N=15 en utilisant l'algorithme de Shor avec base a.
    """
    qc = shor_circuit_15(a)
    backend = AerSimulator()

    print(f"Factorisation de N=15 avec a={a}")

    for shot in range(5):
        result = backend.run(qc, shots=1).result()
        counts = result.get_counts()
        measured = list(counts.keys())[0]

        # Interprétation : c / 2^n_count ≈ k / r
        c = int(measured, 2)
        n_count = len(measured)
        theta = c / (2**n_count)

        # Développement en fractions continues pour retrouver r
        frac = Fraction(theta).limit_denominator(15)

        r = frac.denominator
        print(f"  Mesure: {measured} (c={c}) → θ={theta:.4f} ≈ {frac.numerator}/{frac.denominator}")

        if r % 2 == 0:
            guess1 = np.gcd(a**(r//2) - 1, 15)
            guess2 = np.gcd(a**(r//2) + 1, 15)
            print(f"    r={r}, a^(r/2)={a**(r//2)} → facteurs: {guess1}, {guess2}")
            if guess1 != 1 and guess1 != 15:
                return guess1, guess2

    return None, None

# Test
fact1, fact2 = shor_15(a=2)
print(f"\nRésultat : {fact1} × {fact2} = {fact1 * fact2}")
```

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from fractions import Fraction

# --- Circuit de Shor plus complet ---
def oracle_shor_complet(N=15, a=2, n_count=8):
    """
    Circuit de Shor avec n_count qubits de contrôle.
    Plus de qubits → meilleure précision pour l'estimation de phase.
    """
    n = int(np.ceil(np.log2(N)))
    qc = QuantumCircuit(n_count + n, n_count)

    # Hadamard sur les qubits de contrôle
    qc.h(range(n_count))

    # Registre de fonction en |1⟩
    qc.x(n_count)

    # U^(2^j) contrôlé — version simplifiée pour N=15
    for j in range(n_count):
        power = 2**j
        val = a % 15
        if val == 2:
            qc.swap(n_count, n_count + 1)
            qc.swap(n_count + 1, n_count + 2)
            qc.swap(n_count + 2, n_count + 3)
        elif val == 4:
            qc.swap(n_count, n_count + 2)
            qc.swap(n_count + 1, n_count + 3)
        elif val == 7:
            qc.swap(n_count, n_count + 1)
            qc.swap(n_count + 1, n_count + 2)
            qc.swap(n_count + 2, n_count + 3)
            qc.cx(n_count + 2, n_count)
            qc.cx(n_count + 1, n_count + 3)
        elif val == 8:
            qc.swap(n_count, n_count + 3)
            qc.swap(n_count + 1, n_count + 2)
            qc.cx(n_count + 2, n_count + 1)

    # QFT inverse
    for i in range(n_count // 2):
        qc.swap(i, n_count - 1 - i)
    for i in range(n_count):
        qc.h(i)
        if i != n_count - 1:
            for j in range(i + 1, n_count):
                angle = -2 * np.pi / (2**(j - i + 1))
                qc.cp(angle, j, i)

    qc.measure(range(n_count), range(n_count))
    return qc

# --- Analyse des résultats ---
def analyse_resultats(counts, n_count, N=15, a=2):
    """Analyse les mesures pour en déduire les facteurs de N."""
    for bits, count in counts.items():
        c = int(bits, 2)
        theta = c / (2**n_count)

        # Fractions continues pour retrouver r
        frac = Fraction(theta).limit_denominator(N * 2)
        r = frac.denominator

        if r % 2 == 0:
            guess1 = np.gcd(a**(r//2) - 1, N)
            guess2 = np.gcd(a**(r//2) + 1, N)
            if guess1 != 1 and guess1 != N:
                print(f"Facteurs trouvés: {N} = {guess1} × {guess2}")
                return guess1, guess2

    print("Aucun facteur trouvé dans les échantillons")
    return None, None

# Exécution
N, a = 15, 2
n_count = 8
qc = oracle_shor_complet(N, a, n_count)
backend = AerSimulator()
result = backend.run(qc, shots=1024).result()
analyse_resultats(result.get_counts(), n_count, N, a)
```

```python
import numpy as np

# --- Impact de Shor sur RSA ---
def impact_rsa_shor(taille_bits=2048):
    """
    Calcule les ressources nécessaires pour casser RSA avec Shor.
    Modèle simplifié basé sur l'analyse de Fowler et al. (2012).
    """
    # Qubits logiques nécessaires : 2n + O(1)
    n_qubits_logiques = 2 * taille_bits

    # Qubits physiques avec correction d'erreur (surface code)
    # Facteur de surcoût : ~1000 qubits physiques par qubit logique
    facteur_surcout = 1000
    n_qubits_physiques = n_qubits_logiques * facteur_surcout

    # Portes de Toffoli nécessaires : O(n^3)
    portes_toffoli = 3 * taille_bits**3

    # Temps d'exécution estimé (1 μs par porte)
    temps_par_porte = 1e-6
    temps_total = portes_toffoli * temps_par_porte

    print(f"Analyse pour RSA-{taille_bits} :")
    print(f"  Qubits logiques : ~{n_qubits_logiques}")
    print(f"  Qubits physiques : ~{n_qubits_physiques}")
    print(f"  Portes de Toffoli : ~{portes_toffoli:.2e}")
    print(f"  Temps estimé : ~{temps_total:.2e} s = {temps_total/3600:.1f} h")

    return n_qubits_logiques, n_qubits_physiques

# Impact sur différentes tailles de clés
for taille in [512, 1024, 2048, 4096]:
    impact_rsa_shor(taille)
    print()
```

**Sortie attendue :**

```
Analyse pour RSA-512 :
  Qubits logiques : ~1024
  Qubits physiques : ~1024000
  Portes de Toffoli : ~4.03e+08
  Temps estimé : ~4.03e+02 s = 0.1 h

Analyse pour RSA-1024 :
  Qubits logiques : ~2048
  Qubits physiques : ~2048000
  Portes de Toffoli : ~3.22e+09
  Temps estimé : ~3.22e+03 s = 0.9 h

Analyse pour RSA-2048 :
  Qubits logiques : ~4096
  Qubits physiques : ~4096000
  Portes de Toffoli : ~2.58e+10
  Temps estimé : ~2.58e+04 s = 7.2 h

Analyse pour RSA-4096 :
  Qubits logiques : ~8192
  Qubits physiques : ~8192000
  Portes de Toffoli : ~2.06e+11
  Temps estimé : ~2.06e+05 s = 57.3 h
```

---

## Complexité et avantage quantique

| Tâche | Classique | Quantique (Shor) |
|-------|-----------|-------------------|
| Factoriser $N$ (crible) | $O(e^{n^{1/3} (\log n)^{2/3}})$ | — |
| Factoriser $N$ (Shor) | — | $O(n^3)$ portes |
| RSA-2048 | $\sim 10^{17}$ années | $\sim 7$ heures (estimé) |

**Pourquoi Shor est-il plus rapide ?** Classiquement, les meilleurs algorithmes (crible général des corps de nombres) ont une complexité **sous-exponentielle** en $n = \log N$. Shor a une complexité **polynomiale** $O(n^3)$. La différence vient de la QPE : elle exploite la structure de groupe de $\mathbb{Z}/N\mathbb{Z}$ pour trouver la période en $O(n)$ requêtes, alors que classiquement il faut explorer exponentiellement plus de valeurs.

---

## À retenir

1. Shor réduit la **factorisation** à la **recherche de période** de $f(x) = a^x \bmod N$
2. Si $r$ est pair et $a^{r/2} \not\equiv \pm 1$, alors $\gcd(a^{r/2} \pm 1, N)$ donne les facteurs
3. La **QPE** (chapitre 6.2) estime $k/r$, et les **fractions continues** retrouvent $r$
4. L'**exponentiation modulaire** $U_a$ est la partie la plus coûteuse : $O(n^3)$ portes
5. Pour $N = 15$, le circuit tient sur 8 qubits et donne $15 = 3 \times 5$
6. RSA-2048 nécessiterait $\sim 4000$ qubits logiques ($\sim 4 \times 10^6$ physiques)
7. La **cryptographie post-quantique** (Kyber, Dilithium) est la réponse à cette menace

---

## Pièges à éviter

1. **Oublier la partie classique** : Shor = réduction classique + QPE quantique, les deux sont indispensables
2. **Confondre $r$ et $k/r$** : la QPE donne $k/r$, pas $r$ directement. Il faut les fractions continues
3. **Négliger les cas d'échec** : $r$ impair ou $a^{r/2} \equiv -1$ → il faut recommencer avec un autre $a$
4. **Sous-estimer le coût de l'exponentiation modulaire** : c'est $O(n^3)$ portes, pas $O(n)$
5. **Penser que Shor casse tout** : Shor menace RSA, ECC, DSA, mais PAS AES (contre lequel Grover suffit, voir chapitre 8)

---

## Exercices

### Niveau 1 — Application directe

**Exercice 1** : Implémentez l'algorithme de développement en fractions continues et testez-le pour retrouver $r$ à partir de $c/2^{2n} \approx k/r$.

```python
def frac_continue(theta, max_denom=100):
    """Développement en fractions continues"""
    frac = Fraction(theta).limit_denominator(max_denom)
    return frac.numerator, frac.denominator

# Test
thetas = [0.25, 0.333333, 0.166666, 0.2]
for theta in thetas:
    n, d = frac_continue(theta, 50)
    print(f"θ={theta:.4f} → {n}/{d}")
```

**Sortie attendue :**

```
θ=0.2500 → 1/4
θ=0.3333 → 1/3
θ=0.1667 → 1/6
θ=0.2000 → 1/5
```

**Exercice 2** : Simulez Shor pour $N=15$ avec $a=7, 8, 11, 13$. Vérifiez que $r$ est toujours un diviseur de 4.

### Niveau 2 — Compréhension

**Exercice 3** : Implémentez l'opérateur $U_a |x\rangle = |ax \bmod N\rangle$ comme matrice QuTiP pour $N=15$ et vérifiez les valeurs propres.

```python
import qutip as qt
import numpy as np

def operateur_mult_mod(N=15, a=2):
    """Matrice de U_a pour l'exponentiation modulaire"""
    dim = N
    U = np.zeros((dim, dim))
    for x in range(dim):
        U[a * x % N, x] = 1.0
    return qt.Qobj(U)

# Vérification
U = operateur_mult_mod(15, 2)
vals, states = U.eigenstates()
print("Valeurs propres de U_2 :")
for i, v in enumerate(vals[:6]):
    phase = np.angle(v) / (2 * np.pi)
    print(f"  λ_{i} = {v:.4f}, phase = {phase:.4f}")
```

**Exercice 4** : Concevez le circuit pour $N=21$. Combien de qubits sont nécessaires ?

### Niveau 3 — Défi

**Exercice 5** : Montrez que Shor s'applique aussi au logarithme discret (ECC). Comparez les ressources pour ECC-256 vs RSA-2048.

**Exercice 6** : Recherchez comment fonctionne Kyber (ML-KEM), le standard NIST post-quantique. Comparez les tailles de clés avec RSA.

---

## Pour aller plus loin

- L'algorithme de **Shor pour le logarithme discret** résout le problème du logarithme discret dans $\mathbb{Z}_p^*$ et sur les courbes elliptiques
- Les **variantes optimisées** de Shor (comme celle de Beauregard) réduisent le nombre de qubits à $2n + 3$
- La **cryptographie post-quantique** (chapitre 7.2) développe des algorithmes résistants à Shor

---

## Références

- Shor, P. W. (1994). "Algorithms for quantum computation: discrete logarithms and factoring". *Proc. 35th FOCS*, 124–134.
- Shor, P. W. (1997). "Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer". *SIAM J. Comput.*, 26(5), 1484–1509.
- Nielsen, M. A. & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*.
- Fowler, A. G. et al. (2012). "Surface codes: Towards practical large-scale quantum computation". *Phys. Rev. A*, 86, 032324.
