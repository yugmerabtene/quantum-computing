# Quantum Computing Engineering

**Niveau :** Master / Doctorat (M2 / PhD)  
**Durée :** 28 séances (2 × 2h par semaine, 14 semaines)  
**Langue :** Français  

## Description

Ce cours d'ingénierie propose une couverture complète du calcul quantique, depuis les fondements mathématiques et physiques jusqu'aux algorithmes avancés, à la correction d'erreur et aux architectures matérielles contemporaines. Il s'appuie sur les développements les plus récents (2024–2026) — notamment les processeurs Willow (Google), Condor (IBM), Majorana 1 (Microsoft), les atomes neutres (Harvard/QuEra) et les progrès en correction d'erreur tolérante aux fautes.

Une importance particulière est accordée à l'articulation entre théorie et pratique : chaque module théorique est associé à une implémentation en Python sur simulateurs et machines réelles. La progression pédagogique va de la **simulation physique des qubits** (Hamiltoniens, décohérence via QuTiP) à **l'abstraction circuit** (Qiskit, Cirq), puis à **l'apprentissage automatique quantique** (PennyLane) et à la **correction d'erreur** (Stim).

## Plan du cours

### Partie I : Fondements (Chapitres 1–4)

| Chapitre | Sujet | Fichier |
|--------|-------|---------|
| 1.1 | Introduction historique et panorama | [cours/partie1-fondements/chapitre1-1-introduction.md](cours/partie1-fondements/chapitre1-1-introduction.md) |
| 1.2 | Algèbre linéaire complexe | [cours/partie1-fondements/chapitre1-2-algebre-lineaire.md](cours/partie1-fondements/chapitre1-2-algebre-lineaire.md) |
| 2.1 | Postulats de la mécanique quantique | [cours/partie1-fondements/chapitre2-1-postulats-mq.md](cours/partie1-fondements/chapitre2-1-postulats-mq.md) |
| 2.2 | Superposition et intrication | [cours/partie1-fondements/chapitre2-2-concepts-cles.md](cours/partie1-fondements/chapitre2-2-concepts-cles.md) |
| 3.1 | Portes quantiques | [cours/partie1-fondements/chapitre3-1-portes-quantiques.md](cours/partie1-fondements/chapitre3-1-portes-quantiques.md) |
| 3.2 | Modèle circuit | [cours/partie1-fondements/chapitre3-2-modele-circuit.md](cours/partie1-fondements/chapitre3-2-modele-circuit.md) |
| 4.1 | Opérateur densité et systèmes composites | [cours/partie1-fondements/chapitre4-1-operateur-densite.md](cours/partie1-fondements/chapitre4-1-operateur-densite.md) |
| 4.2 | Canaux quantiques et bruit | [cours/partie1-fondements/chapitre4-2-canaux-bruit.md](cours/partie1-fondements/chapitre4-2-canaux-bruit.md) |

### Partie II : Algorithmes quantiques (Chapitres 5–8)

| Chapitre | Sujet | Fichier |
|--------|-------|---------|
| 5.1 | Deutsch et Deutsch–Jozsa | [cours/partie2-algorithmes/chapitre5-1-deutsch-jozsa.md](cours/partie2-algorithmes/chapitre5-1-deutsch-jozsa.md) |
| 5.2 | Algorithme de Simon | [cours/partie2-algorithmes/chapitre5-2-simon.md](cours/partie2-algorithmes/chapitre5-2-simon.md) |
| 6.1 | Quantum Fourier Transform (QFT) | [cours/partie2-algorithmes/chapitre6-1-qft.md](cours/partie2-algorithmes/chapitre6-1-qft.md) |
| 6.2 | Quantum Phase Estimation (QPE) | [cours/partie2-algorithmes/chapitre6-2-qpe.md](cours/partie2-algorithmes/chapitre6-2-qpe.md) |
| 7.1 | Algorithme de Shor | [cours/partie2-algorithmes/chapitre7-1-shor.md](cours/partie2-algorithmes/chapitre7-1-shor.md) |
| 7.2 | Cryptographie quantique | [cours/partie2-algorithmes/chapitre7-2-cryptographie.md](cours/partie2-algorithmes/chapitre7-2-cryptographie.md) |
| 8.1 | Algorithme de Grover | [cours/partie2-algorithmes/chapitre8-1-grover.md](cours/partie2-algorithmes/chapitre8-1-grover.md) |
| 8.2 | Applications de Grover | [cours/partie2-algorithmes/chapitre8-2-applications-grover.md](cours/partie2-algorithmes/chapitre8-2-applications-grover.md) |

