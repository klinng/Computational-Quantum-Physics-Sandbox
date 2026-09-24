import os

import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt


print("=== Module 4: Quantum Transverse-Field Ising Model ===")


# ============================================================
# 1. PHYSICS CONFIGURATION
# ============================================================

# Number of quantum spins / qubits.
#
# The Hilbert-space dimension grows exponentially:
#
#       dim = 2^N
#
# For N = 4:
#
#       dim = 16
#
N_spins = 4

# Ising interaction strength.
#
#       -J * sum(sigma_z_i sigma_z_j)
#
J = 1.0

# Strength of the transverse quantum field.
#
#       -g * sum(sigma_x_i)
#
g_field = 1.0

# Temperatures used for thermal calculations.
temperatures = np.linspace(0.1, 5.0, 100)

# Boltzmann constant in dimensionless units.
K_B = 1.0

# Hilbert-space dimension.
dim = 2 ** N_spins


print("\n[STEP 1] Quantum System Configuration")

print(
    f"   -> Number of quantum spins: {N_spins}"
)

print(
    f"   -> Hilbert-space dimension: {dim}"
)

print(
    f"   -> Ising coupling J: {J}"
)

print(
    f"   -> Transverse field g: {g_field}"
)


# ============================================================
# 2. PAULI OPERATORS
# ============================================================

# Pauli matrices.
#
# sigma_z:
# Measures the spin orientation in the z direction.
#
# sigma_x:
# Creates transitions between |up> and |down> states.

Sz = np.array(
    [
        [1.0, 0.0],
        [0.0, -1.0]
    ]
)

Sx = np.array(
    [
        [0.0, 1.0],
        [1.0, 0.0]
    ]
)

Identity = np.eye(2)


# ============================================================
# 3. EMBED A SINGLE-SPIN OPERATOR
#    INTO THE MANY-BODY HILBERT SPACE
# ============================================================

def get_tensor_op(op, site, N):
    """
    Construct an operator acting on one site of an N-spin system.

    Example:

        I ⊗ I ⊗ sigma_z ⊗ I

    for sigma_z acting on site 2 of a 4-spin system.
    """

    operator_list = [
        Identity.copy()
        for _ in range(N)
    ]

    operator_list[site] = op

    result = operator_list[0]

    for operator in operator_list[1:]:

        result = np.kron(
            result,
            operator
        )

    return result


# ============================================================
# 4. CONSTRUCT MANY-BODY OPERATORS
# ============================================================

print(
    "\n[STEP 2] Constructing Many-Body Quantum Operators..."
)


# Interaction part:
#
#       H_interaction =
#       -J sum_i sigma_z(i) sigma_z(i+1)
#
# Periodic boundary conditions are used:
#
#       N -> first spin

H_interaction = np.zeros(
    (dim, dim)
)


# Transverse field:
#
#       H_field =
#       -g sum_i sigma_x(i)

H_transverse_field = np.zeros(
    (dim, dim)
)


# Total z-magnetization operator:
#
#       M_z =
#       (1/N) sum_i sigma_z(i)

M_z_operator = np.zeros(
    (dim, dim)
)


# Total x-magnetization operator:
#
#       M_x =
#       (1/N) sum_i sigma_x(i)

M_x_operator = np.zeros(
    (dim, dim)
)


for i in range(N_spins):

    # --------------------------------------------------------
    # Interaction
    # --------------------------------------------------------

    next_neighbor = (
        (i + 1)
        % N_spins
    )

    Sz_i = get_tensor_op(
        Sz,
        i,
        N_spins
    )

    Sz_next = get_tensor_op(
        Sz,
        next_neighbor,
        N_spins
    )

    H_interaction -= (
        J
        * Sz_i
        @ Sz_next
    )

    # --------------------------------------------------------
    # Transverse field
    # --------------------------------------------------------

    Sx_i = get_tensor_op(
        Sx,
        i,
        N_spins
    )

    H_transverse_field -= (
        g_field
        * Sx_i
    )

    # --------------------------------------------------------
    # Magnetization operators
    # --------------------------------------------------------

    M_z_operator += Sz_i

    M_x_operator += Sx_i


