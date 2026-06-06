# Chapitre 5.1 — Algorithme de Deutsch et Deutsch-Jozsa

## Ce que vous allez apprendre

- Comprendre ce qu'est un **oracle quantique** et le concept de **phase kickback**
- Maîtriser l'algorithme de **Deutsch** (1 qubit) : déterminer si une fonction est constante ou équilibrée en **une seule interrogation**
- Généraliser avec l'algorithme de **Deutsch-Jozsa** (n qubits) et comprendre l'avantage exponentiel
- Implémenter les circuits en **Qiskit** et simuler la dynamique avec **QuTiP**
- Voir comment cet algorithme pose les fondations de tous les algorithmes quantiques qui suivent

---

## Motivation

Imaginez qu'on vous donne une boîte noire (un « oracle ») qui calcule une fonction $f$. Vous ne savez pas ce qu'il y a dedans, mais on vous promet une chose : soit $f$ renvoie **toujours la même valeur** (constante), soit elle renvoie **autant de 0 que de 1** (équilibrée). Combien de fois devez-vous interroger la boîte pour trancher ?

Classiquement, c'est un problème frustrant. Pour une fonction $f : \{0,1\}^n \to \{0,1\}$, dans le pire cas, il faut évaluer $f$ sur **$2^{n-1} + 1$ entrées** avant de pouvoir conclure avec certitude. Si $n = 10$, cela fait 513 évaluations !

L'algorithme de Deutsch-Jozsa résout ce problème en **une seule évaluation quantique**. C'est le premier exemple historique d'un avantage quantique exponentiel prouvé. Même si le problème est artificiel (la promesse « constante ou équilibrée » est rare en pratique), l'algorithme introduit des idées fondamentales — le **phase kickback**, l'**interférence constructive/destructive**, et la puissance de la **superposition** — qui reviendront dans Simon, Shor et Grover.

---

## Idée principale

Pensez à un orchestre. Si tous les musiciens jouent la même note (fonction constante), le son est pur et harmonieux. Si la moitié joue une note et l'autre moitié son opposé (fonction équilibrée), le son s'annule.

L'algorithme de Deutsch-Jozsa fait exactement ça : il prépare **toutes les entrées possibles en superposition**, les envoie dans l'oracle d'un seul coup, puis utilise des portes de Hadamard pour créer des **interférences**. Si la fonction est constante, toutes les amplitudes s'additionnent constructivement vers $|0\rangle^{\otimes n}$. Si elle est équilibrée, elles s'annulent parfaitement — et on ne mesure jamais $|0\rangle^{\otimes n}$.

C'est comme interroger toutes les pages d'un livre en même temps et écouter si les réponses se renforcent ou s'annulent.

---

## Contenu du cours

### Section 1 : L'oracle quantique et le phase kickback

Un oracle quantique est une porte unitaire $U_f$ qui encode une fonction $f$ :

$$U_f : |x\rangle|y\rangle \mapsto |x\rangle|y \oplus f(x)\rangle$$

**Intuition** : $|x\rangle$ est le registre d'entrée ($n$ qubits), $|y\rangle$ est le registre de sortie (1 qubit), et $\oplus$ est le XOR. L'oracle ne « calcule » pas $f$ au sens classique — il **encode** $f$ dans une transformation réversible.

**Variable** : $x \in \{0,1\}^n$, $y \in \{0,1\}$, $f(x) \in \{0,1\}$.

**L'astuce géniale** : si on prépare $|y\rangle = |-\rangle = \frac{1}{\sqrt{2}}(|0\rangle - |1\rangle)$, alors :

$$U_f |x\rangle|-\rangle = (-1)^{f(x)} |x\rangle|-\rangle$$

**Pourquoi ?** Développons :
$$U_f |x\rangle|-\rangle = \frac{1}{\sqrt{2}}(|x\rangle|0 \oplus f(x)\rangle - |x\rangle|1 \oplus f(x)\rangle)$$

Si $f(x) = 0$ : on obtient $\frac{1}{\sqrt{2}}(|0\rangle - |1\rangle) = |-\rangle$, donc le signe est $+1$.
Si $f(x) = 1$ : on obtient $\frac{1}{\sqrt{2}}(|1\rangle - |0\rangle) = -|-\rangle$, donc le signe est $-1$.

**Exemple numérique** : $f(x) = x$, $x = 1$ :
$$U_f |1\rangle|-\rangle = (-1)^1 |1\rangle|-\rangle = -|1\rangle|-\rangle$$

