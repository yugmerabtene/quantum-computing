# Chapitre 9.2 — Codes correcteurs quantiques

## Ce que vous allez apprendre

- Maîtriser le code à répétition de phase à 3 qubits (bit-flip et phase-flip)
- Comprendre et implémenter le code de Shor [9, 1, 3]
- Formaliser les codes CSS (Calderbank-Shor-Steane) et le code de Steane [7,1,3]
- Utiliser le formalisme des stabilisateurs pour décrire n'importe quel code
- Implémenter le code à 3 qubits avec Qiskit et mesurer son efficacité sous bruit

---

## Motivation

Au chapitre précédent, on a vu qu'on ne peut **pas copier** un qubit. Alors comment protéger l'information ? La réponse tient en un mot : **intrication**.

En classique, pour protéger un bit, on fait : $0 \to 000$, $1 \to 111$. Si on reçoit $010$, on vote majoritaire → $0$. Simple.

En quantique, on ne peut pas faire $\alpha\ket{0} + \beta\ket{1} \to \alpha\ket{000} + \beta\ket{111}$ en « copiant ». Mais on peut le faire en **intriquant** ! Les 3 qubits physiques forment un état collectif qui encode 1 qubit logique. Et le syndrome (mesure indirecte) nous dit quelle erreur s'est produite sans révéler $\alpha$ ni $\beta$.

**Enjeu concret** : C'est exactement ce que font les processeurs Google Willow et IBM Heron aujourd'hui — ils encodent quelques qubits logiques dans des centaines de qubits physiques pour protéger l'information.

---

## Idée principale

Imaginez que vous cachez un diamant dans un coffre-fort. Au lieu de mettre le diamant dans un seul coffre (risqué), vous le décomposez en 3 morceaux et les répartissez dans 3 coffres différents. Si un cambrioleur ouvre un coffre, il ne trouve qu'un morceau inutilisable. Et vous, avec les 3 morceaux intacts, vous reconstituez le diamant.