# Divide by the number of spins to obtain magnetization
# per spin.

M_z_operator /= N_spins

M_x_operator /= N_spins


# ============================================================
# 5. COMPLETE QUANTUM HAMILTONIAN
# ============================================================

# Quantum transverse-field Ising Hamiltonian:
#
#       H =
#
#       -J sum_i sigma_z(i) sigma_z(i+1)
#
#       -g sum_i sigma_x(i)

Hamiltonian = (
    H_interaction
    + H_transverse_field
)


print(
    "\n[STEP 3] Hamiltonian Constructed"
)

print(
    "   -> H = -J Σ σz(i)σz(i+1) - g Σ σx(i)"
)

print(
    "   -> Periodic boundary conditions: ON"
)

print(
    "\n   Top-left 4x4 slice of H:"
)

print(
    Hamiltonian[:4, :4]
)


# ============================================================
# 6. SOLVE THE QUANTUM EIGENVALUE PROBLEM
# ============================================================

# Solve:
#
#       H |psi_n> = E_n |psi_n>
#
# Since H is Hermitian, scipy.linalg.eigh() is appropriate.

energy_levels, eigenstates = la.eigh(
    Hamiltonian
)


print(
    "\n[STEP 4] Quantum Eigenvalue Problem Solved"
)

print(
    f"   -> Ground-state energy E0 = "
    f"{energy_levels[0]:.6f}"
)

print(
    f"   -> First excited energy E1 = "
    f"{energy_levels[1]:.6f}"
)


# ============================================================
# 7. ENERGY GAP
# ============================================================

# The energy gap between the ground state and first excited
# state is:
#
#       Delta E = E1 - E0

energy_gap = (
    energy_levels[1]
    - energy_levels[0]
)


print(
    f"   -> Energy gap ΔE = "
    f"{energy_gap:.6f}"
)


# ============================================================
# 8. QUANTUM EXPECTATION VALUES
# ============================================================

def expectation_value(
    state,
    operator
):
    """
    Calculate:

        <psi|O|psi>

    for a normalized quantum state |psi>.
    """

    value = np.vdot(
        state,
        operator @ state
    )

    # Numerical calculations may produce tiny imaginary
    # components such as 1e-16j.
    return np.real_if_close(value).real


# Arrays for ground-state observables.

ground_state_magnetization_z = expectation_value(
    eigenstates[:, 0],
    M_z_operator
)

ground_state_magnetization_x = expectation_value(
    eigenstates[:, 0],
    M_x_operator
)


print(
    "\n[STEP 5] Ground-State Quantum Observables"
)

print(
    f"   -> <Mz> = "
    f"{ground_state_magnetization_z:.6f}"
)

print(
    f"   -> <Mx> = "
    f"{ground_state_magnetization_x:.6f}"
)


# ============================================================
# 9. THERMAL QUANTUM ENSEMBLE
# ============================================================

# We now introduce temperature.
#
# The quantum system is described by a Gibbs ensemble:
#
#       p_n = exp(-beta E_n) / Z
#
# where:
#
#       beta = 1 / (k_B T)
#
# and:
#
#       Z = sum_n exp(-beta E_n)
#
# We calculate everything in the energy eigenbasis.


thermal_energy = []

thermal_magnetization_z = []

thermal_magnetization_x = []

thermal_entropy = []

thermal_heat_capacity = []

partition_functions = []


# ============================================================
# 10. THERMAL CALCULATIONS
# ============================================================

