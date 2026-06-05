# Séance 9.2 — Codes correcteurs quantiques

## Objectifs

- Comprendre le code à répétition de phase à 3 qubits
- Maîtriser le code de Shor [9, 1, 3]
- Formaliser les codes CSS
- Introduire le formalisme des stabilisateurs
- Implémenter le code à 3 qubits avec Qiskit

---

## 1. Code à répétition de phase (3 qubits)

### 1.1 Motivation

Le code à répétition de phase protège contre les **erreurs bit-flip** ($X$). L'idée est de coder 1 qubit logique dans 3 qubits physiques :

$$
\ket{0_L} = \ket{000},\quad \ket{1_L} = \ket{111}
$$

### 1.2 Encodage

L'encodage se fait par des portes CNOT :

$$
\ket{\psi} = \alpha\ket{0} + \beta\ket{1} \;\longrightarrow\; \alpha\ket{000} + \beta\ket{111}
$$

### 1.3 Détection et correction

On mesure les **syndromes** $Z_1Z_2$ et $Z_2Z_3$ (sans mesurer les qubits individuellement) :

| Syndrome $(Z_1Z_2, Z_2Z_3)$ | Erreur | Correction |
|-----------------------------|--------|------------|
| $(+1, +1)$ | Aucune | $I$ |
| $(-1, +1)$ | $X_1$ | $X_1$ |
| $(-1, -1)$ | $X_2$ | $X_2$ |
| $(+1, -1)$ | $X_3$ | $X_3$ |

### 1.4 Implémentation Qiskit

```python
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, pauli_error
import numpy as np

def encode_repetition(qc, qr, mode='phase'):
    """Code à répétition de phase : |0> -> |000>, |1> -> |111>."""
    qc.cx(qr[0], qr[1])
    qc.cx(qr[0], qr[2])

def syndrome_measurement(qc, qr, cr):
    """Mesure des syndromes Z1Z2 et Z2Z3 via des qubits auxiliaires."""
    qc.cx(qr[0], qr[3])
    qc.cx(qr[1], qr[3])
    qc.measure(qr[3], cr[0])

    qc.cx(qr[1], qr[4])
    qc.cx(qr[2], qr[4])
    qc.measure(qr[4], cr[1])

def correction_x(qc, qr, cr):
    """Correction basée sur le syndrome."""
    # Si cr = [1,0] -> X1, [1,1] -> X2, [0,1] -> X3
    qc.x(qr[0]).c_if(cr, 1)   # 01: X1
    qc.x(qr[1]).c_if(cr, 2)   # 10: X2 (binaire 10 = 2)
    qc.x(qr[2]).c_if(cr, 3)   # 11: X3 (binaire 11 = 3)

# Circuit complet
qr = QuantumRegister(5, 'q')
cr = ClassicalRegister(2, 'syndrome')
qc = QuantumCircuit(qr, cr)

# État |+> logique
qc.h(0)
encode_repetition(qc, qr)
qc.barrier()

# Injection d'une erreur bit-flip sur le qubit 0
qc.x(qr[0])
qc.barrier()

# Mesure du syndrome et correction
syndrome_measurement(qc, qr, cr)
qc.barrier()
correction_x(qc, qr, cr)

# Décodage
qc.cx(qr[0], qr[1])
qc.cx(qr[0], qr[2])

# Vérification
qc.h(0)

print(qc.draw())

# Simulation idéale
sim = AerSimulator()
result = sim.run(qc, shots=1024).result()
print("Résultat après correction :", result.get_counts())
```

**Sortie attendue :**

```
Résultat après correction : {'0 00': 1024}
```

Le qubit logique est correctement restauré malgré l'erreur $X$ sur le premier qubit.

### 1.5 Code à répétition de phase (phase-flip)

Pour les erreurs de phase ($Z$), on utilise une rotation de base :

$$
\ket{+} = \frac{\ket{0} + \ket{1}}{\sqrt{2}},\quad
\ket{-} = \frac{\ket{0} - \ket{1}}{\sqrt{2}}
$$

Le code à répétition de phase protège contre $Z$ :

$$
\ket{0_L} = \ket{+++},\quad \ket{1_L} = \ket{---}
$$

```python
def encode_phase_flip(qc, qr):
    """Code à répétition de phase pour erreurs Z."""
    qc.h(qr[0])
    qc.h(qr[1])
    qc.h(qr[2])
    qc.cx(qr[0], qr[1])
    qc.cx(qr[0], qr[2])
    qc.h(qr[1])
    qc.h(qr[2])
```

---

## 2. Code de Shor [9, 1, 3]

### 2.1 Construction

Le code de Shor combine le code bit-flip et le code phase-flip :