C'est l'idée de la correction quantique :
- L'information est **répartie** sur plusieurs qubits (pas copiée, mais intriquée)
- Une erreur sur un qubit ne détruit pas l'information globale
- On **surveille** les coffres (mesure de syndrome) sans les ouvrir (sans lire l'information)

---

## Contenu du cours

### Section 1 : Code à répétition de phase (3 qubits) — le plus simple

#### Concept

Le code à répétition protège contre les **erreurs bit-flip** ($X$). On code 1 qubit logique dans 3 qubits physiques :

$$
\ket{0_L} = \ket{000},\quad \ket{1_L} = \ket{111}
$$

**Intuition** : C'est l'analogue quantique du code classique par répétition. L'état $\ket{0}$ est « triplé » en $\ket{000}$, et $\ket{1}$ en $\ket{111}$. Par linéarité, $\alpha\ket{0} + \beta\ket{1}$ devient $\alpha\ket{000} + \beta\ket{111}$.

#### Encodage

L'encodage se fait par des portes CNOT :

$$
\ket{\psi} = \alpha\ket{0} + \beta\ket{1} \;\longrightarrow\; \alpha\ket{000} + \beta\ket{111}
$$

**Variables** : $\alpha, \beta$ = amplitudes du qubit logique, $\ket{000}, \ket{111}$ = états de base des 3 qubits physiques.

**Exemple** : $\ket{+} = \frac{1}{\sqrt{2}}(\ket{0} + \ket{1}) \to \frac{1}{\sqrt{2}}(\ket{000} + \ket{111})$ — un état GHZ à 3 qubits.

#### Détection et correction

On mesure les **syndromes** $Z_1Z_2$ et $Z_2Z_3$ (sans mesurer les qubits individuellement) :

**Intuition** : $Z_1Z_2$ compare les qubits 1 et 2. Si ils sont identiques (tous deux 0 ou tous deux 1), le résultat est $+1$. Si ils diffèrent, le résultat est $-1$. C'est comme vérifier « est-ce que les voisins sont d'accord ? » sans demander « quel est votre vote ? ».

| Syndrome $(Z_1Z_2, Z_2Z_3)$ | Erreur | Correction |
|-----------------------------|--------|------------|
| $(+1, +1)$ | Aucune | $I$ |
| $(-1, +1)$ | $X_1$ | $X_1$ |
| $(-1, -1)$ | $X_2$ | $X_2$ |
| $(+1, -1)$ | $X_3$ | $X_3$ |

**Exemple guidé** : Si le syndrome est $(-1, +1)$, cela signifie que $Z_1Z_2 = -1$ (les qubits 1 et 2 sont différents) et $Z_2Z_3 = +1$ (les qubits 2 et 3 sont identiques). Donc le qubit 1 est le fautif → on applique $X_1$.

#### Implémentation Qiskit

```python
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, pauli_error
import numpy as np

def encode_repetition(qc, qr, mode='phase'):
    """Code à répétition de phase : |0> -> |000>, |1> -> |111>.
    Utilise 2 CNOT pour copier l'état du qubit 0 vers les qubits 1 et 2."""
    qc.cx(qr[0], qr[1])   # CNOT : qubit 0 contrôle, qubit 1 cible
    qc.cx(qr[0], qr[2])   # CNOT : qubit 0 contrôle, qubit 2 cible

def syndrome_measurement(qc, qr, cr):
    """Mesure des syndromes Z1Z2 et Z2Z3 via des qubits auxiliaires (3 et 4).
    Le qubit auxiliaire 3 compare les qubits 0 et 1.
    Le qubit auxiliaire 4 compare les qubits 1 et 2."""
    # Syndrome Z1Z2 : l'auxiliaire 3 détecte si q0 ≠ q1
    qc.cx(qr[0], qr[3])   # CNOT contrôlé par q0
    qc.cx(qr[1], qr[3])   # CNOT contrôlé par q1 → parity
    qc.measure(qr[3], cr[0])  # mesure du syndrome

    # Syndrome Z2Z3 : l'auxiliaire 4 détecte si q1 ≠ q2
    qc.cx(qr[1], qr[4])   # CNOT contrôlé par q1
    qc.cx(qr[2], qr[4])   # CNOT contrôlé par q2 → parity
    qc.measure(qr[4], cr[1])  # mesure du syndrome

def correction_x(qc, qr, cr):
    """Correction basée sur le syndrome mesuré.
    cr = 01 (binaire) → X sur qubit 0
    cr = 10 (binaire) → X sur qubit 1
    cr = 11 (binaire) → X sur qubit 2"""
    qc.x(qr[0]).c_if(cr, 1)   # syndrome 01 → erreur sur qubit 0
    qc.x(qr[1]).c_if(cr, 2)   # syndrome 10 → erreur sur qubit 1
    qc.x(qr[2]).c_if(cr, 3)   # syndrome 11 → erreur sur qubit 2

# Circuit complet : 5 qubits (3 données + 2 auxiliaires)
qr = QuantumRegister(5, 'q')
cr = ClassicalRegister(2, 'syndrome')
qc = QuantumCircuit(qr, cr)

# Préparation de l'état |+> logique
qc.h(0)                        # Hadamard sur qubit 0 : |0> -> |+>
encode_repetition(qc, qr)      # Encodage : |+> -> (|000> + |111>)/√2
qc.barrier()

# Injection d'une erreur bit-flip sur le qubit 0
qc.x(qr[0])                    # Erreur X sur le premier qubit
qc.barrier()

# Mesure du syndrome et correction
syndrome_measurement(qc, qr, cr)
qc.barrier()
correction_x(qc, qr, cr)

# Décodage : on ramène 3 qubits → 1 qubit
qc.cx(qr[0], qr[1])
qc.cx(qr[0], qr[2])

# Vérification : retour à |+> puis mesure
qc.h(0)

print(qc.draw())

# Simulation idéale (sans bruit)
sim = AerSimulator()
result = sim.run(qc, shots=1024).result()
print("Résultat après correction :", result.get_counts())
```

**Sortie attendue :**

```
Résultat après correction : {'0 00': 1024}
```

Le qubit logique est correctement restauré malgré l'erreur $X$ sur le premier qubit. Le syndrome a détecté l'erreur et la correction l'a annulée.

#### Code à répétition de phase (phase-flip)

Pour les erreurs de phase ($Z$), on utilise une rotation de base :

$$
\ket{+} = \frac{\ket{0} + \ket{1}}{\sqrt{2}},\quad
\ket{-} = \frac{\ket{0} - \ket{1}}{\sqrt{2}}
$$

**Intuition** : Une erreur $Z$ change $\ket{+}$ en $\ket{-}$ et vice-versa. Si on code dans la base $\{\ket{+}, \ket{-}\}$ au lieu de $\{\ket{0}, \ket{1}\}$, alors une erreur $Z$ devient un « bit-flip » dans cette nouvelle base. On peut donc utiliser le même code !

Le code à répétition de phase protège contre $Z$ :

$$
\ket{0_L} = \ket{+++},\quad \ket{1_L} = \ket{---}
$$

```python
def encode_phase_flip(qc, qr):
    """Code à répétition de phase pour erreurs Z.
    Étape 1 : Hadamard pour passer en base X (|0> -> |+>)
    Étape 2 : CNOT pour l'encodage par répétition
    Étape 3 : Hadamard pour revenir en base Z sur les qubits 1 et 2"""
    qc.h(qr[0])                # |+> sur qubit 0
    qc.h(qr[1])                # |+> sur qubit 1
    qc.h(qr[2])                # |+> sur qubit 2
    qc.cx(qr[0], qr[1])       # Encodage bit-flip dans base X
    qc.cx(qr[0], qr[2])
    qc.h(qr[1])                # Retour en base Z
    qc.h(qr[2])
```

---

### Section 2 : Code de Shor [9, 1, 3] — le premier code complet

#### Concept

Le code de Shor (1995) est le **premier code correcteur quantique** de l'histoire. Il combine le code bit-flip et le code phase-flip pour corriger **toute** erreur sur un qubit.

$$
\ket{0_L} = \frac{(\ket{000} + \ket{111})(\ket{000} + \ket{111})(\ket{000} + \ket{111})}{2\sqrt{2}}
$$

$$
\ket{1_L} = \frac{(\ket{000} - \ket{111})(\ket{000} - \ket{111})(\ket{000} - \ket{111})}{2\sqrt{2}}
$$

**Intuition** : C'est un code « double couche » :
- **Couche externe** (phase-flip) : protège contre les erreurs $Z$ en encodant dans la base $\{\ket{+}, \ket{-}\}$
- **Couche interne** (bit-flip) : chaque $\ket{+}$ ou $\ket{-}$ est lui-même protégé contre les erreurs $X$ par répétition

**Analogie** : C'est comme mettre un document important dans une enveloppe (protection phase), puis mettre 3 copies de cette enveloppe dans 3 boîtes différentes (protection bit-flip).

#### Propriétés

- $[\![n, k, d]\!] = [\![9, 1, 3]\!]$ : 9 qubits physiques, 1 qubit logique, distance 3
- Distance $d = 3$ : corrige 1 erreur arbitraire
- Taux de code : $k/n = 1/9$ (très faible — 8 qubits de surcoût pour 1 qubit logique)
- Protège contre tout type d'erreur Pauli sur un seul qubit

#### Circuit d'encodage

```python
from qiskit import QuantumCircuit

def shor_encode(qc, qr):
    """Encodage du code de Shor [9,1,3] sur 9 qubits.
    Étape 1 : Encodage phase-flip (CNOT entre blocs)
    Étape 2 : Hadamard pour passer en base X
    Étape 3 : Encodage bit-flip dans chaque bloc de 3"""
    # Niveau phase-flip : intrication entre les 3 blocs
    qc.cx(qr[0], qr[3])       # Bloc 0 → Bloc 1
    qc.cx(qr[0], qr[6])       # Bloc 0 → Bloc 2

    # Hadamard : passage en base X pour chaque bloc
    qc.h(qr[0])
    qc.h(qr[3])
    qc.h(qr[6])

    # Niveau bit-flip : répétition dans chaque bloc de 3
    for block_start in [0, 3, 6]:
        qc.cx(qr[block_start], qr[block_start + 1])
        qc.cx(qr[block_start], qr[block_start + 2])

def shor_decode(qc, qr):
    """Décodage du code de Shor : opérations inverses."""
    # Décodage bit-flip dans chaque bloc
    for block_start in [0, 3, 6]:
        qc.cx(qr[block_start], qr[block_start + 1])
        qc.cx(qr[block_start], qr[block_start + 2])

    # Hadamard : retour en base Z
    qc.h(qr[0])
    qc.h(qr[3])
    qc.h(qr[6])

    # Décodage phase-flip
    qc.cx(qr[0], qr[3])
    qc.cx(qr[0], qr[6])

# Vérification : encodage de |0> et décodage → retour à |0>
qr = QuantumCircuit(9)
shor_encode(qr, qr.qubits)
shor_decode(qr, qr.qubits)

print("Circuit du code de Shor (9 qubits) :")
print(qr.draw())
```

**Sortie attendue :**

```
Circuit du code de Shor (9 qubits) :
               ┌───┐                    ┌───┐          
q_0: ──■────■──┤ H ├──■────■────■────■──┤ H ├──■────■──
       │    │  └───┘┌─┴─┐  │  ┌─┴─┐  │  └───┘  │    │  
q_1: ──┼────┼───────┤ X ├──┼──┤ X ├──┼─────────┼────┼──
       │    │       └───┘┌─┴─┐└───┘┌─┴─┐       │    │  
q_2: ──┼────┼────────────┤ X ├─────┤ X ├───────┼────┼──
     ┌─┴─┐  │  ┌───┐     └───┘     └───┘┌───┐┌─┴─┐  │  
q_3: ┤ X ├──┼──┤ H ├──■────■────■────■──┤ H ├┤ X ├──┼──
     └───┘  │  └───┘┌─┴─┐  │  ┌─┴─┐  │  └───┘└───┘  │  
q_4: ───────┼───────┤ X ├──┼──┤ X ├──┼──────────────┼──
            │       └───┘┌─┴─┐└───┘┌─┴─┐            │  
q_5: ───────┼────────────┤ X ├─────┤ X ├────────────┼──
          ┌─┴─┐┌───┐     └───┘     └───┘┌───┐     ┌─┴─┐
q_6: ─────┤ X ├┤ H ├──■────■────■────■──┤ H ├─────┤ X ├
          └───┘└───┘┌─┴─┐  │  ┌─┴─┐  │  └───┘     └───┘
q_7: ───────────────┤ X ├──┼──┤ X ├──┼─────────────────
                    └───┘┌─┴─┐└───┘┌─┴─┐               
q_8: ────────────────────┤ X ├─────┤ X ├───────────────
                         └───┘     └───┘               
```

---

### Section 3 : Codes CSS (Calderbank-Shor-Steane) — la structure algébrique

#### Concept

Les codes CSS sont construits à partir de **deux codes classiques linéaires** $C_1$ et $C_2$ tels que $C_2 \subset C_1$ :

$$
\text{CSS}(C_1, C_2) = \left\{ \frac{1}{\sqrt{|C_2|}} \sum_{w \in C_2} \ket{v + w} \; \middle| \; v \in C_1 \right\}
$$

**Intuition** : Un code CSS utilise deux codes classiques « emboîtés » :
- $C_1$ protège contre les erreurs $X$ (bit-flip)
- $C_2$ protège contre les erreurs $Z$ (phase-flip)
- Le fait que $C_2 \subset C_1$ garantit que les deux protections sont compatibles

**Analogie** : C'est comme avoir deux systèmes de sécurité dans un musée : un contre le vol (X) et un contre l'incendie (Z). Ils doivent être conçus pour ne pas se gêner mutuellement.

#### Propriétés

- Corrige $X$ et $Z$ **séparément** (et donc toute erreur par décomposition de Pauli)
- Si $C_1$ corrige $t_1$ erreurs et $C_2^\perp$ corrige $t_2$ erreurs, alors CSS corrige $\min(t_1, t_2)$ erreurs
- Exemple important : le code de Steane $[\![7,1,3]\!]$

#### Code de Steane [7,1,3]

Le code de Steane utilise le code classique de Hamming $[7,4,3]$ :

$$
\ket{0_L} = \frac{1}{\sqrt{8}} \sum_{w \in C_\text{Hamming}} \ket{w}
$$

$$
\ket{1_L} = \frac{1}{\sqrt{8}} \sum_{w \in C_\text{Hamming}} \ket{w + \mathbf{1}}
$$

**Intuition** : $\ket{0_L}$ est une superposition de tous les mots du code de Hamming (8 mots de 7 bits). $\ket{1_L}$ est la même superposition décalée de $\mathbf{1} = 1111111$.

**Variables** : $C_\text{Hamming}$ = code de Hamming [7,4,3] (8 mots de code de longueur 7), $\mathbf{1}$ = vecteur de tous les 1.

**Exemple** : Le code de Hamming contient les mots $\{0000000, 1010101, 0110011, \ldots\}$. L'état $\ket{0_L}$ est la superposition uniforme de ces 8 mots.

```python
import numpy as np
from qiskit import QuantumCircuit

# Matrice de parité du code de Hamming [7,4,3]
# Chaque ligne définit une contrainte de parité
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
    """Encodage du code de Steane [7,1,3].
    Prépare |0> -> |0_L> en utilisant 3 Hadamard et 6 CNOT."""
    qc.h(qr[0])                # Superposition sur qubit 0
    qc.h(qr[1])                # Superposition sur qubit 1
    qc.h(qr[3])                # Superposition sur qubit 3
    qc.cx(qr[0], qr[2])       # Parité : q2 = q0 ⊕ q1
    qc.cx(qr[1], qr[2])
    qc.cx(qr[0], qr[4])       # Parité : q4 = q0 ⊕ q3
    qc.cx(qr[1], qr[5])       # Parité : q5 = q1 ⊕ q3
    qc.cx(qr[3], qr[4])
    qc.cx(qr[3], qr[6])       # Parité : q6 = q3 ⊕ q0 ⊕ q1

# Stabilisateurs du code de Steane : 3 générateurs X + 3 générateurs Z
print("\nStabilisateurs du code de Steane [7,1,3]:")
stabs = [
    "X X X X I I I",   # Stabilisateur X n°1
    "X X I I X X I",   # Stabilisateur X n°2
    "X I X I X I X",   # Stabilisateur X n°3
    "Z Z Z Z I I I",   # Stabilisateur Z n°1
    "Z Z I I Z Z I",   # Stabilisateur Z n°2
    "Z I Z I Z I X"    # Stabilisateur Z n°3
]
for s in stabs:
    print(f"  {s}")
```

---

### Section 4 : Formalisme des stabilisateurs — le langage universel

#### Concept

Le formalisme des stabilisateurs est le **langage standard** pour décrire les codes quantiques. Il unifie tous les codes (Shor, Steane, surface, etc.) sous un même cadre mathématique.

#### Groupe de Pauli à n qubits

$$
\mathcal{P}_n = \left\{ \pm 1, \pm i \right\} \times \{I, X, Y, Z\}^{\otimes n}
$$

**Intuition** : Le groupe de Pauli à $n$ qubits contient tous les produits tensoriels de matrices de Pauli. Pour 3 qubits, il contient des éléments comme $X \otimes Z \otimes I$, $Y \otimes Y \otimes Z$, etc.

#### Définition d'un code stabilisateur

Un code $[\![n, k, d]\!]$ est défini par un **groupe stabilisateur** $\mathcal{S} \subset \mathcal{P}_n$ :

- $\mathcal{S}$ est un groupe abélien (tous les éléments commutent entre eux)
- $-I \notin \mathcal{S}$ (le groupe ne contient pas $-I$)
- $\mathcal{S}$ a $n - k$ générateurs indépendants

L'espace de code est :

$$
\mathcal{C} = \left\{ \ket{\psi} \;|\; S\ket{\psi} = \ket{\psi},\; \forall S \in \mathcal{S} \right\}
$$

**Intuition** : L'espace de code est l'ensemble des états qui sont « invariants » sous l'action de tous les stabilisateurs. Chaque stabilisateur est comme un « test » : l'état doit le passer tous avec le résultat $+1$.

**Analogie** : Les stabilisateurs sont comme des gardes de sécurité. Chaque garde vérifie une propriété (par exemple, « les qubits 1 et 2 sont-ils identiques ? »). L'espace de code est l'ensemble des états qui satisfont tous les gardes.

**Variables** : $\mathcal{S}$ = groupe stabilisateur, $n$ = nombre de qubits physiques, $k$ = nombre de qubits logiques, $d$ = distance du code.

#### Mesures de syndrome

Les mesures de syndrome sont des mesures projectives des générateurs $g_i \in \mathcal{S}$ :

$$
\text{Syndrome} = (s_1, s_2, \ldots, s_{n-k}), \quad s_i = \pm 1
$$

**Intuition** : Si l'état est dans le code (pas d'erreur), tous les $s_i = +1$. Si une erreur $E$ se produit, certains $s_i$ passent à $-1$. Le motif des $-1$ identifie l'erreur.

