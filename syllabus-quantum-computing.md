# Syllabus — Calcul Quantique : Fondements, Algorithmes et Perspectives

**Niveau :** Master / Doctorat (M2 / PhD)
**Durée :** 28 séances (2 × 2h par semaine, 14 semaines)
**Langue :** Français


---

## 1. Description du cours

Ce cours propose une couverture complète du calcul quantique, depuis les fondements mathématiques et physiques jusqu'aux algorithmes avancés, à la correction d'erreur et aux architectures matérielles contemporaines. Il s'appuie sur les développements les plus récents (2024–2026) — notamment les processeurs Willow (Google), Condor (IBM), Majorana 1 (Microsoft), les atomes neutres (Harvard/QuEra) et les progrès en correction d'erreur tolérante aux fautes.

Une importance particulière est accordée à l'articulation entre théorie et pratique : chaque module théorique est associé à une implémentation en Python sur simulateurs et machines réelles. La progression pédagogique va de la **simulation physique des qubits** (Hamiltoniens, décohérence via QuTiP) à **l'abstraction circuit** (Qiskit, Cirq), puis à **l'apprentissage automatique quantique** (PennyLane) et à la **correction d'erreur** (Stim).

---

## 2. Prérequis

- Algèbre linéaire (espaces vectoriels complexes, produits tensoriels, valeurs propres)
- Probabilités et statistiques de base
- Notions de mécanique quantique (postulats, notation de Dirac) recommandées mais non obligatoires — un rappel intensif est prévu en début de cours
- Programmation en Python

---

## 3. Objectifs d'apprentissage

À l'issue du cours, l'étudiant sera capable de :

1. Maîtriser le formalisme mathématique du calcul quantique (notation de Dirac, opérateurs unitaires, mesure projective)
2. Concevoir et analyser des circuits quantiques
3. Implémenter et analyser les algorithmes quantiques fondamentaux (Deutsch-Jozsa, Grover, Shor, QFT, QPE)
4. Comprendre les modèles de calcul alternatifs (adiabatique, mesure, atomes neutres)
5. Expliquer les principes de la correction d'erreur quantique et de la tolérance aux fautes
6. Analyser les architectures matérielles (supraconducteurs, ions piégés, atomes neutres, photons, qubits topologiques)
7. Appréhender les avancées récentes (2024–2026) et les défis ouverts du domaine
8. Implémenter des algorithmes sur des simulateurs et du matériel quantique réel via des frameworks cloud

---

## 4. Manuels de référence

### Ouvrages fondamentaux

| Réf. | Ouvrage |
|------|---------|
| [NC00] | **Nielsen, M. A. & Chuang, I. L.** *Quantum Computation and Quantum Information.* Cambridge University Press, 2000 (10th Anniversary Ed. 2010). ISBN 978-1-107-00217-3. — *La référence absolue,  citation la plus élevée en physique.* |
| [Aar13] | **Aaronson, S.** *Quantum Computing Since Democritus.* Cambridge University Press, 2013. ISBN 978-0-521-19956-8. |
| [RP11] | **Rieffel, E. & Polak, W.** *Quantum Computing: A Gentle Introduction.* MIT Press, 2011. ISBN 978-0-262-01506-0. |
| [Won22] | **Wong, T. G.** *Introduction to Classical and Quantum Computing.* Rooted Grove, 2022. ISBN 979-8-9855931-0-5. |
| [Pre98] | **Preskill, J.** *Lecture Notes for Physics 219: Quantum Computation.* Caltech, 1998–2023. Disponible en ligne : theory.caltech.edu/~preskill/ph229 |

### Ouvrages spécialisés

| Réf. | Ouvrage |
|------|---------|
| [Got07] | **Gottesman, D.** « Fault-Tolerant Quantum Computation. » *Quant-ph/0701112*, 2007. |
| [MM24] | **Manenti, R. & Motta, M.** *Quantum Information Science.* Oxford University Press, 2024. ISBN 978-0-19-289351-2. |
| [Day25] | **Cain, M.** « Quantum Algorithms and Quantum Error Correction with Neutral Atoms. » *Thèse de doctorat, Harvard University*, 2025. |
| [Con22] | **Cong, I.** « Quantum Machine Learning, Error Correction, and Topological Phases of Matter. » *Thèse de doctorat, Harvard University*, 2022. |

---

## 5. Articles de recherche récents (2024–2026)

### Correction d'erreur et tolérance aux fautes