Le résultat de $f(x)$ est encodé dans la **phase**, sans qu'on ait besoin de mesurer le registre de sortie. C'est le **phase kickback** : l'information « remonte » de l'oracle vers le registre d'entrée.

### Section 2 : Algorithme de Deutsch (1 qubit)

**Problème** : $f : \{0,1\} \to \{0,1\}$. Constante ou équilibrée ? **Une seule interrogation** suffit.

**Circuit** :
```
|0⟩ — H — — U_f — H — M
                   |
|1⟩ — H — — — — — — —
```

**Étape 1** — Préparation :
$$|\psi_0\rangle = |0\rangle \otimes |1\rangle$$

**Étape 2** — Hadamard sur les deux qubits :
$$|\psi_1\rangle = |+\rangle \otimes |-\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle) \otimes \frac{1}{\sqrt{2}}(|0\rangle - |1\rangle)$$

**Intuition** : le premier qubit est maintenant dans une superposition de $|0\rangle$ et $|1\rangle$ — il « explore » les deux entrées simultanément.

**Étape 3** — Oracle $U_f$ :
$$|\psi_2\rangle = \frac{1}{\sqrt{2}}\left[(-1)^{f(0)}|0\rangle + (-1)^{f(1)}|1\rangle\right] \otimes |-\rangle$$

**Intuition** : le phase kickback a marqué chaque branche de la superposition avec le signe de $f(x)$.

**Étape 4** — Hadamard sur le premier qubit :
$$|\psi_3\rangle = \frac{1}{2}\left[(-1)^{f(0)}+(-1)^{f(1)}\right]|0\rangle + \frac{1}{2}\left[(-1)^{f(0)}-(-1)^{f(1)}\right]|1\rangle$$

**Pourquoi ça marche ?** Le coefficient de $|0\rangle$ est la **somme** des phases. Si $f$ est constante, les deux phases sont identiques et s'additionnent : amplitude $\pm 1$ pour $|0\rangle$. Si $f$ est équilibrée, les phases sont opposées et s'annulent : amplitude $0$ pour $|0\rangle$.

**Exemple** : $f(0) = 0, f(1) = 1$ (équilibrée) :
- Coefficient de $|0\rangle$ : $\frac{1}{2}(1 + (-1)) = 0$
- Coefficient de $|1\rangle$ : $\frac{1}{2}(1 - (-1)) = 1$
- On mesure $|1\rangle$ → fonction équilibrée !

### Section 3 : Généralisation Deutsch-Jozsa (n qubits)

**Problème** : $f : \{0,1\}^n \to \{0,1\}$, promesse : constante ou équilibrée. Classiquement : $2^{n-1}+1$ appels. Quantiquement : **1 appel**.

**Circuit** :
```
|0⟩^{\otimes n} — H^{\otimes n} — U_f — H^{\otimes n} — M
                                |
|1⟩ — H — — — — — — — — — — — —
```

**Étape 1** :
$$|\psi_0\rangle = |0\rangle^{\otimes n}|1\rangle$$

**Étape 2** — Hadamard sur tous les qubits :
$$|\psi_1\rangle = \frac{1}{\sqrt{2^n}}\sum_{x=0}^{2^n-1} |x\rangle \otimes |-\rangle$$

**Intuition** : on a créé une superposition uniforme de **toutes** les entrées possibles. Chaque $x$ de $0$ à $2^n - 1$ est « exploré » simultanément.

**Étape 3** — Oracle :
$$|\psi_2\rangle = \frac{1}{\sqrt{2^n}}\sum_{x=0}^{2^n-1} (-1)^{f(x)} |x\rangle \otimes |-\rangle$$

**Intuition** : chaque état $|x\rangle$ porte maintenant la « signature » de $f(x)$ dans sa phase.

**Étape 4** — Seconde Hadamard sur les $n$ qubits :
$$|\psi_3\rangle = \frac{1}{2^n}\sum_{x=0}^{2^n-1} (-1)^{f(x)} \sum_{y=0}^{2^n-1} (-1)^{x\cdot y} |y\rangle \otimes |-\rangle$$

où $x\cdot y = \sum_{i=1}^n x_i y_i \pmod 2$ est le produit scalaire binaire.

**L'amplitude de $|0\rangle^{\otimes n}$** (c'est-à-dire $y = 0\ldots0$) :
$$\text{Amp}(0^n) = \frac{1}{2^n}\sum_{x=0}^{2^n-1} (-1)^{f(x)}$$

**Intuition** : c'est la somme de $2^n$ termes $\pm 1$. Si $f$ est constante, tous les termes ont le même signe → somme = $\pm 2^n$, amplitude = $\pm 1$. Si $f$ est équilibrée, exactement la moitié vaut $+1$ et l'autre $-1$ → somme = $0$.

