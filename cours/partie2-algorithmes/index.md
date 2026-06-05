# Partie 2 — Algorithmes quantiques

## Table des matières

| Séance | Titre | Sujets | Oracle | QPE | QFT | Grover |
|--------|-------|--------|--------|-----|-----|--------|
| 5.1 | Deutsch-Jozsa | Parallélisme quantique, promesse constante/équilibrée | ✓ | | | |
| 5.2 | Simon | Période cachée, sous-groupe abélien, transformée Hadamard | ✓ | | ✓ | |
| 6.1 | QFT | Transformée de Fourier quantique, circuit $O(n^2)$, récursivité | | | ✓ | |
| 6.2 | QPE | Estimation de phase, précision, portes contrôlées | | ✓ | ✓ | |
| 7.1 | Shor | Factorisation, exponentiation modulaire, $N=15$, RSA | ✓ | ✓ | ✓ | |
| 7.2 | Cryptographie | BB84, E91, sécurité informationnelle, post-quantique | | | | |
| 8.1 | Grover | Recherche $O(\sqrt{N})$, oracle, diffusion, optimalité | ✓ | | | ✓ |
| 8.2 | Applications Grover | Comptage quantique, NP, bornes inférieures, bruit | ✓ | ✓ | | ✓ |

## Progression pédagogique

```
Partie 1 — Fondamentaux
    ↓
Partie 2 — Algorithmes (ce document)
    ├── 5.1 Deutsch-Jozsa   (parallélisme, oracle simple)
    ├── 5.2 Simon           (période cachée, Hadamard)
    ├── 6.1 QFT             (transformée de Fourier quantique)
    ├── 6.2 QPE             (estimation de phase)
    ├── 7.1 Shor            (factorisation, QPE + QFT)
    ├── 7.2 Cryptographie   (QKD, post-quantique)
    ├── 8.1 Grover          (recherche, amplification)
    └── 8.2 Applications    (comptage, NP, bruit)
    ↓
Partie 3 — Correction d'erreur et implantation
```

## Complexités comparées

| Problème | Classique | Quantique | Accélération |
|----------|-----------|-----------|--------------|
| Deutsch-Jozsa | $O(2^{n})$ | $O(1)$ | Exponentielle |
| Simon | $O(2^{n/2})$ | $O(n)$ | Exponentielle |
| Factorisation | $\exp(O(n^{1/3}))$ | $O(n^3)$ | Exponentielle |
| Recherche | $O(N)$ | $O(\sqrt{N})$ | Quadratique |
| Comptage | $O(1/\epsilon^2)$ | $O(1/\epsilon)$ | Quadratique |

## Bibliographie commune

- Nielsen, M. A. & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*. Cambridge University Press.
- Kaye, P., Laflamme, R. & Mosca, M. (2007). *An Introduction to Quantum Computing*. Oxford University Press.
- Mermin, N. D. (2007). *Quantum Computer Science*. Cambridge University Press.
- Qiskit Textbook : https://qiskit.org/textbook/
- Cirq Documentation : https://quantumai.google/cirq
- QuTiP Documentation : http://qutip.org/docs/latest/