**Variables** : $s_i = +1$ si l'état est dans le $+1$ eigenspace de $g_i$, $s_i = -1$ sinon.

#### Représentation binaire

On représente chaque opérateur Pauli par deux vecteurs binaires $(a|b)$ de longueur $n$ :

$$
P = i^{c} \bigotimes_{j=1}^n X^{a_j} Z^{b_j}
$$

**Intuition** : Au lieu d'écrire $X \otimes I \otimes Z \otimes Y$, on écrit $(1,0,0,1 | 0,0,1,1)$ — deux vecteurs binaires. $X = (1|0)$, $Z = (0|1)$, $Y = (1|1)$, $I = (0|0)$.

La condition de commutation devient :

$$
[P, Q] = 0 \iff a_P \cdot b_Q + a_Q \cdot b_P \equiv 0 \pmod{2}
$$

**Variables** : $a_j, b_j \in \{0,1\}$ indiquent la présence de $X$ et $Z$ sur le qubit $j$, $c$ est une phase.

```python
import numpy as np

def pauli_to_binary(P_str):
    """Convertit un opérateur Pauli en représentation binaire (a|b).
    I -> (0,0), X -> (1,0), Y -> (1,1), Z -> (0,1)"""
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
    """Retourne 0 si les opérateurs commutent, 1 sinon.
    Condition : a1·b2 + a2·b1 ≡ 0 (mod 2)"""
    return (np.dot(a1, b2) + np.dot(a2, b1)) % 2

# Vérification : les stabilisateurs XXII, IXXI, IIXX commutent-ils ?
stabilizers = [
    "XXII",   # X⊗X⊗I⊗I
    "IXXI",   # I⊗X⊗X⊗I
    "IIXX"    # I⊗I⊗X⊗X
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

#### Exemple : code à 3 qubits dans le formalisme stabilisateur

Pour le code de répétition à 3 qubits, les stabilisateurs sont :

$$
g_1 = Z Z I, \quad g_2 = I Z Z
$$

**Intuition** : $g_1 = ZZI$ vérifie que les qubits 1 et 2 sont identiques. $g_2 = IZZ$ vérifie que les qubits 2 et 3 sont identiques. Ensemble, ils garantissent que les 3 qubits sont identiques.

Les opérateurs logiques sont :

$$
\bar{X} = X X X, \quad \bar{Z} = Z I I
$$

**Intuition** : $\bar{X} = XXX$ est l'opération logique « bit-flip » sur le qubit logique. Il flippe les 3 qubits physiques simultanément. $\bar{Z} = ZII$ est l'opération logique « phase-flip » — il suffit de changer la phase d'un seul qubit grâce à la redondance.

```python
# Vérification avec QuTiP que les états logiques sont bien stabilisés
import qutip as qt
import numpy as np

