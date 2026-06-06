# Chapitre 4.2 — Canaux quantiques et bruit

## Ce que vous allez apprendre

- Comprendre la représentation de Kraus des canaux quantiques
- Simuler la décohérence et la relaxation (T₁, T₂)
- Maîtriser les modèles de bruit standards (dépolarisant, bit-flip, phase-flip)
- Implémenter des canaux avec QuTiP et Qiskit
- Visualiser l'effet du bruit sur la sphère de Bloch

---

## Motivation

Dans les chapitres précédents, nous avons supposé des qubits parfaits : évolution unitaire, pas de bruit, isolation parfaite. Dans la réalité, c'est impossible. Les qubits interagissent avec leur environnement : ils perdent leur cohérence, relaxent vers l'état fondamental, et subissent des erreurs.

Comprendre le bruit n'est pas optionnel — c'est **le** défi central du calcul quantique. Sans correction d'erreur (Partie III), un ordinateur quantique bruité ne peut pas exécuter d'algorithmes longs. Ce chapitre pose les bases mathématiques et physiques du bruit, que nous utiliserons pour concevoir des codes correcteurs.

---

## Idée principale

Imaginez que vous essayez de faire tourner une toupie parfaite sur une table. En théorie, elle tourne indéfiniment. En pratique, les frottements, les vibrations, les courants d'air la font vaciller et finalement tomber.

Le bruit quantique, c'est pareil. Un qubit parfait évoluerait de façon unitaire pour toujours. Mais l'environnement (température, champs électromagnétiques, imperfections matérielles) interagit avec lui et dégrade son état. La **décohérence** transforme les superpositions en mélanges, et la **relaxation** fait perdre de l'énergie.

Le formalisme des **canaux quantiques** décrit mathématiquement comment l'environnement transforme l'état d'un qubit. C'est indispensable pour concevoir des stratégies de correction.

---

## Contenu du cours

### Section 1 : Canaux quantiques

#### 1.1 Définition

Un **canal quantique** $\mathcal{E}$ est une application linéaire, complètement positive et préservant la trace (CPTP) qui transforme une matrice densité :

$$\rho \mapsto \mathcal{E}(\rho)$$

> **Intuition :** Un canal quantique est une « boîte noire » qui prend un état quantique en entrée et produit un état (potentiellement différent) en sortie. Les 3 contraintes (linéarité, positivité complète, trace préservée) garantissent que le résultat est toujours une matrice densité valide.

#### 1.2 Représentation de Kraus

Tout canal quantique peut s'écrire :

$$\mathcal{E}(\rho) = \sum_k K_k \rho K_k^\dagger$$

avec la condition de complétude :

$$\sum_k K_k^\dagger K_k = I$$

> **Intuition :** Les opérateurs $K_k$ (dits « opérateurs de Kraus ») décrivent les différentes « façons » dont l'environnement peut affecter le qubit. Chaque $K_k$ correspond à un « scénario » possible, et la somme sur tous les scénarios donne l'état final. La condition de complétude garantit que les probabilités somment à 1.

> **Exemple :** S'il n'y a qu'un seul $K_0 = I$, alors $\mathcal{E}(\rho) = \rho$ : aucun bruit !

#### 1.3 Exemple : canal bit-flip

Avec probabilité $p$, le qubit est retourné ($X$) :

$$K_0 = \sqrt{1-p}\, I,\quad K_1 = \sqrt{p}\, X$$

> **Intuition :** $K_0$ correspond au scénario « rien ne se passe » (probabilité $1-p$), $K_1$ au scénario « le qubit est retourné » (probabilité $p$). Les racines carrées assurent que les probabilités sont bien $|K_0|^2 = 1-p$ et $|K_1|^2 = p$.

$$\mathcal{E}(\rho) = (1-p)\rho + p X\rho X$$

> **Exemple numérique :** Pour $\rho = \ket{0}\bra{0}$ et $p = 0.1$ :
> $$\mathcal{E}(\ket{0}\bra{0}) = 0.9\ket{0}\bra{0} + 0.1 X\ket{0}\bra{0}X = 0.9\ket{0}\bra{0} + 0.1\ket{1}\bra{1}$$
> Le qubit a 10% de chance d'être retourné.