| Réf. | Article |
|------|---------|
| [Goo24] | **Google Quantum AI.** « Quantum error correction below the surface code threshold. » *Nature*, 2024. — *Démonstration du processeur Willow : réduction exponentielle des erreurs.* |
| [Har25] | **Bluvstein, D. et al.** « Logical quantum processor based on reconfigurable atom arrays. » *Nature*, 2025. DOI: 10.1038/s41586-025-09848-5. — *Premier processeur logique tolérant aux fautes avec 48 qubits logiques chez Harvard.* |
| [QuE25] | **QuEra Computing.** « Low-Overhead Transversal Fault Tolerance for Universal Quantum Computation. » *Nature*, 2025. — *Framework d'Algorithmic Fault Tolerance (AFT) réduisant le surcoût temporel de la correction d'erreur.* |
| [Riv25] | **Riverlane.** « Quantum Error Correction: 2025 Trends and 2026 Predictions. » *Rapport technique*, 2025. |
| [Che25] | **Chen, K. et al.** « Verifying Fault-Tolerance of Quantum Error Correction Codes. » *CAV 2025*, arXiv:2501.14380. |
| [Üst25] | **Üstün, O. K.** « Quantum Error Correction: A Review of Foundational Principles and Recent Developments. » *TechRxiv*, 2025. |

### Matériel et architectures

| Réf. | Article |
|------|---------|
| [Mic25] | **Microsoft.** « Majorana 1: Topological Qubit Platform. » *Nature / Microsoft Research*, 2025. — *Premier processeur topologique utilisant des fermions de Majorana.* |
| [IBM24] | **IBM.** « IBM Quantum Roadmap: 433-Qubit Condor and Beyond. » *IBM Research*, 2024–2026. |
| [Pho25] | **Photonic Inc.** « SHYPS: A Family of QLDPC Codes for Fault-Tolerant Quantum Computing. » 2025. |
| [Sci26] | « Quantum technology has reached its transistor moment. » *Science*, Janvier 2026. — *Article de synthèse sur la maturité du domaine.* |

### Algorithmes et applications

| Réf. | Article |
|------|---------|
| [McK25] | **Soller, H. et al.** « The Year of Quantum: From Concept to Reality in 2025. » *McKinsey Quantum Technology Monitor*, 2025. — *Rapport sur le marché : 1,4 G$ en 2025, projection 100 G$ d'ici 2035.* |
| [Pro26] | « Quantum Computing Breakthrough 2026: IBM's 433-Qubit Condor, Google's 1000-Qubit Willow. » *Programming Helper*, 2026. |
| [Gil26] | « Latest Breakthroughs in Quantum Computing (2026). » *Gilkut*, Mars 2026. |

---

## 6. Plan détaillé — Calendrier des séances

### PARTIE I : FONDEMENTS

| Séance | Contenu | Références |
|--------|---------|------------|
| **1.1** | **Introduction historique et panorama.** Des machines de Turing au modèle quantique. La boucle de rétroaction physique–information. Le « transistor moment » du quantique (Science, 2026). | [NC00] Ch. 1 ; [Aar13] Ch. 1–3 ; [Sci26] |
| **1.2** | **Algèbre linéaire complexe pour le calcul quantique.** Espaces de Hilbert, notation de Dirac (bras, kets). Opérateurs linéaires, matrices, adjoints. Produit tensoriel. | [NC00] §2.1 ; [Won22] Ch. 3–4 |
| **2.1** | **Postulats de la mécanique quantique.** États, évolution unitaire, mesure projective. Principe de Born. Sphère de Bloch. Qubit : représentation géométrique. | [NC00] §2.2 ; [Pre98] §1–2 |
| **2.2** | **Concepts clés I.** Superposition, intrication (états EPR/Bell), inégalités de Bell. Non-clonage, non-signalement. | [NC00] §2.3–2.6 ; [Aar13] Ch. 10–12 |
| **3.1** | **Portes quantiques.** Portes à un qubit (Pauli X, Y, Z, Hadamard, phase, T). Portes à deux qubits (CNOT, CZ, SWAP). Universalité : décomposition de circuits. Théorème de Solovay–Kitaev. | [NC00] §4.1–4.5 ; [Won22] Ch. 8–11 |
| **3.2** | **Modèle circuit.** Formalisme du circuit quantique. Simulation classique des circuits. Premiers circuits : téléportation quantique, codage superdense. | [NC00] §4.6 ; [RP11] Ch. 5–6 |
| **4.1** | **Opérateur densité et systèmes composites.** Matrice densité, états purs vs. mélanges. Mesures POVM. | [NC00] §2.4 ; [Pre98] §3 |
| **4.2** | **Canaux quantiques et bruit.** Opérations quantiques, représentation de Kraus. Décohérence et relaxation. Modèles de bruit : dépolarisant, bit-flip, phase-flip. | [NC00] §8.1–8.3 |