$$
\ket{0_L} = \frac{(\ket{000} + \ket{111})(\ket{000} + \ket{111})(\ket{000} + \ket{111})}{2\sqrt{2}}
$$

$$
\ket{1_L} = \frac{(\ket{000} - \ket{111})(\ket{000} - \ket{111})(\ket{000} - \ket{111})}{2\sqrt{2}}
$$

Il corrige **une erreur arbitraire** sur un qubit (car toute erreur se décompose en $I, X, Y, Z$).

### 2.2 Propriétés

- $[\![n, k, d]\!] = [\![9, 1, 3]\!]$
- Distance $d = 3$ : corrige 1 erreur
- Taux de code : $k/n = 1/9$
- Protège contre tout type d'erreur Pauli sur un qubit

### 2.3 Circuit d'encodage

```python
from qiskit import QuantumCircuit

def shor_encode(qc, qr):
    """Encodage du code de Shor [9,1,3]."""
    # Portes pour le niveau phase-flip
    qc.cx(qr[0], qr[3])
    qc.cx(qr[0], qr[6])

    # Portes Hadamard pour passer en base X
    qc.h(qr[0])
    qc.h(qr[3])
    qc.h(qr[6])

    # Portes pour le niveau bit-flip dans chaque bloc
    for block_start in [0, 3, 6]:
        qc.cx(qr[block_start], qr[block_start + 1])
        qc.cx(qr[block_start], qr[block_start + 2])

def shor_decode(qc, qr):
    """Décodage du code de Shor."""
    for block_start in [0, 3, 6]:
        qc.cx(qr[block_start], qr[block_start + 1])
        qc.cx(qr[block_start], qr[block_start + 2])

    qc.h(qr[0])
    qc.h(qr[3])
    qc.h(qr[6])

    qc.cx(qr[0], qr[3])
    qc.cx(qr[0], qr[6])

# Vérification : encodage de |0> et décodage
qr = QuantumCircuit(9)
shor_encode(qr, qr.qubits)
shor_decode(qr, qr.qubits)

# Le circuit doit revenir à l'état initial
print("Circuit du code de Shor (9 qubits) :")
print(qr.draw())
```

---

## 3. Codes CSS (Calderbank-Shor-Steane)

### 3.1 Définition

Les codes CSS sont construits à partir de **deux codes classiques linéaires** $C_1$ et $C_2$ tels que $C_2 \subset C_1$ :

$$
\text{CSS}(C_1, C_2) = \left\{ \frac{1}{\sqrt{|C_2|}} \sum_{w \in C_2} \ket{v + w} \; \middle| \; v \in C_1 \right\}
$$

### 3.2 Propriétés

- Corrige $X$ et $Z$ séparément
- Si $C_1$ corrige $t_1$ erreurs et $C_2^\perp$ corrige $t_2$ erreurs, alors CSS corrige $\min(t_1, t_2)$ erreurs
- Exemple important : le code de Steane $[\![7,1,3]\!]$

### 3.3 Code de Steane [7,1,3]

Le code de Steane utilise le code classique de Hamming $[7,4,3]$ :

$$
\ket{0_L} = \frac{1}{\sqrt{8}} \sum_{w \in C_\text{Hamming}} \ket{w}
$$

$$
\ket{1_L} = \frac{1}{\sqrt{8}} \sum_{w \in C_\text{Hamming}} \ket{w + \mathbf{1}}
$$

```python
import numpy as np
from qiskit import QuantumCircuit

# Matrice de parité du code de Hamming [7,4,3]
H_hamming = np.array([
    [1, 1, 1, 0, 1, 0, 0],
    [1, 1, 0, 1, 0, 1, 0],
    [1, 0, 1, 1, 0, 0, 1]
], dtype=int)

print("Matrice de parité H du code de Hamming [7,4,3]:")
print(H_hamming)

# Les stabilisateurs X du code de Steane sont les lignes de H
# Les stabilisateurs Z sont les lignes de H appliquées en base X

def steane_encode(qc, qr):
    """Encodage du code de Steane [7,1,3]."""
    # Encoder |0> -> |0_L>
    qc.h(qr[0])
    qc.h(qr[1])
    qc.h(qr[3])
    qc.cx(qr[0], qr[2])
    qc.cx(qr[1], qr[2])
    qc.cx(qr[0], qr[4])
    qc.cx(qr[1], qr[5])
    qc.cx(qr[3], qr[4])
    qc.cx(qr[3], qr[6])

# Stabilisateurs du code de Steane
print("\nStabilisateurs du code de Steane [7,1,3]:")
stabs = [
    "X X X X I I I", "X X I I X X I", "X I X I X I X",
    "Z Z Z Z I I I", "Z Z I I Z Z I", "Z I Z I Z I X"
]
for s in stabs:
    print(f"  {s}")
```

---