### Partie III : Correction d'erreur (Chapitres 9–11)

| Chapitre | Sujet | Fichier |
|--------|-------|---------|
| 9.1 | Motivation et défis | [cours/partie3-correction-erreur/chapitre9-1-motivation.md](cours/partie3-correction-erreur/chapitre9-1-motivation.md) |
| 9.2 | Codes correcteurs quantiques | [cours/partie3-correction-erreur/chapitre9-2-codes-correcteurs.md](cours/partie3-correction-erreur/chapitre9-2-codes-correcteurs.md) |
| 10.1 | Codes de surface | [cours/partie3-correction-erreur/chapitre10-1-codes-surface.md](cours/partie3-correction-erreur/chapitre10-1-codes-surface.md) |
| 10.2 | Codes QLDPC et avancés | [cours/partie3-correction-erreur/chapitre10-2-codes-qldpc.md](cours/partie3-correction-erreur/chapitre10-2-codes-qldpc.md) |
| 11.1 | Calcul tolérant aux fautes | [cours/partie3-correction-erreur/chapitre11-1-calcul-tolerant.md](cours/partie3-correction-erreur/chapitre11-1-calcul-tolerant.md) |
| 11.2 | Avancées 2024–2026 | [cours/partie3-correction-erreur/chapitre11-2-avancees-2024-2026.md](cours/partie3-correction-erreur/chapitre11-2-avancees-2024-2026.md) |

### Partie IV : Matériel et perspectives (Chapitres 12–14)

| Chapitre | Sujet |
|--------|-------|
| 12.1 | Qubits supraconducteurs (Transmons, IBM Condor, Google Willow) |
| 12.2 | Atomes neutres et ions piégés (Harvard/QuEra) |
| 13.1 | Qubits topologiques (Majorana 1, Microsoft) |
| 13.2 | Qubits photoniques et réseaux quantiques |
| 14.1 | Applications industrielles (chimie, finance, QML) |
| 14.2 | Défis ouverts et horizon |

### Laboratoires

| Lab | Sujet | Bibliothèque | Fichier |
|-----|-------|-------------|---------|
| 1 | Sphère de Bloch, évolution | QuTiP, Qiskit | [labs/lab1-simulation-qubit-bloch/lab1.ipynb](labs/lab1-simulation-qubit-bloch/lab1.ipynb) |
| 2 | Intrication, CHSH | QuTiP, Qiskit, Cirq | [labs/lab2-intrication-bell/lab2.ipynb](labs/lab2-intrication-bell/lab2.ipynb) |
| 3 | Canaux de bruit, décohérence | QuTiP, Qiskit, Stim | [labs/lab3-canaux-bruit/lab3.ipynb](labs/lab3-canaux-bruit/lab3.ipynb) |
| 4 | Téléportation quantique | QuTiP, Qiskit, Cirq | [labs/lab4-teleportation/lab4.ipynb](labs/lab4-teleportation/lab4.ipynb) |
| 5 | Deutsch–Jozsa | Qiskit | [labs/lab5-deutsch-jozsa/lab5.ipynb](labs/lab5-deutsch-jozsa/lab5.ipynb) |
| 6 | QFT et QPE | Qiskit, Cirq | [labs/lab6-qft-qpe/lab6.ipynb](labs/lab6-qft-qpe/lab6.ipynb) |
| 7 | Shor et factorisation | Qiskit, Cirq | [labs/lab7-shor/lab7.ipynb](labs/lab7-shor/lab7.ipynb) |
| 8 | Grover et recherche | Qiskit, Cirq | [labs/lab8-grover/lab8.ipynb](labs/lab8-grover/lab8.ipynb) |
| 9 | Code à répétition | QuTiP, Qiskit, Stim | [labs/lab9-code-repetition/lab9.ipynb](labs/lab9-code-repetition/lab9.ipynb) |
| 10 | Codes de surface | Stim, pymatching | [labs/lab10-codes-surface/lab10.ipynb](labs/lab10-codes-surface/lab10.ipynb) |
| 11 | VQE et chimie | PennyLane | [labs/lab11-vqe/lab11.ipynb](labs/lab11-vqe/lab11.ipynb) |
| 12 | QAOA optimisation | PennyLane, Qiskit | [labs/lab12-qaoa/lab12.ipynb](labs/lab12-qaoa/lab12.ipynb) |
| 13 | Machines réelles | IBM, Braket | [labs/lab13-machines-reelles/lab13.ipynb](labs/lab13-machines-reelles/lab13.ipynb) |

