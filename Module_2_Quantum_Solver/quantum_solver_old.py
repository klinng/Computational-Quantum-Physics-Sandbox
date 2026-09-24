import os
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

print("=== Module 2: The Quantum State Solver (Full Ecosystem) ===")

# 1. PHYSICAL CONSTANTS & GRID DISCRETIZATION
N = 100  # Number of digital grid points
L = 1.0  # Width of the quantum box (meters)
spatial_grid = np.linspace(0, L, N)
dx = spatial_grid[1] - spatial_grid[0]  # True distance between neighboring points

print(f"\n1. Spatial Grid Initialized:")
print(f"   -> Box width (L): {L} meter")
print(f"   -> Grid points (N): {N}")
print(f"   -> Step size (dx): {dx:.4f} meters")

# 2. CONSTRUCT KINETIC ENERGY OPERATOR MATRIX (Second Derivative)
main_diagonal = -2.0 * np.ones(N)
off_diagonal = 1.0 * np.ones(N - 1)
D2_matrix = np.diag(main_diagonal) + np.diag(off_diagonal, 1) + np.diag(off_diagonal, -1)

# Apply physical scaling factor: H_kinetic = -0.5 * (d^2 / dx^2)
H_kinetic = -0.5 * D2_matrix / (dx**2)

print(f"\n2. Kinetic Energy Hamiltonian Matrix Constructed.")
print(f"   -> Top-Left 5x5 Slice of the operator grid:")
print(H_kinetic[:5, :5])

# 3. SOLVE THE TIME-INDEPENDENT SCHRÖDINGER EQUATION
energy_levels, wavefunctions = la.eigh(H_kinetic)

print(f"\n3. Schrödinger Equation Solved!")
print("   --- Numerical Energy Levels (Eigenvalues) ---")
for i in range(3):
    print(f"   -> State n = {i+1} (E_{i}): {energy_levels[i]:.4f} energy units")

# 4. DEFINE ISOLATED DIRECTORY FILE PATHS
script_directory = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------
# 📊 GRAPH 1: The Kinetic Hamiltonian Matrix Grid (The Tool)
# ----------------------------------------------------
plt.figure(figsize=(6, 5))
plt.imshow(H_kinetic[:10, :10], cmap='RdBu_r')
plt.title("Hamiltonian Energy Operator Matrix Grid (Slice 10x10)")
plt.colorbar(label="Energy Coupling Strength")
matrix_graph_path = os.path.join(script_directory, "quantum_hamiltonian_grid.png")
plt.savefig(matrix_graph_path)
plt.close()

# ----------------------------------------------------
# 🌊 GRAPH 2: The Physical Quantum States (The Physics Result)
# ----------------------------------------------------
plt.figure(figsize=(9, 6))
for i in range(3):
    psi = wavefunctions[:, i]
    probability_density = psi**2
    
    # Scale each wave peak to be exactly 5 units tall so they look clean on the chart
    scaled_hill = (probability_density / np.max(probability_density)) * 5.0
    
    # Plot the wave sitting on top of its energy line baseline
    plt.plot(spatial_grid, scaled_hill + energy_levels[i], 
             label=r"State $n=$" + f"{i+1} ($E_{i+1}$)", linewidth=2)
    plt.axhline(energy_levels[i], color='gray', linestyle='--', alpha=0.5)

plt.title("Quantum Particle in a Box: Probability Densities $|\\psi|^2$")
plt.xlabel("Position in Box (x)")
plt.ylabel("Energy / Probability Shift")
plt.grid(True, alpha=0.3)
plt.legend()

wave_graph_path = os.path.join(script_directory, "quantum_states_plot.png")
plt.savefig(wave_graph_path)
plt.close()

print(f"\nSuccess! Both isolated files have been saved in your module folder:")
print(f"-> 🟥 Matrix Grid Graph: quantum_hamiltonian_grid.png")
print(f"-> 📈 Physical Wave Graph: quantum_states_plot.png")

# --- CONVERTING TO HUMAN REALITY (SI UNITS) ---
hbar_SI = 1.054571817e-34  # J·s (Planck's constant / 2pi)
m_electron_SI = 9.1093837e-31  # kg (Mass of an electron)
L_meters = 1e-10  # Let's say our quantum box is 1 Angstrom wide (size of an atom)

# Conversion factor from our code units to real Joules
conversion_factor = (hbar_SI**2) / (m_electron_SI * L_meters**2)

print("\n--- Real World SI Units Conversion (Joules) ---")
for i in range(3):
    real_energy_joules = energy_levels[i] * conversion_factor
    print(f"   -> Real Energy State E_{i+1}: {real_energy_joules:.4e} Joules")