### PARTIE II : ALGORITHMES QUANTIQUES

| Séance | Contenu | Références |
|--------|---------|------------|
| **5.1** | **Problème de Deutsch et Deutsch–Jozsa.** Parallélisme quantique. Oracle et promesse. Généralisation à n qubits. | [NC00] §1.4, §6.1 ; [RP11] Ch. 7 |
| **5.2** | **Algorithme de Simon.** Période cachée et transformée de Hadamard. Lien avec la transformée de Fourier quantique. | [NC00] §6.2–6.3 |
| **6.1** | **Quantum Fourier Transform (QFT).** Définition, circuit efficace O(n²). Implémentation. | [NC00] §5.1 ; [Won22] Ch. 14 |
| **6.2** | **Quantum Phase Estimation (QPE).** Algorithme, analyse de précision. Porte de contrôle. Application fondamentale pour Shor et autres. | [NC00] §5.2 |
| **7.1** | **Algorithme de Shor (factorisation).** Réduction factorisation → recherche de période. Estimation de la complexité. L'impact sur RSA. | [NC00] §5.3 ; [Aar13] Ch. 14 |
| **7.2** | **Cryptographie quantique.** QKD : protocole BB84, E91. Distribution de clés, sécurité informationnelle. Menaces et post-quantique. | [NC00] §12.6 ; [RP11] Ch. 8 |
| **8.1** | **Algorithme de recherche de Grover.** L'oracle, l'inversion autour de la moyenne. Analyse de complexité : O(√N). Optimalité. | [NC00] §6.1–6.3 ; [Won22] Ch. 15 |
| **8.2** | **Applications de Grover.** Recherche dans une base de données, comptage quantique, résolution NP. Bornes inférieures. | [NC00] §6.4–6.6 |

### PARTIE III : CORRECTION D'ERREUR ET TOLÉRANCE AUX FAUTES

| Séance | Contenu | Références |
|--------|---------|------------|
| **9.1** | **Motivation et défis.** Fragilité des qubits. Bruit et décohérence. Différence fondamentale avec la correction classique. | [NC00] §10.1–10.2 ; [Pre98] §5 |
| **9.2** | **Codes correcteurs quantiques.** Code à répétition de phase. Code de Shor [9,1,3]. Codes CSS (Calderbank–Shor–Steane). Stabilisateurs. | [NC00] §10.3–10.4 ; [Üst25] |
| **10.1** | **Codes de surface.** Formalisme des stabilisateurs sur grille 2D. Mesures de syndrome. Decoding par minimum weight perfect matching (MWPM). | [Got07] ; [Goo24] |
| **10.2** | **Code couleur et codes QLDPC.** Codes de couleur, codes de Floquet. Codes QLDPC (IBM, Photonic SHYPS). Comparaison des architectures. | [Riv25] ; [Pho25] |
| **11.1** | **Calcul tolérant aux fautes.** États magiques, distillation. Théorème du seuil. Portes logiques Clifford + T. Framework de tolérance transversale (QuEra). | [Got07] ; [QuE25] |
| **11.2** | **Avancées 2024–2026 en correction d'erreur.** Willow : passage sous le seuil (Google). Processeur logique à 48 qubits (Harvard). Vérification automatique de codes (CAV 2025). Défis ouverts : latence, décodeurs temps réel. | [Goo24] ; [Har25] ; [Che25] |

### PARTIE IV : MATÉRIEL, ARCHITECTURES ET PERSPECTIVES