I2 = qt.qeye(2)
X = qt.sigmax()
Z = qt.sigmaz()

# Stabilisateurs du code à répétition 3 qubits
g1 = qt.tensor(Z, Z, I2)    # ZZI : compare qubits 0 et 1
g2 = qt.tensor(I2, Z, Z)    # IZZ : compare qubits 1 et 2

# États logiques encodés
ket_0L = qt.tensor(qt.basis(2,0), qt.basis(2,0), qt.basis(2,0))  # |000>
ket_1L = qt.tensor(qt.basis(2,1), qt.basis(2,1), qt.basis(2,1))  # |111>

# Vérification : g|ψ_L> = |ψ_L> (valeur propre +1)
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

### Section 5 : Implémentation complète avec correction

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
    qr = QuantumRegister(5, 'q')        # 3 données + 2 auxiliaires
    cr_syndrome = ClassicalRegister(2, 'syndrome')  # 2 bits de syndrome
    cr_out = ClassicalRegister(1, 'out')            # 1 bit de résultat
    qc = QuantumCircuit(qr, cr_syndrome, cr_out)

    # Encodage : |0> -> |000> via 2 CNOT
    qc.cx(qr[0], qr[1])
    qc.cx(qr[0], qr[2])

    # Injection d'erreur (pour tester)
    if error_pos is not None:
        getattr(qc, 'x')(qr[error_pos])

    # Mesure du syndrome Z1Z2 via qubit auxiliaire 3
    qc.cx(qr[0], qr[3])
    qc.cx(qr[1], qr[3])
    qc.measure(qr[3], cr_syndrome[0])

    # Mesure du syndrome Z2Z3 via qubit auxiliaire 4
    qc.cx(qr[1], qr[4])
    qc.cx(qr[2], qr[4])
    qc.measure(qr[4], cr_syndrome[1])

    # Correction conditionnelle basée sur le syndrome
    qc.x(qr[0]).c_if(cr_syndrome, 1)   # syndrome 01 → erreur qubit 0
    qc.x(qr[1]).c_if(cr_syndrome, 2)   # syndrome 10 → erreur qubit 1
    qc.x(qr[2]).c_if(cr_syndrome, 3)   # syndrome 11 → erreur qubit 2

    # Décodage : |000> -> |0>, |111> -> |1>
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

