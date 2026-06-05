"""
Diagrammes pour le calcul quantique.

Ce module contient les scripts de génération de figures et schémas
utilisés dans le cours Quantum Computing Engineering.

Conventions :
- Bloch : sphère de Bloch, états sur la sphère
- Bell : intrication, états de Bell, corrélations
- circuits : portes quantiques, circuits
- surface : codes de surface, syndromes
- qft : transformée de Fourier quantique
- grover : algorithme de Grover, oracle, amplification
- shor : factorisation, recherche de période

Utilisation :
    python diagrams.py [figure_name]
    ou
    from diagrams import bloch_sphere, bell_state_viz
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import Axes3D, proj3d
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def bloch_sphere(states=None, title="Sphère de Bloch", filename="bloch_sphere.png"):
    """
    Génère la sphère de Bloch avec les axes et les états de base.

    Parameters
    ----------
    states : list of tuple
        Liste de (theta, phi, label, color) pour chaque état à afficher
    title : str
        Titre de la figure
    filename : str
        Nom du fichier de sortie
    """
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    u = np.linspace(0, 2 * np.pi, 60)
    v = np.linspace(0, np.pi, 60)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))

    ax.plot_surface(x, y, z, color='lightblue', alpha=0.15, edgecolor='none')

    for ang in np.linspace(0, 2 * np.pi, 12):
        ax.plot(np.cos(ang) * np.sin(v), np.sin(ang) * np.sin(v), np.cos(v),
                color='gray', alpha=0.2, lw=0.5)

    ax.plot(np.cos(u), np.sin(u), np.zeros_like(u), 'gray', alpha=0.3, lw=0.5)
    ax.plot(np.zeros_like(u), np.cos(u), np.sin(u), 'gray', alpha=0.3, lw=0.5)
    ax.plot(np.sin(u), np.zeros_like(u), np.cos(u), 'gray', alpha=0.3, lw=0.5)

    L = 1.15
    ax.quiver(0, 0, 0, L, 0, 0, color='red', arrow_length_ratio=0.08)
    ax.quiver(0, 0, 0, 0, L, 0, color='green', arrow_length_ratio=0.08)
    ax.quiver(0, 0, 0, 0, 0, L, color='blue', arrow_length_ratio=0.08)
    ax.text(L, 0, 0, r'$|0\rangle$', color='red', fontsize=16)
    ax.text(0, L, 0, r'$\hat{y}$', color='green', fontsize=14)
    ax.text(0, 0, L, r'$|0\rangle$', color='blue', fontsize=16)
    ax.text(-L, 0, 0, r'$|1\rangle$', color='red', fontsize=16)
    ax.text(0, -L, 0, r'$-\hat{y}$', color='green', fontsize=14)
    ax.text(0, 0, -L, r'$|1\rangle$', color='blue', fontsize=16)

    ax.text(0.7, 0, 0.7, r'$|+\rangle$', fontsize=14, color='purple')
    ax.text(-0.7, 0, 0.7, r'$|-\rangle$', fontsize=14, color='purple')
    ax.text(0, 0.7, 0.7, r'$|+i\rangle$', fontsize=14, color='orange')
    ax.text(0, -0.7, 0.7, r'$|-i\rangle$', fontsize=14, color='orange')

    if states:
        for theta, phi, label, color in states:
            x_s = np.sin(theta) * np.cos(phi)
            y_s = np.sin(theta) * np.sin(phi)
            z_s = np.cos(theta)
            ax.quiver(0, 0, 0, x_s, y_s, z_s, color=color, arrow_length_ratio=0.1)
            ax.text(x_s * 1.1, y_s * 1.1, z_s * 1.1, label, color=color, fontsize=14)

    ax.set_xlim([-1.3, 1.3])
    ax.set_ylim([-1.3, 1.3])
    ax.set_zlim([-1.3, 1.3])
    ax.set_box_aspect([1, 1, 1])
    ax.set_title(title, fontsize=14)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    out_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(out_path, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"✓ Sauvegardé : {out_path}")


def bell_states_grid(filename="bell_states.png"):
    """Visualise les 4 états de Bell dans une grille 2x2."""
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))

    bell = [
        (r'$|\Phi^+\rangle = (|00\rangle + |11\rangle)/\sqrt{2}$', [0, 3]),
        (r'$|\Phi^-\rangle = (|00\rangle - |11\rangle)/\sqrt{2}$', [0, 3]),
        (r'$|\Psi^+\rangle = (|01\rangle + |10\rangle)/\sqrt{2}$', [1, 2]),
        (r'$|\Psi^-\rangle = (|01\rangle - |10\rangle)/\sqrt{2}$', [1, 2]),
    ]

    for ax, (label, peaks) in zip(axes.flat, bell):
        probs = np.zeros(4)
        for p in peaks:
            probs[p] = 0.5
        bars = ax.bar(range(4), probs, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
        ax.set_xticks(range(4))
        ax.set_xticklabels([r'$|00\rangle$', r'$|01\rangle$', r'$|10\rangle$', r'$|11\rangle$'])
        ax.set_ylim(0, 1)
        ax.set_ylabel('Probabilité')
        ax.set_title(label, fontsize=12)
        ax.grid(alpha=0.3)
        for bar, p in zip(bars, probs):
            if p > 0:
                ax.text(bar.get_x() + bar.get_width()/2, p + 0.02,
                        f'{p:.3f}', ha='center', fontsize=10)

    plt.suptitle("Les 4 états de Bell", fontsize=14)
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(out_path, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"✓ Sauvegardé : {out_path}")


def chsh_correlations(filename="chsh.png"):
    """Trace les corrélations quantiques vs classiques pour le test de CHSH."""
    theta = np.linspace(0, 2 * np.pi, 200)
    classical = -np.cos(theta)
    quantum = -np.cos(theta)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(np.degrees(theta), classical, 'b-', lw=2, label='Classique (Bell) : $\\leq 2$')
    ax.plot(np.degrees(theta), quantum, 'r--', lw=2, label='Quantique (mécanique Q) : $\\leq 2\\sqrt{2}$')
    ax.axhline(2, color='blue', ls=':', alpha=0.5)
    ax.axhline(2 * np.sqrt(2), color='red', ls=':', alpha=0.5)
    ax.axvline(45, color='green', ls=':', alpha=0.5)
    ax.text(46, 2.7, 'Choix optimal quantique : 45°', fontsize=10, color='green')
    ax.set_xlabel('Angle de mesure (degrés)')
    ax.set_ylabel('$|S|$ (paramètre CHSH)')
    ax.set_title("Violation des inégalités de Bell : $|S| = 2\\sqrt{2}$")
    ax.legend(loc='lower right', fontsize=11)
    ax.grid(alpha=0.3)
    ax.set_ylim(-3.2, 3.2)
    out_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(out_path, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"✓ Sauvegardé : {out_path}")


def circuit_diagram(filename="quantum_circuit.png"):
    """Dessine un circuit quantique simple (style matplotlib)."""
    fig, ax = plt.subplots(figsize=(12, 4))

    n_qubits = 3
    n_cols = 6

    for q in range(n_qubits):
        ax.axhline(y=q, color='black', lw=1.5)

    gates = [
        (0, 0, 'H', '#1f77b4'),
        (1, 0, 'X', '#d62728'),
        (2, 1, 'H', '#1f77b4'),
        (0, 2, 'CNOT', '#2ca02c'),
        (1, 2, 'CNOT', '#2ca02c'),
        (0, 3, 'Z', '#9467bd'),
        (1, 4, 'H', '#1f77b4'),
        (2, 4, 'H', '#1f77b4'),
        (0, 5, 'M', '#000000'),
        (1, 5, 'M', '#000000'),
    ]

    for q, col, label, color in gates:
        box = FancyBboxPatch((col - 0.35, q - 0.35), 0.7, 0.7,
                             boxstyle="round,pad=0.05", linewidth=2,
                             edgecolor=color, facecolor='white')
        ax.add_patch(box)
        ax.text(col, q, label, ha='center', va='center', fontsize=12, fontweight='bold')

    cnot_pairs = [(0, 1, 2)]
    for c_q, t_q, col in cnot_pairs:
        ax.plot([col, col], [c_q, t_q], 'k-', lw=1.5)
        ax.plot(col, c_q, 'o', color='black', markersize=10)
        ax.plot(col, t_q, '+', color='black', markersize=10, markeredgewidth=2)

    ax.set_xlim(-0.7, n_cols - 0.3)
    ax.set_ylim(-0.7, n_qubits - 0.3)
    ax.invert_yaxis()
    ax.set_yticks(range(n_qubits))
    ax.set_yticklabels([f'$|q_{i}\\rangle$' for i in range(n_qubits)])
    ax.set_xticks(range(n_cols))
    ax.set_xticklabels([f't{i}' for i in range(n_cols)])
    ax.set_aspect('equal')
    ax.set_title("Exemple de circuit quantique : intrication, mesure", fontsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    out_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(out_path, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"✓ Sauvegardé : {out_path}")


def surface_code_grid(d=3, filename="surface_code.png"):
    """Dessine un code de surface de distance d."""
    fig, ax = plt.subplots(figsize=(7, 7))

    for i in range(d):
        for j in range(d):
            x, y = j, -i
            color_x = '#ff7f0e' if (i + j) % 2 == 0 else '#1f77b4'
            color_z = '#2ca02c' if (i + j) % 2 == 1 else '#d62728'

            if i < d - 1 and j < d - 1:
                ax.plot([x, x + 0.5], [y, y - 0.5], '-', color=color_z, lw=2, alpha=0.7)
                ax.plot([x, x + 0.5], [y, y + 0.5], '-', color=color_x, lw=2, alpha=0.7)

            circle = Circle((x, y), 0.18, color='white', ec='black', lw=1.5)
            ax.add_patch(circle)

    ax.set_xlim(-0.7, d - 0.3)
    ax.set_ylim(-d + 0.3, 0.7)
    ax.set_aspect('equal')
    ax.set_title(f"Code de surface de distance $d={d}$", fontsize=13)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(0.05, 0.95, "— X-stabilizer\n— Z-stabilizer\n○ qubit de donnée",
            transform=ax.transAxes, fontsize=10, va='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    out_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(out_path, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"✓ Sauvegardé : {out_path}")


def qft_circuit_diagram(n=4, filename="qft_circuit.png"):
    """Dessine le circuit QFT pour n qubits."""
    fig, ax = plt.subplots(figsize=(13, 6))

    for q in range(n):
        ax.axhline(y=q, color='black', lw=1.5)

    col = 0
    for q in range(n):
        ax.add_patch(FancyBboxPatch((col - 0.35, q - 0.35), 0.7, 0.7,
                                    boxstyle="round,pad=0.05", lw=2,
                                    ec='#1f77b4', fc='white'))
        ax.text(col, q, 'H', ha='center', va='center', fontsize=12, fontweight='bold')
        col += 1

        for k in range(2, n - q + 1):
            if q + k - 1 < n:
                ctrl_col = col
                ax.plot([ctrl_col, col], [q, q + k - 1], 'k-', lw=1.2)
                ax.plot(ctrl_col, q, 'o', color='black', markersize=8)
                ax.plot(col, q + k - 1, '+', color='#9467bd', markersize=12, markeredgewidth=2)
                ax.text(col + 0.15, (q + q + k - 1) / 2, f'$R_{{{k}}}$',
                        fontsize=10, color='#9467bd')
                col += 1

    for q in range(n // 2):
        y_src, y_dst = q, n - 1 - q
        ax.plot([col + 0.5, col + 0.5], [y_src, y_dst], 'k-', lw=1.5)
        ax.plot(col + 0.5, y_src, 'x', color='#d62728', markersize=12, markeredgewidth=2)
        ax.plot(col + 0.5, y_dst, 'x', color='#d62728', markersize=12, markeredgewidth=2)
        col += 2

    ax.set_xlim(-0.7, col + 0.3)
    ax.set_ylim(-0.7, n - 0.3)
    ax.invert_yaxis()
    ax.set_yticks(range(n))
    ax.set_yticklabels([f'$|q_{i}\\rangle$' for i in range(n)])
    ax.set_xticks([])
    ax.set_title(f"QFT pour {n} qubits (complexité $O(n^2)$)", fontsize=13)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    out_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(out_path, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"✓ Sauvegardé : {out_path}")


def grover_iteration(filename="grover.png"):
    """Visualise l'itération de Grover : Oracle + Diffuseur."""
    fig, ax = plt.subplots(figsize=(12, 5))

    n_qubits = 4
    for q in range(n_qubits):
        ax.axhline(y=q, color='black', lw=1.5)

    boxes = [
        (0, 0, 'H', '#1f77b4'),
        (1, 0, 'H', '#1f77b4'),
        (2, 0, 'H', '#1f77b4'),
        (3, 0, 'H', '#1f77b4'),
        (4, 0, 'Oracle\n$U_f$', '#d62728'),
        (4, 1, 'Oracle\n$U_f$', '#d62728'),
        (4, 2, 'Oracle\n$U_f$', '#d62728'),
        (4, 3, 'Oracle\n$U_f$', '#d62728'),
        (5, 0, 'H', '#1f77b4'),
        (5, 1, 'H', '#1f77b4'),
        (5, 2, 'H', '#1f77b4'),
        (5, 3, 'H', '#1f77b4'),
        (6, 1, 'X', '#9467bd'),
        (6, 2, 'X', '#9467bd'),
        (7, 1, '$Z_0$', '#000000'),
        (7, 2, '$Z_0$', '#000000'),
        (8, 1, 'X', '#9467bd'),
        (8, 2, 'X', '#9467bd'),
        (9, 0, 'H', '#1f77b4'),
        (9, 1, 'H', '#1f77b4'),
        (9, 2, 'H', '#1f77b4'),
        (9, 3, 'H', '#1f77b4'),
        (10, 0, 'M', '#000000'),
        (10, 1, 'M', '#000000'),
        (10, 2, 'M', '#000000'),
        (10, 3, 'M', '#000000'),
    ]
    for q, c, lbl, c_ in boxes:
        ax.add_patch(FancyBboxPatch((c - 0.45, q - 0.4), 0.9, 0.8,
                                    boxstyle="round,pad=0.05", lw=2,
                                    ec=c_, fc='white'))
        ax.text(c, q, lbl, ha='center', va='center', fontsize=9, fontweight='bold')

    ax.annotate('', xy=(5, -0.7), xytext=(4, -0.7),
                arrowprops=dict(arrowstyle='<->', color='red', lw=1.5))
    ax.text(4.5, -1.1, 'Oracle', ha='center', fontsize=11, color='red')
    ax.annotate('', xy=(9, -0.7), xytext=(6, -0.7),
                arrowprops=dict(arrowstyle='<->', color='blue', lw=1.5))
    ax.text(7.5, -1.1, 'Diffuseur', ha='center', fontsize=11, color='blue')

    ax.set_xlim(-0.7, 11)
    ax.set_ylim(-1.6, n_qubits - 0.3)
    ax.invert_yaxis()
    ax.set_yticks(range(n_qubits))
    ax.set_yticklabels([f'$|q_{i}\\rangle$' for i in range(n_qubits)])
    ax.set_xticks([])
    ax.set_title("Une itération de Grover = Oracle + Diffuseur ($O(\\sqrt{N})$ appels)", fontsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    out_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(out_path, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"✓ Sauvegardé : {out_path}")


def decoherence_curve(filename="decoherence.png"):
    """Trace T1 (relaxation) et T2 (décohérence)."""
    t = np.linspace(0, 10, 200)
    T1, T2 = 3.0, 2.0

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(t, np.exp(-t / T1), 'b-', lw=2, label=f'$T_1 = {T1}$ (relaxation $|1\\rangle \\to |0\\rangle$)')
    ax.plot(t, np.exp(-t / T2), 'r--', lw=2, label=f'$T_2 = {T2}$ (décohérence de phase)')
    ax.axhline(1/np.e, color='gray', ls=':', alpha=0.5)
    ax.axvline(T1, color='blue', ls=':', alpha=0.5)
    ax.axvline(T2, color='red', ls=':', alpha=0.5)
    ax.fill_between(t, 0, np.exp(-t / T1), alpha=0.1, color='blue')
    ax.fill_between(t, 0, np.exp(-t / T2), alpha=0.1, color='red')
    ax.set_xlabel('Temps ($\\mu$s)', fontsize=12)
    ax.set_ylabel('Cohérence / Population', fontsize=12)
    ax.set_title("Décohérence d'un qubit : $T_1$ vs $T_2$", fontsize=13)
    ax.legend(fontsize=11, loc='upper right')
    ax.grid(alpha=0.3)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1.05)
    out_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(out_path, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"✓ Sauvegardé : {out_path}")