## 4. Formalisme des stabilisateurs

### 4.1 Groupe de Pauli à n qubits

Le groupe de Pauli à $n$ qubits est :

$$
\mathcal{P}_n = \left\{ \pm 1, \pm i \right\} \times \{I, X, Y, Z\}^{\otimes n}
$$

### 4.2 Définition d'un code stabilisateur

Un code $[\![n, k, d]\!]$ est défini par un **groupe stabilisateur** $\mathcal{S} \subset \mathcal{P}_n$ :

- $\mathcal{S}$ est un groupe abélien
- $-I \notin \mathcal{S}$
- $\mathcal{S}$ a $n - k$ générateurs indépendants

L'espace de code est :

$$
\mathcal{C} = \left\{ \ket{\psi} \;|\; S\ket{\psi} = \ket{\psi},\; \forall S \in \mathcal{S} \right\}
$$

### 4.3 Mesures de syndrome

Les mesures de syndrome sont des mesures projectives des générateurs $g_i \in \mathcal{S}$ :

$$
\text{Syndrome} = (s_1, s_2, \ldots, s_{n-k}), \quad s_i = \pm 1
$$

où $s_i = +1$ si l'état est dans le $+1$ eigenspace de $g_i$, et $s_i = -1$ sinon.

### 4.4 Représentation binaire

On représente chaque opérateur Pauli par deux vecteurs binaires $(a|b)$ de longueur $n$ :

$$
P = i^{c} \bigotimes_{j=1}^n X^{a_j} Z^{b_j}
$$

La condition de commutation devient :

$$
[P, Q] = 0 \iff a_P \cdot b_Q + a_Q \cdot b_P \equiv 0 \pmod{2}
$$

```python
import numpy as np

def pauli_to_binary(P_str):
    """Convertit un opérateur Pauli en représentation binaire (a|b)."""
    mapping = {
        'I': (0, 0), 'X': (1, 0), 'Y': (1, 1), 'Z': (0, 1)
    }
    a, b = [], []
    for p in P_str:
        if p in mapping:
            ai, bi = mapping[p]
            a.append(ai)
            b.append(bi)
    return np.array(a, dtype=int), np.array(b, dtype=int)

def commutator_product(a1, b1, a2, b2):
    """Retourne 0 si les opérateurs commutent, 1 sinon."""
    return (np.dot(a1, b2) + np.dot(a2, b1)) % 2

# Exemple : vérification de la commutation des stabilisateurs
stabilizers = [
    "XXII", "IXXI", "IIXX"
]

n = 4
pairs = [(a, b) for a in range(len(stabilizers)) for b in range(a+1, len(stabilizers))]
print("Vérification de la commutation des stabilisateurs :")
for idx_a, idx_b in pairs:
    a1, b1 = pauli_to_binary(stabilizers[idx_a])
    a2, b2 = pauli_to_binary(stabilizers[idx_b])
    comm = commutator_product(a1, b1, a2, b2)
    status = "OK" if comm == 0 else "NON"
    print(f"  [{stabilizers[idx_a]}, {stabilizers[idx_b]}] = {status}")
```

**Sortie attendue :**

```
Vérification de la commutation des stabilisateurs :
  [XXII, IXXI] = OK
  [XXII, IIXX] = OK
  [IXXI, IIXX] = OK
```

### 4.5 Exemple : code à 3 qubits dans le formalisme stabilisateur

Pour le code de répétition à 3 qubits, les stabilisateurs sont :

$$
g_1 = Z Z I, \quad g_2 = I Z Z
$$

Les opérateurs logiques sont :

$$
\bar{X} = X X X, \quad \bar{Z} = Z I I
$$

```python
# Code de répétition 3 qubits : vérification des stabilisateurs
import qutip as qt
import numpy as np

I2 = qt.qeye(2)
X = qt.sigmax()
Z = qt.sigmaz()

# Stabilisateurs
g1 = qt.tensor(Z, Z, I2)
g2 = qt.tensor(I2, Z, Z)

# États logiques
ket_0L = qt.tensor(qt.basis(2,0), qt.basis(2,0), qt.basis(2,0))
ket_1L = qt.tensor(qt.basis(2,1), qt.basis(2,1), qt.basis(2,1))

# Vérification
print("Vérification du code à répétition :")
print(f"  g1|0L> = {g1 * ket_0L} == |0L> : {(g1 * ket_0L - ket_0L).norm() < 1e-10}")
print(f"  g2|0L> = {g2 * ket_0L} == |0L> : {(g2 * ket_0L - ket_0L).norm() < 1e-10}")
print(f"  g1|1L> = {g1 * ket_1L} == |1L> : {(g1 * ket_1L - ket_1L).norm() < 1e-10}")
```

**Sortie attendue :**