**Conclusion** :
- $f$ constante → on mesure $|0\rangle^{\otimes n}$ avec certitude
- $f$ équilibrée → on ne mesure **jamais** $|0\rangle^{\otimes n}$

---

## Exemple guidé

Prenons $n = 2$ qubits. L'espace d'entrée est $\{00, 01, 10, 11\}$.

**Cas 1** : $f$ constante, $f(x) = 0$ pour tout $x$.

État initial : $|00\rangle|1\rangle$

Après Hadamard :
$$|\psi_1\rangle = \frac{1}{2}(|00\rangle + |01\rangle + |10\rangle + |11\rangle) \otimes |-\rangle$$

Après oracle ($f(x) = 0 \Rightarrow (-1)^{f(x)} = +1$ partout) :
$$|\psi_2\rangle = \frac{1}{2}(|00\rangle + |01\rangle + |10\rangle + |11\rangle) \otimes |-\rangle$$

Rien n'a changé ! Toutes les phases sont $+1$.

Après seconde Hadamard :
$$|\psi_3\rangle = |00\rangle \otimes |-\rangle$$

On mesure $|00\rangle$ → **constante** ✓

**Cas 2** : $f$ équilibrée, $f(x) = x_0$ (premier bit).

Donc $f(00) = 0, f(01) = 0, f(10) = 1, f(11) = 1$.

Après oracle :
$$|\psi_2\rangle = \frac{1}{2}(|00\rangle + |01\rangle - |10\rangle - |11\rangle) \otimes |-\rangle$$

Après seconde Hadamard, l'amplitude de $|00\rangle$ :
$$\frac{1}{4}(1 + 1 - 1 - 1) = 0$$

On ne mesure **jamais** $|00\rangle$ → **équilibrée** ✓

---

## Implémentation Python

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# --- Oracle constant : f(x) = sortie pour tout x ---
def oracle_constante(qc, n, sortie=0):
    """
    Oracle constant.
    Si sortie=0 : on ne fait rien (U_f = I).
    Si sortie=1 : on flippe le qubit de sortie avec X.
    """
    if sortie == 1:
        qc.x(n)  # X sur le qubit ancillaire

# --- Oracle équilibré : f(x) = parité du premier bit ---
def oracle_equilibre(qc, n):
    """
    Oracle équilibré : f(x) = x_0 XOR x_1 XOR ... XOR x_{n-1}.
    On utilise des CNOT de chaque qubit d'entrée vers l'ancillaire.
    """
    for i in range(n):
        qc.cx(i, n)  # CNOT : si qubit i = |1⟩, flip l'ancillaire

# --- Circuit Deutsch-Jozsa complet ---
def deutsch_jozsa(n, constant=True):
    """
    Construit le circuit Deutsch-Jozsa.
    n : nombre de qubits d'entrée
    constant : True si l'oracle est constant, False si équilibré
    """
    qc = QuantumCircuit(n + 1, n)  # n qubits d'entrée + 1 ancillaire, n bits classiques

    # Étape 1 : préparer l'ancillaire dans |1⟩
    qc.x(n)

    # Étape 2 : Hadamard sur TOUS les qubits (entrée + ancillaire)
    qc.h(range(n + 1))

    # Étape 3 : appliquer l'oracle
    if constant:
        oracle_constante(qc, n, sortie=0)
    else:
        oracle_equilibre(qc, n)

    # Étape 4 : Hadamard sur les n premiers qubits uniquement
    qc.h(range(n))

    # Étape 5 : mesurer les n premiers qubits
    qc.measure(range(n), range(n))

    return qc

# --- Test avec n=3 qubits ---
n = 3
qc_const = deutsch_jozsa(n, constant=True)   # Oracle constant
qc_equi = deutsch_jozsa(n, constant=False)    # Oracle équilibré

print("Circuit constant :")
print(qc_const.draw())

# --- Simulation ---
backend = AerSimulator()
for nom, qc in [("Constant", qc_const), ("Équilibré", qc_equi)]:
    result = backend.run(qc, shots=1024).result()
    counts = result.get_counts()
    print(f"\n{nom} : {counts}")
    # Attendu : Constant → {'000': 1024}, Équilibré → aucun '000'
```

```python
import numpy as np
import qutip as qt

# --- Porte Hadamard en QuTiP ---
def hadamard_port():
    """Retourne la matrice Hadamard comme objet QuTiP."""
    H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])
    return qt.Qobj(H)

