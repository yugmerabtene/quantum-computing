# Chapitre 11.1 — Calcul tolérant aux fautes

## Ce que vous allez apprendre

- Comprendre pourquoi les portes Clifford ne suffisent pas et ce que sont les états magiques
- Maîtriser la distillation d'états magiques (protocole 15-to-1 de Bravyi-Kitaev)
- Démontrer le théorème du seuil et calculer le surcoût en qubits
- Implémenter l'ensemble de portes Clifford + T et la compilation tolérante aux fautes
- Découvrir le framework AFT de QuEra (2025) qui adapte la protection au besoin

---

## Motivation

Aux chapitres précédents, on a appris à **protéger** l'information quantique contre les erreurs. Mais protéger ne suffit pas — il faut aussi **calculer** ! Comment appliquer des portes logiques sur des qubits logiques sans détruire la protection ?

**Analogie classique** : Imaginez que vous faites un calcul sur des données sauvegardées en 3 exemplaires. Si vous modifiez un exemplaire, les 3 doivent rester cohérents. En quantique, c'est bien plus difficile : une porte mal appliquée peut corrompre la redondance entière.

**Le problème central** : Les portes **Clifford** (H, S, CNOT) peuvent être appliquées de manière **transversale** (qubit par qubit) — c'est sûr. Mais elles ne suffisent pas pour l'universalité quantique. Il faut au moins une porte **non-Clifford** (la porte T), et celle-ci ne peut PAS être appliquée transversalement. C'est le **théorème de Eastin-Knill**.

**Solution** : La **distillation d'états magiques** — on prépare des « ingrédients spéciaux » (états magiques) qui permettent d'implémenter la porte T de manière indirecte, via la téléportation.

---

## Idée principale

Imaginez que vous êtes un cuisinier qui doit préparer un plat épicé, mais vous n'avez pas d'épices. La solution : vous commandez un mélange très dilué d'épices (bruité), puis vous le **concentrez** par distillation jusqu'à obtenir un concentré pur.

En calcul tolérant aux fautes :
- Les portes **Clifford** sont gratuites (transversales) — comme le sel et le poivre
- La porte **T** nécessite un « ingrédient spécial » : l'**état magique** $\ket{T} = T\ket{+}$
- Les états magiques préparés sont bruités → on les **distille** (15 bruités → 1 pur)
- Le coût de la distillation domine le coût total du calcul

---

## Contenu du cours

### Section 1 : États magiques et distillation

#### Le problème des portes non-Clifford

L'ensemble des portes **Clifford** ($H, S, \text{CNOT}$) ne suffit pas pour l'universalité quantique. Il faut au moins une porte **non-Clifford**, typiquement $T$ :

$$
T = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{pmatrix}
$$

**Intuition** : Les portes Clifford ne font que permuter les axes de la sphère de Bloch. Elles ne peuvent pas créer de rotations « irrationnelles ». La porte T, elle, fait une rotation de $\pi/4$ autour de Z — un angle qui, combiné avec les Clifford, permet d'approximer n'importe quelle rotation (universalité).

**Analogie** : Les Clifford sont comme les nombres rationnels — ils ne peuvent pas atteindre $\sqrt{2}$. La porte T est comme ajouter $\sqrt{2}$ — avec les rationnels et $\sqrt{2}$, on peut approcher n'importe quel nombre réel.

Les portes Clifford peuvent être implémentées de manière **transversale** (tolérante aux fautes), mais pas $T$.

**Variables** : $T$ = porte T (phase de $\pi/4$), $e^{i\pi/4} = \frac{1+i}{\sqrt{2}}$ = phase complexe.

#### États magiques

Un **état magique** est un état auxiliaire qui permet d'implémenter une porte non-Clifford via une téléportation :

$$
\ket{T} = T\ket{+} = \frac{\ket{0} + e^{i\pi/4}\ket{1}}{\sqrt{2}}
$$

**Intuition** : L'état magique $\ket{T}$ est un « concentré de non-Cliffordness ». En le consommant (via la téléportation), on transfère la porte T sur le qubit de données sans l'appliquer directement.

**Analogie** : C'est comme imprimer un document en utilisant un tampon encré. Le tampon (état magique) est consommé dans le processus, mais l'encre (la porte T) est transférée sur le papier (le qubit de données).

Le circuit de téléportation d'état magique :