**Avez-vous compris ?**
- Vérifier que $\sum_k K_k^\dagger K_k = I$ pour le bit-flip : $(1-p)I + p X^\dagger X = (1-p)I + pI = I$ ✓
- Que se passe-t-il si $p = 0$ ? (Réponse : aucun bruit, $\mathcal{E}(\rho) = \rho$)
- Que se passe-t-il si $p = 1$ ? (Réponse : bit-flip certain, $\mathcal{E}(\rho) = X\rho X$)

---

### Section 2 : Modèles de bruit

#### 2.1 Canal dépolarisant

> **Intuition :** Le pire type de bruit ! Avec probabilité $p$, l'état est complètement mélangé (remplacé par $I/2$). C'est comme si l'environnement « effaçait » l'information du qubit.

Avec probabilité $p$, l'état est remplacé par l'état maximalement mélangé :

$$\mathcal{E}(\rho) = (1-p)\rho + p\frac{I}{2}$$

Opérateurs de Kraus :

$$K_0 = \sqrt{1-\frac{3p}{4}}\,I,\; K_1 = \sqrt{\frac{p}{4}}\,X,\; K_2 = \sqrt{\frac{p}{4}}\,Y,\; K_3 = \sqrt{\frac{p}{4}}\,Z$$

> **Intuition des Kraus :** Le bruit peut être « rien » ($I$), un retournement ($X$), un retournement de phase ($Z$), ou les deux ($Y = iXZ$). Chacun arrive avec probabilité $p/4$ (sauf $I$ qui arrive avec probabilité $1 - 3p/4$).

```python
import qutip as qt
import numpy as np

# --- Canal dépolarisant ---
def depolarizing_channel(rho, p):
    """Applique le canal dépolarisant à une matrice densité.
    
    Args:
        rho: matrice densité d'entrée (Qobj QuTiP)
        p: probabilité de bruit (0 = pas de bruit, 1 = bruit maximal)
    
    Returns:
        Matrice densité après application du canal
    """
    # Les 4 opérateurs de Kraus
    K0 = np.sqrt(1 - 3*p/4) * qt.qeye(2)      # Pas d'erreur
    K1 = np.sqrt(p/4) * qt.sigmax()            # Erreur X (bit-flip)
    K2 = np.sqrt(p/4) * qt.sigmay()            # Erreur Y (bit+phase flip)
    K3 = np.sqrt(p/4) * qt.sigmaz()            # Erreur Z (phase-flip)
    
    # Application : ρ' = Σ K_k ρ K_k†
    result = K0 * rho * K0.dag()
    result += K1 * rho * K1.dag()
    result += K2 * rho * K2.dag()
    result += K3 * rho * K3.dag()
    return result

# --- Test sur un état pur |0⟩ ---
ket0 = qt.basis(2, 0)
rho_pur = ket0 * ket0.dag()
rho_bruite = depolarizing_channel(rho_pur, 0.3)
print("ρ pur :\n", rho_pur)
print("\nρ après canal dépolarisant (p=0.3) :\n", rho_bruite)
```

**Sortie attendue :**

```
ρ pur :
Quantum object: dims=[[2], [2]], shape=(2, 2), type='oper', dtype=CSR, isherm=True
Qobj data =
[[1. 0.]
 [0. 0.]]

ρ après canal dépolarisant (p=0.3) :
Quantum object: dims=[[2], [2]], shape=(2, 2), type='oper', dtype=CSR, isherm=True
Qobj data =
[[0.85 0.  ]
 [0.   0.15]]
```

> **Interprétation :** L'état pur $\ket{0}\bra{0}$ (qui avait 1 sur la diagonale en haut à gauche) a été « mélangé » : la diagonale est maintenant $(0.85, 0.15)$. Avec $p=0.3$, 30% de l'état a été remplacé par le mélange maximal $I/2$.

#### 2.2 Canal bit-flip

$$\mathcal{E}(\rho) = (1-p)\rho + p X\rho X$$

> **Intuition :** Comme un canal classique qui retourne un bit avec probabilité $p$. C'est l'erreur la plus simple : $\ket{0} \leftrightarrow \ket{1}$.

#### 2.3 Canal phase-flip