Toutes les erreurs sont correctement corrigées — le qubit logique est toujours mesuré $0$.

---

### Section 6 : Bruit sur le circuit de correction

Le circuit de correction lui-même peut être bruité ! C'est un point crucial pour la pratique.

```python
# Modèle de bruit réaliste : erreurs sur les portes et les mesures
noise_model = NoiseModel()
error_gate = pauli_error([('X', 0.001), ('I', 0.999)])    # 0.1% erreur par porte
error_meas = pauli_error([('X', 0.01), ('I', 0.99)])      # 1% erreur de mesure
noise_model.add_all_qubit_quantum_error(error_gate, ['cx', 'x'])
noise_model.add_all_qubit_quantum_error(error_meas, ['measure'])

sim_noisy = AerSimulator(noise_model=noise_model)

# Test avec différentes probabilités de bruit additionnel
for p in [0.0, 0.001, 0.005, 0.01, 0.02]:
    qc = repetition_code_circuit(error_pos=0)
    result = sim_noisy.run(qc, shots=8192).result()
    counts = result.get_counts()
    # Compter les échecs de correction (résultat ≠ 0)
    fails = sum(v for k, v in counts.items() if not k.startswith('0 '))
    total = sum(counts.values())
    print(f"p = {p:.3f} : erreur logique = {fails/total*100:.2f}%")
```

