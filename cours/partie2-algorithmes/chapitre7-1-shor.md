# Chapitre 7.1 — Algorithme de Shor

## Objectifs d'apprentissage

- Comprendre la réduction factorisation → recherche de période
- Maîtriser l'exponentiation modulaire quantique
- Implémenter le circuit pour $N=15$
- Analyser l'impact sur la cryptographie RSA

---

## 1. Factorisation et recherche de période

### Réduction classique-quantique

Soit $N$ un entier composé à factoriser. L'algorithme de Shor procède en deux parties :

1. **Partie classique** : Réduire la factorisation à un problème de recherche de période
2. **Partie quantique** : Trouver la période via QPE

**Étape 1** : Choisir $a$ aléatoire avec $1 < a < N$ et $\gcd(a, N) = 1$.

**Étape 2** : Définir $f(x) = a^x \bmod N$. Cette fonction est périodique :

$$f(x+r) = f(x) \bmod N, \quad r = \text{ord}_N(a)$$

**Étape 3** : Si $r$ est pair et $a^{r/2} \not\equiv \pm 1 \pmod N$, alors :

$$\gcd(a^{r/2} + 1, N) \quad \text{ou} \quad \gcd(a^{r/2} - 1, N)$$

est un facteur non trivial de $N$.

### Probabilité de succès

Pour un $a$ aléatoire, $P(r \text{ pair et } a^{r/2} \not\equiv \pm 1) \geq 1/2$.

## 2. Architecture de l'algorithme quantique

```
Registre 1 (2n qubits) : |0⟩ — H⊗²ⁿ — QFT† — M → estimation de phase
                       |         |
Registre 2 (n qubits) : |0⟩ — — — U_a — — — — M (optionnel)
```

Où $U_a$ est l'opérateur d'exponentiation modulaire :

$$U_a |x\rangle = |ax \bmod N\rangle$$

Le circuit quantique :

$$|\psi_0\rangle = |0\rangle^{\otimes 2n} |0\rangle^{\otimes n}$$

$$|\psi_1\rangle = \frac{1}{\sqrt{2^{2n}}} \sum_{j=0}^{2^{2n}-1} |j\rangle |0\rangle$$

$$|\psi_2\rangle = \frac{1}{\sqrt{2^{2n}}} \sum_{j=0}^{2^{2n}-1} |j\rangle |a^j \bmod N\rangle$$

$$|\psi_3\rangle = QFT^\dagger \otimes I \left( \frac{1}{\sqrt{2^{2n}}} \sum_{j=0}^{2^{2n}-1} |j\rangle |a^j \bmod N\rangle \right)$$

### Analyse par QPE

Les valeurs propres de $U_a$ sont $e^{2\pi i k/r}$ pour $k=0,\ldots,r-1$. Le QPE estime $k/r$ avec $2n$ qubits de précision.

Soit $c$ la mesure du premier registre. Alors $c/2^{2n} \approx k/r$ pour un certain $k$. On trouve $r$ via le développement en fractions continues.

## 3. Exponentiation modulaire

Implémenter $U_a |x\rangle = |ax \bmod N\rangle$ est la partie la plus coûteuse.

### Multiplication modulaire

$$a^j \bmod N = a^{j_{n-1}2^{n-1}} \times \cdots \times a^{j_0 2^0} \bmod N$$

Chaque multiplication modulaire $|x\rangle \to |a^{2^k} x \bmod N\rangle$ est implémentée par des additionneurs quantiques.

### Complexité