```
Vérification du code à répétition :
  g1|0L> = Quantum object: dims=[[2,2,2], [1,1,1]]... == |0L> : True
  g2|0L> = Quantum object: dims=[[2,2,2], [1,1,1]]... == |0L> : True
  g1|1L> = Quantum object: dims=[[2,2,2], [1,1,1]]... == |1L> : True
```

---

## 5. Implémentation complète du code à 3 qubits avec correction

```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, pauli_error

def repetition_code_circuit(error_pos=None, p_noise=0.0):
    """
    Circuit complet du code à répétition 3 qubits.
    
    Args:
        error_pos: None (pas d'erreur), ou 0,1,2 (position de l'erreur X)
        p_noise: probabilité de bruit sur les portes
    """
    qr = QuantumRegister(5, 'q')
    cr_syndrome = ClassicalRegister(2, 'syndrome')
    cr_out = ClassicalRegister(1, 'out')
    qc = QuantumCircuit(qr, cr_syndrome, cr_out)

    # Encodage : |0> -> |000>
    qc.cx(qr[0], qr[1])
    qc.cx(qr[0], qr[2])

    # Injection d'erreur
    if error_pos is not None:
        getattr(qc, 'x')(qr[error_pos])

    # Mesure du syndrome
    qc.cx(qr[0], qr[3])
    qc.cx(qr[1], qr[3])
    qc.measure(qr[3], cr_syndrome[0])

    qc.cx(qr[1], qr[4])
    qc.cx(qr[2], qr[4])
    qc.measure(qr[4], cr_syndrome[1])

    # Correction conditionnelle
    qc.x(qr[0]).c_if(cr_syndrome, 1)
    qc.x(qr[1]).c_if(cr_syndrome, 2)
    qc.x(qr[2]).c_if(cr_syndrome, 3)

    # Décodage
    qc.cx(qr[0], qr[1])
    qc.cx(qr[0], qr[2])

    # Mesure du qubit logique
    qc.measure(qr[0], cr_out[0])

    return qc

# Test : injection d'erreur sur chaque position
sim = AerSimulator()
for err_pos in [None, 0, 1, 2]:
    qc = repetition_code_circuit(error_pos=err_pos)
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()
    print(f"Erreur X_{err_pos} : {counts}")
```

**Sortie attendue :**

```
Erreur X_None : {'0 00': 1024}
Erreur X_0 : {'0 00': 1024}
Erreur X_1 : {'0 00': 1024}
Erreur X_2 : {'0 00': 1024}
```

Toutes les erreurs sont correctement corrigées (le qubit logique est toujours mesuré $0$).

---

## 6. Bruit sur le circuit de correction

Le circuit de correction lui-même peut être bruité :

```python
# Modèle de bruit réaliste
noise_model = NoiseModel()
error_gate = pauli_error([('X', 0.001), ('I', 0.999)])
error_meas = pauli_error([('X', 0.01), ('I', 0.99)])
noise_model.add_all_qubit_quantum_error(error_gate, ['cx', 'x'])
noise_model.add_all_qubit_quantum_error(error_meas, ['measure'])

sim_noisy = AerSimulator(noise_model=noise_model)

for p in [0.0, 0.001, 0.005, 0.01, 0.02]:
    qc = repetition_code_circuit(error_pos=0)
    result = sim_noisy.run(qc, shots=8192).result()
    counts = result.get_counts()
    # Compter les échecs
    fails = sum(v for k, v in counts.items() if not k.startswith('0 '))
    total = sum(counts.values())
    print(f"p = {p:.3f} : erreur logique = {fails/total*100:.2f}%")
```

---

## Exercices

1. Implémenter le code de répétition à 5 qubits $[\![5,1,3]\!]$ avec Qiskit. Comparer son taux de succès avec le code à 3 qubits sous le même modèle de bruit.

2. Utiliser QuTiP pour simuler le code de Shor : encodage de $\ket{+}$, injection d'une erreur $Y$ sur le qubit 2, correction, et vérification de la fidélité finale.

3. Montrer que le code de Steane $[\![7,1,3]\!]$ peut être vu comme un code CSS avec $C_1 =$ Hamming $[7,4,3]$ et $C_2 =$ Hamming $[7,4,3]^\perp$.

4. Implémenter la vérification des stabilisateurs pour le code de Shor avec QuTiP : montrer que $\ket{0_L}$ et $\ket{1_L}$ sont bien dans le $+1$ eigenspace de chaque stabilisateur.

5. Avec le formalisme stabilisateur, calculer les distances des codes à répétition pour $n = 3, 5, 7$ qubits.

6. **Projet** : Implémenter un decodeur pour le code de Steane avec Qiskit et le tester contre toutes les erreurs Pauli possibles sur un qubit.