## Prérequis

- Algèbre linéaire (espaces vectoriels complexes, produits tensoriels, valeurs propres)
- Probabilités et statistiques de base
- Notions de mécanique quantique recommandées mais non obligatoires
- Programmation en Python

## Objectifs d'apprentissage

1. Maîtriser le formalisme mathématique du calcul quantique (notation de Dirac, opérateurs unitaires, mesure projective)
2. Concevoir et analyser des circuits quantiques
3. Implémenter et analyser les algorithmes quantiques fondamentaux
4. Comprendre les modèles de calcul alternatifs
5. Expliquer les principes de la correction d'erreur quantique
6. Analyser les architectures matérielles contemporaines
7. Appréhender les avancées récentes (2024–2026)
8. Implémenter des algorithmes sur simulateurs et matériel quantique réel

## Bibliothèques Python utilisées

| Bibliothèque | Rôle |
|---|---|
| **Qiskit** | Circuits quantiques, simulateur Aer, accès IBM |
| **QuTiP** | Simulation physique de qubits, Hamiltoniens, décohérence |
| **Cirq** | Circuits NISQ, optimisation |
| **PennyLane** | Apprentissage automatique quantique, VQE, QAOA |
| **Stim** | Simulation ultra-rapide de circuits stabilisateurs |
| **Amazon Braket** | Accès multi-plateforme (IonQ, Rigetti, QuEra) |
| **Cuda-Q** | Simulation GPU-accélérée |

## Installation

```bash
pip install -r code/requirements.txt
```

## Références

### Ouvrages fondamentaux
- [NC00] Nielsen & Chuang, *Quantum Computation and Quantum Information.* Cambridge University Press, 2000.
- [Aar13] Aaronson, *Quantum Computing Since Democritus.* Cambridge University Press, 2013.
- [RP11] Rieffel & Polak, *Quantum Computing: A Gentle Introduction.* MIT Press, 2011.
- [Pre98] Preskill, *Lecture Notes for Physics 219: Quantum Computation.* Caltech.

### Articles récents (2024–2026)
- [Goo24] Google Quantum AI, « Quantum error correction below the surface code threshold. » *Nature*, 2024.
- [Har25] Bluvstein et al., « Logical quantum processor based on reconfigurable atom arrays. » *Nature*, 2025.
- [Mic25] Microsoft, « Majorana 1: Topological Qubit Platform. » *Nature*, 2025.
- [QuE25] QuEra Computing, « Low-Overhead Transversal Fault Tolerance. » *Nature*, 2025.

## Structure du dépôt

```
cours/                         # Contenu théorique (Markdown + LaTeX)
├── partie1-fondements/        # Chapitres 1-4
├── partie2-algorithmes/       # Chapitres 5-8
├── partie3-correction-erreur/ # Chapitres 9-11
└── partie4-materiel/          # Chapitres 12-14

labs/                          # Travaux pratiques (Jupyter notebooks)
├── lab1-simulation-qubit-bloch/
├── lab2-intrication-bell/
├── lab3-canaux-bruit/
├── lab4-teleportation/
└── ... (jusqu'à lab13)

code/                          # Scripts Python et utilitaires
├── diagrams/                  # Scripts de génération de figures
└── requirements.txt

figures/                       # Diagrammes générés (PNG)
exercices/                     # Devoirs
references/                    # Ressources complémentaires
syllabus-quantum-computing.md  # Syllabus détaillé original
```

## Évaluation

| Élément | Poids |
|---------|-------|
| Devoirs (×4) | 40 % |
| Projet de mi-parcours | 20 % |
| Projet final | 30 % |
| Présentation orale | 10 % |