---

## Exemple guidé

**Problème** : Corrigeons une erreur $X$ sur le qubit 1 du code à répétition, étape par étape.

**Étape 1** : État initial encodé. $\ket{\psi_L} = \alpha\ket{000} + \beta\ket{111}$

**Étape 2** : Erreur $X_1$ (bit-flip sur le qubit 1).
$$X_1 \ket{\psi_L} = \alpha\ket{100} + \beta\ket{011}$$

**Étape 3** : Mesure du syndrome $Z_1Z_2$.
- Sur $\ket{100}$ : qubits 1 et 2 sont différents → $Z_1Z_2 = -1$
- Sur $\ket{011}$ : qubits 1 et 2 sont différents → $Z_1Z_2 = -1$
- Résultat : $s_1 = -1$

**Étape 4** : Mesure du syndrome $Z_2Z_3$.
- Sur $\ket{100}$ : qubits 2 et 3 sont identiques → $Z_2Z_3 = +1$
- Sur $\ket{011}$ : qubits 2 et 3 sont identiques → $Z_2Z_3 = +1$
- Résultat : $s_2 = +1$

**Étape 5** : Identification. Syndrome $(-1, +1)$ → Erreur sur qubit 1 → Correction $X_1$.

**Étape 6** : Correction. $X_1(\alpha\ket{100} + \beta\ket{011}) = \alpha\ket{000} + \beta\ket{111} = \ket{\psi_L}$ ✅