for T in temperatures:

    beta = 1.0 / (
        K_B * T
    )

    # --------------------------------------------------------
    # Shift energies by E0.
    #
    # This does NOT change normalized probabilities.
    #
    # It prevents numerical overflow when beta is large.
    # --------------------------------------------------------

    shifted_energies = (
        energy_levels
        - energy_levels[0]
    )

    boltzmann_weights = np.exp(
        -beta * shifted_energies
    )

    partition_function = np.sum(
        boltzmann_weights
    )

    probabilities = (
        boltzmann_weights
        / partition_function
    )

    partition_functions.append(
        partition_function
    )

    # --------------------------------------------------------
    # Thermal average energy
    #
    # <E> = sum_n p_n E_n
    # --------------------------------------------------------

    average_energy = np.sum(
        probabilities
        * energy_levels
    )

    thermal_energy.append(
        average_energy
    )

    # --------------------------------------------------------
    # Thermal energy fluctuation
    #
    # <E²>
    # --------------------------------------------------------

    average_energy_squared = np.sum(
        probabilities
        * energy_levels ** 2
    )

    # --------------------------------------------------------
    # Heat capacity
    #
    # C =
    #     (<E²> - <E>²)
    #     ----------------
    #          k_B T²
    # --------------------------------------------------------

    heat_capacity = (
        average_energy_squared
        - average_energy ** 2
    ) / (
        K_B * T ** 2
    )

    thermal_heat_capacity.append(
        heat_capacity
    )

    # --------------------------------------------------------
    # Thermal magnetization
    # --------------------------------------------------------

    mz_average = 0.0

    mx_average = 0.0

    for state_idx in range(dim):

        state = eigenstates[
            :,
            state_idx
        ]

        mz_state = expectation_value(
            state,
            M_z_operator
        )

        mx_state = expectation_value(
            state,
            M_x_operator
        )

        mz_average += (
            probabilities[state_idx]
            * mz_state
        )

        mx_average += (
            probabilities[state_idx]
            * mx_state
        )

    thermal_magnetization_z.append(
        mz_average
    )

    thermal_magnetization_x.append(
        mx_average
    )

    # --------------------------------------------------------
    # Thermal entropy
    #
    # S = -k_B sum_n p_n ln(p_n)
    #
    # This is Gibbs/Shannon entropy of the energy
    # eigenstate populations.
    #
    # It is NOT a decoherence measure.
    # --------------------------------------------------------

    entropy = -K_B * np.sum(
        probabilities
        * np.log(
            probabilities + 1e-15
        )
    )

    thermal_entropy.append(
        entropy
    )


# Convert everything to NumPy arrays.

thermal_energy = np.asarray(
    thermal_energy
)

thermal_magnetization_z = np.asarray(
    thermal_magnetization_z
)

thermal_magnetization_x = np.asarray(
    thermal_magnetization_x
)

thermal_entropy = np.asarray(
    thermal_entropy
)

thermal_heat_capacity = np.asarray(
    thermal_heat_capacity
)

partition_functions = np.asarray(
    partition_functions
)


# ============================================================
# 11. PRINT THERMAL RESULTS
# ============================================================

print(
    "\n[STEP 6] Thermal Quantum Ensemble Calculated"
)

print(
    f"   -> Low-temperature energy: "
    f"{thermal_energy[0]:.6f}"
)

print(
    f"   -> High-temperature energy: "
    f"{thermal_energy[-1]:.6f}"
)

print(
    f"   -> Low-temperature entropy: "
    f"{thermal_entropy[0]:.6f}"
)

print(
    f"   -> High-temperature entropy: "
    f"{thermal_entropy[-1]:.6f}"
)


# ============================================================
# 12. SAVE FIGURES
# ============================================================

script_directory = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# GRAPH 1 — HAMILTONIAN MATRIX
# ============================================================

plt.figure(
    figsize=(7, 6)
)

plt.imshow(
    Hamiltonian,
    cmap="seismic"
)

plt.title(
    "Quantum Transverse-Field Ising Hamiltonian"
)

plt.xlabel(
    "Basis-state index"
)

