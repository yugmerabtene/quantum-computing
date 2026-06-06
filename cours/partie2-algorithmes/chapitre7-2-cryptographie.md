# Chapitre 7.2 — Cryptographie quantique

## Ce que vous allez apprendre

- Comprendre les protocoles **BB84** et **E91** de distribution quantique de clés (QKD)
- Maîtriser le concept de **sécurité informationnelle** (garantie par les lois de la physique, pas par la complexité calculatoire)
- Analyser les **menaces post-quantiques** sur la cryptographie classique (Shor, Grover)
- Implémenter les protocoles en **simulation** avec Qiskit et QuTiP

---

## Motivation

Les chapitres précédents ont montré que les ordinateurs quantiques peuvent casser RSA (Shor, chapitre 7.1) et accélérer la recherche (Grover, chapitre 8.1). Mais la mécanique quantique offre aussi des **outils de protection** : la cryptographie quantique utilise les lois de la physique pour garantir la confidentialité, indépendamment de la puissance de calcul de l'adversaire.

L'idée centrale repose sur deux principes fondamentaux : le **théorème de non-clonage** (impossible de copier un état quantique inconnu) et le fait que toute **mesure perturbe l'état mesuré**. Si Eve espionne la communication, elle laisse des traces détectables.

Contrairement à RSA (dont la sécurité repose sur la difficulté supposée de la factorisation), la QKD offre une **sécurité prouvée** par les lois de la mécanique quantique. C'est une différence fondamentale : même un ordinateur quantique ne peut pas casser BB84.

---

## Idée principale

Imaginez qu'Alice envoie à Bob des lettres dans des boîtes fermées par des cadenas. Si Eve ouvre une boîte pour la lire, elle ne peut pas la refermer exactement comme avant — la serrure est modifiée. Bob et Alice peuvent détecter cette modification en vérifiant quelques lettres au hasard.

En cryptographie quantique, les « boîtes » sont des qubits dans des bases aléatoires. Si Eve mesure un qubit dans la mauvaise base, elle le perturbe irréversiblement. Alice et Bob détectent cette perturbation en comparant publiquement un sous-ensemble de leurs bits.

---

## Contenu du cours

### Section 1 : Distribution quantique de clés (QKD)

**Principe général** : Alice et Bob génèrent une clé secrète partagée avec une sécurité garantie par les lois de la mécanique quantique, **indépendamment de la puissance de calcul d'Eve**.

**Propriétés fondamentales** :
- **Non-clonage** : impossible de copier un état quantique inconnu
- **Mesure = perturbation** : une mesure modifie l'état mesuré
- **Sécurité informationnelle** : $I(A:B) > I(A:E)$ (l'information mutuelle Alice-Bob excède celle d'Eve)

**Intuition** : contrairement à la cryptographie classique (où Eve peut copier les données et les décrypter plus tard), en QKD, toute tentative d'interception modifie le signal et est détectable.

### Section 2 : Protocole BB84 (Bennett-Brassard 1984)

**Encodage** : Alice choisit aléatoirement une base et un bit :

| Base | Bit 0 | Bit 1 |
|------|-------|-------|
| $+$ (Z) | $|0\rangle$ | $|1\rangle$ |
| $\times$ (X) | $|+\rangle$ | $|-\rangle$ |

où $|\pm\rangle = \frac{1}{\sqrt{2}}(|0\rangle \pm |1\rangle)$.

**Intuition** : les états $|0\rangle, |1\rangle$ (base Z) et $|+\rangle, |-\rangle$ (base X) sont **mutuellement non orthogonaux**. Mesurer dans la mauvaise base donne un résultat aléatoire et détruit l'information.

**Étapes du protocole** :

1. **Alice** : Génère $4n$ bits aléatoires et $4n$ bases aléatoires (+ ou ×). Envoie les qubits correspondants.