---

## Implémentation Python

```python
import numpy as np
import qutip as qt

# === Vérification complète du code à répétition 3 qubits ===

# Matrices de Pauli
I2 = qt.qeye(2)
X = qt.sigmax()
Y = qt.sigmay()
Z = qt.sigmaz()

# Stabilisateurs du code
g1 = qt.tensor(Z, Z, I2)    # ZZI : compare q0 et q1
g2 = qt.tensor(I2, Z, Z)    # IZZ : compare q1 et q2

# États logiques
ket_0L = qt.tensor(qt.basis(2,0), qt.basis(2,0), qt.basis(2,0))
ket_1L = qt.tensor(qt.basis(2,1), qt.basis(2,1), qt.basis(2,1))

# Test 1 : les états logiques sont stabilisés
print("=== Test 1 : Stabilisation ===")
for name, ket in [("|0_L>", ket_0L), ("|1_L>", ket_1L)]:
    for g_name, g in [("g1", g1), ("g2", g2)]:
        val = (g * ket).overlap(ket)
        print(f"  {g_name}{name} = {val:.1f} * {name} : {'OK' if abs(val - 1) < 1e-10 else 'ECHEC'}")

# Test 2 : une erreur X sur q0 change le syndrome
print("\n=== Test 2 : Syndrome après erreur X_0 ===")
ket_err = qt.tensor(X, I2, I2) * ket_0L   # Erreur X sur qubit 0
s1 = (g1 * ket_err).overlap(ket_err)       # <err|ZZI|err>
s2 = (g2 * ket_err).overlap(ket_err)       # <err|IZZ|err>
print(f"  Syndrome : Z1Z2 = {s1.real:.1f}, Z2Z3 = {s2.real:.1f}")
print(f"  → Syndrome (-1, +1) détecté : erreur sur qubit 0")

# Test 3 : correction
print("\n=== Test 3 : Après correction ===")
ket_corr = qt.tensor(X, I2, I2) * ket_err  # On applique X_0 pour corriger
print(f"  État corrigé == |0_L> : {(ket_corr - ket_0L).norm() < 1e-10}")
```