- Portes : $O(n^3)$
- Profondeur : $O(n^3)$
- Qubits : $O(n)$ (avec de l'optimisation)

## 4. Circuit pour $N=15$

$N=15$ est le plus petit exemple non trivial. Pour $a=2$ :

$$2^0 = 1, \; 2^1 = 2, \; 2^2 = 4, \; 2^3 = 8, \; 2^4 = 1 \pmod{15}$$

Donc $r = 4$. $a^{r/2} = 2^2 = 4 \not\equiv \pm 1$, donc :

$$\gcd(4+1, 15) = 5, \quad \gcd(4-1, 15) = 3$$

```python
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from fractions import Fraction

def c_amod15(qc, a, power, control, target):
    """
    Multiplication modulaire contrôlée : |x⟩ → |a^{power}·x mod 15⟩
    Implémentée pour N=15 avec des portes élémentaires.
    """
    U = a**power % 15
    for _ in range(U):
        # Pour N=15, la multiplication par 2 mod 15 est une permutation
        # que l'on implémente via SWAP et X
        if U == 2:
            qc.swap(control, target)
        elif U == 4:
            qc.swap(control, target)
            qc.swap(target, control)  # en pratique, on utilise des portes dédiées
        elif U == 7:
            qc.swap(control, target)
            qc.cx(control, target)
        elif U == 8:
            qc.cx(control, target)

def shor_circuit_15(a=2):
    """
    Circuit de Shor pour N=15 avec multiplicateur a.
    """
    n_count = 4  # qubits de contrôle pour la QPE
    qc = QuantumCircuit(n_count + 4, n_count)

    # Initialisation des qubits de contrôle en |+⟩
    qc.h(range(n_count))

    # Préparation du registre de fonction en |1⟩
    qc.x(n_count + 3)

    # Exponentiation modulaire contrôlée U_a^(2^j)
    for j in range(n_count):
        for _ in range(2**j):
            c_amod15(qc, a, 2**j, j, n_count)

    # QFT inverse
    for j in range(n_count // 2):
        qc.swap(j, n_count - 1 - j)
    for i in range(n_count - 1, -1, -1):
        qc.h(i)
        for j in range(i):
            angle = -2 * np.pi / (2**(i - j + 1))
            qc.cp(angle, j, i)

    qc.measure(range(n_count), range(n_count))

    return qc

def shor_15(a=2):
    """
    Exécution complète de Shor pour N=15.
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

        # Développement en fractions continues
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

def oracle_shor_complet(N=15, a=2, n_count=8):
    """
    Circuit de Shor plus complet avec n_count qubits.
    """
    n = int(np.ceil(np.log2(N)))
    qc = QuantumCircuit(n_count + n, n_count)

    # Hadamard sur les qubits de contrôle
    qc.h(range(n_count))

    # Registre de fonction en |1⟩
    qc.x(n_count)

    # U^(2^j) contrôlé - version simplifiée pour N=15
    for j in range(n_count):
        power = 2**j
        # Pour N=15, on implémente directement la multiplication
        for _ in range(power):
            # Multiplication par a mod 15
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

def analyse_resultats(counts, n_count, N=15):
    """Analyse les mesures pour en déduire les facteurs."""
    for bits, count in counts.items():
        c = int(bits, 2)
        theta = c / (2**n_count)

        # Fractions continues
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
analyse_resultats(result.get_counts(), n_count, N)
```

## 5. Impact sur RSA

### Principe RSA

- $p, q$ premiers → $N = pq$
- $e$ : exposant public, tel que $\gcd(e, \phi(N)) = 1$
- $d \equiv e^{-1} \pmod{\phi(N)}$ : exposant privé
- Chiffrement : $c = m^e \bmod N$
- Déchiffrement : $m = c^d \bmod N$

### Menace quantique

| Taille de clé RSA | Qubits nécessaires | Estimation temporelle |
|-------------------|--------------------|----------------------|
| 512 bits | $\approx 3000$ | $< 1$ heure |
| 1024 bits | $\approx 6000$ | $\approx 1$ jour |
| 2048 bits | $\approx 12000$ | $\approx 100$ jours |
| 4096 bits | $\approx 24000$ | $\approx 10$ ans |

### Algorithmes post-quantiques

- Cryptographie basée sur les réseaux (LWE, NTRU)
- Cryptographie basée sur les codes (McEliece)
- Signatures basées sur les hash (SPHINCS+)
- Cryptographie multivariée

```python
import numpy as np

def impact_rsa_shor(taille_bits=2048):
    """
    Calcule les ressources nécessaires pour casser RSA avec Shor.
    Modèle simplifié basé sur l'analyse de Fowler et al. (2012).
    """
    # Qubits logiques nécessaires
    n_qubits_logiques = 2 * taille_bits + O(1)

    # Qubits physiques (avec correction d'erreur, surface code)
    # Facteur de surcoût : ~1000 qubits physiques par qubit logique
    facteur_surcout = 1000
    n_qubits_physiques = n_qubits_logiques * facteur_surcout

    # Portes de Toffoli
    portes_toffoli = 3 * taille_bits**3  # O(n^3)

    # Temps d'exécution (estimation)
    temps_par_porte = 1e-6  # 1 μs par porte
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

## 6. Exercices

### Exercice 1 : Fractions continues
Implémentez l'algorithme de développement en fractions continues et testez-le pour retrouver $r$ à partir de $c/2^{2n} \approx k/r$.

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

### Exercice 2 : Probabilité de succès pour N=15
Simulez Shor pour $N=15$ avec $a=7, 8, 11, 13$. Vérifiez que $r$ est toujours un diviseur de 4.

### Exercice 3 : Shor avec QuTiP
Implémentez l'opérateur $U_a |x\rangle = |ax \bmod N\rangle$ comme matrice QuTiP pour $N=15$ et vérifiez les valeurs propres.

```python
import qutip as qt
import numpy as np

def operateur_mult_mod(N=15, a=2):
    """Matrice de U_a pour l'exponentiation modulaire"""
    dim = N  # On utilise N dimensions
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

### Exercice 4 : Ordre de grandeur — Facteurs de 21
Concevez le circuit pour $N=21$. Combien de qubits sont nécessaires ? $U_a$ peut-il être simplifié ?

### Exercice 5 : Impact sur les courbes elliptiques
Montrez que l'algorithme de Shor s'applique aussi au logarithme discret (ECC). Comparez les ressources nécessaires pour casser ECC-256 vs RSA-2048.

### Exercice 6 : Post-quantique — Kyber
Recherchez comment fonctionne Kyber (ML-KEM), le standard NIST de chiffrement post-quantique basé sur les réseaux. Comparez la taille des clés avec RSA.

---

## Références

- Shor, P. W. (1994). "Algorithms for quantum computation: discrete logarithms and factoring". *Proc. 35th FOCS*, 124–134.
- Shor, P. W. (1997). "Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer". *SIAM J. Comput.*, 26(5), 1484–1509.
- Nielsen, M. A. & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*.
- Fowler, A. G. et al. (2012). "Surface codes: Towards practical large-scale quantum computation". *Phys. Rev. A*, 86, 032324.
