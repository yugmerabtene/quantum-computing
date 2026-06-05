# Séance 7.2 — Cryptographie quantique

## Objectifs d'apprentissage

- Comprendre les protocoles BB84 et E91 de distribution quantique de clés
- Maîtriser le concept de sécurité informationnelle (information-theoretic security)
- Analyser les menaces post-quantique sur la cryptographie classique
- Implémenter les protocoles en simulation

---

## 1. Distribution quantique de clés (QKD)

### Principe général

La QKD permet à deux parties, Alice et Bob, de générer une clé secrète partagée, avec une sécurité garantie par les lois de la mécanique quantique, **indépendamment de la puissance de calcul de l'adversaire**.

### Propriétés fondamentales

- **No-cloning** : Impossible de copier un état quantique inconnu
- **Mesure = perturbation** : Une mesure modifie l'état mesuré
- **Sécurité informationnelle** : $I(A:B) > I(A:E)$ (l'information mutuelle Alice-Bob excède celle d'Eve)

## 2. Protocole BB84 (Bennett-Brassard 1984)

### Encodage

Alice choisit aléatoirement une base et un bit :

| Base | $|0\rangle$ | $|1\rangle$ |
|------|------------|------------|
| $+$ (Z) | $|0\rangle$ | $|1\rangle$ |
| $\times$ (X) | $|+\rangle$ | $|-\rangle$ |

où $|\pm\rangle = \frac{1}{\sqrt{2}}(|0\rangle \pm |1\rangle)$.

### Étapes du protocole

1. **Alice** : Génère $4n$ bits aléatoires et $4n$ bases aléatoires (+ ou ×). Envoie les qubits correspondants.

2. **Bob** : Mesure chaque qubit reçu dans une base aléatoire (+ ou ×). Obtient $4n$ bits.

3. **Bases publiques** : Alice et Bob comparent publiquement leurs bases (pas les bits). Ils gardent les bits où les bases concordent (≈ $2n$ bits).

4. **Estimation d'erreur** : Ils révèlent $n$ bits aléatoires pour estimer le taux d'erreur quantique (QBER).

   $$QBER = \frac{\text{bits discordants}}{\text{bits révélés}}$$

5. **Correction d'erreur** : Si $QBER \leq \text{seuil}$ (≈ 11%), ils corrigent les erreurs restantes (ex. protocole Cascade).

6. **Amplification de confidentialité** : Réduire l'information d'Eve par hachage universel.

### Base de mesure et probabilités

Soit $p$ la probabilité qu'Alice et Bob choisissent la même base :

$$P(\text{même base}) = \frac{1}{2}$$

Pour les bits où les bases concordent : $P(\text{bit identique}) = 1$ (sans bruit).

### Taux de clé

$$R = \frac{1}{2} \left[1 - h_2(QBER) - h_2(QBER)\right]$$

où $h_2(x) = -x\log_2 x - (1-x)\log_2(1-x)$ est l'entropie binaire.

## 3. Protocole E91 (Ekert 1991)

### Intrication quantique

E91 utilise des paires EPR (intriquées) :

$$|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$

### Étapes

1. **Source** : Génère $4n$ paires intriquées $|\Phi^+\rangle$. Envoie un qubit à Alice, l'autre à Bob.

2. **Mesures** : Alice et Bob mesurent chacun leur qubit dans une base aléatoire parmi $\{0^\circ, 45^\circ, 90^\circ\}$ ou $\{45^\circ, 90^\circ, 135^\circ\}$.

3. **Bases** : Ils comparent publiquement les bases.

4. **Génération de clé** : Quand les bases sont identiques, les bits sont parfaitement corrélés → clé.

5. **Test CHSH** : Pour les bases différentes, ils calculent la valeur CHSH :

   $$S = E(a,b) - E(a,b') + E(a',b) + E(a',b')$$

   où $E(a,b) = \frac{C_{++} + C_{--} - C_{+-} - C_{-+}}{C_{++}+C_{--}+C_{+-}+C_{-+}}$

   - Mécanique quantique : $|S| \leq 2\sqrt{2}$ (violation de Bell)
   - Classique : $|S| \leq 2$ (inégalité de Bell-CHSH)
   - Si $|S| > 2$ : l'intrication est vérifiée → sécurité garantie