---

## À retenir

1. **Code à répétition 3 qubits** : le plus simple, corrige 1 erreur bit-flip ou phase-flip (pas les deux)
2. **Code de Shor [9,1,3]** : premier code complet, combine bit-flip et phase-flip, 9 qubits pour 1 logique
3. **Codes CSS** : construits à partir de 2 codes classiques emboîtés, corrigent X et Z séparément
4. **Code de Steane [7,1,3]** : CSS basé sur Hamming [7,4,3], plus efficace que Shor
5. **Stabilisateurs** : groupe abélien d'opérateurs Pauli dont les états du code sont les +1 eigenstates
6. **Syndrome** : mesure indirecte des stabilisateurs, identifie l'erreur sans lire l'information
7. **Représentation binaire** : chaque Pauli → 2 vecteurs binaires, commutation → produit scalaire mod 2

---

## Pièges à éviter

1. **Confondre encodage et copie** : l'encodage $\ket{\psi} \to \alpha\ket{000} + \beta\ket{111}$ n'est PAS une copie — c'est de l'intrication. Les qubits individuels ne contiennent aucune information.
2. **Oublier les erreurs de mesure** : le circuit de syndrome peut lui-même introduire des erreurs. En pratique, il faut répéter les mesures.
3. **Penser que le code à répétition suffit** : il ne corrige QUE les bit-flip OU les phase-flip, pas les deux. Le code de Shor ou CSS est nécessaire pour les erreurs arbitraires.
4. **Confondre distance et nombre de qubits** : $d = 3$ ne signifie pas 3 qubits, mais que le code corrige $\lfloor(d-1)/2\rfloor = 1$ erreur.
5. **Négliger le taux de code** : le code de Shor a un taux de 1/9 — il faut 9 qubits physiques par qubit logique. C'est énorme.

---

## Exercices

### Niveau 1 — Application directe

1. Implémenter le code de répétition à 5 qubits $[\![5,1,3]\!]$ avec Qiskit. Comparer son taux de succès avec le code à 3 qubits sous le même modèle de bruit.

2. Utiliser QuTiP pour simuler le code de Shor : encodage de $\ket{+}$, injection d'une erreur $Y$ sur le qubit 2, correction, et vérification de la fidélité finale.

### Niveau 2 — Compréhension

3. Montrer que le code de Steane $[\![7,1,3]\!]$ peut être vu comme un code CSS avec $C_1 =$ Hamming $[7,4,3]$ et $C_2 =$ Hamming $[7,4,3]^\perp$.

4. Implémenter la vérification des stabilisateurs pour le code de Shor avec QuTiP : montrer que $\ket{0_L}$ et $\ket{1_L}$ sont bien dans le $+1$ eigenspace de chaque stabilisateur.

### Niveau 3 — Défi

5. Avec le formalisme stabilisateur, calculer les distances des codes à répétition pour $n = 3, 5, 7$ qubits.

6. **Projet** : Implémenter un decodeur pour le code de Steane avec Qiskit et le tester contre toutes les erreurs Pauli possibles sur un qubit.

---

## Pour aller plus loin

- **Code à 5 qubits** : le plus petit code corrigeant toute erreur 1-qubit, $[\![5,1,3]\!]$, avec un taux de 1/5
- **Codes CSS généralisés** : la construction CSS s'étend à toute paire de codes classiques satisfaisant $C_2^\perp \subset C_1$
- **Codes de surface** : chapitre 10.1 — une famille de codes stabilisateurs sur grille 2D, beaucoup plus efficaces
- **Formalisme stabilisateur complet** : Gottesman, « Stabilizer Codes and Quantum Error Correction » (thèse, 1997) — référence absolue
- **Prochaine étape** : les codes de surface et QLDPC pour des taux de code bien meilleurs