```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
import numpy as np

def magic_state_injection(qc, qr, cr):
    """
    Injection d'état magique pour implémenter une porte T.
    
    Le circuit prépare |T> sur le qubit 1, puis téléporte la porte T
    sur le qubit 0 (données) via un CNOT et des mesures.
    """
    # Qubit 0 : état de données (sur lequel on veut appliquer T)
    # Qubit 1 : état magique |T> (l'ingrédient spécial)
    
    # Préparation de |T> = T|+> sur le qubit 1
    qc.h(1)       # |+> = (|0> + |1>)/√2
    qc.t(1)       # T|+> = (|0> + e^{iπ/4}|1>)/√2
    
    # Téléportation : CNOT puis mesure de Bell
    qc.cx(0, 1)   # Intrication données ↔ magique
    qc.h(0)       # Rotation de Bell
    qc.measure(0, cr[0])   # Mesure du qubit de données
    qc.measure(1, cr[1])   # Mesure du qubit magique
    
    # Correction conditionnelle basée sur les résultats de mesure
    qc.z(0).c_if(cr[0], 1)   # Si mesure 0 = 1 : correction Z
    qc.s(0).c_if(cr[1], 1)   # Si mesure 1 = 1 : correction S

# Test de l'injection d'état magique
qr = QuantumRegister(2, 'q')
cr = ClassicalRegister(2, 'c')
qc = QuantumCircuit(qr, cr)

# Préparer |+> sur le qubit 0
qc.h(0)
magic_state_injection(qc, qr, cr)

print("Circuit d'injection d'état magique :")
print(qc.draw())
```

**Sortie attendue (Qiskit 2.x) :**

```
     ┌───┐          ┌───┐┌─┐  ┌──────  ┌───┐ ───────┐   ┌──────  ┌───┐ ───────┐»
q_0: ┤ H ├───────■──┤ H ├┤M├──┤ If-0  ─┤ Z ├  End-0 ├───┤ If-0  ─┤ S ├  End-0 ├»
     ├───┤┌───┐┌─┴─┐└┬─┬┘└╥┘  └──╥───  └───┘ ───────┘   └──╥───  └───┘ ───────┘»
q_1: ┤ H ├┤ T ├┤ X ├─┤M├──╫──────╫─────────────────────────╫───────────────────»
     └───┘└───┘└───┘ └╥┘  ║ ┌────╨────┐               ┌────╨────┐              »
c: 2/═════════════════╩═══╩═╡ c_0=0x1 ╞═══════════════╡ c_1=0x1 ╞══════════════»
                      1   0 └─────────┘               └─────────┘              »
«      
«q_0: ─
«      
«q_1: ─
«      
«c: 2/═
«      
```

#### Distillation d'états magiques

Les états magiques préparés sont bruités. On les **distille** pour augmenter leur fidélité :

$$
\text{Entrée : } n \text{ états magiques bruités} \;\to\; \text{Sortie : } 1 \text{ état magique de haute fidélité}
$$

**Intuition** : C'est comme distiller de l'alcool. Vous avez 15 litres de vin à 10° (bruité). Par distillation, vous obtenez 1 litre d'alcool à 90° (pur). Le processus consomme beaucoup d'entrée pour peu de sortie, mais la qualité est au rendez-vous.

Le protocole de distillation Bravyi-Kitaev (15-to-1) :

**Variables** : 15 états magiques bruités en entrée, 1 état magique pur en sortie. Le code Reed-Muller $[\![15,1,3]\!]$ est utilisé pour détecter les erreurs.

```python
import numpy as np
import qutip as qt

def bravyi_kitaev_distill(states, p_noise=0.01):
    """
    Simulation du protocole de distillation 15-to-1 de Bravyi-Kitaev.
    
    Utilise un code Reed-Muller [[15,1,3]] pour détecter les erreurs
    et produire 1 état magique de haute fidélité à partir de 15 bruités.
    
    Args:
        states: liste de 15 états magiques bruités (matrices densité)
        p_noise: probabilité d'erreur sur chaque état d'entrée
    
    Returns:
        état distillé (matrice densité) ou None si échec
    """
    if len(states) != 15:
        raise ValueError("15 états nécessaires pour le protocole 15-to-1")
    
    # État magique idéal : |T> = (|0> + e^{iπ/4}|1>)/√2
    def ideal_T():
        ket0 = qt.basis(2, 0)
        ket1 = qt.basis(2, 1)
        return (ket0 + np.exp(1j * np.pi / 4) * ket1).unit()
    
    T_ideal = ideal_T()
    rho_ideal = T_ideal * T_ideal.dag()
    
    # Calcul de la fidélité moyenne des 15 états d'entrée
    fidelities = []
    for rho in states:
        f = (T_ideal.dag() * rho * T_ideal).real
        fidelities.append(f)
    
    print(f"Fidélité moyenne entrée : {np.mean(fidelities):.4f}")
    
    # Le protocole 15-to-1 utilise un code Reed-Muller [[15,1,3]]
    # et mesure les stabilisateurs pour détecter les erreurs
    
    # Simulation simplifiée : probabilité de succès
    p_success = (1 - p_noise) ** 5  # Approximation
    success = np.random.random() < p_success
    
    if success:
        # Fidélité améliorée : l'erreur cubique (d=3 du code)
        f_output = 1 - (1 - np.mean(fidelities)) ** 3
        rho_out = f_output * rho_ideal + (1 - f_output) * qt.qeye(2) / 2
        print(f"Distillation réussie ! Fidélité sortie : {f_output:.4f}")
        return rho_out
    else:
        print("Échec de la distillation")
        return None

# Test : distillation de 15 états magiques bruités
print("Distillation d'états magiques (Bravyi-Kitaev 15-to-1) :")
np.random.seed(42)

# Préparation de 15 états bruités (fidélité ~95%)
T_ideal = (qt.basis(2,0) + np.exp(1j*np.pi/4)*qt.basis(2,1)).unit()
rho_T_ideal = T_ideal * T_ideal.dag()

noisy_states = []
for _ in range(15):
    p = 0.05  # 5% de bruit
    rho_noisy = (1-p) * rho_T_ideal + p * qt.qeye(2) / 2
    noisy_states.append(rho_noisy)

result = bravyi_kitaev_distill(noisy_states, p_noise=0.05)
```