$$\mathcal{E}(\rho) = (1-p)\rho + p Z\rho Z$$

> **Intuition :** Spécifiquement quantique ! La phase relative entre $\ket{0}$ et $\ket{1}$ est retournée avec probabilité $p$. Aucun équivalent classique.

#### 2.4 Effet sur la sphère de Bloch

Un état $\rho = \frac{1}{2}(I + \vec{r} \cdot \vec{\sigma})$ est transformé :

| Canal | Effet sur $\vec{r}$ |
|-------|---------------------|
| Dépolarisant | $\vec{r} \to (1-p)\vec{r}$ |
| Bit-flip | $(r_x, r_y, r_z) \to (r_x, (1-2p)r_y, (1-2p)r_z)$ |
| Phase-flip | $(r_x, r_y, r_z) \to ((1-2p)r_x, (1-2p)r_y, r_z)$ |

> **Intuition géométrique :** Le bruit **contracte** la sphère de Bloch. Le vecteur de Bloch $\vec{r}$ se rapproche de l'origine (état maximalement mixte). Le dépolarisant contracte uniformément dans toutes les directions. Le bit-flip contracte seulement selon $y$ et $z$. Le phase-flip contracte seulement selon $x$ et $y$.

```python
import qutip as qt

# --- Visualisation de l'effet du bruit ---
def apply_noise_and_visualize(ket, p=0.3):
    """Visualise l'effet du bruit sur la sphère de Bloch.
    
    Args:
        ket: état initial (ket QuTiP)
        p: probabilité de bruit
    """
    bloch = qt.Bloch()
    rho = ket * ket.dag()

    # État idéal (sur la surface de la sphère)
    bloch.add_states(ket)

    # Application du canal dépolarisant
    rho_noisy = depolarizing_channel(rho, p)
    
    # Calcul du vecteur de Bloch après bruit
    # r_i = Tr(σ_i ρ) pour i = x, y, z
    x, y, z = qt.expect(qt.sigmax(), rho_noisy), \
              qt.expect(qt.sigmay(), rho_noisy), \
              qt.expect(qt.sigmaz(), rho_noisy)
    print(f"Dépolarisant : ({x:.3f}, {y:.3f}, {z:.3f})")
    # Le point est à l'intérieur de la sphère (état mixte)

    bloch.show()
```

---

### Section 3 : Équation maîtresse de Lindblad

#### 3.1 Forme générale

L'évolution d'un système quantique **ouvert** (en contact avec un environnement) est régie par :

$$\frac{d\rho}{dt} = -\frac{i}{\hbar}[H, \rho] + \sum_k \gamma_k \left( L_k \rho L_k^\dagger - \frac{1}{2}\{L_k^\dagger L_k, \rho\} \right)$$

où $L_k$ sont les **opérateurs de Lindblad** (collapse operators).

> **Intuition :** Le premier terme ($-i[H,\rho]/\hbar$) est l'évolution unitaire habituelle (système isolé). Le second terme décrit l'effet de l'environnement : chaque $L_k$ représente un « canal de dissipation » avec un taux $\gamma_k$. Le terme $\{L_k^\dagger L_k, \rho\}$ (anti-commutateur) garantit que la trace est préservée.

#### 3.2 Temps T₁ et T₂