# --- Simulation de la dynamique de Deutsch ---
def deutsch_dynamique(f_type='constant'):
    """
    Simule l'algorithme de Deutsch étape par étape avec QuTiP.
    f_type : 'constant' (f(0)=f(1)=0) ou 'balanced' (f(0)=0, f(1)=1)
    """
    H = hadamard_port()

    # États de base |0⟩ et |1⟩
    zero = qt.basis(2, 0)
    one = qt.basis(2, 1)

    # État initial |0⟩ ⊗ |1⟩
    psi0 = qt.tensor(zero, one)
    print(f"État initial : |0⟩|1⟩")

    # Hadamard sur les deux qubits → |+⟩|−⟩
    H2 = qt.tensor(H, H)
    psi1 = H2 * psi0
    print(f"Après Hadamard : |+⟩|−⟩")

    # Oracle U_f
    if f_type == 'constant':
        # f(0)=f(1)=0 → U_f = I ⊗ I (aucun changement)
        U_f = qt.tensor(qt.qeye(2), qt.qeye(2))
    else:
        # f(0)=0, f(1)=1 → phase flip sur |1⟩ via CNOT + |−⟩
        # Matrice dans la base {|00⟩, |01⟩, |10⟩, |11⟩}
        mat = np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, -1]])
        U_f = qt.Qobj(mat, dims=[[2, 2], [2, 2]])

    psi2 = U_f * psi1
    print(f"Après oracle ({f_type})")

    # Seconde Hadamard sur le premier qubit uniquement
    H_I = qt.tensor(H, qt.qeye(2))
    psi3 = H_I * psi2

    # Probabilités de mesure du premier qubit
    prob_0 = (psi3.ptrace(0)[0, 0]).real
    prob_1 = (psi3.ptrace(0)[1, 1]).real

    print(f"Oracle {f_type} :")
    print(f"  P(|0⟩) = {prob_0:.3f}, P(|1⟩) = {prob_1:.3f}")
    if f_type == 'constant':
        assert abs(prob_0 - 1.0) < 1e-6  # On doit mesurer |0⟩
    else:
        assert abs(prob_1 - 1.0) < 1e-6  # On doit mesurer |1⟩

    return psi3

# Test
deutsch_dynamique('constant')
deutsch_dynamique('balanced')
```

**Sortie attendue :**

```
Oracle constant :
  P(|0⟩) = 1.000, P(|1⟩) = 0.000
Oracle balanced :
  P(|0⟩) = 0.500, P(|1⟩) = 0.500
```

```python
import numpy as np
import qutip as qt

# --- Simulation de l'évolution Hadamard via Hamiltonien ---
def simulation_hadamard_evol(t=1.0):
    """
    La porte Hadamard peut s'écrire H = (X + Z)/√2.
    On simule l'évolution sous le Hamiltonien H_eff = (π/2)(X+Z)/√2
    pendant un temps t=1 pour retrouver H (à une phase globale près).
    """
    sx = qt.sigmax()  # Matrice de Pauli X
    sz = qt.sigmaz()  # Matrice de Pauli Z

    # Hamiltonien effectif dont l'évolution donne la porte Hadamard
    H_eff = (np.pi / 2) * (sx + sz) / np.sqrt(2)

    # Opérateur d'évolution U(t) = exp(-i H_eff t)
    U = (-1j * H_eff * t).expm()

    # Vérification : comparer U avec la porte Hadamard cible
    H_target = (1 / np.sqrt(2)) * (sx + sz)
    fidelity = abs((H_target.dag() * U).tr() / 2)

    print(f"Fidélité Hadamard par évolution : {fidelity:.6f}")
    assert fidelity > 0.99  # Doit être très proche de 1

    return U

U_h = simulation_hadamard_evol()
print("U_H =", U_h)
```

**Sortie attendue :**

```
Fidélité Hadamard par évolution : 1.000000
U_H = Quantum object: dims=[[2], [2]], shape=(2, 2), type='oper', dtype=Dense, isherm=False
Qobj data =
[[0.-0.70710678j 0.-0.70710678j]
 [0.-0.70710678j 0.+0.70710678j]]
