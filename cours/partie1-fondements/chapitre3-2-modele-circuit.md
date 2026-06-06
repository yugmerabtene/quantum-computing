# Chapitre 3.2 — Modèle circuit

## Objectifs

- Maîtriser le formalisme du circuit quantique
- Implémenter la téléportation quantique
- Implémenter le codage superdense
- Comprendre le rôle de la mesure et du feed-forward classique

---

## 1. Formalisme du circuit quantique

Un **circuit quantique** est une séquence de portes appliquées à des qubits, suivies de mesures.

### 1.1 Conventions

- Chaque ligne représente un qubit (ou registre classique)
- Le temps va de gauche à droite
- Les portes sont appliquées séquentiellement
- Les doubles traits indiquent des bits classiques

```
     ┌───┐     ┌─┐
q_0: ┤ H ├──■──┤M├───
     └───┘┌─┴─┐└╥┘┌─┐
q_1: ─────┤ X ├─╫─┤M├
          └───┘ ║ └╥┘
c_0: ═══════════╩══╬═
c_1: ══════════════╩═
```

### 1.2 Règles de composition

1. **Séquentielle** : $U_2 U_1$ (d'abord $U_1$, puis $U_2$)
2. **Parallèle** : $U \otimes V$ (sur des qubits différents)
3. **Conditionnelle** : $|0\rangle\langle0| \otimes I + |1\rangle\langle1| \otimes U$ (porte contrôlée)

---

## 2. Téléportation quantique

### 2.1 Principe

Transférer un état quantique $\ket{\psi}$ d'Alice à Bob en utilisant :
- Un état intriqué partagé
- 2 bits classiques
- Une porte de correction conditionnelle

**Ne viole pas la relativité :** la transmission classique est limitée par $c$.

### 2.2 Circuit

```
                    ┌───┐          ┌─┐
ψ: ────────────────┤ X ├──────────┤M├───
               ┌───┐└─┬─┘     ┌─┐└╥┘
A: ──────■─────┤ H ├──■───────┤M├─╫─⊕───
         └─┴─┘ └───┘          └╥┘ ║ │
B: ──────■─────────────────────╫──╫─■─⊕─
         │                     ║  ║   │
```

### 2.3 Implémentation Qiskit

```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
import numpy as np

# Registres
qr = QuantumRegister(3, 'q')  # q[0]=ψ, q[1]=A, q[2]=B
cr = ClassicalRegister(2, 'c')
qc = QuantumCircuit(qr, cr)

# État à téléporter |ψ⟩ = cos(θ/2)|0⟩ + e^{iφ}sin(θ/2)|1⟩
theta, phi = np.pi/3, np.pi/4
qc.ry(theta, 0)
qc.rz(phi, 0)

# Intrication Alice-Bob
qc.h(1)
qc.cx(1, 2)

# Téléportation
qc.cx(0, 1)
qc.h(0)
qc.measure(0, 0)
qc.measure(1, 1)

# Correction conditionnelle
qc.cx(1, 2)
qc.cz(0, 2)

print("Circuit de téléportation :")
print(qc.draw())

# Simulation
sim = AerSimulator()
job = sim.run(qc, shots=1024)
result = job.result()
counts = result.get_counts(qc)
print("\nRésultats :", counts)
```

### 2.4 Vérification avec QuTiP

```python
import qutip as qt
import numpy as np

# État à téléporter
theta, phi = np.pi/3, np.pi/4
psi_in = np.cos(theta/2) * qt.basis(2,0) + np.exp(1j*phi) * np.sin(theta/2) * qt.basis(2,1)

# État initial total : |ψ⟩_A ⊗ |00⟩_{AB}
psi0 = qt.tensor(psi_in, qt.basis(2,0), qt.basis(2,0))

# Portes
H = (1/np.sqrt(2)) * qt.Qobj([[1,1],[1,-1]])
CNOT = qt.Qobj(np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]),
               dims=[[2,2],[2,2]])

# Intrication Alice-Bob (porte sur qubits 1,2)
U_entangle = qt.tensor(qt.qeye(2), CNOT) * qt.tensor(qt.qeye(2), H, qt.qeye(2))
psi1 = U_entangle * psi0

# Après téléportation, le qubit 2 devrait être dans l'état ψ_in
rho_B = (psi1 * psi1.dag()).ptrace(2)
fidelity = (psi_in.dag() * rho_B * psi_in).real
print(f"Fidélité : {fidelity:.4f}")
```

**Sortie attendue :**

```
Fidélité : 0.5000
```

---

## 3. Codage superdense

### 3.1 Principe

Transmettre 2 bits classiques en envoyant 1 qubit, grâce à l'intrication.

### 3.2 Protocole

1. Préparation de $\ket{\Phi^+} = (\ket{00} + \ket{11})/\sqrt{2}$
2. Alice applique une porte sur SON qubit selon les 2 bits à envoyer
3. Alice envoie son qubit à Bob
4. Bob mesure dans la base de Bell

### 3.3 Encodage

| Bits | Porte d'Alice | État résultant |
|------|---------------|----------------|
| $00$ | $I$ | $\ket{\Phi^+}$ |
| $01$ | $X$ | $\ket{\Psi^+}$ |
| $10$ | $Z$ | $\ket{\Phi^-}$ |
| $11$ | $iY$ | $\ket{\Psi^-}$ |

### 3.4 Implémentation Qiskit

```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def superdense(b0, b1):
    """Envoie 2 bits classiques (b0, b1) via 1 qubit."""
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'c')
    qc = QuantumCircuit(qr, cr)

    # Intrication
    qc.h(0)
    qc.cx(0, 1)

    # Encodage par Alice
    if b1:
        qc.x(0)  # Bit 1
    if b0:
        qc.z(0)  # Bit 0

    # Décodage par Bob
    qc.cx(0, 1)
    qc.h(0)
    qc.measure([0, 1], [0, 1])

    sim = AerSimulator()
    result = sim.run(qc, shots=1).result()
    bits = list(result.get_counts(qc).keys())[0]
    return bits

# Test
for b0, b1 in [(0,0), (0,1), (1,0), (1,1)]:
    result = superdense(b0, b1)
    # Qiskit retourne les bits en ordre inverse (MSB en premier)
    bits_recus = result[::-1]
    print(f"Envoyé : {b0}{b1}, Reçu : {bits_recus}")
```

**Sortie (après réordonnancement) :**

```
Envoyé : 00, Reçu : 00
Envoyé : 01, Reçu : 01
Envoyé : 10, Reçu : 10
Envoyé : 11, Reçu : 11
```

---

## 4. Simulation classique des circuits

### 4.1 Limitations

La simulation classique d'un circuit quantique à $n$ qubits nécessite $O(2^n)$ mémoire. Limite pratique : $\sim 30$ qubits sur un ordinateur standard, $\sim 50$ qubits sur supercalculateur.

### 4.2 Simulateur Qiskit Aer

```python
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector

# Circuit à 3 qubits : GHZ state
qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 2)

# Simulation du statevector
state = Statevector.from_instruction(qc)
print("État GHZ :", state)

# Mesures
qc.measure_all()
sim = AerSimulator()
job = sim.run(qc, shots=4096)
counts = job.result().get_counts()
print("Distribution :", counts)
```

### 4.3 Pourquoi la simulation est coûteuse

Un état à $n$ qubits est un vecteur de $2^n$ amplitudes complexes :

$$
\ket{\psi} = \sum_{i=0}^{2^n-1} \alpha_i \ket{i}, \quad \alpha_i \in \mathbb{C}
$$

Pour $n=30$ : $2^{30} \approx 10^9$ amplitudes $\to$ 16 Go de RAM.

---

## 5. Exercices

1. Implémenter le protocole BB84 de distribution de clés quantiques en circuit Qiskit.
2. Modifier le circuit de téléportation pour téléporter $\ket{-}$ et vérifier le résultat.
3. Implémenter le codage superdense avec QuTiP en calculant la fidélité.
4. Construire un circuit qui génère l'état W : $\ket{W} = (\ket{001} + \ket{010} + \ket{100})/\sqrt{3}$.
5. Comparer le nombre de portes entre une implémentation naïve et optimisée de la téléportation.
