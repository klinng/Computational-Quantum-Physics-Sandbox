"""
Module 5 — Open Quantum Systems
================================

A numerical introduction to density matrices, Lindblad dynamics,
quantum dephasing, purity, and von Neumann entropy.

Physical system:
    Single qubit

Hamiltonian:
    H = -(g/2) * sigma_x

Dephasing:
    L = sqrt(gamma) * sigma_z

Master equation:
    dρ/dt = -i[H, ρ]
             + LρL†
             - 1/2 {L†L, ρ}

The numerical solution is compared with the analytical solution
for pure dephasing when the Hamiltonian is turned off.

Units:
    hbar = 1
    k_B = 1
"""

import os

import numpy as np
import scipy.linalg as la
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


print("=== Module 5: Open Quantum System ===")


# ============================================================
# 1. PHYSICAL CONFIGURATION
# ============================================================

hbar = 1.0

# Qubit parameters
g = 0.0

# Dephasing rate
gamma = 0.5

# Initial state: |+> = (|0> + |1>) / sqrt(2)
# This is a coherent superposition and is therefore ideal
# for demonstrating decoherence.
psi_initial = np.array(
    [1.0, 1.0],
    dtype=complex
) / np.sqrt(2)

rho_initial = np.outer(
    psi_initial,
    np.conjugate(psi_initial)
)

# Time grid
t_start = 0.0
t_end = 10.0
number_of_times = 500

times = np.linspace(
    t_start,
    t_end,
    number_of_times
)


# ============================================================
# 2. PAULI MATRICES
# ============================================================

I = np.eye(2, dtype=complex)

sigma_x = np.array(
    [
        [0, 1],
        [1, 0]
    ],
    dtype=complex
)

sigma_y = np.array(
    [
        [0, -1j],
        [1j, 0]
    ],
    dtype=complex
)

sigma_z = np.array(
    [
        [1, 0],
        [0, -1]
    ],
    dtype=complex
)


# ============================================================
# 3. SYSTEM HAMILTONIAN
# ============================================================

# H = -(g/2) sigma_x
Hamiltonian = -(g / 2.0) * sigma_x


# ============================================================
# 4. LINDBLAD COLLAPSE OPERATOR
# ============================================================

# Pure dephasing operator
#
# L = sqrt(gamma) sigma_z
#
# This leaves populations unchanged but suppresses
# quantum coherence.
collapse_operator = np.sqrt(gamma) * sigma_z


# ============================================================
# 5. BASIC DENSITY-MATRIX FUNCTIONS
# ============================================================

def commutator(A, B):
    """
    Compute the commutator:

        [A, B] = AB - BA
    """

    return A @ B - B @ A


def anticommutator(A, B):
    """
    Compute the anticommutator:

        {A, B} = AB + BA
    """

    return A @ B + B @ A


def expectation_value(rho, operator):
    """
    Calculate:

        <A> = Tr(rho A)
    """

    value = np.trace(rho @ operator)

    return float(np.real_if_close(value))


def purity(rho):
    """
    Quantum-state purity:

        P = Tr(rho^2)

    Pure state:
        P = 1

    Mixed state:
        P < 1
    """

    value = np.trace(rho @ rho)

    return float(np.real_if_close(value))


def von_neumann_entropy(rho):
    """
    Von Neumann entropy:

        S = -Tr(rho ln(rho))

    Calculated from the eigenvalues of rho.
    """

    eigenvalues = np.linalg.eigvalsh(rho)

    # Remove tiny numerical negative values
    eigenvalues = np.clip(
        eigenvalues.real,
        0.0,
        None
    )

    # Only non-zero eigenvalues contribute
    nonzero = eigenvalues[eigenvalues > 1e-14]

    if len(nonzero) == 0:
        return 0.0

    return float(
        -np.sum(nonzero * np.log(nonzero))
    )


# ============================================================
# 6. LINDBLAD MASTER EQUATION
# ============================================================

