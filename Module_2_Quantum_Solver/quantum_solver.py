import os

import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt


print("=== Module 2: 1D Quantum Particle in a Box ===")


# ============================================================
# 1. PHYSICAL PARAMETERS AND GRID
# ============================================================

# Number of unknown/interior grid points.
N = 100

# Dimensionless width of the box.
L = 1.0

# For an infinite square well:
#
#       psi(0) = 0
#       psi(L) = 0
#
# We therefore include the two boundary points in x_full,
# but solve only for the N interior points.

x_full = np.linspace(0.0, L, N + 2)

dx = x_full[1] - x_full[0]

# Interior grid points only.
x = x_full[1:-1]

print("\n1. Spatial Grid Initialized")
print(f"   -> Box width L = {L}")
print(f"   -> Interior grid points = {N}")
print(f"   -> Grid spacing dx = {dx:.6f}")


# ============================================================
# 2. SECOND-DERIVATIVE MATRIX
# ============================================================

# Central finite-difference approximation:
#
# d²psi/dx² ≈
# (psi[i+1] - 2*psi[i] + psi[i-1]) / dx²
#
# This produces a tridiagonal matrix.

main_diagonal = -2.0 * np.ones(N)
off_diagonal = 1.0 * np.ones(N - 1)

D2 = (
    np.diag(main_diagonal)
    + np.diag(off_diagonal, k=1)
    + np.diag(off_diagonal, k=-1)
)

print("\n2. Second-Derivative Matrix Constructed")


# ============================================================
# 3. HAMILTONIAN
# ============================================================

# Time-independent Schrödinger equation:
#
#       H psi = E psi
#
# For a particle in an infinite box, inside the box V(x) = 0.
#
# In dimensionless units:
#
#       hbar = 1
#       m    = 1
#
# Therefore:
#
#       H = -(1/2) d²/dx²

H = -0.5 * D2 / dx**2

print("\n3. Hamiltonian Constructed")
print("   -> Dimensionless Hamiltonian:")
print("      H = -(1/2) d²/dx²")


# ============================================================
# 4. SOLVE THE EIGENVALUE PROBLEM
# ============================================================

# Solve:
#
#       H psi_n = E_n psi_n
#
# H is real and symmetric, so scipy.linalg.eigh()
# is appropriate.

energy_levels, wavefunctions = la.eigh(H)

print("\n4. Schrödinger Equation Solved")

print("\n   Numerical energy levels:")

for i in range(3):
    print(
        f"   -> n = {i + 1}: "
        f"E = {energy_levels[i]:.8f}"
    )


# ============================================================
# 5. PHYSICAL NORMALIZATION
# ============================================================

# eigh() normalizes the eigenvectors using a discrete vector norm.
#
# For a physical wavefunction we require:
#
#       integral |psi(x)|² dx = 1
#
# We therefore normalize using numerical integration.

for i in range(3):

    psi = wavefunctions[:, i]

    normalization = np.sqrt(
        np.trapezoid(np.abs(psi) ** 2, x)
    )

    wavefunctions[:, i] = psi / normalization


print("\n5. Wavefunctions normalized using numerical integration")


# ============================================================
# 6. ANALYTICAL SOLUTION
# ============================================================

# For an infinite square well:
#
#       E_n = n²*pi²*hbar² / (2*m*L²)
#
# With hbar = 1 and m = 1:
#
#       E_n = n²*pi² / (2*L²)

analytical_energies = np.array([
    (n**2 * np.pi**2) / (2.0 * L**2)
    for n in range(1, 4)
])


print("\n6. Numerical vs Analytical Energies")

print(
    "\n   n        Numerical        "
    "Analytical        Relative Error"
)

for i in range(3):

    numerical = energy_levels[i]
    analytical = analytical_energies[i]

    relative_error = abs(
        (numerical - analytical) / analytical
    )

    print(
        f"   {i + 1:<8}"
        f"{numerical:<17.8f}"
        f"{analytical:<18.8f}"
        f"{relative_error:.3e}"
    )


# ============================================================
# 7. SAVE FIGURES
# ============================================================

# Save figures next to this Python file so that the script
# works regardless of the current terminal directory.

script_directory = os.path.dirname(
    os.path.abspath(__file__)
)


# ------------------------------------------------------------
# 7A. Hamiltonian matrix
# ------------------------------------------------------------

plt.figure(figsize=(6, 5))

plt.imshow(
    H[:10, :10],
    cmap="RdBu_r"
)

plt.title(
    "Hamiltonian Matrix "
    "(10 × 10 Interior Slice)"
)

plt.xlabel("Grid index")
plt.ylabel("Grid index")

plt.colorbar(
    label="Hamiltonian matrix element"
)

matrix_graph_path = os.path.join(
    script_directory,
    "quantum_hamiltonian_grid.png"
)

plt.savefig(
    matrix_graph_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ------------------------------------------------------------
# 7B. Probability densities
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))

for i in range(3):

    psi = wavefunctions[:, i]

    # Physical probability density:
    #
    #       |psi(x)|²

    probability_density = np.abs(psi) ** 2

    # This scaling is ONLY for visualization.
    # It does not modify the physical wavefunction.

    scaled_density = (
        probability_density
        / np.max(probability_density)
        * 0.8
    )

    plt.plot(
        x,
        scaled_density + energy_levels[i],
        label=f"n = {i + 1}"
    )

    plt.axhline(
        energy_levels[i],
        linestyle="--",
        alpha=0.5
    )


plt.title(
    "Particle in a Box: "
    "Numerical Probability Densities"
)

plt.xlabel("Position x")
plt.ylabel(
    "Energy + scaled probability density"
)

plt.grid(
    True,
    alpha=0.3
)

plt.legend()

wave_graph_path = os.path.join(
    script_directory,
    "quantum_states_plot.png"
)

plt.savefig(
    wave_graph_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 8. CONVERT NUMERICAL ENERGIES TO SI UNITS
# ============================================================

# Physical constants.
hbar_SI = 1.054571817e-34       # J*s
m_electron_SI = 9.1093837e-31   # kg

# Example physical box width:
# 1 Angstrom = 1e-10 m
L_meters = 1e-10

# Our dimensionless Hamiltonian has an energy scale:
#
#       hbar² / (m*L²)
#
# Therefore:
#
#       E_SI =
#       E_dimensionless * hbar²/(m*L²)

conversion_factor = (
    hbar_SI**2
    / (m_electron_SI * L_meters**2)
)

print("\n7. Example Conversion to SI Units")

print(
    f"   Physical box width = {L_meters:.2e} m"
)

for i in range(3):

    energy_joules = (
        energy_levels[i]
        * conversion_factor
    )

    # 1 eV = 1.602176634e-19 J
    energy_eV = (
        energy_joules
        / 1.602176634e-19
    )

    print(
        f"   -> n = {i + 1}: "
        f"{energy_joules:.4e} J "
        f"= {energy_eV:.4f} eV"
    )


print("\n=== Module 2 completed successfully ===")