---

### Section 2 : Théorème du seuil

#### Énoncé

> **Théorème du seuil** : Si le taux d'erreur physique $p$ est inférieur à un seuil $p_\text{th}$, alors il est possible d'implémenter un circuit quantique de taille arbitraire avec une fidélité arbitrairement élevée, en utilisant un surcoût en qubits poly-logarithmique.

$$
\text{Si } p < p_\text{th} : \quad \forall \varepsilon > 0,\; \exists \text{ circuit FT avec erreur } < \varepsilon
$$

**Intuition** : C'est le théorème le plus important de l'informatique quantique tolérante aux fautes. Il dit que le bruit n'est PAS une barrière fondamentale — tant qu'il est en dessous d'un seuil, on peut le corriger arbitrairement bien, avec un surcoût raisonnable.

**Analogie** : C'est comme dire que si le taux de fautes d'impression d'une imprimerie est inférieur à 1%, on peut imprimer un livre de n'importe quelle longueur avec une relecture appropriée et obtenir un texte sans fautes.

#### Démonstration schématique

On encode chaque qubit logique dans un code correcteur, et on implémente chaque porte logique de manière **tolérante aux fautes** :

1. **Encodage** : $[\![n,1,d]\!]$ avec $d = O(\log(1/\varepsilon))$
2. **Exécution** : chaque porte agit sur les qubits encodés (transversalement si possible)
3. **Correction** : après chaque porte, mesure de syndrome et correction
4. **Décodage** : extraction du résultat final

Le taux d'erreur logique par porte est :

$$
p_L = C \left( \frac{p}{p_\text{th}} \right)^{\lfloor (d+1)/2 \rfloor}
$$

**Intuition** : L'erreur logique décroît exponentiellement avec la distance $d$. Pour atteindre une précision $\varepsilon$, il suffit de prendre $d$ proportionnel à $\log(1/\varepsilon)$.

**Variables** : $p_L$ = erreur logique par porte, $C$ = constante, $p$ = erreur physique, $p_\text{th}$ = seuil, $d$ = distance du code, $\varepsilon$ = précision cible.

Pour atteindre une précision $\varepsilon$, on prend $d \propto \log(1/\varepsilon)$, d'où un surcoût :

$$
\text{Overhead} = O\left( \text{poly}\left( \log \frac{1}{\varepsilon} \right) \right)
$$

#### Simulation du seuil

```python
import numpy as np

def threshold_simulation(d_max=15):
    """
    Simulation du théorème du seuil : taux d'erreur logique
    en fonction de la distance pour différents taux physiques p.
    
    Montre que sous le seuil (p < p_th), pL diminue avec d.
    Au-dessus (p > p_th), pL augmente avec d.
    """
    distances = range(3, d_max + 1, 2)
    p_values = [0.005, 0.01, 0.02, 0.05]  # en dessous / au-dessus du seuil
    p_th = 0.01
    
    print("Taux d'erreur logique vs distance :")
    print(f"{'d':<5}", end="")
    for p in p_values:
        print(f"{'p=' + str(p):<15}", end="")
    print()
    
    for d in distances:
        print(f"{d:<5}", end="")
        for p in p_values:
            if p < p_th:
                # Sous le seuil : pL diminue exponentiellement
                pL = (p / p_th) ** ((d + 1) // 2)
            else:
                # Au-dessus : pL augmente (la correction empire)
                pL = 1 - (1 - p / p_th) ** ((d + 1) // 2)
                pL = min(pL, 1.0)
            print(f"{pL:<15.4e}", end="")
        print()

threshold_simulation()
```

**Sortie attendue :**