2. **Bob** : Mesure chaque qubit reçu dans une base aléatoire (+ ou ×). Obtient $4n$ bits.

3. **Bases publiques** : Alice et Bob comparent publiquement leurs bases (pas les bits). Ils gardent les bits où les bases concordent (≈ $2n$ bits). C'est la « sifted key ».

4. **Estimation d'erreur** : Ils révèlent $n$ bits aléatoires pour estimer le QBER (Quantum Bit Error Rate) :
   $$QBER = \frac{\text{bits discordants}}{\text{bits révélés}}$$

5. **Correction d'erreur** : Si $QBER \leq \text{seuil}$ (≈ 11%), ils corrigent les erreurs restantes (protocole Cascade).

6. **Amplification de confidentialité** : Réduire l'information d'Eve par hachage universel.

**Pourquoi ça marche ?** Si Eve intercepte et re-mesure chaque qubit dans une base aléatoire, elle choisit la bonne base 50% du temps. Quand elle se trompe (50%), elle perturbe l'état. Bob a alors 25% de chance de détecter une erreur par bit testé. Sur $n$ bits testés, la probabilité de ne PAS détecter Eve est $(3/4)^n \to 0$.

### Section 3 : Taux de clé sécurisé

$$R = \frac{1}{2} \left[1 - h_2(QBER) - h_2(QBER)\right]$$

où $h_2(x) = -x\log_2 x - (1-x)\log_2(1-x)$ est l'entropie binaire.

**Intuition** : le facteur $1/2$ vient du fait qu'Alice et Bob n'utilisent la même base que la moitié du temps. Le terme $h_2(QBER)$ représente l'information qu'Eve peut avoir grâce au bruit.

**Exemple numérique** : $QBER = 0.05$ (5%) :
$h_2(0.05) = -0.05 \log_2(0.05) - 0.95 \log_2(0.95) \approx 0.286$
$R = \frac{1}{2}[1 - 2 \times 0.286] = 0.214$ bits par qubit envoyé.

### Section 4 : Protocole E91 (Ekert 1991)

**Intrication quantique** : E91 utilise des paires EPR (intriquées) :

$$|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$

**Intuition** : les paires intriquées ont des corrélations parfaites : si Alice et Bob mesurent dans la même base, ils obtiennent toujours le même résultat, même s'ils sont séparés de milliers de kilomètres.

**Étapes** :

1. **Source** : Génère $4n$ paires intriquées $|\Phi^+\rangle$. Envoie un qubit à Alice, l'autre à Bob.

2. **Mesures** : Alice et Bob mesurent chacun dans une base aléatoire parmi $\{0^\circ, 45^\circ, 90^\circ\}$ ou $\{45^\circ, 90^\circ, 135^\circ\}$.

3. **Bases** : Ils comparent publiquement les bases.

4. **Génération de clé** : Quand les bases sont identiques, les bits sont parfaitement corrélés → clé.

5. **Test CHSH** : Pour les bases différentes, ils calculent la valeur CHSH :
   $$S = E(a,b) - E(a,b') + E(a',b) + E(a',b')$$
   où $E(a,b) = \frac{C_{++} + C_{--} - C_{+-} - C_{-+}}{C_{++}+C_{--}+C_{+-}+C_{-+}}$

**Intuition du test CHSH** : si les corrélations violent l'inégalité de Bell ($|S| > 2$), cela prouve que les qubits étaient vraiment intriqués et qu'Eve n'a pas pu les intercepter sans détruire l'intrication.

- Mécanique quantique : $|S| \leq 2\sqrt{2} \approx 2.83$ (violation de Bell)
- Classique (variables cachées locales) : $|S| \leq 2$
- Si $|S| > 2$ : l'intrication est vérifiée → sécurité garantie

---

## Exemple guidé

**BB84 avec 8 qubits** :

Alice génère : bits = `1 0 1 1 0 0 1 0`, bases = `+ × + × + × + ×`

