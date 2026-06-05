# Partie III : Correction d'erreur quantique (Chapitres 9–11)

## Présentation

La correction d'erreur quantique est l'un des défis les plus importants pour la réalisation d'ordinateurs quantiques à grande échelle. Cette partie du cours couvre les fondements de la correction d'erreur, les codes correcteurs quantiques, les codes de surface, les codes QLDPC avancés, le calcul tolérant aux fautes, et les avancées récentes (2024–2026).

## Tableau récapitulatif

| Chapitre | Sujet | Bibliothèques | Concepts clés |
|--------|-------|---------------|---------------|
| [9.1 — Motivation](chapitre9-1-motivation.md) | Fragilité des qubits, décohérence, seuil | QuTiP, Qiskit | Canaux de bruit, T₁/T₂, théorème du seuil, décomposition de Kraus |
| [9.2 — Codes correcteurs](chapitre9-2-codes-correcteurs.md) | Code répétition, Shor [9,1,3], CSS, stabilisateurs | QuTiP, Qiskit | Non-clonage, syndromes, formalisme stabilisateur, code de Steane |
| [10.1 — Codes de surface](chapitre10-1-codes-surface.md) | Grille 2D, syndrome, MWPM, passage sous le seuil | Stim, pymatching, Qiskit | Stabilisateurs 2D, décodage MWPM, Google Willow 2024 |
| [10.2 — Codes QLDPC](chapitre10-2-codes-qldpc.md) | Couleur, Floquet, QLDPC, SHYPS | Stim, numpy | Taux de code non nul, hypergraphes, décodeur BP, comparaison architectures |
| [11.1 — Calcul tolérant](chapitre11-1-calcul-tolerant.md) | États magiques, distillation, Clifford+T, AFT | Qiskit, QuTiP, numpy | Distillation 15-to-1, seuil, Solovay-Kitaev, AFT QuEra 2025 |
| [11.2 — Avancées 2024–2026](chapitre11-2-avancees-2024-2026.md) | Willow, Harvard 48Q, CAV 2025, défis ouverts | Stim, pymatching, numpy | Passage sous le seuil, processeur logique, vérification formelle |

## Prérequis

- **Chapitres 1–4** : postulats de la mécanique quantique, formalisme de la matrice densité
- **Chapitre 4.2** : canaux quantiques et bruit (modèles de Kraus)
- Python : numpy, QuTiP, Qiskit, Stim, pymatching

## Plan détaillé

### Chapitre 9.1 — Motivation et défis (chapitre9-1-motivation.md)

1. Fragilité des qubits et décohérence
   - T₁ (relaxation) et T₂ (déphasage)
   - Simulation QuTiP d'un qubit bruité
2. Différence fondamentale avec la correction classique
   - Non-clonage, mesure destructive, erreurs continues
   - Décomposition sur la base de Pauli
3. Seuil de correction d'erreur
   - Théorème du seuil
   - Passage sous le seuil : scaling exponentiel
4. Simulation QuTiP : canaux dépolarisant, bit-flip, phase-flip

### Chapitre 9.2 — Codes correcteurs (chapitre9-2-codes-correcteurs.md)

1. Code à répétition de phase (3 qubits)
   - Encodage, syndrome, correction
   - Implémentation Qiskit complète
2. Code de Shor [9,1,3]
   - Construction, distance 3, correction d'erreur arbitraire
3. Codes CSS (Calderbank-Shor-Steane)
   - Code de Steane [7,1,3]
4. Formalisme des stabilisateurs
   - Groupe de Pauli, représentation binaire
   - Mesures de syndrome

### Chapitre 10.1 — Codes de surface (chapitre10-1-codes-surface.md)

1. Stabilisateurs sur grille 2D
   - Plaquettes Z et étoiles X
   - Paramètres : [n, k, d], opérateurs logiques
2. Mesures de syndrome
   - Circuit de mesure des stabilisateurs
   - Simulation Stim
3. Décodage MWPM avec pymatching
   - Graphe de décodage
   - Algorithm de Blossom
4. Résultats Google Willow 2024
   - Passage sous le seuil
   - Scaling exponentiel

### Chapitre 10.2 — Codes QLDPC (chapitre10-2-codes-qldpc.md)

1. Codes de couleur
   - Triangulation 2D, portes transversales
2. Codes de Floquet
   - Stabilisateurs dynamiques, séquence périodique