def lindblad_rhs(rho):
    """
    Right-hand side of the Lindblad master equation:

        dρ/dt =
            -i/hbar [H,ρ]
            + LρL†
            - 1/2 {L†L,ρ}
    """

    # Hamiltonian contribution
    unitary_part = (
        -1j / hbar
        * commutator(Hamiltonian, rho)
    )

    # Dissipative contribution
    L = collapse_operator
    L_dagger = L.conj().T

    dissipative_part = (
        L @ rho @ L_dagger
        - 0.5
        * anticommutator(
            L_dagger @ L,
            rho
        )
    )

    return unitary_part + dissipative_part


# ============================================================
# 7. CONVERT COMPLEX MATRIX <-> REAL VECTOR
# ============================================================

def matrix_to_vector(matrix):
    """
    scipy.solve_ivp works naturally with a 1D vector.

    A complex 2x2 density matrix is flattened into
    four complex numbers.
    """

    return matrix.flatten()


def vector_to_matrix(vector):
    """
    Convert the flattened vector back into
    the 2x2 density matrix.
    """

    return vector.reshape((2, 2))


def ode_function(t, vector):
    """
    Function passed to scipy.integrate.solve_ivp.
    """

    rho = vector_to_matrix(vector)

    drho_dt = lindblad_rhs(rho)

    return matrix_to_vector(drho_dt)


# ============================================================
# 8. NUMERICALLY SOLVE THE MASTER EQUATION
# ============================================================

print("\n[STEP 1] Initial density matrix:")
print(rho_initial)

print("\n[STEP 2] Solving Lindblad master equation...")

solution = solve_ivp(
    ode_function,
    (t_start, t_end),
    matrix_to_vector(rho_initial),
    t_eval=times,
    method="RK45",
    rtol=1e-9,
    atol=1e-11
)

if not solution.success:
    raise RuntimeError(
        "Lindblad integration failed: "
        + solution.message
    )


# ============================================================
# 9. EXTRACT DENSITY MATRICES
# ============================================================

density_matrices = []

for index in range(len(times)):

    rho = vector_to_matrix(
        solution.y[:, index]
    )

    # Remove tiny numerical imaginary errors
    rho = 0.5 * (
        rho + rho.conj().T
    )

    density_matrices.append(rho)


# ============================================================
# 10. MEASURE PHYSICAL QUANTITIES
# ============================================================

population_0 = []
population_1 = []

coherence = []

x_expectation = []
y_expectation = []
z_expectation = []

purity_values = []
entropy_values = []

trace_values = []


for rho in density_matrices:

    # Populations
    population_0.append(
        np.real(rho[0, 0])
    )

    population_1.append(
        np.real(rho[1, 1])
    )

    # Magnitude of the off-diagonal coherence
    coherence.append(
        np.abs(rho[0, 1])
    )

    # Quantum expectation values
    x_expectation.append(
        expectation_value(rho, sigma_x)
    )

    y_expectation.append(
        expectation_value(rho, sigma_y)
    )

    z_expectation.append(
        expectation_value(rho, sigma_z)
    )

    # State properties
    purity_values.append(
        purity(rho)
    )

    entropy_values.append(
        von_neumann_entropy(rho)
    )

    # Trace should remain equal to 1
    trace_values.append(
        np.trace(rho).real
    )


# ============================================================
# 11. ANALYTICAL DEPHASING SOLUTION
# ============================================================

"""
For:

    H = 0

and

    L = sqrt(gamma) sigma_z

the off-diagonal density-matrix element follows:

    rho_01(t) = rho_01(0) exp(-2 gamma t)

Therefore:

    |rho_01(t)|
        = |rho_01(0)| exp(-2 gamma t)
"""

initial_coherence = np.abs(
    rho_initial[0, 1]
)

analytical_coherence = (
    initial_coherence
    * np.exp(-2.0 * gamma * times)
)


# ============================================================
# 12. NUMERICAL VALIDATION
# ============================================================

maximum_error = np.max(
    np.abs(
        np.array(coherence)
        - analytical_coherence
    )
)

print("\n[STEP 3] Analytical validation:")
print(
    f"   -> Maximum coherence error: "
    f"{maximum_error:.3e}"
)

print(
    f"   -> Initial purity: "
    f"{purity_values[0]:.6f}"
)

print(
    f"   -> Final purity: "
    f"{purity_values[-1]:.6f}"
)