Qubits envoyés :
- bit 1, base + → $|1\rangle$
- bit 0, base × → $|+\rangle$
- bit 1, base + → $|1\rangle$
- bit 1, base × → $|-\rangle$
- bit 0, base + → $|0\rangle$
- bit 0, base × → $|+\rangle$
- bit 1, base + → $|1\rangle$
- bit 0, base × → $|+\rangle$

Bob choisit bases = `× × + × × + + ×`

Mesures de Bob :
- $|1\rangle$ mesuré en × → résultat aléatoire (disons 0)
- $|+\rangle$ mesuré en × → 0 (même base, résultat certain)
- $|1\rangle$ mesuré en + → 1 (même base)
- $|-\rangle$ mesuré en × → 1 (même base)
- $|0\rangle$ mesuré en × → résultat aléatoire (disons 1)
- $|+\rangle$ mesuré en + → résultat aléatoire (disons 0)
- $|1\rangle$ mesuré en + → 1 (même base)
- $|+\rangle$ mesuré en × → 0 (même base)

Bases concordantes (positions 2, 3, 4, 7, 8) :
- Alice : 0, 1, 1, 1, 0
- Bob : 0, 1, 1, 1, 0

Parfait accord ! (sans bruit ni Eve)

---

## Implémentation Python

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import random

# --- Simulation du protocole BB84 ---
def bb84_simulation(n=100, qber=0.0, eavesdrop=False):
    """
    Simulation du protocole BB84.
    n : nombre de bits de clé souhaités
    qber : taux d'erreur quantique (bruit)
    eavesdrop : présence d'Eve (intercepte-renvoie)
    """
    # Génération des bits et bases d'Alice (4n pour obtenir ~n bits de clé)
    alice_bits = [random.randint(0, 1) for _ in range(4 * n)]
    alice_bases = [random.randint(0, 1) for _ in range(4 * n)]

    # Préparation des qubits par Alice
    circuits = []
    for bit, base in zip(alice_bits, alice_bases):
        qc = QuantumCircuit(1, 1)
        if bit == 1:
            qc.x(0)       # |0⟩ → |1⟩
        if base == 1:      # Base X
            qc.h(0)        # |0⟩ → |+⟩ ou |1⟩ → |−⟩

        # Attaque d'Eve (intercepte-renvoie)
        if eavesdrop:
            eve_base = random.randint(0, 1)  # Eve choisit une base aléatoire
            if eve_base == 1:
                qc.h(0)    # Mesure en base X
            qc.measure(0, 0)
            # Après mesure, l'état est effondré — Eve renvoie un qubit
            if random.random() < 0.5:
                qc.x(0)
            if eve_base == 1:
                qc.h(0)

        # Bruit (bit-flip)
        if random.random() < qber:
            qc.x(0)

        circuits.append(qc)

    # Bob : bases aléatoires et mesures
    bob_bases = [random.randint(0, 1) for _ in range(4 * n)]
    backend = AerSimulator()

    bob_bits = []
    for i, qc in enumerate(circuits):
        if bob_bases[i] == 1:
            qc.h(0)        # Mesure en base X
        qc.measure(0, 0)
        result = backend.run(qc, shots=1).result()
        bob_bits.append(int(list(result.get_counts().keys())[0]))

    # Filtrage : garder uniquement les bits où les bases concordent
    key_bits = []
    for i in range(4 * n):
        if alice_bases[i] == bob_bases[i]:
            key_bits.append((alice_bits[i], bob_bits[i]))

    # Estimation d'erreur sur les n premiers bits concordants
    test_bits = key_bits[:n]
    errors = sum(1 for a, b in test_bits if a != b)
    estimated_qber = errors / n if n > 0 else 0.0

    # Clé finale (reste des bits concordants)
    final_key = key_bits[n:]

    print(f"=== BB84 Simulation ===")
    print(f"Qubits envoyés : {4 * n}")
    print(f"Bases concordantes : {len(key_bits)} (≈50%)")
    print(f"Test QBER : {estimated_qber:.3f} ({errors}/{n})")
    if eavesdrop:
        print(f"⚠️  Écoute présente ! QBER > 0")
    print(f"Clé finale : {len(final_key)} bits")

    if final_key:
        print(f"Premiers bits : {final_key[:min(10, len(final_key))]}")
    return final_key, estimated_qber