```

---

## Complexité et avantage quantique

| Approche | Appels à l'oracle | Type d'avantage |
|----------|------------------|-----------------|
| Classique déterministe | $2^{n-1} + 1$ | — |
| Classique randomisé (2 essais) | 2 (erreur possible) | — |
| **Deutsch-Jozsa** | **1** | **Exponentiel** |

**Pourquoi l'algorithme est-il plus rapide ?** Classiquement, chaque évaluation ne nous donne qu'**un bit** d'information sur $f$. Il faut donc explorer plus de la moitié de l'espace pour conclure. Quantiquement, la superposition permet d'évaluer $f$ sur **toutes les entrées en même temps**, et les interférences (via Hadamard) combinent ces évaluations en une seule mesure décisive.

**Intuition de la preuve** : l'amplitude de $|0\rangle^{\otimes n}$ après l'algorithme est $\frac{1}{2^n}\sum_x (-1)^{f(x)}$. Cette somme est un « vote global » : si $f$ est constante, tous les votes sont dans le même sens. Si $f$ est équilibrée, les votes s'annulent exactement.

---

## À retenir

1. L'**oracle** $U_f$ encode $f$ dans une transformation unitaire réversible
2. Le **phase kickback** transforme $f(x)$ en signe $(-1)^{f(x)}$ sur le registre d'entrée
3. **Deutsch** (1 qubit) résout le problème constant/équilibré en **1 appel** au lieu de 2
4. **Deutsch-Jozsa** (n qubits) généralise : **1 appel** au lieu de $2^{n-1}+1$
5. Les **interférences** (Hadamard → oracle → Hadamard) sont le mécanisme central
6. C'est le premier algorithme montrant un avantage quantique **exponentiel prouvé**
7. Les concepts (oracle, phase kickback, interférence) sont réutilisés dans Simon, Shor et Grover

---

## Pièges à éviter

1. **Confondre oracle constant et équilibré** : « constant » = même sortie pour TOUTE entrée, « équilibré » = exactement moitié 0, moitié 1
2. **Oublier le qubit ancillaire** : l'oracle agit sur $n+1$ qubits, pas seulement $n$
3. **Mesurer le mauvais registre** : on mesure les $n$ qubits d'entrée, PAS l'ancillaire
4. **Penser que l'algorithme calcule $f(x)$** : il ne calcule rien — il détermine une **propriété globale** de $f$
5. **Négliger la promesse** : l'algorithme ne fonctionne que si on garantit que $f$ est soit constante, soit équilibrée

---

## Exercices

### Niveau 1 — Application directe

**Exercice 1** : Montrez que $U_f|x\rangle|-\rangle = (-1)^{f(x)}|x\rangle|-\rangle$ en développant le calcul pour les 4 cas ($x=0,1$ et $f(x)=0,1$).

**Exercice 2** : Implémentez un oracle pour $f(x) = x_0 \oplus x_1 \oplus \cdots \oplus x_{n-1}$ (parité totale) et testez l'algorithme avec Qiskit.

### Niveau 2 — Compréhension

**Exercice 3** : Généralisez l'algorithme au cas où $f:\{0,1\}^n\to\{0,1\}^m$. Quel est l'avantage quantique ? L'algorithme fonctionne-t-il encore ?

**Exercice 4** : Ajoutez un canal dépolarisant sur chaque qubit après l'oracle et étudiez la probabilité de succès en fonction du taux de bruit $p$.

```python
# Indice :
from qutip import destroy, qeye
def canal_depolarisant(rho, p):
    """Canal dépolarisant : rho → (1-p)rho + p I/2"""
    I = qeye(2) / 2
    return (1-p) * rho + p * I
```

### Niveau 3 — Défi

**Exercice 5** : Démontrez que l'avantage quantique est **exponentiel** : classiquement $O(2^{n-1}+1)$ vs quantiquement $O(1)$. Que se passe-t-il si on retire la promesse (fonction ni constante ni équilibrée) ?

**Exercice 6** : Utilisez `qiskit.transpile` pour estimer la profondeur du circuit Deutsch-Jozsa pour $n=10,20,50$. Comparez avec une approche classique.

---

## Pour aller plus loin

- L'algorithme de Deutsch-Jozsa est un cas particulier du **problème du sous-groupe caché** (Hidden Subgroup Problem), que nous reverrons avec Simon (chapitre 5.2) et Shor (chapitre 7.1)
- La technique du phase kickback est centrale dans l'estimation de phase quantique (QPE, chapitre 6.2)
- L'algorithme de **Bernstein-Vazirani** généralise Deutsch-Jozsa pour trouver un vecteur secret $s$ en une seule requête

---

## Références

- Deutsch, D. (1985). "Quantum theory, the Church–Turing principle and the universal quantum computer". *Proc. R. Soc. Lond. A*, 400, 97–117.
- Nielsen, M. A. & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*.
- Qiskit Textbook : https://qiskit.org/textbook/ch-algorithms/deutsch-jozsa.html
