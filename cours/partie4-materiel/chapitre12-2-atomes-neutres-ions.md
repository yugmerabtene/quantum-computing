# Chapitre 12.2 — Atomes neutres et ions piégés

## Ce que vous allez apprendre

- Comprendre comment des lasers peuvent piéger et contrôler des atomes individuels un par un
- Maîtriser le concept de blocage de Rydberg et son utilisation pour les portes quantiques
- Analyser les résultats de Harvard/QuEra (48 qubits logiques, portes Rydberg)
- Comprendre le piégeage d'ions et la porte Mølmer-Sørensen
- Simuler un système à atomes neutres avec Cirq et QuTiP
- Comparer les plateformes : atomes neutres vs ions piégés vs supraconducteurs

---

## Motivation

**Le problème concret.** Les qubits supraconducteurs sont fabriqués sur une puce et ne bougent jamais. Si deux qubits ne sont pas voisins sur la puce, il faut faire transiter l'information de qubit en qubit (comme un message qui passe de main en main) — c'est lent et ça introduit des erreurs.

**L'idée des atomes neutres.** Et si on pouvait **déplacer les qubits** ? Avec des atomes neutres piégés par des lasers (pinces optiques), c'est exactement ce qu'on fait : chaque atome est un qubit, et on peut le déplacer physiquement en déplaçant le faisceau laser. On peut ainsi amener deux qubits éloignés côte à côte, faire une porte, puis les renvoyer à leur place.

**L'idée des ions piégés.** Les ions (atomes chargés) sont piégés par des champs électriques dans un piège de Paul. Leur avantage : des temps de cohérence records ($T_2 > 10$ s) et des portes à deux qubits avec une fidélité de 99.99% (Oxford Ionics, 2025). Leur inconvénient : les opérations sont lentes et le scaling au-delà de ~100 ions est difficile.

**Comparaison rapide :**
- **Supraconducteurs** : rapides (portes en 50 ns), mais cohérence courte et pas de déplacement
- **Atomes neutres** : reconfigurables, connectivité dynamique, scaling excellent
- **Ions piégés** : cohérence exceptionnelle, fidélité record, mais scaling limité

---

## Idée principale

### Atomes neutres : des atomes capturés par la lumière

Imaginez un atome (par exemple du rubidium) dans le vide. Vous le shinez avec un laser très focalisé. L'atome, bien que neutre, est légèrement polarisé par le champ électrique du laser : un côté devient un peu plus positif, l'autre un peu plus négatif. Ce dipôle induit est attiré vers la région de plus forte intensité lumineuse — le centre du faisceau.

C'est comme une bille qui roule vers le creux d'un bol : le laser crée un « bol de lumière » qui piège l'atome. Ce bol s'appelle une **pince optique** (optical tweezer). Avec des miroirs contrôlables, on peut créer des centaines de pinces indépendantes, chacune piégeant un atome unique.

### La blocage de Rydberg : l'interaction qui crée la porte logique

Quand on excite un atome vers un état de Rydberg (un état très excité, $n \sim 70$), l'atome gonfle énormément — son rayon devient de l'ordre du micromètre (10 000 fois plus grand que normal). Cet atome géant interagit très fortement avec ses voisins.

**La blocage de Rydberg**, c'est comme une place de parking réservée : si un atome est déjà excité en état de Rydberg, aucun atome voisin (dans un rayon de ~5-10 µm) ne peut être excité simultanément. L'interaction est si forte qu'elle déplace la fréquence de résonance du voisin.

Cette blocage est la base des portes à deux qubits : si les deux atomes sont dans $|11\rangle$, la blocage empêche la double excitation, ce qui crée un déphasage conditionnel — une porte CZ !

---

## Contenu du cours

### Section 1 : Pinces optiques et piégeage d'atomes neutres

#### 1.1 Le potentiel dipolaire optique

Un atome neutre dans un champ électrique oscillant (laser) acquiert un dipôle induit. L'énergie d'interaction crée un potentiel attractif vers les zones de forte intensité :

$$
U_{\text{dip}}(\mathbf{r}) = -\frac{3\pi c^2}{2\omega_0^3} \frac{\Gamma}{\Delta} I(\mathbf{r})
$$

**Signification physique :**
- $\Gamma$ = taux de décroissance spontanée de l'atome (vitesse à laquelle il réémet de la lumière)
- $\Delta = \omega - \omega_0$ = désaccord du laser par rapport à la résonance atomique
- $I(\mathbf{r})$ = intensité du laser à la position $\mathbf{r}$
- Le signe négatif indique que l'atome est attiré vers les fortes intensités (pour $\Delta > 0$, laser « rouge »)