# Tests
print("BB84 sans écoute :")
bb84_simulation(n=100, qber=0.01)

print("\nBB84 avec écoute (Eve) :")
bb84_simulation(n=100, eavesdrop=True)
```

```python
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# --- Circuit BB84 en Qiskit ---
def bb84_circuit_qiskit():
    """
    Circuit Qiskit illustrant le protocole BB84.
    Alice prépare des qubits, Bob mesure dans des bases aléatoires.
    """
    n = 4  # nombre de bits de clé
    qc = QuantumCircuit(2 * n, 2 * n)

    # Alice prépare ses qubits (positions 0 à n-1)
    for i in range(n):
        base_a = np.random.randint(2)  # 0 = base Z, 1 = base X
        bit_a = np.random.randint(2)

        if bit_a == 1:
            qc.x(i)       # Encoder le bit 1
        if base_a == 1:
            qc.h(i)        # Changer de base (Z → X)

    # Bob choisit ses bases et mesure (positions n à 2n-1)
    for i in range(n):
        base_b = np.random.randint(2)
        if base_b == 1:
            qc.h(n + i)   # Mesure en base X

    # Mesures
    qc.measure(range(n), range(n))

    print("Circuit BB84 :")
    print(qc.draw())

    backend = AerSimulator()
    result = backend.run(qc, shots=1024).result()
    counts = result.get_counts()
    print("Distribution des mesures :", counts)

bb84_circuit_qiskit()
```

```python
import numpy as np

# --- Simulation du protocole E91 ---
def simulate_e91(shots=1024):
    """
    Simulation du protocole E91 avec paires intriquées |Φ+⟩.
    Alice et Bob mesurent dans des bases angulaires.
    """
    n_angles = 3
    angles_a = [0, np.pi/4, np.pi/2]        # 0°, 45°, 90°
    angles_b = [np.pi/4, np.pi/2, 3*np.pi/4] # 45°, 90°, 135°

    results_a = []
    results_b = []

    for _ in range(shots):
        # Choix aléatoire des bases
        base_a = np.random.randint(n_angles)
        base_b = np.random.randint(n_angles)

        # Simulation de la corrélation quantique
        r = np.random.random()
        if base_a == base_b:
            # Bases identiques → corrélations parfaites
            bit = np.random.randint(2)
            results_a.append((base_a, bit))
            results_b.append((base_b, bit))
        else:
            # Bases différentes → corrélations quantiques (cos²)
            delta = angles_a[base_a] - angles_b[base_b]
            p_same = np.cos(delta)**2
            bit_a = np.random.randint(2)
            bit_b = bit_a if np.random.random() < p_same else 1 - bit_a
            results_a.append((base_a, bit_a))
            results_b.append((base_b, bit_b))

    # Extraction de la clé (bases identiques)
    key_bits = [(a[1], b[1]) for a, b in zip(results_a, results_b)
                if a[0] == b[0]]
    key = [a for a, b in key_bits if a == b]

    # Calcul de la valeur CHSH
    E = [[0, 0] for _ in range(3)]
    counts = [[0, 0] for _ in range(3)]
    for (a, ba), (b, bb) in zip(results_a, results_b):
        for i in range(n_angles):
            for j in range(n_angles):
                if a == i and b == j:
                    E[i][j] += (1 if ba == bb else -1)
                    counts[i][j] += 1

    # Normaliser les corrélations
    for i, j in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        if counts[i][j] > 0:
            E[i][j] /= counts[i][j]

    S = E[0][0] - E[0][1] + E[1][0] + E[1][1]

    print(f"=== E91 Simulation ===")
    print(f"Nombre de paires : {shots}")
    print(f"Bases identiques : {len(key_bits)}")
    print(f"Bits de clé : {len(key)}")
    print(f"Valeur CHSH : S = {S:.4f}")
    print(f"  Limite classique : |S| ≤ 2")
    print(f"  Limite quantique : |S| ≤ 2√2 ≈ {2*np.sqrt(2):.4f}")
    if abs(S) > 2:
        print("  ✓ Violation de Bell détectée — sécurité garantie")
    else:
        print("  ✗ Pas de violation de Bell")