| Séance | Contenu | Références |
|--------|---------|------------|
| **12.1** | **Qubits supraconducteurs.** Transmons, grille de couplage. IBM Condor (433 qubits), Google Willow (105 qubits, 99,97% fidélité). Limites et défis. | [IBM24] ; [Goo24] |
| **12.2** | **Atomes neutres et ions piégés.** Reconfigurabilité dynamique (Harvard/QuEra). Haute fidélité (Oxford Ionics 99,99%). Portes à deux qubits. | [Har25] ; [Day25] ; [QuE25] |
| **13.1** | **Qubits topologiques.** Fermions de Majorana. Puce Majorana 1 (Microsoft). Stabilité topologique. Potentiel et état d'avancement. | [Mic25] |
| **13.2** | **Qubits photoniques et distribution intriquée.** Calcul quantique linéaire optique (LOQC). Architecture Entanglement-First (Photonic Inc.). Réseaux quantiques et Internet quantique. | [Pho25] |
| **14.1** | **Applications industrielles.** Chimie quantique et drug discovery. Optimisation (finance, logistique). Apprentissage automatique quantique (QML). Simulation de matériaux. McKinsey : marché 72 G$ d'ici 2035. | [McK25] ; [Con22] |
| **14.2** | **Défis ouverts et horizon.** Scalabilité, coût de la correction d'erreur, main-d'œuvre (600–700 spécialistes QEC mondiaux, besoin de 5 000–16 000 d'ici 2030). Feuille de route : avantage quantique pratique 2027–2029. Post-quantique et normalisation (NIST). | [Riv25] ; [McK25] ; [Pro26] |

---

## 7. Travaux pratiques et projets — Laboratoires Python

### 7.1 Écosystème Python pour le calcul quantique

Sept bibliothèques Python sont utilisées dans ce cours, choisies pour leur complémentarité, leur adoption académique et industrielle, et leur pertinence pédagogique :

| Bibliothèque | Version | Rôle dans le cours | Domaine | Install |
|---|---|---|---|---|
| **Qiskit** (IBM) | 2.x | Construction et exécution de circuits, transpilation, accès au matériel IBM | Circuits quantiques, algorithmes | `pip install qiskit qiskit-aer` |
| **QuTiP** | 5.3+ | Simulation physique de qubits : Hamiltoniens, décohérence, canaux, équations maîtresses | Physique des qubits, systèmes ouverts | `pip install qutip[full]` |
| **Cirq** (Google) | 1.x | Conception de circuits NISQ, optimisation, intégration Google Quantum AI | Circuits NISQ, QEC | `pip install cirq` |
| **PennyLane** (Xanadu) | 0.45+ | Apprentissage automatique quantique, différentiation automatique, optimisation | QML, VQE, QAOA | `pip install pennylane` |
| **Stim** (Google) | 1.x | Simulation ultra-rapide de circuits stabilisateurs pour la correction d'erreur | Correction d'erreur | `pip install stim` |
| **Amazon Braket** | 1.x | Accès unifié multi-matériel (IonQ, Rigetti, QuEra) | Cloud quantique | `pip install amazon-braket-sdk` |
| **Cuda-Q** (NVIDIA) | 0.x | Simulation GPU-accélérée, hybridation classique-quantique | HPC quantique | `pip install cuda-quantum` |

**Justification du choix :**

- **Qiskit** est le SDK le plus utilisé au monde (7,4k ⭐, 2,9k forks) et offre la couverture la plus large : construction de circuits, simulateur haute performance (Aer), accès au matériel IBM Quantum via le cloud, et une bibliothèque d'algorithmes. Utilisé dans des milliers d'articles de recherche.
- **QuTiP** est l'outil de référence pour la simulation *physique* des qubits (plus de 3 700 citations, publié dans *Physics Reports* 2025). Là où Qiskit manipule des circuits abstraits, QuTiP simule l'équation de Schrödinger, l'équation maîtresse de Lindblad, les Hamiltoniens dépendant du temps — essentiel pour comprendre la décohérence, les portes réalistes, et le bruit.
- **Cirq** est optimisé pour les circuits NISQ et s'intègre nativement à **Stim** (simulation de correction d'erreur stabilisatrice) et **Qualtran** (algorithmes tolérants aux fautes), tous deux maintenus par Google Quantum AI.
- **PennyLane** est la librairie de référence en apprentissage automatique quantique, avec différentiation automatique des circuits et intégration des frameworks ML classiques (PyTorch, TensorFlow, JAX).
- **Amazon Braket** offre un point d'accès unifié aux machines de différents fabricants (IonQ, Rigetti, QuEra) sans changer d'API.
- **Cuda-Q** (NVIDIA) permet la simulation massivement parallèle sur GPU, nécessaire quand le nombre de qubits dépasse la capacité des simulateurs CPU.

### 7.2 Structure des laboratoires

