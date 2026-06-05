# Plan du cours

## Partie I : Fondements (Chapitres 1–4)

| Chapitre | Sujet |
|--------|-------|
| [1.1 — Introduction historique](partie1-fondements/chapitre1-1-introduction.md) | Des machines de Turing au modèle quantique |
| [1.2 — Algèbre linéaire complexe](partie1-fondements/chapitre1-2-algebre-lineaire.md) | Espaces de Hilbert, notation de Dirac, produit tensoriel |
| [2.1 — Postulats de la mécanique quantique](partie1-fondements/chapitre2-1-postulats-mq.md) | États, évolution, mesure, sphère de Bloch |
| [2.2 — Superposition et intrication](partie1-fondements/chapitre2-2-concepts-cles.md) | États EPR, inégalités de Bell, non-clonage |
| [3.1 — Portes quantiques](partie1-fondements/chapitre3-1-portes-quantiques.md) | Pauli, Hadamard, CNOT, universalité |
| [3.2 — Modèle circuit](partie1-fondements/chapitre3-2-modele-circuit.md) | Téléportation, codage superdense |
| [4.1 — Opérateur densité](partie1-fondements/chapitre4-1-operateur-densite.md) | Matrice densité, états purs vs mélanges, POVM |
| [4.2 — Canaux quantiques et bruit](partie1-fondements/chapitre4-2-canaux-bruit.md) | Kraus, décohérence, modèles de bruit |

## Partie II : Algorithmes quantiques (Chapitres 5–8)

| Chapitre | Sujet |
|--------|-------|
| 5.1 — Deutsch et Deutsch–Jozsa | Parallélisme quantique, oracle |
| 5.2 — Algorithme de Simon | Période cachée, lien QFT |
| 6.1 — Quantum Fourier Transform (QFT) | Circuit efficace O(n²) |
| 6.2 — Quantum Phase Estimation (QPE) | Analyse de précision |
| 7.1 — Algorithme de Shor | Factorisation, impact RSA |
| 7.2 — Cryptographie quantique | BB84, E91, post-quantique |
| 8.1 — Algorithme de Grover | Recherche O(√N), optimalité |
| 8.2 — Applications de Grover | Comptage, résolution NP |

## Partie III : Correction d'erreur (Chapitres 9–11)

| Chapitre | Sujet |
|--------|-------|
| 9.1 — Motivation et défis | Fragilité des qubits, bruit |
| 9.2 — Codes correcteurs | Code de Shor, codes CSS, stabilisateurs |
| 10.1 — Codes de surface | Grille 2D, syndrome, MWPM |
| 10.2 — Codes QLDPC | Floquet, SHYPS, comparaisons |
| 11.1 — Calcul tolérant aux fautes | États magiques, seuil |
| 11.2 — Avancées 2024–2026 | Willow, Harvard, vérification |

## Partie IV : Matériel et perspectives (Chapitres 12–14)

| Chapitre | Sujet |
|--------|-------|
| 12.1 — Qubits supraconducteurs | Transmons, IBM Condor, Google Willow |
| 12.2 — Atomes neutres et ions piégés | Harvard/QuEra, Oxford Ionics |
| 13.1 — Qubits topologiques | Majorana 1 (Microsoft) |
| 13.2 — Qubits photoniques | LOQC, Photonic Inc., réseaux |
| 14.1 — Applications industrielles | Chimie, finance, QML |
| 14.2 — Défis ouverts | Scalabilité, feuille de route |

## Laboratoires

| Lab | Sujet | Bibliothèque |
|-----|-------|-------------|
| [Lab 1](../labs/lab1-simulation-qubit-bloch/) | Sphère de Bloch, évolution unitaire | QuTiP, Qiskit |
| [Lab 2](../labs/lab2-intrication-bell/) | Intrication, CHSH | QuTiP, Qiskit, Cirq |
| [Lab 3](../labs/lab3-canaux-bruit/) | Canaux de bruit, décohérence | QuTiP, Qiskit, Stim |
| [Lab 4](../labs/lab4-teleportation/) | Téléportation quantique | QuTiP, Qiskit, Cirq |
| [Lab 5](../labs/lab5-deutsch-jozsa/) | Deutsch–Jozsa | Qiskit |
| [Lab 6](../labs/lab6-qft-qpe/) | QFT et QPE | Qiskit, Cirq |
| [Lab 7](../labs/lab7-shor/) | Shor et factorisation | Qiskit, Cirq |
| [Lab 8](../labs/lab8-grover/) | Grover et recherche | Qiskit, Cirq |
| [Lab 9](../labs/lab9-code-repetition/) | Code à répétition | QuTiP, Qiskit, Stim |
| [Lab 10](../labs/lab10-codes-surface/) | Codes de surface | Stim, pymatching |
| [Lab 11](../labs/lab11-vqe/) | VQE et chimie | PennyLane |
| [Lab 12](../labs/lab12-qaoa/) | QAOA optimisation | PennyLane, Qiskit |
| [Lab 13](../labs/lab13-machines-reelles/) | Machines réelles | IBM, Braket |