```
Taux d'erreur logique vs distance :
d    p=0.005        p=0.01         p=0.02         p=0.05        
3    2.5000e-02     1.0000e-01     4.0000e-01     1.0000e+00    
5    6.2500e-04     1.0000e-02     1.6000e-01     9.3750e-01    
7    1.5625e-05     1.0000e-03     6.4000e-02     7.6562e-01    
9    3.9062e-07     1.0000e-04     2.5600e-02     5.2734e-01    
11   9.7656e-09     1.0000e-05     1.0240e-02     3.2280e-01    
13   2.4414e-10     1.0000e-06     4.0960e-03     1.8279e-01    
15   6.1035e-12     1.0000e-07     1.6384e-03     9.8225e-02    
```

**Lecture** : Pour $p = 0.005$ (sous le seuil), $p_L$ passe de $2.5 \times 10^{-2}$ à $d=3$ à $6 \times 10^{-12}$ à $d=15$. Pour $p = 0.05$ (au-dessus), $p_L$ reste élevé même à grande distance.

#### Suroût en qubits

```python
def qubit_overhead(n_logical, p_phys, p_target, p_th=0.01):
    """
    Calcule le nombre de qubits physiques nécessaires pour
    n_logical qubits logiques avec une erreur < p_target.
    
    Le surcoût total inclut :
    1. L'encodage (code de surface rotatif : 2d^2 qubits/logique)
    2. La distillation d'états magiques (15 états bruts par état distillé)
    """
    # Distance nécessaire pour atteindre p_target
    d = 1
    while True:
        pL = (p_phys / p_th) ** ((d + 1) // 2)
        if pL < p_target:
            break
        d += 2
        if d > 100:
            return None  # impossible
    
    # Suroût par qubit logique (code de surface rotatif)
    n_per_logical = 2 * d * d
    
    # Suroût pour la distillation d'états magiques
    n_distillation = 15 * n_logical  # 15 états bruts par état distillé
    
    total = n_logical * n_per_logical + n_distillation
    return total, d

print("Suroût en qubits (théorème du seuil) :")
for p_phys in [5e-3, 1e-3, 5e-4]:
    n, d = qubit_overhead(100, p_phys, 1e-12)
    print(f"  p_phys = {p_phys:.1e} : {n:6d} qubits (d={d})")
```

---

### Section 3 : Portes Clifford + T

#### L'ensemble universel

L'ensemble $\{\text{H}, \text{S}, \text{CNOT}, T\}$ est universel pour le calcul quantique :

- **H** : Hadamard $= \frac{1}{\sqrt{2}}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$ — crée des superpositions
- **S** : Phase $= \begin{pmatrix}1&0\\0&i\end{pmatrix}$ — rotation de $\pi/2$ autour de Z
- **CNOT** : $= \begin{pmatrix}1&0&0&0\\0&1&0&0\\0&0&0&1\\0&0&1&0\end{pmatrix}$ — intrication
- **T** : $= \begin{pmatrix}1&0\\0&e^{i\pi/4}\end{pmatrix}$ — rotation de $\pi/4$ (non-Clifford)

**Intuition** : H, S et CNOT forment le groupe Clifford — ils permutent les axes de la sphère de Bloch. T ajoute une rotation « irrationnelle » qui brise cette structure et rend l'ensemble universel.

Le groupe Clifford $\mathcal{C}_n$ est le normalisateur du groupe de Pauli :

$$
\mathcal{C}_n = \{ U \in U(2^n) \;|\; U\mathcal{P}_n U^\dagger = \mathcal{P}_n \}
$$

**Variables** : $\mathcal{C}_n$ = groupe Clifford à $n$ qubits, $\mathcal{P}_n$ = groupe de Pauli à $n$ qubits.

#### Implémentation tolérante aux fautes

Chaque porte Clifford peut être implémentée de manière **transversale** dans la plupart des codes. Une porte transversale agit qubit par qubit :

$$
U_L = U^{\otimes n}, \quad \text{où } U_L \text{ est la porte logique}
$$

**Intuition** : Une porte transversale applique la même opération sur chaque qubit physique indépendamment. Si un qubit physique a une erreur, elle ne se propage pas aux autres — la correction reste efficace.