Chaque laboratoire suit un canevas identique : **fondement théorique** (formel) → **simulation physique du qubit** (QuTiP) → **implémentation circuit** (Qiskit/Cirq) → **exécution et analyse**. Cette progression permet à l'étudiant de comprendre à la fois la physique sous-jacente et l'abstraction algorithmique.

#### Laboratoire 1 — Simulation d'un qubit et sphère de Bloch (Semaine 2)

| Aspect | Détail |
|--------|--------|
| **Objectifs** | Comprendre la représentation d'état d'un qubit, visualiser la sphère de Bloch, simuler l'évolution unitaire |
| **QuTiP** | Construction de `Qobj` pour |0⟩, |1⟩, états en superposition. Opérateurs de Pauli (sigmaz, sigmax, sigmay). Visualisation Bloch sphere. Simulation d'évolution sous Hamiltonien H = ω σ_z/2 : `sesolve(H, psi0, tlist)` |
| **Qiskit** | `Statevector`, `plot_bloch_sphere()`, portes X, Y, Z, H, S, T. Mesure et distribution de probabilités |
| **Notions** | Sphère de Bloch, phase globale vs relative, rotation, fréquence de Rabi |

#### Laboratoire 2 — Intrication et inégalités de Bell (Semaine 2)

| Aspect | Détail |
|--------|--------|
| **Objectifs** | Générer et caractériser des états intriqués, violer les inégalités de Bell en simulation |
| **QuTiP** | États de Bell : `bell_state()`. Matrice densité réduite : `ptrace()`. Entropie d'intrication. Évolution sous influence de l'environnement : `lindblad` avec opérateurs de collapse |
| **Qiskit** | Circuit Bell (H + CNOT). `plot_state_city()` pour visualiser la matrice densité. Test de CHSH |
| **Cirq** | Construction équivalente. Mise en évidence du non-signalement |
| **Notions** | Intrication, CHSH, matrice densité, mesure partielle |

#### Laboratoire 3 — Canaux de bruit et décohérence (Semaine 4)

| Aspect | Détail |
|--------|--------|
| **Objectifs** | Simuler des canaux quantiques réalistes, observer la décohérence et la relaxation |
| **QuTiP** | Résolution de l'équation maîtresse de Lindblad : `mesolve()`. Canaux dépolarisant, bit-flip, phase-flip. Temps T₁ et T₂ : `lindblad` avec σ₋, σ_z. Visualisation de l'évolution de la matrice densité |
| **Qiskit** | `NoiseModel` avec les mêmes canaux. Ajout de bruit à un circuit. Comparaison simulation bruitée vs. idéale |
| **Stim** | Modèle de bruit Pauli en correction d'erreur |
| **Notions** | Opérateurs de Kraus, T₁/T₂, équation de Lindblad, modèle de bruit |

#### Laboratoire 4 — Circuit quantique et téléportation (Semaine 3)

| Aspect | Détail |
|--------|--------|
| **Objectifs** | Implémenter la téléportation quantique, simuler chaque étape physique |
| **QuTiP** | Simulation du circuit avec opérateurs unitaires. Visualisation du transfert d'état via la matrice densité |
| **Qiskit** | Circuit de téléportation avec mesures et opérations conditionnelles classiques. Exécution sur simulateur Aer |
| **Cirq** | Implémentation similaire avec mesures et `ClassicalRegister` |
| **Notions** | Téléportation, mesure projective, feed-forward classique, codage superdense |

#### Laboratoire 5 — Algorithme de Deutsch–Jozsa (Semaine 5)

| Aspect | Détail |
|--------|--------|
| **Objectifs** | Implémenter le premier algorithme quantique à avantage prouvé, analyser l'oracle |
| **Qiskit** | Construction de l'oracle pour fonctions constantes vs. équilibrées à n qubits. Exécution, mesure, interprétation |
| **QuTiP** | Simulation du Hamiltonien d'évolution pour comprendre la dynamique des portes de Hadamard |
| **Notions** | Parallélisme quantique, oracle, promesse, accélération |

#### Laboratoire 6 — QFT et estimation de phase quantique (Semaine 6)

| Aspect | Détail |
|--------|--------|
| **Objectifs** | Implémenter la transformée de Fourier quantique, l'utiliser pour l'estimation de phase |
| **Qiskit** | Circuit QFT récursif. Circuit QPE complet. Analyse de la précision en fonction du nombre de qubits |
| **Cirq** | Optimisation du circuit par décomposition en portes élémentaires |
| **QuTiP** | Simulation de l'évolution Hamiltonienne derrière QPE |
| **Notions** | QFT, QPE, précision, porte contrôlée, superposition |

