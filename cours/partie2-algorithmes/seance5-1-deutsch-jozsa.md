# Séance 5.1 — Algorithme de Deutsch et Deutsch-Jozsa

## Objectifs d'apprentissage

- Comprendre le parallélisme quantique et le concept d'oracle
- Maîtriser l'algorithme de Deutsch (1 qubit) et sa généralisation Deutsch-Jozsa (n qubits)
- Distinguer oracle constant vs équilibré via la mesure
- Implémenter les circuits en Qiskit et la dynamique Hadamard en QuTiP

---

## 1. Parallélisme quantique

Le parallélisme quantique exploite la superposition pour évaluer une fonction $f(x)$ sur plusieurs états d'entrée simultanément.

Soit un oracle $U_f$ agissant sur $n+1$ qubits :

$$
U_f : |x\rangle|y\rangle \mapsto |x\rangle|y \oplus f(x)\rangle
$$

En préparant $|y\rangle = |-\rangle = \frac{1}{\sqrt{2}}(|0\rangle - |1\rangle)$, on obtient :

$$
U_f |x\rangle|-\rangle = (-1)^{f(x)} |x\rangle|-\rangle
$$

La phase $(-1)^{f(x)}$ encode le résultat de $f(x)$ sans le mesurer directement. C'est le **truc de la phase** (phase kickback).

## 2. Algorithme de Deutsch (1 qubit)

**Problème** : Étant donné une fonction $f : \{0,1\} \to \{0,1\}$, déterminer si $f$ est **constante** ($f(0)=f(1)$) ou **équilibrée** ($f(0)\neq f(1)$) avec une seule interrogation.

### Circuit

```
|0⟩ — H — — U_f — H — M
                  |
|1⟩ — H — — — — — —
```

### Étapes

1. Préparer $|\psi_0\rangle = |0\rangle \otimes |1\rangle$
2. Appliquer Hadamard : $|\psi_1\rangle = |+\rangle \otimes |-\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle) \otimes \frac{1}{\sqrt{2}}(|0\rangle - |1\rangle)$
3. Appliquer $U_f$ : $|\psi_2\rangle = \frac{1}{\sqrt{2}}\left[(-1)^{f(0)}|0\rangle + (-1)^{f(1)}|1\rangle\right] \otimes |-\rangle$
4. Appliquer $H$ sur le premier registre :
   $$
   |\psi_3\rangle = \frac{1}{2}\left[(-1)^{f(0)}+(-1)^{f(1)}\right]|0\rangle + \frac{1}{2}\left[(-1)^{f(0)}-(-1)^{f(1)}\right]|1\rangle
   $$

Si $f$ constante → $(-1)^{f(0)} = (-1)^{f(1)}$ → amplitude de $|0\rangle$ = $\pm 1$, amplitude de $|1\rangle$ = 0
Si $f$ équilibrée → $(-1)^{f(0)} = -(-1)^{f(1)}$ → amplitude de $|0\rangle$ = 0, amplitude de $|1\rangle$ = $\pm 1$

**Une seule mesure** détermine le type de $f$ avec certitude.

## 3. Généralisation de Deutsch-Jozsa (n qubits)

**Problème** : Étant donné $f : \{0,1\}^n \to \{0,1\}$ avec la **promesse** qu'elle est soit constante, soit équilibrée (autant de $0$ que de $1$ en sortie), déterminer laquelle classiquement : $2^{n-1}+1$ appels, quantiquement : **1 seul appel**.

### Circuit

```
|0⟩^{\otimes n} — H^{\otimes n} — U_f — H^{\otimes n} — M
                               |
|1⟩ — H — — — — — — — — — — — —
```

### Analyse

$$|\psi_0\rangle = |0\rangle^{\otimes n}|1\rangle$$
$$|\psi_1\rangle = \frac{1}{\sqrt{2^n}}\sum_{x=0}^{2^n-1} |x\rangle \otimes |-\rangle$$
$$|\psi_2\rangle = \frac{1}{\sqrt{2^n}}\sum_{x=0}^{2^n-1} (-1)^{f(x)} |x\rangle \otimes |-\rangle$$

Après la seconde transformée de Hadamard sur les $n$ qubits :

$$|\psi_3\rangle = \frac{1}{2^n}\sum_{x=0}^{2^n-1} (-1)^{f(x)} \sum_{y=0}^{2^n-1} (-1)^{x\cdot y} |y\rangle \otimes |-\rangle$$

L'amplitude de $|0\rangle^{\otimes n}$ est :

$$\frac{1}{2^n}\sum_{x=0}^{2^n-1} (-1)^{f(x)}$$

- Si $f$ constante → amplitude = $\pm 1$ → mesure $|0\rangle^{\otimes n}$ avec probabilité 1
- Si $f$ équilibrée → amplitude = 0 → on ne mesure **jamais** $|0\rangle^{\otimes n}$

## 4. Implémentation Qiskit

```python
import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram

def oracle_constante(qc, n, sortie=0):
    """Oracle constant : f(x) = sortie pour tout x"""
    if sortie == 1:
        qc.x(n)  # flip le qubit de sortie

def oracle_equilibre(qc, n):
    """Oracle équilibré : f(x) = x_0 (parité du premier bit)"""
    for i in range(n):
        qc.cx(i, n)

def deutsch_jozsa(n, constant=True):
    qc = QuantumCircuit(n + 1, n)

    # Initialisation du registre de sortie à |1⟩
    qc.x(n)

    # Hadamard sur tous les qubits
    qc.h(range(n + 1))

    # Oracle
    if constant:
        oracle_constante(qc, n, sortie=0)
    else:
        oracle_equilibre(qc, n)

    # Hadamard sur les n premiers qubits
    qc.h(range(n))

    # Mesure
    qc.measure(range(n), range(n))

    return qc

# Test avec n=3 qubits
n = 3
qc_const = deutsch_jozsa(n, constant=True)
qc_equi = deutsch_jozsa(n, constant=False)

print("Circuit constant :")
print(qc_const.draw())

# Simulation
backend = Aer.get_backend('qasm_simulator')
for nom, qc in [("Constant", qc_const), ("Équilibré", qc_equi)]:
    result = execute(qc, backend, shots=1024).result()
    counts = result.get_counts()
    print(f"\n{nom} : {counts}")
```