plt.ylabel(
    "Basis-state index"
)

plt.colorbar(
    label="Hamiltonian matrix element"
)

matrix_path = os.path.join(
    script_directory,
    "quantum_hamiltonian_matrix.png"
)

plt.savefig(
    matrix_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# GRAPH 2 — ENERGY SPECTRUM
# ============================================================

plt.figure(
    figsize=(8, 5)
)

plt.plot(
    range(dim),
    energy_levels,
    marker="o"
)

plt.xlabel(
    "Eigenstate index n"
)

plt.ylabel(
    "Energy E_n"
)

plt.title(
    "Quantum Ising Energy Spectrum"
)

plt.grid(
    True
)

spectrum_path = os.path.join(
    script_directory,
    "quantum_energy_spectrum.png"
)

plt.savefig(
    spectrum_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# GRAPH 3 — THERMAL ENERGY
# ============================================================

plt.figure(
    figsize=(8, 5)
)

plt.plot(
    temperatures,
    thermal_energy
)

plt.xlabel(
    "Temperature T"
)

plt.ylabel(
    "Thermal average energy <E>"
)

plt.title(
    "Quantum Ising Model: Energy vs Temperature"
)

plt.grid(
    True
)

energy_path = os.path.join(
    script_directory,
    "quantum_energy_vs_temperature.png"
)

plt.savefig(
    energy_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# GRAPH 4 — MAGNETIZATION
# ============================================================

plt.figure(
    figsize=(8, 5)
)

plt.plot(
    temperatures,
    thermal_magnetization_z,
    label="Mz"
)

plt.plot(
    temperatures,
    thermal_magnetization_x,
    label="Mx"
)

plt.xlabel(
    "Temperature T"
)

plt.ylabel(
    "Thermal expectation value"
)

plt.title(
    "Quantum Ising Model: Magnetization vs Temperature"
)

plt.grid(
    True
)

plt.legend()

magnetization_path = os.path.join(
    script_directory,
    "quantum_magnetization_vs_temperature.png"
)

plt.savefig(
    magnetization_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# GRAPH 5 — HEAT CAPACITY
# ============================================================

plt.figure(
    figsize=(8, 5)
)

plt.plot(
    temperatures,
    thermal_heat_capacity
)

plt.xlabel(
    "Temperature T"
)

plt.ylabel(
    "Heat capacity C"
)

plt.title(
    "Quantum Ising Model: Heat Capacity vs Temperature"
)

plt.grid(
    True
)

heat_capacity_path = os.path.join(
    script_directory,
    "quantum_heat_capacity_vs_temperature.png"
)

plt.savefig(
    heat_capacity_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# GRAPH 6 — THERMAL ENTROPY
# ============================================================

plt.figure(
    figsize=(8, 5)
)

plt.plot(
    temperatures,
    thermal_entropy
)

plt.xlabel(
    "Temperature T"
)

plt.ylabel(
    "Gibbs entropy S"

)

plt.title(
    "Quantum Ising Model: Thermal Entropy vs Temperature"
)

plt.grid(
    True
)

entropy_path = os.path.join(
    script_directory,
    "quantum_thermal_entropy_vs_temperature.png"
)

plt.savefig(
    entropy_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 13. FINAL SUMMARY
# ============================================================

print(
    "\n[STEP 7] Visual Assets Generated"
)

print(
    f"   -> Hamiltonian matrix: "
    f"{matrix_path}"
)

print(
    f"   -> Energy spectrum: "
    f"{spectrum_path}"
)

print(
    f"   -> Energy vs temperature: "
    f"{energy_path}"
)

print(
    f"   -> Magnetization vs temperature: "
    f"{magnetization_path}"
)

print(
    f"   -> Heat capacity: "
    f"{heat_capacity_path}"
)

print(
    f"   -> Thermal entropy: "
    f"{entropy_path}"
)


print(
    "\n=== Quantum Ising Module Completed Successfully ==="
)