print(
    f"   -> Initial entropy: "
    f"{entropy_values[0]:.6f}"
)

print(
    f"   -> Final entropy: "
    f"{entropy_values[-1]:.6f}"
)

print(
    f"   -> Initial trace: "
    f"{trace_values[0]:.6f}"
)

print(
    f"   -> Final trace: "
    f"{trace_values[-1]:.6f}"
)


# ============================================================
# 13. OUTPUT DIRECTORY
# ============================================================

script_directory = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# 14. GRAPH 1 — DENSITY MATRIX COHERENCE
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    times,
    coherence,
    linewidth=2,
    label="Numerical |ρ₀₁(t)|"
)

plt.plot(
    times,
    analytical_coherence,
    linestyle="--",
    linewidth=2,
    label="Analytical solution"
)

plt.xlabel("Time")
plt.ylabel("Coherence |ρ₀₁|")

plt.title(
    "Quantum Dephasing: Loss of Coherence"
)

plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

coherence_path = os.path.join(
    script_directory,
    "dephasing_coherence.png"
)

plt.savefig(
    coherence_path,
    dpi=150
)

plt.close()


# ============================================================
# 15. GRAPH 2 — POPULATIONS
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    times,
    population_0,
    linewidth=2,
    label="Population |0⟩"
)

plt.plot(
    times,
    population_1,
    linewidth=2,
    label="Population |1⟩"
)

plt.xlabel("Time")
plt.ylabel("Population")

plt.title(
    "Populations During Pure Dephasing"
)

plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

population_path = os.path.join(
    script_directory,
    "dephasing_populations.png"
)

plt.savefig(
    population_path,
    dpi=150
)

plt.close()


# ============================================================
# 16. GRAPH 3 — PURITY
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    times,
    purity_values,
    linewidth=2
)

plt.xlabel("Time")
plt.ylabel("Purity Tr(ρ²)")

plt.title(
    "Quantum-State Purity"
)

plt.grid(alpha=0.3)
plt.tight_layout()

purity_path = os.path.join(
    script_directory,
    "quantum_purity.png"
)

plt.savefig(
    purity_path,
    dpi=150
)

plt.close()


# ============================================================
# 17. GRAPH 4 — VON NEUMANN ENTROPY
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    times,
    entropy_values,
    linewidth=2
)

plt.xlabel("Time")
plt.ylabel("Entropy S")

plt.title(
    "Von Neumann Entropy"
)

plt.grid(alpha=0.3)
plt.tight_layout()

entropy_path = os.path.join(
    script_directory,
    "von_neumann_entropy.png"
)

plt.savefig(
    entropy_path,
    dpi=150
)

plt.close()


# ============================================================
# 18. GRAPH 5 — BLOCH VECTOR
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    times,
    x_expectation,
    linewidth=2,
    label="⟨σx⟩"
)

plt.plot(
    times,
    y_expectation,
    linewidth=2,
    label="⟨σy⟩"
)

plt.plot(
    times,
    z_expectation,
    linewidth=2,
    label="⟨σz⟩"
)

plt.xlabel("Time")
plt.ylabel("Expectation value")

plt.title(
    "Bloch-Vector Components During Dephasing"
)

plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

bloch_path = os.path.join(
    script_directory,
    "bloch_vector_components.png"
)

plt.savefig(
    bloch_path,
    dpi=150
)

plt.close()


# ============================================================
# 19. FINAL VALIDATION
# ============================================================

trace_error = np.max(
    np.abs(
        np.array(trace_values) - 1.0
    )
)

print("\n[STEP 4] Physical validation:")

print(
    f"   -> Maximum trace error: "
    f"{trace_error:.3e}"
)

print(
    f"   -> Maximum analytical coherence error: "
    f"{maximum_error:.3e}"
)

print(
    "\n[STEP 5] Output files:"
)

print(
    "   -> dephasing_coherence.png"
)

print(
    "   -> dephasing_populations.png"
)

print(
    "   -> quantum_purity.png"
)

print(
    "   -> von_neumann_entropy.png"
)

print(
    "   -> bloch_vector_components.png"
)

print(
    "\n=== Module 5 completed successfully ==="
)