def bloch_trajectory(filename="bloch_trajectory.png"):
    """Trajectoire de Rabi sur la sphère de Bloch."""
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111, projection='3d')

    u = np.linspace(0, 2 * np.pi, 60)
    v = np.linspace(0, np.pi, 60)
    ax.plot_surface(np.outer(np.cos(u), np.sin(v)),
                    np.outer(np.sin(u), np.sin(v)),
                    np.outer(np.ones_like(u), np.cos(v)),
                    color='lightblue', alpha=0.15, edgecolor='none')

    theta = np.linspace(0, 4 * np.pi, 200)
    omega = 1.0
    x = np.sin(theta) * np.cos(omega * theta)
    y = np.sin(theta) * np.sin(omega * theta)
    z = np.cos(theta)
    ax.plot(x, y, z, 'r-', lw=2.5, label='Oscillation de Rabi')
    ax.plot([x[0]], [y[0]], [z[0]], 'go', markersize=12, label='Départ $|0\\rangle$')
    ax.plot([x[-1]], [y[-1]], [z[-1]], 'r^', markersize=12, label='Après 2π')

    L = 1.2
    ax.quiver(0, 0, 0, L, 0, 0, color='red', arrow_length_ratio=0.08)
    ax.quiver(0, 0, 0, 0, 0, L, color='blue', arrow_length_ratio=0.08)
    ax.text(L, 0, 0, r'$|0\\rangle$', color='red', fontsize=16)
    ax.text(0, 0, L, r'$|0\\rangle$', color='blue', fontsize=16)
    ax.text(-L, 0, 0, r'$|1\\rangle$', color='red', fontsize=16)
    ax.text(0, 0, -L, r'$|1\\rangle$', color='blue', fontsize=16)

    ax.set_xlim([-1.3, 1.3])
    ax.set_ylim([-1.3, 1.3])
    ax.set_zlim([-1.3, 1.3])
    ax.set_box_aspect([1, 1, 1])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_title("Oscillation de Rabi : $H = \\frac{\\Omega}{2}\\sigma_x$", fontsize=13)
    ax.legend(loc='upper left', fontsize=11)
    out_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(out_path, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"✓ Sauvegardé : {out_path}")


def all_diagrams():
    """Génère tous les diagrammes."""
    print("=== Génération de tous les diagrammes ===\n")
    bloch_sphere()
    bell_states_grid()
    chsh_correlations()
    circuit_diagram()
    surface_code_grid(d=3)
    qft_circuit_diagram(n=4)
    grover_iteration()
    decoherence_curve()
    bloch_trajectory()
    print(f"\n✓ Tous les diagrammes sont dans {OUTPUT_DIR}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        name = sys.argv[1]
        func = globals().get(name)
        if func is None:
            print(f"Figure '{name}' non trouvée.")
            print("Options :", [k for k in globals() if callable(globals()[k]) and not k.startswith('_')])
        else:
            func()
    else:
        all_diagrams()