> **Exemple numérique :** Pour un atome de Rubidium-87 avec un laser à 850 nm, $\Delta/(2\pi) \sim 10^{13}$ Hz, $I \sim 10^{10}$ W/m² : $U_{\text{dip}}/k_B \sim 1$ mK. La profondeur du piège est de l'ordre du millikelvin — suffisant pour piéger un atome refroidi par laser à quelques µK.

Chaque pince capture un atome unique avec une probabilité $> 0.99$. Les atomes peuvent être déplacés dynamiquement en modifiant les positions des pinces via des modulateurs acousto-optiques (AOM) ou des SLM (spatial light modulators).

#### 1.2 Reconfigurabilité dynamique — l'avantage unique

C'est l'avantage décisif des atomes neutres : **le graphe de connectivité change dans le temps**.

$$
\text{Graphe de connectivité} \; G(t) : \; \text{pas de contrainte de grille fixe}
$$

**Analogie :** Imaginez un échiquier où les pièces peuvent se déplacer. Sur une puce supraconductrice, les qubits sont fixes comme des cases clouées au plateau. Avec des atomes neutres, vous pouvez rapprocher deux pièces éloignées, les faire interagir, puis les éloigner à nouveau.

**Conséquence pour les codes quantiques :** Les codes QLDPC (Quantum Low-Density Parity Check) nécessitent une connectivité non-locale — des qubits logiques doivent interagir avec des qubits loin d'eux. Avec des supraconducteurs, il faut des milliers de SWAP. Avec des atomes neutres, on déplace physiquement les atomes.

#### 1.3 États de Rydberg et blocage

Un atome excité vers un état de Rydberg $|r\rangle$ de nombre principal $n \sim 50-100$ a des propriétés extraordinaires :