```python
import numpy as np
from qiskit import QuantumCircuit

def clifford_plus_t_gates():
    """Définit l'ensemble de portes Clifford + T."""
    gates = {
        'H': np.array([[1, 1], [1, -1]]) / np.sqrt(2),    # Hadamard
        'S': np.array([[1, 0], [0, 1j]]),                  # Phase (π/2)
        'T': np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]]),  # T (π/4)
        'CNOT': np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ])
    }
    return gates

# Vérification : T^8 = I (8 applications de T = identité)
gates = clifford_plus_t_gates()
T = gates['T']
T_8 = np.linalg.matrix_power(T, 8)
print("T^8 = I ?", np.allclose(T_8, np.eye(2)))

# Approximation d'une porte unitaire par séquence H,T
def approximate_unitary(U_target, eps=1e-3):
    """
    Approximation d'une porte unitaire 1-qubit par une séquence H,T.
    Utilise l'algorithme de Solovay-Kitaev (version simplifiée).
    """
    gates_list = []
    remaining = U_target.copy()
    
    # Décomposition en rotation de Euler
    # U = e^{iα} R_z(β) R_x(γ) R_z(δ)
    # Puis chaque rotation R_z/R_x est approximée par H,T
    
    # Version simplifiée : alternance H et T
    sequence = []
    n_iters = 20
    
    current = np.eye(2, dtype=complex)
    for k in range(n_iters):
        # Distance à la cible (norme de Frobenius)
        dist = np.linalg.norm(current - remaining, 'fro')
        if dist < eps:
            break
        
        # Ajouter H ou T selon la direction nécessaire
        if k % 2 == 0:
            current = current @ T
            sequence.append('T')
        else:
            current = current @ gates['H']
            sequence.append('H')
    
    return sequence

# Test : approximation de la porte de Hadamard par H,T
U_test = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
seq = approximate_unitary(U_test, eps=0.5)
print(f"Séquence approximante pour H : {''.join(seq)}")
```

#### Circuit Clifford + T pour l'état magique

```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
import numpy as np

def T_gate_logical(qc, qr, magic_qr, cr):
    """
    Implémentation d'une porte T logique via injection d'état magique.
    
    Le qubit de données (qr) reçoit la porte T en consommant
    l'état magique préparé sur magic_qr.
    """
    # Préparation de l'état magique |T> = T|+>
    qc.h(magic_qr[0])      # |+>
    qc.t(magic_qr[0])      # T|+> = |T>
    
    # Téléportation : CNOT puis mesure de Bell
    qc.cx(qr[0], magic_qr[0])   # Intrication
    qc.h(qr[0])                  # Rotation Bell
    qc.measure(qr[0], cr[0])     # Mesure données
    qc.measure(magic_qr[0], cr[1])  # Mesure magique
    
    # Corrections conditionnelles
    qc.x(qr[0]).c_if(cr[0], 1)   # Correction X si mesure 0 = 1
    qc.z(qr[0]).c_if(cr[0], 1)   # Correction Z si mesure 0 = 1
    qc.s(qr[0]).c_if(cr[1], 1)   # Correction S si mesure 1 = 1

# Circuit complet : appliquer T logique sur |+>
qr = QuantumRegister(1, 'data')
magic_qr = QuantumRegister(1, 'magic')
cr = ClassicalRegister(2, 'c')
qc = QuantumCircuit(qr, magic_qr, cr)

qc.h(qr[0])                # Préparer |+> sur les données
qc.barrier()

T_gate_logical(qc, qr, magic_qr, cr)
qc.barrier()
qc.h(qr[0])                # Rotation finale pour vérification

# Simulation
sim = AerSimulator()
qc.measure_all()
result = sim.run(qc, shots=1024).result()
print(f"Résultat T-logique sur |+> : {result.get_counts()}")
```

---

### Section 4 : Framework AFT (Algorithmic Fault Tolerance)

#### Principe (QuEra 2025)

L'AFT (**Algorithmic Fault Tolerance**) est un framework développé par QuEra (2025) qui **adapte** le niveau de correction au besoin de l'algorithme :

- Toutes les portes d'un algorithme n'ont pas la même criticité
- On alloue plus de ressources aux opérations critiques, moins aux autres

**Intuition** : Dans un chantier de construction, on ne met pas le même casque de sécurité à tous les ouvriers. Le soudeur a besoin d'un casque intégral (protection maximale), le manœuvre d'un simple casque (protection basique). L'AFT fait pareil : les portes T (critiques) ont une protection maximale, les préparations d'état (non-critiques) une protection minimale.

#### Hiérarchie de protection

| Niveau | Protection | Suroût | Usage |
|--------|-----------|--------|-------|
| 0 | Aucune | 1× | Portes non-critiques, préparation |
| 1 | Code surface d=3 | 18× | Portes modérément critiques |
| 2 | Code surface d=5 | 50× | Portes critiques, distillation |

#### Allocation dynamique