## 5. Dynamique Hadamard avec QuTiP

```python
import numpy as np
import qutip as qt

def hadamard_port():
    """Porte Hadamard en QuTiP"""
    H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])
    return qt.Qobj(H)

def deutsch_dynamique(f_type='constant'):
    """
    Simule la dynamique de l'algorithme de Deutsch
    f_type : 'constant' ou 'balanced'
    """
    H = hadamard_port()

    # États de base
    zero = qt.basis(2, 0)  # |0⟩
    one = qt.basis(2, 1)   # |1⟩

    # État initial |0⟩ ⊗ |1⟩
    psi0 = qt.tensor(zero, one)

    # Hadamard sur les deux qubits
    H2 = qt.tensor(H, H)
    psi1 = H2 * psi0

    # Oracle U_f sous forme de matrice
    if f_type == 'constant':
        # f(0)=f(1)=0  → U_f = I ⊗ I (pas de changement de phase)
        U_f = qt.tensor(qt.qeye(2), qt.qeye(2))
    else:
        # f(0)=0, f(1)=1  → phase flip sur |1⟩
        # U_f |x⟩|y⟩ = |x⟩|y ⊕ f(x)⟩
        # Pour y=|−⟩, cela donne (−1)^{f(x)}|x⟩|−⟩
        mat = np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, -1]])
        U_f = qt.Qobj(mat, dims=[[2, 2], [2, 2]])

    psi2 = U_f * psi1

    # Second Hadamard sur le premier qubit seulement
    H_I = qt.tensor(H, qt.qeye(2))
    psi3 = H_I * psi2

    # Mesure du premier qubit
    prob_0 = (psi3.ptrace(0)[0, 0]).real
    prob_1 = (psi3.ptrace(0)[1, 1]).real

    print(f"Oracle {f_type} :")
    print(f"  P(|0⟩) = {prob_0:.3f}, P(|1⟩) = {prob_1:.3f}")
    if f_type == 'constant':
        assert abs(prob_0 - 1.0) < 1e-6
    else:
        assert abs(prob_1 - 1.0) < 1e-6

    return psi3

# Test
deutsch_dynamique('constant')
deutsch_dynamique('balanced')
```

```python
import numpy as np
import qutip as qt

def simulation_hadamard_evol(t=1.0):
    """
    Simulation de l'évolution Hadamard comme rotation
    H = (X + Z)/√2  → Hamiltonien H_eff = (π/2)*(X+Z)/√2
    """
    sx = qt.sigmax()
    sz = qt.sigmaz()

    # Hamiltonien effectif pour la porte Hadamard
    H_eff = (np.pi / 2) * (sx + sz) / np.sqrt(2)

    # Opérateur d'évolution
    U = (-1j * H_eff * t).expm()

    # Vérification : U doit être proche de la porte Hadamard
    H_target = (1 / np.sqrt(2)) * (sx + sz)
    fidelity = abs((H_target.dag() * U).tr() / 2)

    print(f"Fidélité Hadamard par évolution : {fidelity:.6f}")
    assert fidelity > 0.99

    return U

U_h = simulation_hadamard_evol()
print("U_H =", U_h)
```

## 6. Exercices

### Exercice 1 : Preuve du truc de la phase
Montrez que $U_f|x\rangle|-\rangle = (-1)^{f(x)}|x\rangle|-\rangle$.

### Exercice 2 : Généralisation
Généralisez l'algorithme de Deutsch-Jozsa au cas où $f:\{0,1\}^n\to\{0,1\}^m$. Quel est l'avantage quantique ?

### Exercice 3 : Implémentation — Oracle arbitraire
Écrivez un oracle pour $f(x) = x_0 \oplus x_1 \oplus \cdots \oplus x_{n-1}$ (parité totale) et testez l'algorithme.

### Exercice 4 : Simulation QuTiP — Bruit dépolarisant
Ajoutez un canal dépolarisant sur chaque qubit après l'oracle et étudiez la probabilité de succès en fonction du taux de bruit $p$.

```python
# Indice :
from qutip import destroy, qeye
def canal_depolarisant(rho, p):
    """Canal dépolarisant : rho → (1-p)rho + p I/2"""
    I = qeye(2) / 2
    return (1-p) * rho + p * I
```

### Exercice 5 : Qiskit Runtime — Estimer les ressources
Utilisez `qiskit.transpile` pour estimer la profondeur du circuit Deutsch-Jozsa pour $n=10,20,50$. Comparez avec une approche classique.

### Exercice 6 : Analyse de complexité
Démontrez que l'avantage quantique est **exponentiel** : classiquement $O(2^{n-1}+1)$ vs quantiquement $O(1)$ appels à l'oracle.

---

## Références

- Deutsch, D. (1985). "Quantum theory, the Church–Turing principle and the universal quantum computer". *Proc. R. Soc. Lond. A*, 400, 97–117.
- Nielsen, M. A. & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*.
- Qiskit Textbook : https://qiskit.org/textbook/ch-algorithms/deutsch-jozsa.html