#### Laboratoire 7 — Algorithme de Shor et factorisation (Semaine 7)

| Aspect | Détail |
|--------|--------|
| **Objectifs** | Implémenter la factorisation de N=15 (et plus), analyser la recherche de période |
| **Qiskit** | Circuit modulaire : QPE + exponentiation modulaire. Shor pour 15 = 3 × 5. Extension à des nombres plus grands |
| **Cirq** | Implémentation alternative avec optimisation des portes |
| **Notions** | Période, exponentiation modulaire, ordre, RSA |

#### Laboratoire 8 — Algorithme de recherche de Grover (Semaine 8)

| Aspect | Détail |
|--------|--------|
| **Objectifs** | Implémenter la recherche non-structurée, analyser la complexité O(√N) |
| **Qiskit** | Oracle pour marquer un état. Diffuseur de Grover (inversion autour de la moyenne). Généralisation à M solutions |
| **Cirq** | Optimisation du nombre de portes |
| **QuTiP** | Simulation de l'évolution Hamiltonienne de l'algorithme |
| **Notions** | Oracle, amplification d'amplitude, rotation de Grover, optimalité |

#### Laboratoire 9 — Correction d'erreur : code à répétition (Semaine 9)

| Aspect | Détail |
|--------|--------|
| **Objectifs** | Implémenter le code à répétition quantique, détecter et corriger les erreurs |
| **QuTiP** | Simulation du code à 3 qubits : encodage, injection d'erreur, syndrome, correction. Visualisation sur la sphère de Bloch |
| **Qiskit** | Circuit encodeur, détection de syndrome (portes CNOT+mesure), correction conditionnelle |
| **Stim** | Circuit stabilisateur équivalent, décodage, seuil d'erreur |
| **Notions** | Syndrome, code distance, détection vs. correction, seuil |

#### Laboratoire 10 — Codes de surface et décodage (Semaine 10)

| Aspect | Détail |
|--------|--------|
| **Objectifs** | Simuler un code de surface, implémenter un décodeur |
| **Stim** | Génération de circuits de code de surface (rotated surface code). Extraction de syndrome. Décodage MWPM via `pymatching` |
| **Qiskit** | Transpilation du code de surface sur un graphe de qubits |
| **Notions** | Grille 2D, stabilisateurs, matching, correction topologique |

#### Laboratoire 11 — VQE et chimie quantique (Semaine 12)

| Aspect | Détail |
|--------|--------|
| **Objectifs** | Calculer l'état fondamental d'une molécule simple (H₂, LiH) par variational quantum eigensolver |
| **PennyLane** | Définition d'un ansatz (UCCSD, hardware-efficient). Fonction de coût : `ExpvalCost` avec Hamiltonien moléculaire. Optimisation classique-quantique hybride (Adam, SPSA). Différentiation automatique du circuit |
| **Qiskit Nature** | Construction de l'Hamiltonien via `PySCFDriver`. Exécution VQE sur simulateur |
| **Notions** | VQE, ansatz, Hamiltonien, minimisation variationnelle |

#### Laboratoire 12 — QAOA pour l'optimisation combinatoire (Semaine 13)

| Aspect | Détail |
|--------|--------|
| **Objectifs** | Résoudre MaxCut sur un graphe avec l'algorithme d'optimisation approximatif quantique |
| **PennyLane** | Implémentation du circuit QAOA (couches de mélangeur + phase separator). Optimisation des angles (β, γ) |
| **Qiskit** | `QAOA` depuis `qiskit-optimization`. Comparaison avec solveur classique |
| **Notions** | Hamiltonien d'optimisation, mélangeur, couches QAOA, approximation ratio |

#### Laboratoire 13 — Exécution sur machines réelles (Semaine 14)

| Aspect | Détail |
|--------|--------|
| **Objectifs** | Exécuter un circuit sur du matériel quantique réel via le cloud, analyser le bruit |
| **IBM Quantum** | Soumission d'un circuit Bell sur `ibm_brisbane` (127 qubits). Analyse des erreurs, calibration |
| **Amazon Braket** | Exécution sur Rigetti (supraconducteur) et IonQ (ions piégés). Comparaison des fidélités |
| **Analyse** | Histogrammes des résultats, mitigation d'erreur par `zero-noise extrapolation` |
| **Notions** | NISQ, calibration, readout error, gate error, mitigation |