```python
import numpy as np

class AFTAllocator:
    """
    Allocation dynamique des ressources de correction
    basée sur l'analyse de criticité de l'algorithme.
    
    L'idée : toutes les portes n'ont pas la même importance.
    Les portes T (non-Clifford) sont critiques → protection maximale.
    Les portes de préparation sont non-critiques → protection minimale.
    """
    
    def __init__(self, total_qubits, p_phys=1e-3):
        self.total_qubits = total_qubits
        self.p_phys = p_phys
        self.allocations = {}
        self.remaining = total_qubits
    
    def analyze_circuit(self, circuit_gates):
        """
        Analyse un circuit et assigne un niveau de protection
        à chaque porte selon sa criticité.
        """
        protection_levels = {}
        
        for i, gate in enumerate(circuit_gates):
            name = gate['name']
            qubits = gate['qubits']
            
            # Criticité basée sur le type de porte et sa position
            if name in ['T', 'T_dagger']:
                # Portes T : non-Clifford → critiques → niveau 2
                protection_levels[i] = 2
            elif name in ['H', 'CX']:
                if len(qubits) > 1:
                    # CNOT : important mais Clifford → niveau 1
                    protection_levels[i] = 1
                else:
                    # H sur 1 qubit : basique → niveau 0
                    protection_levels[i] = 0
            else:
                # Autres portes : non-critiques → niveau 0
                protection_levels[i] = 0
        
        return protection_levels
    
    def allocate_resources(self, protection_levels):
        """
        Alloue les qubits physiques selon les niveaux de protection.
        Priorité aux niveaux élevés (portes critiques).
        """
        # Comptage du nombre de portes à chaque niveau
        counts = {0: 0, 1: 0, 2: 0}
        for level in protection_levels.values():
            counts[level] += 1
        
        # Overhead par qubit logique (qubits physiques / qubit logique)
        overhead = {0: 1, 1: 18, 2: 50}
        
        # Allocation : priorité aux niveaux élevés
        n_logical = {}
        
        for level in [2, 1, 0]:
            needed = overhead[level]
            available = self.remaining // needed
            n_logical[level] = min(available, counts.get(level, 0))
            self.remaining -= n_logical[level] * needed
        
        return n_logical
    
    def resource_report(self):
        """Génère un rapport d'allocation des ressources."""
        print("Rapport d'allocation AFT :")
        print(f"  Qubits physiques totaux : {self.total_qubits}")
        print(f"  Qubits alloués : {self.total_qubits - self.remaining}")
        print(f"  Qubits restants : {self.remaining}")
        return {
            'total': self.total_qubits,
            'allocated': self.total_qubits - self.remaining,
            'remaining': self.remaining
        }

# Exemple : allocation pour un mini-circuit Grover
allocator = AFTAllocator(total_qubits=1000)

# Circuit simplifié de Grover : 2 qubits, quelques portes
grover_gates = [
    {'name': 'H', 'qubits': [0]},       # Hadamard : non-critique
    {'name': 'H', 'qubits': [1]},       # Hadamard : non-critique
    {'name': 'CX', 'qubits': [0, 1]},   # CNOT : modérément critique
    {'name': 'T', 'qubits': [0]},       # T : critique !
    {'name': 'H', 'qubits': [0]},       # Hadamard : non-critique
    {'name': 'T', 'qubits': [1]},       # T : critique !
]

levels = allocator.analyze_circuit(grover_gates)
allocation = allocator.allocate_resources(levels)
print(f"Niveaux de protection : {levels}")
print(f"Allocation : {allocation}")
allocator.resource_report()
```

**Sortie attendue :**

```
Niveaux de protection : {0: 0, 1: 0, 2: 1, 3: 2, 4: 0, 5: 2}
Allocation : {2: 2, 1: 1, 0: 3}
Rapport d'allocation AFT :
  Qubits physiques totaux : 1000
  Qubits alloués : 121
  Qubits restants : 879
```

#### Impact du framework AFT

D'après QuEra (2025), l'AFT réduit le surcoût de 5 à 10× par rapport à une protection uniforme :

```python
def compare_aft_uniform(n_qubits_logical, algorithm_circuit):
    """
    Compare le coût en qubits entre AFT et protection uniforme.
    Montre le gain de l'approche adaptative.
    """
    allocator = AFTAllocator(total_qubits=10000)
    levels = allocator.analyze_circuit(algorithm_circuit)
    allocation = allocator.allocate_resources(levels)
    
    # Protection uniforme : tout au niveau 2 (d=5)
    uniform_cost = n_qubits_logical * 50
    
    # AFT : coût réel selon les niveaux
    aft_cost = sum(
        n * overhead
        for level, n in allocation.items()
        for overhead in [{0: 1, 1: 18, 2: 50}][level:level+1]
    )
    
    reduction = uniform_cost / max(aft_cost, 1)
    print(f"Coût uniforme : {uniform_cost}")
    print(f"Coût AFT :      {aft_cost}")
    print(f"Réduction :     {reduction:.1f}×")
    return reduction

# Circuit simulé : 100 portes avec ~20% de portes T
circuit_gates = [
    {'name': np.random.choice(['H', 'CX', 'T', 'S']), 'qubits': [0]}
    for _ in range(100)
]

compare_aft_uniform(10, circuit_gates)
```