simulate_e91(2048)
```

```python
import numpy as np

# --- Analyse des menaces post-quantiques ---
def analyse_menace_pq():
    """
    Analyse des risques post-quantique par horizon temporel.
    """
    print("=== Analyse des risques post-quantique ===")
    horizons = {
        "Court terme (0-5 ans)": "Développement NIST, premières implémentations hash-based",
        "Moyen terme (5-15 ans)": "Ordinateurs quantiques ~1000 qubits logiques, menace RSA-1024",
        "Long terme (15-25 ans)": "Ordinateurs quantiques ~10000 qubits, menace RSA-2048",
        "Très long terme (25+ ans)": "Menace généralisée sur PKI, migration complète nécessaire"
    }

    for horizon, desc in horizons.items():
        print(f"  {horizon} : {desc}")

    # Comparaison des tailles de clés
    print("\n=== Comparaison tailles de clés (bits) ===")
    print(f"{'Primitive':<20} {'Classique':<15} {'Post-quantique':<15}")
    print("-" * 50)
    primitives = [
        ("RSA-2048", "2048", "—"),
        ("ECC-256", "256", "—"),
        ("Kyber-512", "—", "800"),
        ("Dilithium-2", "—", "1312"),
        ("SPHINCS+-128s", "—", "64 (hash)"),
    ]
    for name, cls, pq in primitives:
        print(f"  {name:<18} {cls:<15} {pq:<15}")

analyse_menace_pq()
```

**Sortie attendue :**

```
=== Analyse des risques post-quantique ===
  Court terme (0-5 ans) : Développement NIST, premières implémentations hash-based
  Moyen terme (5-15 ans) : Ordinateurs quantiques ~1000 qubits logiques, menace RSA-1024
  Long terme (15-25 ans) : Ordinateurs quantiques ~10000 qubits, menace RSA-2048
  Très long terme (25+ ans) : Menace généralisée sur PKI, migration complète nécessaire

=== Comparaison tailles de clés (bits) ===
Primitive            Classique       Post-quantique 
--------------------------------------------------
  RSA-2048           2048            --             
  ECC-256            256             --             
  Kyber-512          --              800            
  Dilithium-2        --              1312           
  SPHINCS+-128s      --              64 (hash)      