## 4. Sécurité informationnelle

### Information mutuelle

$$I(A:B) = H(A) + H(B) - H(A,B)$$
$$I(A:E) = H(A) + H(E) - H(A,E)$$

### Condition de sécurité

$$I(A:B) > I(A:E) \quad \text{ou} \quad \Delta I = I(A:B) - I(A:E) > 0$$

### Attaque intercepte-renvoie (Intercept-Resend)

Eve intercepte chaque qubit, mesure dans une base aléatoire, et renvoie un nouveau qubit. Probabilité de détection :

$$P(\text{détection}) = 1 - \left(\frac{3}{4}\right)^{4n}$$

Pour $n$ grand, $P(\text{détection}) \to 1$.

## 5. Implémentation en simulation

```python
import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
import random

def bb84_simulation(n=100, qber=0.0, eavesdrop=False):
    """
    Simulation du protocole BB84.
    n : nombre de bits de base
    qber : taux d'erreur quantique (bruit)
    eavesdrop : présence d'Eve
    """
    # Génération des bits et bases d'Alice
    alice_bits = [random.randint(0, 1) for _ in range(4 * n)]
    alice_bases = [random.randint(0, 1) for _ in range(4 * n)]

    # Préparation des qubits
    qc = QuantumCircuit(1, 1)
    circuits = []
    for bit, base in zip(alice_bits, alice_bases):
        qc = QuantumCircuit(1, 1)
        if bit == 1:
            qc.x(0)
        if base == 1:  # Base X
            qc.h(0)

        # Ajout de bruit ou écoute
        if eavesdrop:
            # Eve mesure dans une base aléatoire
            eve_base = random.randint(0, 1)
            if eve_base == 1:
                qc.h(0)
            qc.measure(0, 0)
            # État après mesure (effondrement)
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
    backend = Aer.get_backend('qasm_simulator')

    bob_bits = []
    for i, qc in enumerate(circuits):
        if bob_bases[i] == 1:
            qc.h(0)
        qc.measure(0, 0)
        result = execute(qc, backend, shots=1).result()
        bob_bits.append(int(list(result.get_counts().keys())[0]))

    # Filtrage : mêmes bases
    key_bits = []
    for i in range(4 * n):
        if alice_bases[i] == bob_bases[i]:
            key_bits.append((alice_bits[i], bob_bits[i]))

    # Estimation d'erreur sur les n premiers bits
    test_bits = key_bits[:n]
    errors = sum(1 for a, b in test_bits if a != b)
    estimated_qber = errors / n if n > 0 else 0.0

    # Clé finale (reste des bits)
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
from qiskit import QuantumCircuit, Aer, execute

def bb84_circuit_qiskit():
    """
    Circuit Qiskit illustrant le protocole BB84.
    """
    n = 4  # nombre de bits de clé
    qc = QuantumCircuit(2 * n, 2 * n)

    # Alice prépare ses qubits
    for i in range(n):
        # Base Z (0) ou X (1) aléatoire
        base_a = np.random.randint(2)
        bit_a = np.random.randint(2)

        if bit_a == 1:
            qc.x(i)
        if base_a == 1:
            qc.h(i)

    # Bob choisit ses bases et mesure
    for i in range(n):
        base_b = np.random.randint(2)
        if base_b == 1:
            qc.h(n + i)

    # Mesures
    qc.measure(range(n), range(n))

    print("Circuit BB84 :")
    print(qc.draw())

    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend, shots=1024).result()
    counts = result.get_counts()
    print("Distribution des mesures :", counts)

bb84_circuit_qiskit()
```