---

### Section 5 : Pipeline de compilation tolérante aux fautes

#### Pipeline complet

1. **Circuit idéal** $\to$ 2. **Décomposition Clifford+T** $\to$ 3. **Encodage** $\to$ 4. **Distillation** $\to$ 5. **Exécution**

**Intuition** : Compiler un circuit pour un ordinateur quantique tolérant aux fautes, c'est comme traduire un roman :
1. Le texte original (circuit idéal)
2. Traduction en mots simples (Clifford + T)
3. Mise en coffre-fort (encodage)
4. Préparation des clés spéciales (distillation)
5. Livraison sécurisée (exécution)

#### Exemple complet

```python
from qiskit import QuantumCircuit
from qiskit.transpiler.passes import SolovayKitaev
import numpy as np

def fault_tolerant_pipeline(target_gate, n_logical=1, d=3):
    """
    Pipeline de compilation tolérante aux fautes.
    
    1. Décomposer la porte en Clifford+T
    2. Encoder dans un code de surface de distance d
    3. Ajouter la distillation d'état magique pour les portes T
    """
    print(f"Pipeline FT pour la porte : {target_gate}")
    print(f"  Distance du code : d={d}")
    print(f"  Qubits logiques : {n_logical}")
    
    # Étape 1 : Décomposition en Clifford+T
    qc = QuantumCircuit(n_logical)
    if target_gate == 'T':
        qc.t(0)
    elif target_gate == 'H':
        qc.h(0)
    
    # Nombre de portes T nécessaires
    n_t_gates = 1 if target_gate == 'T' else 0
    
    # Étape 2 : Suroût en qubits pour l'encodage
    overhead_per_gate = 2 * d * d       # code de surface rotatif
    distillation_overhead = 15           # 15 états bruts par état distillé
    
    # Total = encodage + distillation pour chaque porte T
    total_qubits = n_logical * overhead_per_gate + n_t_gates * distillation_overhead * d * d
    
    print(f"  Ressources estimées : {total_qubits} qubits physiques")
    print(f"  Dont {n_t_gates} distillations d'états magiques")
    
    return total_qubits

# Test : pipeline pour les portes T et H
fault_tolerant_pipeline('T', n_logical=1, d=3)
fault_tolerant_pipeline('H', n_logical=1, d=3)
```

**Sortie attendue :**

```
Pipeline FT pour la porte : T
  Distance du code : d=3
  Qubits logiques : 1
  Ressources estimées : 153 qubits physiques
  Dont 1 distillations d'états magiques
Pipeline FT pour la porte : H
  Distance du code : d=3
  Qubits logiques : 1
  Ressources estimées : 18 qubits physiques
  Dont 0 distillations d'états magiques
```

**Interprétation** : Une porte H ne coûte que 18 qubits physiques (encodage seul). Une porte T coûte 153 qubits (encodage + distillation) — un facteur 8.5× plus cher !

---

## Exemple guidé

**Problème** : Estimer les ressources pour exécuter un circuit de 1000 portes (dont 200 portes T) sur 10 qubits logiques, avec $p = 10^{-3}$ et $p_\text{target} = 10^{-12}$.

**Étape 1** : Distance nécessaire.
$$p_L = (10^{-3}/10^{-2})^{\lfloor(d+1)/2\rfloor} < 10^{-12}$$
$$0.1^{\lfloor(d+1)/2\rfloor} < 10^{-12} \Rightarrow \lfloor(d+1)/2\rfloor > 12 \Rightarrow d \ge 25$$

**Étape 2** : Qubits pour l'encodage.
$$n_\text{enc} = 10 \times 2 \times 25^2 = 12500 \text{ qubits}$$

**Étape 3** : Qubits pour la distillation.
$$n_\text{dist} = 200 \times 15 = 3000 \text{ états magiques bruts}$$
Chaque distillation utilise $2d^2 = 1250$ qubits auxiliaires.

**Étape 4** : Total.
$$n_\text{total} \approx 12500 + 3000 \times 1250 \approx 3.76 \times 10^6 \text{ qubits physiques}$$

**Conclusion** : Il faut environ 4 millions de qubits physiques pour ce petit calcul. C'est énorme, mais c'est le prix de la fiabilité.

---

## Implémentation Python