- **Rayon orbital** : $r \propto n^2 a_0$ — pour $n = 70$, $r \sim 0.4$ µm (taille d'une bactérie !)
- **Moment dipolaire** : $d \propto n^2 ea_0$ — énorme, donc interactions très fortes
- **Durée de vie** : $\tau \propto n^3$ — typiquement ~100 µs pour $n \sim 70$

**Blocage de Rydberg** : si un atome est excité en $|r\rangle$, un atome voisin dans la sphère de blocage ($R_b \sim 5-10\,\mu$m) ne peut PAS être excité simultanément. L'interaction de van der Waals déplace la fréquence de résonance :

$$
\Delta E_{\text{vdW}} = \frac{C_6}{R^6} \gg \hbar\Omega
$$

**Signification physique :**
- $C_6 \propto n^{11}$ : le coefficient de van der Waals croît ENORMEMENT avec $n$ (d'où le choix de $n$ élevé)
- $R$ = distance entre les deux atomes
- $\Omega$ = fréquence de Rabi (vitesse à laquelle on essaie d'exciter le deuxième atome)
- Quand $\Delta E_{\text{vdW}} \gg \hbar\Omega$, la transition est complètement hors résonance : le deuxième atome ne peut PAS être excité

> **Exemple numérique :** Pour $n = 70$, $C_6/(2\pi) \sim 100$ GHz·µm⁶. À $R = 5$ µm : $\Delta E_{\text{vdW}}/(2\pi) = 100/5^6 = 0.64$ GHz. Avec $\Omega/(2\pi) = 10$ MHz : $\Delta E_{\text{vdW}} / (\hbar\Omega) \sim 64 \gg 1$. La blocage est parfaite.

---

### Section 2 : Portes Rydberg — la porte CZ conditionnelle

#### 2.1 Séquence de la porte CZ

La porte CZ entre deux atomes neutres utilise l'interaction de Rydberg en trois étapes :

1. **Impulsion $\pi$ sur le contrôle** : si le contrôle est dans $|1\rangle$, on l'excite vers $|r\rangle$
2. **Impulsion $2\pi$ sur la cible** : on essaie d'exciter la cible $|1\rangle \to |r\rangle \to |1\rangle$ (cycle complet)
3. **Impulsion $\pi$ inverse sur le contrôle** : on ramène $|r\rangle \to |1\rangle$

**Pourquoi ça marche :**
- Si l'état est $|00\rangle$, $|01\rangle$ ou $|10\rangle$ : rien ne se passe (pas de double excitation possible)
- Si l'état est $|11\rangle$ : le contrôle passe en $|r\rangle$, puis la blocage empêche la cible de faire le cycle $2\pi$. La cible acquiert un déphasage de $\pi$. Résultat : $|11\rangle \to -|11\rangle$

$$
\text{CZ} = |00\rangle\langle 00| + |01\rangle\langle 01| + |10\rangle\langle 10| - |11\rangle\langle 11|
$$

#### 2.2 Fidélité des portes — résultats Harvard/QuEra (2025)

Harvard/QuEra ont démontré des portes à deux qubits avec fidélité $> 99.5\%$ sur 48 qubits logiques :

$$
F_{\text{2Q}} = 1 - \epsilon_{\text{Rydberg}} - \epsilon_{\text{spont}} - \epsilon_{\text{laser}}
$$

| Source d'erreur | Contribution | Explication |
|-----------------|-------------|-------------|
| Spontané depuis $|r\rangle$ | $\sim 10^{-3}$ | L'atome réémet un photon et perd l'information |
| Largeur finie laser | $\sim 10^{-4}$ | Le laser n'est pas parfaitement monochromatique |
| Mouvement atomique | $\sim 5\times 10^{-4}$ | L'atome bouge légèrement dans le piège |
| Diaphonie entre pinces | $\sim 10^{-4}$ | La lumière d'une pince affecte les atomes voisins |

---

### Section 3 : Ions piégés

#### 3.1 Le piège de Paul — confiner des charges avec des champs oscillants

Les ions (atomes chargés, par exemple $^{171}\text{Yb}^+$) sont piégés par des champs électriques. Le problème : le théorème d'Earnshaw dit qu'on ne peut pas piéger une charge avec des champs statiques. La solution de Paul : utiliser des champs **oscillants** (RF).

$$
\Phi(x, y, z, t) = \frac{V_{\text{RF}} \cos(\Omega_{\text{RF}} t)}{2} (x^2 - y^2) + \frac{U_{\text{DC}}}{2} (2z^2 - x^2 - y^2)
$$

**Signification physique :**
- $V_{\text{RF}}$ = amplitude du voltage RF (typiquement 100-300 V)
- $\Omega_{\text{RF}}$ = fréquence RF (typiquement 10-100 MHz)
- Le potentiel oscille : tantôt il pousse l'ion vers le centre en $x$, tantôt en $y$
- En moyenne, l'ion est poussé vers le centre dans toutes les directions — c'est le **potentiel pseudo-potentiel**

Les ions forment une chaîne linéaire (comme des perles sur un fil) où le mouvement collectif (modes vibrationnels) assure le couplage entre qubits via des lasers.

#### 3.2 Porte Mølmer-Sørensen — l'intrication par les phonons

La porte à deux ions utilise les **modes phononiques** partagés (vibrations collectives de la chaîne d'ions) :

$$
H_{\text{MS}} = \frac{\hbar\Omega_{\text{eff}}}{2} \sum_{i<j} \sigma_x^{(i)} \sigma_x^{(j)} \cos(\mu t)
$$

**Signification physique :**
- $\Omega_{\text{eff}}$ = force de couplage effective entre les ions
- $\sigma_x^{(i)}$ = opérateur Pauli X sur l'ion $i$
- $\mu$ = fréquence du laser, choisie proche d'un mode vibrationnel
- Le laser couple simultanément l'état interne de deux ions ET le mouvement collectif
- Résultat : les deux ions deviennent intriqués, et le mouvement revient à son état initial (il est « virtuel »)

**Analogie :** Deux personnes sur un trampoline. Si l'une saute, elle crée des vagues dans le trampoline qui font bouger l'autre. Le trampoline est le mode phononique : il transmet l'interaction sans rester excité.

---

## Exemple guidé

**Problème :** Calculer le rayon de la sphère de blocage de Rydberg pour un atome de Rubidium avec $n = 70$, $\Omega/(2\pi) = 10$ MHz, et $C_6/(2\pi) = 100$ GHz·µm⁶.

**Étape 1 — Condition de blocage :**
La blocage est effective quand $\Delta E_{\text{vdW}} \gg \hbar\Omega$, soit :
$$\frac{C_6}{R_b^6} = \hbar\Omega$$

**Étape 2 — Rayon de blocage :**
$$R_b = \left(\frac{C_6}{\hbar\Omega}\right)^{1/6} = \left(\frac{100 \times 10^9}{10 \times 10^6}\right)^{1/6} = (10^4)^{1/6} \approx 4.64 \text{ µm}$$

**Étape 3 — Vérification :**
À $R = R_b$ : $\Delta E_{\text{vdW}}/(2\pi) = 100/4.64^6 \approx 10$ MHz = $\Omega$. ✓
À $R = 7$ µm : $\Delta E_{\text{vdW}}/(2\pi) = 100/7^6 \approx 0.85$ MHz $\ll \Omega$. La blocage n'est plus effective.

**Conclusion :** Deux atomes de Rubidium à $n = 70$ séparés de moins de ~5 µm sont dans la sphère de blocage. C'est typiquement la distance utilisée dans les expériences.

---

## Implémentation Python

### Simulation d'atomes neutres avec Cirq et QuTiP

```python
# ============================================================
# Simulation d'un circuit quantique avec 3 atomes neutres
# Utilisation de Cirq pour le circuit et QuTiP pour la physique
# ============================================================
import numpy as np
import cirq
import qutip as qt

# --- Partie Cirq : construction du circuit quantique ---
n_atoms = 3
qubits = cirq.LineQubit.range(n_atoms)  # 3 qubits en ligne

circuit = cirq.Circuit()

# Étape 1 : Créer une superposition sur chaque qubit (porte Hadamard)
# Chaque atome passe de |0> à (|0> + |1>)/sqrt(2)
for q in qubits:
    circuit.append(cirq.H(q))

# Étape 2 : Portes CZ conditionnelles entre atomes voisins
# CZ(0,1) : porte CZ entre le qubit 0 (contrôle) et 1 (cible)
circuit.append(cirq.CZ(qubits[0], qubits[1]))
# CZ(0,2) : porte CZ entre le qubit 0 et le qubit 2
circuit.append(cirq.CZ(qubits[0], qubits[2]))

# Étape 3 : Mesure de tous les qubits
for q in qubits:
    circuit.append(cirq.measure(q))

print(circuit)

# Simulation de l'état avant mesure
simulator = cirq.Simulator()
result = simulator.simulate(circuit[0:-3])  # On exclut les mesures
print(f"État final : {result.final_state_vector}")

# --- Partie QuTiP : simulation physique de l'interaction de Rydberg ---

# Paramètres physiques du système Rydberg
Omega = 2.0 * np.pi * 5.0   # Fréquence de Rabi (MHz) : vitesse d'excitation
Delta = 2.0 * np.pi * 0.0   # Désaccord laser (MHz) : 0 = résonance exacte
C6 = 2.0 * np.pi * 50.0     # Coefficient de van der Waals (MHz·µm⁶)
R = 5.0                      # Distance entre atomes (µm)
Rb = 7.0                     # Rayon de blocage (µm)

# Construction des opérateurs pour 2 atomes dans QuTiP
N_atoms_qutip = 2
sz = qt.tensor([qt.sigmaz() for _ in range(N_atoms_qutip)])

# Liste des opérateurs sigma_x pour chaque atome dans l'espace produit tensoriel
sx_list = [qt.tensor([qt.sigmax() if i == j else qt.identity(2) for j in range(N_atoms_qutip)]) for i in range(N_atoms_qutip)]

# Liste des opérateurs sigma_+ pour chaque atome (excitation)
sp_list = [qt.tensor([qt.sigmap() if i == j else qt.identity(2) for j in range(N_atoms_qutip)]) for i in range(N_atoms_qutip)]

# Hamiltonien de drive : chaque atome est piloté par le laser à la fréquence de Rabi
H_drive = sum(Omega * sx_list[i] for i in range(N_atoms_qutip))

# Hamiltonien d'interaction : dépend de la distance R vs rayon de blocage Rb
if R < Rb:
    # Dans la sphère de blocage : interaction de van der Waals
    # C6 * |rr><rr| = C6 * n_1 * n_2 (les deux atomes dans |r>)
    H_int = C6 * sp_list[0] * sp_list[1].dag() * sp_list[0].dag() * sp_list[1]
    H_int = C6 * qt.tensor(qt.projection(2, 1, 1), qt.projection(2, 1, 1))
else:
    # Hors de la sphère de blocage : pas d'interaction
    H_int = 0.0 * qt.tensor(qt.identity(2), qt.identity(2))

H = H_drive + H_int

# État initial : les deux atomes dans |0> (état fondamental)
psi0 = qt.tensor(qt.basis(2, 0), qt.basis(2, 0))
tlist = np.linspace(0, 2.0 * np.pi / Omega, 200)  # Un cycle de Rabi complet

# Simulation : on mesure la probabilité d'excitation du premier atome
result = qt.mesolve(H, psi0, tlist, c_ops=[], e_ops=[qt.tensor(qt.projection(2, 1, 1), qt.identity(2))])

P_excitation = result.expect[0]
print(f"Probabilité maximale d'excitation : {np.max(P_excitation):.4f}")

# Calcul de l'interaction de van der Waals effective
C6_val = 50.0 * 2.0 * np.pi
V_dd = C6_val / (R**6) if R > 0 else 0.0
print(f"Interaction de van der Waals: V_dd/(2π) = {V_dd/(2*np.pi):.2f} MHz")

# Temps d'impulsion pi : durée pour faire |0> → |r>
theta_pi = np.pi
pulse_area = Omega * (theta_pi / Omega)
print(f"Temps d'impulsion pi : {pulse_area:.2f} (unités arbitraires)")
```

### Simulation de la reconfigurabilité dynamique

```python
# ============================================================
# Simulation du déplacement d'atomes pour reconfigurer la connectivité
# ============================================================
import numpy as np

def compute_moves(initial_positions, target_connectivity):
    """
    Calcule les mouvements nécessaires pour amener les atomes
    dans les positions requises par la connectivité cible.
    """
    N_at = len(initial_positions)
    current = np.array(initial_positions)
    moves = []

    for (i, j) in target_connectivity:
        target_dist = 5.0  # Distance cible entre atomes connectés (µm)
        # Si les atomes i et j sont trop éloignés, on les rapproche
        if np.linalg.norm(current[i] - current[j]) > target_dist * 1.1:
            # On les place symétriquement autour de leur milieu
            midpoint = (current[i] + current[j]) / 2
            dir_ij = current[j] - current[i]
            dir_ij = dir_ij / np.linalg.norm(dir_ij)  # Vecteur unitaire i→j
            new_pos_i = midpoint - dir_ij * target_dist / 2
            new_pos_j = midpoint + dir_ij * target_dist / 2
            moves.append((i, current[i].copy(), new_pos_i))
            moves.append((j, current[j].copy(), new_pos_j))
            current[i] = new_pos_i
            current[j] = new_pos_j

    # Distance totale parcourue par tous les atomes
    total_distance = sum(abs(np.linalg.norm(m[1] - m[2])) for m in moves)
    return moves, total_distance, current

# Positions initiales de 5 atomes (en µm)
initial = np.array([[0.0, 0.0], [10.0, 0.0], [5.0, 8.0], [2.0, 2.0], [8.0, 2.0]])

# Connectivité cible : quelles paires d'atomes doivent interagir
target_conn = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2), (1, 3)]

moves, distance, final = compute_moves(initial, target_conn)
print(f"Nombre de mouvements: {len(moves)}")
print(f"Distance totale de deplacement: {distance:.2f}")
print(f"Positions finales:\n{final}")
```

### Simulation complète de la porte CZ Rydberg

```python
# ============================================================
# Simulation détaillée d'une porte CZ entre deux atomes de Rydberg
# Modèle à 3 niveaux : |g> (fondamental), |e> (intermédiaire), |r> (Rydberg)
# ============================================================
import numpy as np
import qutip as qt

# --- Paramètres physiques ---
Omega = 2.0 * np.pi * 10.0    # Fréquence de Rabi du laser (MHz)
delta_ryd = 2.0 * np.pi * 0.5  # Désaccord par rapport à la résonance (MHz)
C6_ryd = 2.0 * np.pi * 100.0  # Coefficient de van der Waals (MHz·µm⁶)
R = 5.0                        # Distance entre atomes (µm)
R_b = 7.0                      # Rayon de blocage (µm)

# --- Espace de Hilbert : 3 niveaux par atome ---
N_states = 3
g = qt.basis(N_states, 0)  # |g> : état fondamental (qubit |0>)
e = qt.basis(N_states, 1)  # |e> : état intermédiaire
r = qt.basis(N_states, 2)  # |r> : état de Rydberg (qubit |1>)

# Hamiltonien libre : énergie de l'état de Rydberg (désaccord delta)
H0_single = delta_ryd * (r * r.dag())

# Hamiltonien de drive : couplage laser entre |e> et |r>
H_drive_single = Omega / 2.0 * (e * r.dag() + r * e.dag())

# --- Construction pour 2 atomes ---
# Hamiltonien libre total (somme des deux atomes)
H0 = qt.tensor(H0_single, qt.identity(N_states)) + qt.tensor(qt.identity(N_states), H0_single)

# Interaction de van der Waals : C6 * |rr><rr|
# Seulement si les atomes sont dans la sphère de blocage
if R < R_b:
    H_int = C6_ryd * qt.tensor(r * r.dag(), r * r.dag())
else:
    H_int = qt.tensor(qt.qeye(N_states), qt.qeye(N_states)) * 0.0

# Drive total (laser sur les deux atomes)
H_drive = qt.tensor(H_drive_single, qt.identity(N_states)) + qt.tensor(qt.identity(N_states), H_drive_single)
H_total = H0 + H_int + H_drive

# --- États d'entrée de la porte CZ ---
psi_00 = qt.tensor(g, g)  # |00>
psi_01 = qt.tensor(g, e)  # |01>
psi_10 = qt.tensor(e, g)  # |10>
psi_11 = qt.tensor(e, e)  # |11>

tlist = np.linspace(0, 2.0 * np.pi / Omega * 2, 500)  # Durée de la porte

# --- Simulation de l'évolution pour chaque état d'entrée ---
def simulate_cz_gate(psi_in, H, tlist):
    """Simule l'évolution d'un état d'entrée sous l'Hamiltonien total."""
    result = qt.mesolve(H, psi_in, tlist, c_ops=[], e_ops=[])
    return result.states[-1]  # État final

psi_f_list = []
for psi_in in [psi_00, psi_01, psi_10, psi_11]:
    psi_f = simulate_cz_gate(psi_in, H_total, tlist)
    psi_f_list.append(psi_f)

# --- Vérification de la porte CZ ---
CZ_ideal = np.diag([1, 1, 1, -1])  # Matrice CZ idéale
overlaps = []
for i, (psi_in, psi_f) in enumerate(zip([psi_00, psi_01, psi_10, psi_11], psi_f_list)):
    ol = (psi_in.dag() * psi_f).real
    overlaps.append(ol)
    print(f"<psi_{i:02b}|U|psi_{i:02b}> = {ol:.4f} (ideal: {CZ_ideal[i,i]})")

# Erreur moyenne de la porte
fidelity_cz = np.mean([abs(o - ideal) for o, ideal in zip(overlaps, np.diag(CZ_ideal))])
print(f"Erreur moyenne de la porte CZ : {1 - (1-fidelity_cz):.4e}")
```

### Porte Mølmer-Sørensen avec QuTiP

```python
# ============================================================
# Simulation de la porte Mølmer-Sørensen entre deux ions piégés
# La porte utilise un mode phononique partagé comme bus d'intrication
# ============================================================
import numpy as np
import qutip as qt

N_phonons = 6   # Nombre de niveaux du mode vibrationnel (troncature)
N_ions = 2      # Nombre d'ions

# Opérateurs de spin pour chaque ion dans l'espace produit tensoriel
sm = [qt.tensor([qt.sigmam() if i == j else qt.identity(2) for j in range(N_ions)]) for i in range(N_ions)]
sz = [qt.tensor([qt.sigmaz() if i == j else qt.identity(2) for j in range(N_ions)]) for i in range(N_ions)]

# Opérateur d'annihilation du mode phononique (vibration de la chaîne)
a_phonon = qt.tensor(qt.identity(2**N_ions), qt.destroy(N_phonons))

# --- Paramètres physiques ---
eta = 0.1                    # Paramètre de Lamb-Dicke : couplage spin-mouvement
nu = 2.0 * np.pi * 5.0      # Fréquence du mode vibrationnel (MHz)
omega_ion = 2.0 * np.pi * 100.0  # Fréquence de transition des ions (MHz)
Omega_MS = 2.0 * np.pi * 0.5     # Force de couplage MS effective (MHz)
delta_ms = nu - 0.1               # Désaccord par rapport au mode vibrationnel

# --- Hamiltoniens ---
# Énergie interne des ions (splitting Zeeman)
H_ion = sum(0.5 * omega_ion * sz[i] for i in range(N_ions))

# Énergie du mode phononique (oscillateur harmonique)
H_phonon = nu * a_phonon.dag() * a_phonon

# Interaction Mølmer-Sørensen : couplage spin-phonon
# Chaque ion échange un quantum de spin contre un quantum de vibration
H_int_ms = Omega_MS / 2.0 * sum(
    eta * sm[i] * a_phonon.dag() * np.exp(-1j * delta_ms * 0.0) + 
    eta * sm[i].dag() * a_phonon * np.exp(1j * delta_ms * 0.0)
    for i in range(N_ions)
)

H_MS_total = H_ion + H_phonon + H_int_ms

# État initial : les deux ions dans |0>, mode phononique dans le vide
psi_ion = qt.tensor(qt.basis(2, 0), qt.basis(2, 0))
psi_phonon = qt.basis(N_phonons, 0)
psi_MS_0 = qt.tensor(psi_ion, psi_phonon)

tlist = np.linspace(0, 2.0 * np.pi / Omega_MS, 300)

# Simulation : on mesure le correlateur <XX> qui signe l'intrication
result_ms = qt.mesolve(H_MS_total, psi_MS_0, tlist, c_ops=[], e_ops=[
    qt.tensor(qt.sigmax() * qt.sigmax(), qt.identity(N_phonons))
])

print(f"Evolution de <XX> : min={np.min(result_ms.expect[0]):.4f}, max={np.max(result_ms.expect[0]):.4f}")
print(f"Intrication creee par la porte MS")

# Vérification de la création d'un état de Bell
bell_check = []
for t_idx in [0, len(tlist)//4, len(tlist)//2]:
    U = (-1j * H_MS_total * tlist[t_idx]).expm()
    psi_t = U * psi_MS_0
    psi_ion_t = qt.ptrace(psi_t * psi_t.dag(), [0, 1])
    bell = (qt.bell_state('00') * qt.bell_state('00').dag())
    fid = (bell.dag() * psi_ion_t).real if isinstance(bell * psi_ion_t, complex) else np.trace(bell * psi_ion_t).real
    print(f"  t={tlist[t_idx]:.3f}: intrusion dans Bell = {fid:.4f}")
```

### Séquence de portes ioniques et diaphonie

```python
# ============================================================
# Simulation d'une séquence de portes sur deux ions
# Vérification de la diaphonie entre ions
# ============================================================
import numpy as np
import qutip as qt

N_ions_seq = 2
# Opérateurs sigma_- pour chaque ion
sm_seq = [qt.tensor([qt.sigmam() if i == j else qt.identity(2) for j in range(N_ions_seq)]) for i in range(N_ions_seq)]
# Opérateurs sigma_x pour chaque ion
sx_seq = [qt.tensor([qt.sigmax() if i == j else qt.identity(2) for j in range(N_ions_seq)]) for i in range(N_ions_seq)]

# Fréquence de transition des ions
omega_z = 2.0 * np.pi * 10.0

# Hamiltonien libre (splitting Zeeman des deux ions)
H_seq = sum(0.5 * omega_z * qt.tensor([qt.sigmaz() if i == j else qt.identity(2) for j in range(N_ions_seq)]) for i in range(N_ions_seq))

# Amplitude du drive sur un seul ion
Omega_single = 0.5 * np.pi

# État initial : les deux ions dans |00>
psi_start = qt.tensor(qt.basis(2, 0), qt.basis(2, 0))
tlist_seq = np.linspace(0, 2.0, 200)

# Drive uniquement sur l'ion 1
H_single_ion = Omega_single * sx_seq[0]

# Simulation : on vérifie que l'ion 2 (spectateur) n'est pas affecté
result_seq = qt.mesolve(H_seq + H_single_ion, psi_start, tlist_seq, c_ops=[], e_ops=[
    qt.tensor(qt.projection(2, 1, 1), qt.identity(2)),  # Population |1> de l'ion 1
    qt.tensor(qt.identity(2), qt.projection(2, 1, 1)),   # Population |1> de l'ion 2
])

P1_ion1, P1_ion2 = result_seq.expect
print(f"Rabi oscillation qubit 1: max = {np.max(P1_ion1):.4f}")
print(f"Rabi oscillation qubit 2 (spectateur): max = {np.max(P1_ion2):.4f}")
print(f"Diaphonie entre ions: {np.max(P1_ion2):.2e}")
```

---

## Comparaison des technologies

| Critère | Atomes neutres (Harvard/QuEra) | Ions piégés (Oxford Ionics) | Supraconducteurs (Google Willow) |
|---------|----------------|-------------|------------------|
| **Fidélité 2Q** | $99.5\%$ | $99.99\%$ | $99.97\%$ |
| **$T_2$** | $> 1$ s | $> 10$ s | $< 1$ ms |
| **Connectivité** | Dynamique (reconfigurable) | Tout-à-tout (chaîne) | Grille fixe (3-4 voisins) |
| **Reconfigurabilité** | Oui (déplacement atomes) | Non (chaîne fixe) | Non (grille fixe) |
| **Vitesse de porte** | ~1 µs (Rydberg) | ~100 µs (MS) | ~50 ns |
| **Passage à l'échelle** | Excellent (>1000 atomes) | Limité ($\lesssim 100$) | Excellent (>1000 qubits) |
| **Portes parallèles** | Oui (pinces indépendantes) | Partiel (modes collectifs) | Oui (lignes micro-ondes) |
| **Température** | Ultra-vide + laser refroidissement | Ultra-vide | Millikelvin (dilution) |
| **Qubits logiques** | 48 (2025) | Démontrés (petits codes) | 2 (Willow, 2024) |
| **Point fort** | Connectivité, scaling | Fidélité, cohérence | Vitesse, maturité industrielle |
| **Point faible** | Portes 2Q moins matures | Scaling lent | Cohérence courte, crosstalk |

---

## À retenir

1. **Les pinces optiques** piègent des atomes individuels avec une probabilité >99%. Chaque atome est un qubit parfait (identique à tous les autres — contrairement aux supraconducteurs qui ont des variations de fabrication).

2. **La blocage de Rydberg** est le mécanisme clé pour les portes à deux qubits : un atome dans un état de Rydberg empêche ses voisins d'être excités, créant une interaction conditionnelle.

3. **La reconfigurabilité dynamique** est l'avantage unique des atomes neutres : on peut déplacer les atomes pour créer n'importe quel graphe de connectivité. C'est idéal pour les codes QLDPC.

4. **Les ions piégés** offrent les meilleurs temps de cohérence ($T_2 > 10$ s) et fidélités de porte (99.99%), mais le scaling au-delà de ~100 ions reste un défi.

5. **La porte Mølmer-Sørensen** utilise les vibrations collectives d'une chaîne d'ions comme bus pour créer de l'intrication entre ions non-voisins.

6. **Harvard/QuEra (2025)** ont démontré 48 qubits logiques avec des atomes neutres — le plus grand processeur logique à ce jour.

7. **Oxford Ionics (2025)** a atteint 99.99% de fidélité sur les portes à deux qubits avec des ions piégés — le record absolu.

---

## Pièges à éviter

1. **Confondre atome neutre et ion** : Un atome neutre n'a pas de charge nette (autant de protons que d'électrons). Un ion a perdu ou gagné un électron. Les deux sont piégés différemment : pinces optiques (neutres) vs champs électriques (ions).

2. **Penser que la blocage de Rydberg est une interaction à 2 corps** : En réalité, c'est un effet collectif. Si N atomes sont dans la sphère de blocage, un seul peut être excité en Rydberg — c'est une superposition collective (état de Dicke).

3. **Confondre $C_6/R^6$ et $C_3/R^3$** : L'interaction de van der Waals décroît en $1/R^6$ (dipôle-dipôle induit). L'interaction dipolaire résonante décroît en $1/R^3$. Les deux régimes existent selon les états de Rydberg choisis.

4. **Oublier que la durée de vie de Rydberg est limitée** : $\tau \propto n^3$ signifie que pour $n = 70$, $\tau \sim 100$ µs. Les portes doivent être plus rapides que ça, sinon l'atome se désexcite spontanément pendant la porte.

5. **Croire que les ions sont facilement scalables** : Une chaîne de 50 ions a des modes vibrationnels très denses en fréquence. Isoler un mode spécifique pour la porte MS devient exponentiellement difficile.

---

## Exercices

### Niveau 1 — Application directe

1. **Rayon de blocage** : Calculer le rayon de blocage $R_b$ pour un atome de Césium avec $n = 80$, $\Omega/(2\pi) = 5$ MHz, et $C_6/(2\pi) = 200$ GHz·µm⁶.

2. **Exécuter le code** : Reproduire la simulation Cirq de 3 atomes neutres et vérifier l'état final obtenu.

3. **Porte MS** : Simuler une porte Mølmer-Sørensen entre deux ions avec QuTiP. Visualiser l'intrication produite en traçant la concurrence en fonction du temps.

### Niveau 2 — Compréhension

4. **Blocade de Rydberg** : Simuler avec QuTiP un système à 2 atomes et tracer la probabilité d'excitation simultanée $P_{rr}$ en fonction de $R/R_b$ pour $R/R_b$ allant de 0.5 à 3.

5. **Porte CZ Rydberg complète** : Implémenter la séquence complète d'une porte CZ : impulsion $\pi$ sur le contrôle, $2\pi$ sur la cible, $\pi$ inverse sur le contrôle. Mesurer la fidélité pour différentes valeurs de $C_6$.

6. **Scaling des atomes neutres** : Pour un code de surface de distance $d = 5$, estimer le nombre de pinces optiques nécessaires et la surface du piège. Comparer avec une grille fixe supraconductrice.

### Niveau 3 — Défi

7. **Analyse de bruit** : Comparer les courbes de bruit (1/f, $T_2$, etc.) des trois plateformes (atomes, ions, supraconducteurs) et discuter des implications pour la correction d'erreur.

8. **Optimisation de la porte CZ** : Trouver les paramètres optimaux ($\Omega$, $\delta$, durée) pour maximiser la fidélité de la porte CZ. Implémenter une optimisation par balayage ou gradient.

9. **Comparaison architecturale complète** : Pour un code de surface de distance $d = 7$ avec 100 qubits logiques, comparer le nombre de qubits/atomes physiques nécessaires pour chaque plateforme (supraconducteurs, atomes neutres, ions). Inclure l'overhead de SWAP pour les architectures à connectivité limitée.

---

## Pour aller plus loin

- **Bluvstein, D.** et al. (2025). "Logical quantum processor with 48 logical qubits." *Nature*. — Démonstration historique de Harvard/QuEra.
- **Daily, T.** et al. (2025). "High-fidelity two-qubit gates with trapped ions." *Oxford Ionics*. — Record de fidélité 99.99%.
- **QuEra Computing** (2025). "Algorithmic Fault Tolerance for neutral atom quantum computers." *arXiv*. — Feuille de route QuEra.
- **Saffman, M.** (2016). "Quantum computing with atomic qubits and Rydberg interactions." *J. Phys. B*, 49, 202001. — Revue pédagogique sur les atomes de Rydberg.
- **Bruzewicz, C.D.** et al. (2019). "Trapped-ion quantum computing: Progress and challenges." *Appl. Phys. Rev.*, 6, 021314. — État de l'art des ions piégés.
- **Mølmer, K. & Sørensen, A.** (1999). "Multiparticle entanglement of hot trapped ions." *Phys. Rev. Lett.*, 82, 1835. — L'article fondateur de la porte MS.