```python
import numpy as np

def simulate_e91(shots=1024):
    """
    Simulation du protocole E91 avec paires intriquées.
    """
    n_angles = 3
    angles_a = [0, np.pi/4, np.pi/2]   # 0°, 45°, 90°
    angles_b = [np.pi/4, np.pi/2, 3*np.pi/4]  # 45°, 90°, 135°

    # Résultats de mesure
    results_a = []
    results_b = []

    for _ in range(shots):
        # Choix aléatoire des bases
        base_a = np.random.randint(n_angles)
        base_b = np.random.randint(n_angles)

        # Simulation de la corrélation parfaite
        # Pour une paire |Φ+⟩, les mesures sont parfaitement corrélées
        # quand les angles sont égaux
        r = np.random.random()
        if base_a == base_b:
            # Parfaitement corrélé
            bit = np.random.randint(2)
            results_a.append((base_a, bit))
            results_b.append((base_b, bit))
        else:
            # Corrélation imparfaite
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

    # Calcul CHSH
    E = [[0, 0] for _ in range(3)]
    counts = [[0, 0] for _ in range(3)]
    for (a, ba), (b, bb) in zip(results_a, results_b):
        for i in range(n_angles):
            for j in range(n_angles):
                if a == i and b == j:
                    E[i][j] += (1 if ba == bb else -1)
                    counts[i][j] += 1

    S = 0
    pairs = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for i, j in pairs:
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

## 6. Menaces post-quantique

### Problèmes mathématiques vulnérables

| Système | Problème sous-jacent | Vulnérable à |
|---------|----------------------|--------------|
| RSA | Factorisation d'entiers | Shor (quantique) |
| ECC | Logarithme discret | Shor (quantique) |
| DSA | Logarithme discret | Shor (quantique) |
| AES-128 | Recherche exhaustive | Grover ($\approx 2^{64}$) |

### Impact de Grover sur AES

Grover réduit la sécurité effective de moitié :

| Algorithme | Sécurité classique | Sécurité quantique |
|------------|-------------------|-------------------|
| AES-128 | 128 bits | 64 bits |
| AES-256 | 256 bits | 128 bits |
| SHA-256 | 256 bits | 128 bits |

### Chronologie de la menace

```python
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

    # Taille de clé équivalente post-quantique
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

## 7. Exercices

### Exercice 1 : BB84 avec QuTiP
Implémentez le protocole BB84 en utilisant QuTiP avec des matrices de densité.

```python
import qutip as qt
import numpy as np

def bb84_qutip():
    """BB84 avec matrices de densité"""
    # États de base
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

### Exercice 2 : Attaque PNS (Photon Number Splitting)
Simulez l'attaque PNS sur BB84 avec des impulsions multi-photons. Montrez qu'un attaquant peut obtenir l'information sans se faire détecter.

### Exercice 3 : E91 — Inégalité CHSH
Démontrez que $|S| \leq 2\sqrt{2}$ pour des mesures sur $|\Phi^+\rangle$. Montrez que $S = 2\sqrt{2}$ pour $\theta_a = 0, \pi/2$ et $\theta_b = \pi/4, 3\pi/4$.

### Exercice 4 : Correction d'erreur Cascade
Implémentez le protocole Cascade pour corriger les erreurs sur la clé BB84.

### Exercice 5 : Amplification de confidentialité
Implémentez l'amplification de confidentialité en utilisant des fonctions de hachage universelles.

### Exercice 6 : Analyse de sécurité
Montrez que $I(A:E) \leq 2^{-m}$ après amplification de confidentialité avec $m$ bits de hachage.

---

## Références

- Bennett, C. H. & Brassard, G. (1984). "Quantum cryptography: Public key distribution and coin tossing". *Proc. IEEE ICC*, 175–179.
- Ekert, A. K. (1991). "Quantum cryptography based on Bell's theorem". *Phys. Rev. Lett.*, 67, 661–663.
- Scarani, V. et al. (2009). "The security of practical quantum key distribution". *Rev. Mod. Phys.*, 81, 1301–1350.
- NIST Post-Quantum Cryptography Standardization : https://csrc.nist.gov/projects/post-quantum-cryptography