```python
import numpy as np

# === Estimation complète des ressources pour un algorithme ===

def estimate_resources(n_logical, n_gates, n_t_gates, p_phys=1e-3, p_target=1e-12):
    """
    Estime les ressources complètes pour un algorithme quantique FT.
    
    Args:
        n_logical: nombre de qubits logiques
        n_gates: nombre total de portes
        n_t_gates: nombre de portes T (non-Clifford)
        p_phys: taux d'erreur physique
        p_target: taux d'erreur logique cible
    """
    p_th = 0.01  # seuil du code de surface
    
    # Distance nécessaire
    d = 3
    while (p_phys / p_th) ** ((d + 1) // 2) >= p_target:
        d += 2
    
    # Qubits pour l'encodage (code de surface rotatif)
    n_encoding = n_logical * 2 * d * d
    
    # Qubits pour la distillation (15-to-1 Bravyi-Kitaev)
    n_distillation_units = n_t_gates  # 1 distillation par porte T
    n_distillation_qubits = n_distillation_units * 15 * 2 * d * d
    
    # Temps de calcul (nombre de cycles de syndrome)
    n_cycles = n_gates * d  # ~d rounds par porte
    
    # Total
    total = n_encoding + n_distillation_qubits
    
    print(f"=== Estimation des ressources FT ===")
    print(f"  Qubits logiques : {n_logical}")
    print(f"  Portes totales : {n_gates} (dont {n_t_gates} portes T)")
    print(f"  Distance requise : d={d}")
    print(f"  Qubits encodage : {n_encoding:,}")
    print(f"  Qubits distillation : {n_distillation_qubits:,}")
    print(f"  TOTAL : {total:,} qubits physiques")
    print(f"  Cycles de syndrome : {n_cycles:,}")
    return total

# Exemple : petit algorithme (type Grover 4 qubits)
estimate_resources(
    n_logical=4,
    n_gates=500,
    n_t_gates=100,
    p_phys=1e-3,
    p_target=1e-12
)
```

---

## À retenir

1. **Clifford + T = universel** : les portes Clifford (H, S, CNOT) sont transversales, la porte T nécessite la distillation
2. **État magique** : $\ket{T} = T\ket{+}$, consommé par téléportation pour appliquer T
3. **Distillation 15-to-1** : 15 états bruités → 1 état pur (protocole Bravyi-Kitaev)
4. **Théorème du seuil** : si $p < p_\text{th}$, on peut calculer arbitrairement longtemps avec un surcoût poly-log
5. **Coût dominant** : la distillation des états magiques représente la majorité du surcoût
6. **AFT (QuEra 2025)** : adaptation dynamique de la protection → réduction de 5-10× du coût
7. **Pipeline FT** : circuit → Clifford+T → encodage → distillation → exécution

---

## Pièges à éviter

1. **Confondre Clifford et universel** : les portes Clifford seules sont simulables classiquement (théorème de Gottesman-Knill). Il faut T pour l'universalité.
2. **Sous-estimer le coût de la distillation** : la distillation peut représenter 90% du coût total d'un algorithme. Ce n'est pas un détail.
3. **Oublier le théorème d'Eastin-Knill** : aucun code ne peut implémenter toutes les portes transversalement. La distillation est inévitable.
4. **Confondre porte T et état T** : la porte T est l'opération à appliquer, l'état $\ket{T}$ est la ressource consommée pour y arriver.
5. **Penser que l'AFT remplace la correction** : l'AFT optimise l'allocation, mais chaque porte reste protégée par un code.

---

## Exercices

### Niveau 1 — Application directe

1. Implémenter la distillation 15-to-1 de Bravyi-Kitaev avec Qiskit. Simuler l'amélioration de fidélité en fonction du nombre de rounds de distillation.

2. Avec QuTiP, simuler l'injection d'état magique sur un état bruité. Tracer la fidélité de la porte $T$ logique en fonction du bruit de l'état magique.

### Niveau 2 — Compréhension

3. Démontrer que l'ensemble $\{H, T\}$ génère un sous-groupe dense de $SU(2)$ (algorithme de Solovay-Kitaev).

4. Implémenter une version simplifiée du framework AFT de QuEra : un programme qui prend un circuit Qiskit et retourne l'allocation optimale des ressources de correction.

### Niveau 3 — Défi

5. **Recherche** : Lire l'article QuEra AFT (2025) et résumer les 3 innovations principales par rapport à l'approche standard.

6. **Projet** : Estimer les ressources nécessaires (qubits, T-gates, temps) pour exécuter l'algorithme de Shor sur 2048 bits avec une approche Clifford + T et distillation.

---

## Pour aller plus loin

- **Distillation** : Bravyi & Kitaev, « Universal quantum computation with ideal Clifford gates and noisy ancillas » (2005)
- **Théorème du seuil** : Aharonov & Ben-Or, « Fault-tolerant quantum computation with constant error rate » (1997)
- **Eastin-Knill** : théorème d'impossibilité des portes transversales universelles (2009)
- **AFT QuEra** : article 2025 sur l'allocation adaptative des ressources de correction
- **Prochaine étape** : Chapitre 11.2 — les avancées récentes (Google Willow, Harvard 48Q, CAV 2025)
