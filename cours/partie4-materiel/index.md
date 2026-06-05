# Partie IV : Matériel et perspectives (Séances 12–14)

## Présentation

Cette dernière partie du cours explore les différentes architectures physiques de calcul quantique, leurs applications industrielles, et les défis ouverts pour la réalisation d'ordinateurs quantiques à grande échelle. Les séances 12 et 13 couvrent les principales plateformes matérielles (supraconducteurs, atomes neutres, ions piégés, qubits topologiques, photoniques), tandis que la séance 14 examine les applications, le marché, et les perspectives.

## Tableau récapitulatif

| Séance | Sujet | Bibliothèques | Concepts clés |
|--------|-------|---------------|---------------|
| [12.1 — Supraconducteurs](seance12-1-supraconducteurs.md) | Qubits supraconducteurs, transmons, grille de couplage | QuTiP, numpy | Anharmonicité, Hamiltonien transmon, ZZ-crosstalk, IBM Condor (433Q), Google Willow (105Q, 99.97%) |
| [12.2 — Atomes neutres et ions](seance12-2-atomes-neutres-ions.md) | Atomes neutres, pinces optiques, ions piégés, Rydberg | Cirq, QuTiP, numpy | Blocade de Rydberg, portes CZ, reconfigurabilité dynamique, Harvard/QuEra 48QL, Oxford Ionics 99.99% |
| [13.1 — Topologiques](seance13-1-topologiques.md) | Fermions de Majorana, qubits topologiques, protection | numpy, scipy | Modèle de Kitaev, MZM, gap topologique, Microsoft Majorana 1, invariant topologique |
| [13.2 — Photoniques et réseaux](seance13-2-photoniques-reseaux.md) | LOQC, architecture Entanglement-First, codes SHYPS | QuTiP, numpy, scipy | États de Bell, pertes fibre, répéteurs quantiques, Photonic Inc., Internet quantique |
| [14.1 — Applications](seance14-1-applications-industrielles.md) | Chimie, optimisation, QML, finance | PennyLane, numpy | VQE, QAOA, QUBO, QNN, marché 72 G$ (McKinsey 2025) |
| [14.2 — Défis ouverts](seance14-2-defis-ouverts.md) | Scalabilité, correction d'erreur, main-d'œuvre, post-quantique | numpy, time | Overhead QEC, feuille de route 2027–2029, NIST, point de croisement classique/quantique |

## Prérequis

- **Séances 1–4** : fondements de la mécanique quantique, formalisme de Dirac
- **Séances 5–8** : algorithmes quantiques (QFT, QPE, VQE, QAOA)
- **Séances 9–11** : correction d'erreur quantique, codes de surface, QLDPC
- **Python** : numpy, QuTiP, Cirq, PennyLane, scipy

## Plan détaillé

### Séance 12.1 — Qubits supraconducteurs (seance12-1-supraconducteurs.md)

1. Circuits LC et non-linéarité Josephson
   - Hamiltonien du transmon, anharmonicité $\alpha = -E_C$
2. Architectures de processeurs
   - IBM Condor (433Q, heavy-hexagonal)
   - Google Willow (105Q, 99.97%, tunable couplers)
3. Simulation QuTiP : transmon, spectre, anharmonicité
4. Diaphonie (crosstalk) et grille de couplage
5. Défis : temps de cohérence, passage à l'échelle

### Séance 12.2 — Atomes neutres et ions piégés (seance12-2-atomes-neutres-ions.md)

1. Pièges optiques, pinces optiques, reconfigurabilité
2. États de Rydberg, blocade de Rydberg, portes CZ
3. Simulation Cirq/QuTiP : excitation Rydberg
4. Ions piégés : piège de Paul, portes Mølmer-Sørensen
5. Oxford Ionics : 99.99% fidélité, $T_2 > 10$ s
6. Comparaison des plateformes (atomes, ions, supra)

### Séance 13.1 — Qubits topologiques (seance13-1-topologiques.md)

1. Fermions de Majorana, modes zéro (MZM)
2. Modèle de Kitaev : Hamiltonien, gap topologique
3. Simulation Python : diagonalisation exacte, étude du gap
4. Microsoft Majorana 1 : puce topologique, protection
5. Comparaison avec supraconducteurs et atomes neutres

### Séance 13.2 — Qubits photoniques et réseaux (seance13-2-photoniques-reseaux.md)

1. LOQC : codage dual-rail, beam splitters, KLM
2. Architecture Entanglement-First (Photonic Inc.)
3. Codes QLDPC SHYPS : hypergraphes, tolérance perte
4. Distribution d'intrication, pertes fibre, répéteurs
5. Simulation QuTiP : état de Bell bruité, atténuation