```

---

## Complexité et avantage quantique

| Système | Problème sous-jacent | Vulnérable à | Sécurité post-quantique |
|---------|----------------------|--------------|------------------------|
| RSA | Factorisation | Shor | ✗ |
| ECC | Logarithme discret | Shor | ✗ |
| DSA | Logarithme discret | Shor | ✗ |
| AES-128 | Recherche exhaustive | Grover ($\approx 2^{64}$) | △ (doubler la clé) |
| **BB84** | **Physique** | **Aucun** | **✓** |

**Impact de Grover sur AES** : Grover réduit la sécurité effective de moitié. AES-256 reste sûr ($2^{128}$ quantique), mais AES-128 devient vulnérable ($2^{64}$ quantique).

---

## À retenir

1. **BB84** utilise 2 bases non orthogonales pour détecter l'espionnage
2. **E91** utilise l'intrication et le test CHSH pour garantir la sécurité
3. La sécurité est **informationnelle** : garantie par les lois de la physique, pas par la complexité
4. Le **QBER** seuil est ≈ 11% : au-delà, la clé n'est plus sûre
5. L'attaque intercepte-renvoie est détectée avec probabilité $1 - (3/4)^n$
6. **Shor** menace RSA/ECC, **Grover** réduit de moitié la sécurité de AES
7. La **cryptographie post-quantique** (Kyber, Dilithium, SPHINCS+) est la solution pour remplacer RSA

---

## Pièges à éviter

1. **Confondre QKD et cryptographie post-quantique** : la QKD utilise des qubits, le post-quantique utilise des maths classiques résistantes aux ordinateurs quantiques
2. **Penser que BB84 est infaillible** : les implémentations pratiques ont des failles (attaques PNS, attaques par canal auxiliaire)
3. **Oublier l'authentification** : BB84 nécessite un canal authentifié (sinon attaque de l'homme du milieu)
4. **Négliger le taux de perte** : dans les fibres optiques, les pertes limitent la distance à ~100-200 km
5. **Confondre sécurité prouvée et sécurité pratique** : la preuve de sécurité suppose des dispositifs parfaits, ce qui n'est jamais le cas en pratique

---

## Exercices

### Niveau 1 — Application directe

**Exercice 1** : Implémentez le protocole BB84 en utilisant QuTiP avec des matrices de densité.

```python
import qutip as qt
import numpy as np

def bb84_qutip():
    """BB84 avec matrices de densité"""
    zero = qt.basis(2, 0)
    one = qt.basis(2, 1)
    plus = (zero + one).unit()
    minus = (zero - one).unit()

    # Encodage par Alice
    etats = {
        (0, 0): zero,   # bit 0, base Z
        (0, 1): one,    # bit 1, base Z
        (1, 0): plus,   # bit 0, base X
        (1, 1): minus,  # bit 1, base X
    }

    # Matrices de mesure
    M_Z0 = zero * zero.dag()
    M_Z1 = one * one.dag()
    M_X0 = plus * plus.dag()
    M_X1 = minus * minus.dag()

    # Complétez l'implémentation...
    pass
```

**Exercice 2** : Démontrez que $|S| \leq 2\sqrt{2}$ pour des mesures sur $|\Phi^+\rangle$. Montrez que $S = 2\sqrt{2}$ pour les angles optimaux.

### Niveau 2 — Compréhension

**Exercice 3** : Simulez l'attaque PNS (Photon Number Splitting) sur BB84 avec des impulsions multi-photons.

**Exercice 4** : Implémentez le protocole Cascade pour corriger les erreurs sur la clé BB84.

### Niveau 3 — Défi

**Exercice 5** : Implémentez l'amplification de confidentialité en utilisant des fonctions de hachage universelles.

**Exercice 6** : Montrez que $I(A:E) \leq 2^{-m}$ après amplification de confidentialité avec $m$ bits de hachage.

---

## Pour aller plus loin

- Les **répéteurs quantiques** permettent d'étendre la portée de la QKD au-delà de 200 km
- Le **réseau quantique chinois** (Micius) a démontré la QKD sur 1200 km par satellite
- Le standard **NIST post-quantique** (Kyber, Dilithium) sera déployé massivement d'ici 2030

---

## Références

- Bennett, C. H. & Brassard, G. (1984). "Quantum cryptography: Public key distribution and coin tossing". *Proc. IEEE ICC*, 175–179.
- Ekert, A. K. (1991). "Quantum cryptography based on Bell's theorem". *Phys. Rev. Lett.*, 67, 661–663.
- Scarani, V. et al. (2009). "The security of practical quantum key distribution". *Rev. Mod. Phys.*, 81, 1301–1350.
- NIST Post-Quantum Cryptography Standardization : https://csrc.nist.gov/projects/post-quantum-cryptography
