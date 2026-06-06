# Partie I — Fondements mathématiques et physiques

## Table des matières

| Chapitre | Titre | Sujets clés | Outils |
|----------|-------|-------------|--------|
| [1.1 — Introduction historique](chapitre1-1-introduction.md) | Des machines de Turing au modèle quantique | Feynman, Deutsch, Shor, Grover, Willow, Harvard | — |
| [1.2 — Algèbre linéaire complexe](chapitre1-2-algebre-lineaire.md) | Espaces de Hilbert, notation de Dirac, produit tensoriel | Bras, kets, opérateurs unitaires, valeurs propres | QuTiP, numpy |
| [2.1 — Postulats de la mécanique quantique](chapitre2-1-postulats-mq.md) | États, évolution, mesure, sphère de Bloch | Qubit, Hamiltonien, principe de Born | QuTiP, matplotlib |
| [2.2 — Superposition et intrication](chapitre2-2-concepts-cles.md) | États EPR/Bell, inégalités de Bell, non-clonage | CHSH, interférence, corrélations | QuTiP, Qiskit |
| [3.1 — Portes quantiques](chapitre3-1-portes-quantiques.md) | Pauli, Hadamard, CNOT, universalité | Solovay-Kitaev, décomposition | Qiskit, QuTiP |
| [3.2 — Modèle circuit](chapitre3-2-modele-circuit.md) | Téléportation, codage superdense | Feed-forward, simulation classique | Qiskit, QuTiP |
| [4.1 — Opérateur densité](chapitre4-1-operateur-densite.md) | Matrice densité, états purs vs mélanges, POVM | Trace partielle, entropie de von Neumann | QuTiP |
| [4.2 — Canaux quantiques et bruit](chapitre4-2-canaux-bruit.md) | Kraus, décohérence, modèles de bruit | T₁, T₂, Lindblad, dépolarisant | QuTiP, Qiskit |

## Progression pédagogique

```
Chapitres 1-2 : Mathématiques et physique de base
    ↓ (espaces de Hilbert, qubits, mesure)
Chapitres 3-4 : Circuits et bruit
    ↓ (portes, téléportation, décohérence)
Partie II : Algorithmes quantiques
```

## Prérequis

- Algèbre linéaire (espaces vectoriels, matrices, valeurs propres)
- Nombres complexes (module, phase, conjugué)
- Probabilités de base
- Python (numpy)

## Objectifs d'apprentissage

À l'issue de cette partie, l'étudiant sera capable de :
1. Manipuler la notation de Dirac et les opérateurs quantiques
2. Représenter un qubit sur la sphère de Bloch
3. Construire et simuler des circuits quantiques simples
4. Comprendre la décohérence et les modèles de bruit
5. Distinguer états purs, mélanges et intrication