### Séance 14.1 — Applications industrielles (seance14-1-applications-industrielles.md)

1. Chimie quantique : VQE, simulation moléculaire, drug discovery
2. Optimisation : QAOA, QUBO, finance, logistique
3. Quantum Machine Learning : kernels, QNN
4. PennyLane : classification avec QNN
5. Marché 72 G$ (McKinsey 2025), feuille de route consulting

### Séance 14.2 — Défis ouverts (seance14-2-defis-ouverts.md)

1. Scalabilité : nombre, qualité, connectivité des qubits
2. Coût de la correction d'erreur : overhead physique/logique
3. Main-d'œuvre : 600–700 spécialistes QEC, besoin de 5000–16000
4. Feuille de route : avantage quantique 2027–2029
5. Standardisation post-quantique : NIST (Kyber, Dilithium)
6. Benchmark : simulation classique vs estimation quantique

## Ressources

### Articles fondateurs

- Kitaev, A.Yu. (2001). "Unpaired Majorana fermions in quantum wires." *Physics-Uspekhi*, 44, 131.
- Knill, E., Laflamme, R. & Milburn, G.J. (2001). "A scheme for efficient quantum computation with linear optics." *Nature*, 409, 46–52.
- Koch, J. et al. (2007). "Charge-insensitive qubit design derived from the Cooper pair box." *Phys. Rev. A*, 76, 042319.
- Mølmer, K. & Sørensen, A. (1999). "Multiparticle entanglement of hot trapped ions." *Phys. Rev. Lett.*, 82, 1835.

### Articles récents (2025–2026)

- Google Quantum AI (2024). "Quantum error correction below the surface code threshold." *Nature*, 636, 74–79. [Goo24]
- IBM Quantum (2023). "IBM Quantum Condor: 433-qubit processor." [IBM24]
- Bluvstein, D. et al. (2025). "Logical quantum processor with 48 logical qubits." *Nature*. [Har25]
- Daily, T. et al. (2025). "High-fidelity two-qubit gates with trapped ions." *Oxford Ionics*. [Day25]
- QuEra Computing (2025). "Algorithmic Fault Tolerance for neutral atom quantum computers." [QuE25]
- Microsoft Quantum (2025). "Majorana 1: A topological qubit platform." *Nature*. [Mic25]
- Photonic Inc. (2025). "Entanglement-First architecture for fault-tolerant quantum computing." *Nature Photonics*. [Pho25]
- McKinsey & Company (2025). "Quantum computing: An emerging ecosystem and industry use cases." [McK25]
- Consentino, M. et al. (2022). "Quantum computing for finance: A review." *Nature Reviews Physics*, 4, 421–433. [Con22]

### Bibliothèques Python

| Bibliothèque | Utilisation | Installation |
|-------------|-------------|-------------|
| [QuTiP](https://qutip.org) | Simulation de systèmes ouverts | `pip install qutip` |
| [Qiskit](https://qiskit.org) | Circuits quantiques | `pip install qiskit qiskit-aer` |
| [Cirq](https://quantumai.google/cirq) | Circuits quantiques (Google) | `pip install cirq` |
| [PennyLane](https://pennylane.ai) | QML, VQE, optimisation | `pip install pennylane` |
| [Stim](https://github.com/quantumlib/Stim) | Codes stabilisateurs | `pip install stim` |

### Compilation des codes Python

```python
import numpy as np
import matplotlib.pyplot as plt
import qutip as qt
import cirq
import pennylane as qml
from scipy.linalg import eigh
from scipy.sparse import csr_matrix
import time
```

## Exercices transversaux

1. **Comparaison d'architectures** : Pour 100 qubits logiques avec $\epsilon_{\text{log}} = 10^{-12}$, estimer le nombre de qubits physiques nécessaires pour chaque plateforme (supra, atomes neutres, ions, topologique, photonique). Inclure l'overhead de correction d'erreur.

2. **Simulation multi-plateforme** : Implémenter un circuit de téléportation sur les trois plateformes (QuTiP pour supra, Cirq pour atomes neutres, PennyLane pour photonique). Comparer les fidélités avec des modèles de bruit réalistes.

3. **Scalabilité** : Projeter la courbe de croissance des qubits physiques et logiques pour chaque architecture jusqu'en 2035. Identifier le point où chaque plateforme atteint 1000 qubits logiques.

4. **Analyse de marché** : Construire un rapport de 3 pages sur l'impact économique du calcul quantique dans un secteur au choix, incluant une analyse des verrous technologiques et des délais de déploiement.

5. **Défis ouverts** : Identifier les 3 défis les plus critiques pour chaque architecture et proposer une approche de recherche pour les résoudre. Justifier en termes de ressources, temps et impact.