### 7.3 Projets

#### Projet de mi-parcours (Semaine 7 — 20 % de la note)

Implémentation complète d'un algorithme quantique avec analyse de bruit :
- **Choix 1 — Shor factoriel** : Circuit complet de factorisation de N=15, 21, ou 33 avec analyse de la probabilité de succès en fonction du bruit (modèle de décohérence QuTiP)
- **Choix 2 — Grover avec bruit** : Implémentation de la recherche avec analyse de la dégradation de l'amplification d'amplitude sous bruit dépolarisant

#### Projet final (Semaine 14 — 30 % de la note)

Au choix parmi :

1. **Chaîne complète de correction d'erreur** : Implémentation d'un code de surface (Stim), ajout de bruit réaliste (QuTiP), décodage (pymatching), calcul du seuil de tolérance
2. **Application QML** : Classification de données (iris, wine) avec un circuit variationnel (PennyLane), comparaison classique vs. quantique
3. **Simulation d'un processeur quantique complet** : Utilisation de QuTiP-QIP pour simuler un processeur à N qubits avec Hamiltonien réaliste, couplages, et bruit
4. **Benchmark multi-plateforme** : Implémentation du VQE pour H₂ sur IBM, IonQ (via Braket), et simulateur. Analyse comparative des ressources, fidélité, et coût

---

## 8. Évaluation

| Élément | Poids | Description |
|---------|-------|-------------|
| **Devoirs** (×4) | 40 % | Problèmes théoriques + implémentations |
| **Projet de mi-parcours** | 20 % | Implémentation et analyse d'un algorithme quantique (Shor ou Grover avancé) avec analyse de complexité et bruit |
| **Projet final** | 30 % | Chaîne complète : correction d'erreur sur un circuit réel, démonstration d'un protocole tolérant aux fautes, ou application QML |
| **Présentation orale** | 10 % | Analyse critique d'un article de recherche récent (2024–2026) parmi une liste fournie |

---

## 9. Ressources complémentaires

### Cours en ligne et vidéos
- **MIT 18.435J** — Quantum Computation (Peter Shor) — MIT OCW
- **Caltech Ph229** — Quantum Computation (John Preskill) — theory.caltech.edu/~preskill/ph229
- **Qiskit Textbook** — qiskit.org/learn
- **IBM Quantum Learning** — learning.quantum.ibm.com
- **Qubit by Qubit** (The Coding School) — qubitbyqubit.org

### Logiciels et SDK
- **Qiskit** (IBM) — github.com/Qiskit/qiskit — SDK le plus populaire, circuits + Aer + accès IBM
- **QuTiP** (RIKEN) — github.com/qutip/qutip — Simulation physique de qubits, équation maîtresse, Hamiltoniens
- **Cirq** (Google) — github.com/quantumlib/Cirq — Circuits NISQ, optimisation
- **PennyLane** (Xanadu) — github.com/PennyLaneAI/pennylane — QML, différentiation automatique, VQE, QAOA
- **Stim** (Google) — github.com/quantumlib/Stim — Simulation ultra-rapide de circuits stabilisateurs
- **Qualtran** (Google) — github.com/quantumlib/Qualtran — Algorithmes tolérants aux fautes
- **Amazon Braket** — github.com/amazon-braket/amazon-braket-sdk-python — Accès multi-plateforme
- **Cuda-Q** (NVIDIA) — github.com/NVIDIA/cuda-quantum — Simulation GPU-accélérée
- **pymatching** — github.com/oscarhiggott/PyMatching — Décodage MWPM pour codes de surface

### Conférences et séminaires
- **QIP** (Quantum Information Processing) — conférence annuelle
- **QEC** (Quantum Error Correction) — workshop annuel
- **IEEE QCE** (IEEE International Conference on Quantum Computing and Engineering)
- **APS March Meeting** — sessions quantiques

---

*Dernière mise à jour : Juin 2026*

*Ce syllabus intègre les résultats de recherche les plus récents issus de Nature, Science, Physical Review Letters, arXiv, et des conférences CAV, QIP et IEEE QCE. Les références aux publications de Google Quantum AI, IBM Quantum, Microsoft Quantum, Harvard/MIT/CALTECH et QuEra Computing sont citées tout au long du cours.*