3. Codes QLDPC
   - Matrice de parité creuse, taux non nul
   - Décodeur Belief Propagation
4. Architecture SHYPS (Photonic Inc.)
   - Hypergraphes, tolérance à la perte
5. Comparaison des architectures

### Chapitre 11.1 — Calcul tolérant (chapitre11-1-calcul-tolerant.md)

1. États magiques et distillation
   - Portes non-Clifford, état |T⟩
   - Distillation Bravyi-Kitaev 15-to-1
2. Théorème du seuil
   - Énoncé et démonstration schématique
   - Suroût polylogarithmique
3. Portes Clifford + T
   - Universalité, implémentation transversale
   - Injection d'état magique
4. Framework AFT (QuEra 2025)
   - Protection adaptative, réduction du surcoût

### Chapitre 11.2 — Avancées 2024–2026 (chapitre11-2-avancees-2024-2026.md)

1. Google Willow : passage sous le seuil
   - Analyse des données, scaling exponentiel
   - Comparaison Sycamore → Willow
2. Harvard : processeur logique à 48 qubits
   - Atomes neutres, reconfigurabilité
   - Comparaison des plateformes
3. Vérification automatique (CAV 2025)
   - Vérification de commutation, distance
4. Défis ouverts
   - Décodage temps réel, leakage, connectivité QLDPC
   - Feuille de route 2026–2030

## Ressources

### Articles fondateurs

- Shor, P. (1995). "Scheme for reducing decoherence in quantum computer memory." *Phys. Rev. A*, 52, R2493.
- Gottesman, D. (1997). "Stabilizer Codes and Quantum Error Correction." PhD thesis, Caltech.
- Calderbank, A.R. & Shor, P. (1996). "Good quantum error-correcting codes exist." *Phys. Rev. A*, 54, 1098.
- Steane, A.M. (1996). "Error Correcting Codes in Quantum Theory." *Phys. Rev. Lett.*, 77, 793.

### Articles récents (2024–2026)

- Google Quantum AI (2024). "Quantum error correction below the surface code threshold." *Nature*, 636, 74–79.
- Bluvstein, D. et al. (2025). "Logical quantum processor with 48 logical qubits." *Nature*.
- QuEra Computing (2025). "Algorithmic Fault Tolerance for neutral atom quantum computers." *arXiv*.
- Photonic Inc. (2025). "SHYPS: Scalable Holographic Yield-Protected Storage." *Nature Photonics*.

### Bibliothèques Python

| Bibliothèque | Utilisation | Installation |
|-------------|-------------|-------------|
| [QuTiP](https://qutip.org) | Simulation de systèmes ouverts | `pip install qutip` |
| [Qiskit](https://qiskit.org) | Circuits quantiques, noise model | `pip install qiskit qiskit-aer` |
| [Stim](https://github.com/quantumlib/Stim) | Simulation de codes stabilisateurs | `pip install stim` |
| [PyMatching](https://github.com/oscarhiggott/PyMatching) | Décodage MWPM | `pip install pymatching` |

### Compilation des codes Python

Les exemples de code de cette partie utilisent les importations suivantes :

```python
# Bibliothèques standard
import numpy as np
import matplotlib.pyplot as plt

# QuTiP : simulation de systèmes quantiques ouverts
import qutip as qt

# Qiskit : circuits quantiques
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, pauli_error

# Stim : simulation de codes stabilisateurs
import stim

# PyMatching : décodage MWPM
import pymatching
```

## Exercices transversaux

1. **Implémentation complète** : Implémenter un code de surface de distance 5 avec Stim, incluant le bruit réaliste (dépolarisant 0.1%), et le décodage MWPM avec pymatching.

2. **Analyse de scaling** : Tracer le taux d'erreur logique en fonction de la distance pour p = 0.1%, 0.3%, 0.5%, 1%, 2% et identifier le seuil.

3. **Comparaison de codes** : Pour un budget de 1000 qubits physiques, quel code (surface, QLDPC, SHYPS) offre la meilleure protection ? Justifier.

4. **Distillation et coût** : Estimer le nombre de qubits nécessaires pour exécuter 10⁶ portes T avec une fidélité de 10⁻¹², en utilisant le protocole de distillation 15-to-1.

5. **Projet final** : Concevoir l'architecture de correction d'erreur pour un processeur de 100 qubits logiques avec un taux d'erreur physique de 10⁻³. Inclure le choix du code, la stratégie de décodage, et le budget de distillation.