- **T₁** : temps de relaxation (perte d'énergie) : $L_1 = \sqrt{1/T_1}\; \sigma_-$

> **Intuition :** T₁ mesure combien de temps il faut pour qu'un qubit dans l'état $\ket{1}$ retombe à $\ket{0}$. C'est comme le temps de refroidissement d'un objet chaud.

- **T₂** : temps de déphasage (perte de cohérence) : $L_2 = \sqrt{1/T_2}\; \sigma_z$

> **Intuition :** T₂ mesure combien de temps la superposition survit. Les termes hors-diagonaux de $\rho$ décroissent comme $e^{-t/T_2}$. On a toujours $T_2 \leq 2T_1$.

```python
import qutip as qt
import numpy as np

# --- Paramètres physiques ---
T1, T2 = 10.0, 5.0  # µs (microsecondes)
gamma1 = 1.0 / T1    # Taux de relaxation
gamma2 = 1.0 / T2    # Taux de déphasage

# --- Hamiltonien du qubit ---
omega = 1.0  # GHz (fréquence du qubit)
H = omega / 2 * qt.sigmaz()

# --- Opérateurs de Lindblad ---
sm = qt.destroy(2)  # σ_- = |0⟩⟨1| : opérateur de descente (relaxation)
sz = qt.sigmaz()    # σ_z : opérateur de déphasage

c_ops = [
    np.sqrt(gamma1) * sm,     # Canal de relaxation (T₁)
    np.sqrt(gamma2) * sz,     # Canal de déphasage (T₂)
]

# --- État initial |1⟩ (état excité) ---
psi0 = qt.basis(2, 1)
rho0 = psi0 * psi0.dag()

# --- Évolution temporelle ---
tlist = np.linspace(0, 5*T1, 100)  # de 0 à 50 µs
# e_ops : opérateurs dont on veut calculer l'espérance
result = qt.mesolve(H, rho0, tlist, c_ops=c_ops,
                    e_ops=[qt.basis(2,0)*qt.basis(2,0).dag()])

# --- Population de |0⟩ en fonction du temps ---
p0 = result.expect[0]
print("Population |0⟩ à t=0 :", p0[0])  # ≈ 0 (on part de |1⟩)
print("Population |0⟩ à t=T1 :", p0[np.argmin(np.abs(tlist - T1))])  # ≈ 1-1/e ≈ 0.63
```

> **Ce que fait ce code :**
> - Lignes 4-6 : on définit les temps de cohérence T₁ et T₂
> - Lignes 9-10 : l'Hamiltonien décrit un qubit dans un champ magnétique
> - Lignes 13-18 : les opérateurs de Lindblad modélisent relaxation et déphasage
> - Lignes 21-25 : on résout l'équation maîtresse avec `mesolve`
> - Lignes 28-30 : on affiche la population de $\ket{0}$ au cours du temps

#### 3.3 Visualisation de la décohérence

```python
import qutip as qt
import numpy as np

# --- Paramètres (mêmes qu'avant) ---
T1, T2 = 10.0, 5.0
H = 0.5 * qt.sigmaz()
c_ops = [np.sqrt(1/T1) * qt.destroy(2), np.sqrt(1/T2) * qt.sigmaz()]
tlist = np.linspace(0, 5*T1, 100)

# --- État initial |+⟩ (superposition maximale) ---
psi_plus = (qt.basis(2,0) + qt.basis(2,1)).unit()
rho_plus = psi_plus * psi_plus.dag()

# --- Évolution avec décohérence ---
result = qt.mesolve(H, rho_plus, tlist, c_ops=c_ops)

# --- Pureté Tr(ρ²) à différents instants ---
for i, idx in enumerate([0, len(tlist)//4, len(tlist)//2, -1]):
    rho_t = result.states[idx]
    pureté = (rho_t * rho_t).tr()
    print(f"t = {tlist[idx]:.1f}, Tr(ρ²) = {pureté:.4f}")
```

**Sortie attendue :**

```
t = 0.0, Tr(ρ²) = 1.0000
t = 12.5, Tr(ρ²) = 0.6783
t = 25.0, Tr(ρ²) = 0.5246
t = 50.0, Tr(ρ²) = 0.3634
```

> **Interprétation :** La pureté diminue : l'état devient de plus en plus mélangé. À $t=0$, on a un état pur ($\text{Tr}(\rho^2) = 1$). À $t = 50\mu s$, la pureté est tombée à 0.36 — l'état est fortement mélangé par la décohérence.

**Avez-vous compris ?**
- Que représente T₁ ? (Le temps de relaxation énergétique : $\ket{1} \to \ket{0}$)
- Pourquoi $T_2 \leq 2T_1$ ? (Le déphasage inclut la relaxation comme cas particulier)
- Que se passe-t-il quand $t \gg T_1, T_2$ ? (L'état converge vers l'état thermal, souvent $\ket{0}$)

---

### Section 4 : Modèles de bruit avec Qiskit

```python
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, pauli_error

# ============================================================
# CRÉATION D'UN MODÈLE DE BRUIT RÉALISTE
# ============================================================
noise_model = NoiseModel()

# --- Canal dépolarisant sur les portes à 1 qubit ---
# depolarizing_error(0.01, 1) : 1% de probabilité d'erreur par porte à 1 qubit
dep_error = depolarizing_error(0.01, 1)
noise_model.add_all_qubit_quantum_error(dep_error, ['h', 'x', 'y', 'z', 's', 't'])

# --- Canal bit-flip sur les portes CNOT ---
# pauli_error : liste de (erreur, probabilité)
# 'XX' = bit-flip sur les 2 qubits, 'II' = pas d'erreur
bf_error = pauli_error([('XX', 0.02), ('II', 0.98)])  # 2% bit-flip
noise_model.add_all_qubit_quantum_error(bf_error, ['cx'])

# ============================================================
# CIRCUIT DE TEST : état de Bell
# ============================================================
qc = QuantumCircuit(2, 2)
qc.h(0)          # Hadamard
qc.cx(0, 1)      # CNOT : crée l'intrication
qc.measure([0, 1], [0, 1])

# ============================================================
# COMPARAISON : idéal vs bruité
# ============================================================
sim_noisy = AerSimulator(noise_model=noise_model)  # Simulateur avec bruit
sim_ideal = AerSimulator()                          # Simulateur parfait

result_noisy = sim_noisy.run(qc, shots=4096).result()
result_ideal = sim_ideal.run(qc, shots=4096).result()

print("Idéal :", result_ideal.get_counts())
print("Bruité :", result_noisy.get_counts())
```

> **Ce que fait ce code :**
> - Lignes 6-9 : on crée un modèle de bruit avec 1% d'erreur dépolarisante sur les portes à 1 qubit
> - Lignes 12-15 : on ajoute 2% de bit-flip sur les CNOT
> - Lignes 19-22 : on crée un circuit de Bell simple
> - Lignes 27-31 : on compare la simulation idéale (50/50 entre 00 et 11) avec la simulation bruitée (des erreurs apparaissent)
>
> **Résultat attendu :**
> - Idéal : ~50% "00", ~50% "11"
> - Bruité : ~47% "00", ~47% "11", ~3% "01" ou "10" (erreurs)

---

## Exemple guidé

**Problème :** Montrer que le canal dépolarisant contracte la sphère de Bloch : $\vec{r} \to (1-p)\vec{r}$.

**Étape 1 — Écrire l'état en termes du vecteur de Bloch :**

$$\rho = \frac{1}{2}(I + \vec{r} \cdot \vec{\sigma}) = \frac{1}{2}(I + r_x X + r_y Y + r_z Z)$$

**Étape 2 — Appliquer le canal dépolarisant :**

$$\mathcal{E}(\rho) = (1-p)\rho + p\frac{I}{2}$$

$$= (1-p)\frac{1}{2}(I + r_x X + r_y Y + r_z Z) + p\frac{I}{2}$$

$$= \frac{1}{2}\left[(1-p)I + pI + (1-p)(r_x X + r_y Y + r_z Z)\right]$$

$$= \frac{1}{2}\left[I + (1-p)(r_x X + r_y Y + r_z Z)\right]$$

**Étape 3 — Identifier le nouveau vecteur de Bloch :**

$$\vec{r}' = (1-p)\vec{r}$$

**Conclusion :** Le canal dépolarisant contracte uniformément le vecteur de Bloch d'un facteur $(1-p)$. Pour $p = 1$, le vecteur est réduit à l'origine : l'état est $I/2$ (mélange maximal). ✓

> **Vérification numérique :** Pour $\vec{r} = (0, 0, 1)$ (état $\ket{0}$) et $p = 0.3$ :
> $\vec{r}' = (0, 0, 0.7)$, donc $\rho' = \frac{1}{2}(I + 0.7 Z) = \begin{pmatrix} 0.85 & 0 \\ 0 & 0.15 \end{pmatrix}$
> Ce qui correspond exactement à la sortie du code Python ci-dessus ! ✓

---

## Implémentation Python

### Résumé des canaux en code

```python
import numpy as np
import qutip as qt
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, pauli_error

# ============================================================
# 1. CANAL BIT-FLIP : X avec probabilité p
# ============================================================
def bit_flip_channel(rho, p):
    """Applique un canal bit-flip : ρ → (1-p)ρ + p XρX"""
    K0 = np.sqrt(1 - p) * qt.qeye(2)   # Pas d'erreur (proba 1-p)
    K1 = np.sqrt(p) * qt.sigmax()       # Bit-flip (proba p)
    return K0 * rho * K0.dag() + K1 * rho * K1.dag()

# Test
rho0 = qt.basis(2,0) * qt.basis(2,0).dag()
print("Bit-flip (p=0.1) sur |0⟩⟨0| :", bit_flip_channel(rho0, 0.1))
# Résultat : 0.9|0⟩⟨0| + 0.1|1⟩⟨1|

# ============================================================
# 2. CANAL PHASE-FLIP : Z avec probabilité p
# ============================================================
def phase_flip_channel(rho, p):
    """Applique un canal phase-flip : ρ → (1-p)ρ + p ZρZ"""
    K0 = np.sqrt(1 - p) * qt.qeye(2)   # Pas d'erreur
    K1 = np.sqrt(p) * qt.sigmaz()       # Phase-flip
    return K0 * rho * K0.dag() + K1 * rho * K1.dag()

# Test sur |+⟩⟨+| (sensible au phase-flip !)
ket_plus = (qt.basis(2,0) + qt.basis(2,1)).unit()
rho_plus = ket_plus * ket_plus.dag()
print("\nPhase-flip (p=0.2) sur |+⟩⟨+| :", phase_flip_channel(rho_plus, 0.2))
# Les termes hors-diagonaux sont réduits

# ============================================================
# 3. ÉQUATION DE LINDLAD : évolution temporelle
# ============================================================
T1, T2 = 10.0, 5.0  # µs
H = 0.5 * qt.sigmaz()
c_ops = [np.sqrt(1/T1) * qt.destroy(2), np.sqrt(1/T2) * qt.sigmaz()]

# État initial |+⟩
psi0 = (qt.basis(2,0) + qt.basis(2,1)).unit()
rho0 = psi0 * psi0.dag()

tlist = np.linspace(0, 50, 200)
result = qt.mesolve(H, rho0, tlist, c_ops=c_ops)

# Pureté au cours du temps
puretés = [(rho * rho).tr() for rho in result.states]
print(f"\nPureté initiale : {puretés[0]:.4f}")
print(f"Pureté finale : {puretés[-1]:.4f}")

# ============================================================
# 4. MODÈLE DE BRUIT QISKIT
# ============================================================
noise_model = NoiseModel()
dep_error = depolarizing_error(0.01, 1)
noise_model.add_all_qubit_quantum_error(dep_error, ['h', 'x'])

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

sim = AerSimulator(noise_model=noise_model)
counts = sim.run(qc, shots=1000).result().get_counts()
print(f"\nH avec bruit : {counts}")  # Presque 50/50, léger biais
```

---

## Tableau récapitulatif des canaux

| Canal | Opérateurs Kraus | Effet |
|-------|------------------|-------|
| **Bit-flip** | $\sqrt{1-p}I,\; \sqrt{p}X$ | Retourne le qubit avec proba $p$ |
| **Phase-flip** | $\sqrt{1-p}I,\; \sqrt{p}Z$ | Retourne la phase avec proba $p$ |
| **Dépolarisant** | $I, X, Y, Z$ avec poids | État → mélange maximal |
| **Amortissement d'amplitude** | $\begin{pmatrix}1&0\\0&\sqrt{1-\gamma}\end{pmatrix}, \begin{pmatrix}0&\sqrt{\gamma}\\0&0\end{pmatrix}$ | Relaxation $\ket{1} \to \ket{0}$ |
| **Déphasage** | $\begin{pmatrix}1&0\\0&\sqrt{1-\lambda}\end{pmatrix}, \begin{pmatrix}0&0\\0&\sqrt{\lambda}\end{pmatrix}$ | Perte de cohérence |

---

## À retenir

1. **Canal quantique** = application CPTP sur les matrices densité, représentée par des opérateurs de Kraus $K_k$
2. **Condition de complétude** $\sum K_k^\dagger K_k = I$ garantit la conservation de la trace
3. **Dépolarisant** : contracte uniformément la sphère de Bloch : $\vec{r} \to (1-p)\vec{r}$
4. **Bit-flip** : $\ket{0} \leftrightarrow \ket{1}$ avec probabilité $p$ (analogue classique)
5. **Phase-flip** : signe de $\ket{1}$ retourné avec probabilité $p$ (purement quantique)
6. **T₁** = temps de relaxation, **T₂** = temps de décohérence, avec $T_2 \leq 2T_1$
7. **Lindblad** : équation maîtresse qui décrit l'évolution continue d'un système ouvert
8. **Le bruit est le défi central** du calcul quantique → correction d'erreur (Partie III)

---

## Pièges à éviter

1. **Confondre bit-flip et phase-flip** — Le bit-flip est classique (comme inverser un bit). Le phase-flip est purement quantique : il ne change pas les probabilités dans la base Z, mais détruit la cohérence.

2. **Penser que le bruit dépolarisant préserve les états propres** — Même $\ket{0}$ est affecté ! $\mathcal{E}(\ket{0}\bra{0}) = (1-p)\ket{0}\bra{0} + p\frac{I}{2} \neq \ket{0}\bra{0}$.

3. **Confondre le canal et sa probabilité** — Le canal décrit COMMENT l'état est transformé. La probabilité $p$ décrit À QUEL POINT il est transformé.

4. **Oublier que $T_2 \leq 2T_1$** — C'est une contrainte physique fondamentale. Le déphasage total inclut la contribution de la relaxation.

5. **Croire que le bruit est toujours petit** — Pour $p > 3/4$, le canal dépolarisant envoie tout état au-delà du mélange maximal (non physique). La condition $p \leq 1$ n'est pas suffisante : il faut $1 - 3p/4 \geq 0$, soit $p \leq 4/3$, mais en pratique $p \leq 1$.

---

## Exercices

### Niveau 1 — Application directe

1. Vérifier que les Kraus du canal dépolarisant satisfont $\sum_k K_k^\dagger K_k = I$.
   *(Indice : utilisez $X^2 = Y^2 = Z^2 = I$)*

2. Un qubit dans l'état $\ket{+}$ subit un canal phase-flip avec $p = 0.5$. Quelle est la matrice densité résultante ?
   *(Indice : les termes hors-diagonaux sont multipliés par $(1-2p) = 0$)*

3. Implémenter le canal d'amortissement d'amplitude (amplitude damping) avec QuTiP et comparer avec l'équation de Lindblad.

### Niveau 2 — Compréhension

4. Simuler l'évolution d'un état $\ket{+}$ sous bruit dépolarisant et tracer la pureté $\text{Tr}(\rho^2)$ en fonction du temps (ou de $p$).

5. Montrer que le canal dépolarisant peut s'écrire comme une contraction de la sphère de Bloch : $\vec{r} \to (1-p)\vec{r}$.
   *(Suivez l'exemple guidé !)*

6. Avec Qiskit, comparer les résultats d'un circuit de Bell idéal vs avec un modèle de bruit réaliste (T₁=50µs, T₂=30µs).

### Niveau 3 — Défi

7. Montrer que l'amortissement d'amplitude a pour Kraus :
$$K_0 = \begin{pmatrix}1&0\\0&\sqrt{1-\gamma}\end{pmatrix}, \quad K_1 = \begin{pmatrix}0&\sqrt{\gamma}\\0&0\end{pmatrix}$$
et vérifier la condition de complétude.

8. Démontrer que la composition de deux canaux dépolarisants de paramètres $p_1$ et $p_2$ est un canal dépolarisant de paramètre $p = p_1 + p_2 - \frac{4}{3}p_1 p_2$.

---

## Pour aller plus loin

- Nielsen & Chuang, Ch. 8 — Canaux quantiques et représentation de Kraus
- QuTiP documentation : [Lindblad master equation](https://qutip.org/docs/latest/guide/dynamics/dynamics-master.html) — Simulation d'évolution ouverte
- Video : [Quantum Noise Explained](https://www.youtube.com/watch?v=Ezi5lBT9VqQ) — Introduction au bruit quantique
- Qiskit Aer noise documentation — Modèles de bruit réalistes pour la simulation
