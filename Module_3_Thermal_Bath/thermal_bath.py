"""
Module 3: 1D Ising Model — Metropolis Monte Carlo

Classical statistical-physics model:

    E = -J * sum_i s_i s_{i+1}

where:

    s_i = +1 or -1
    J = 1
    k_B = 1

The simulation:
    1. Equilibrates the spin chain.
    2. Samples thermal states.
    3. Repeats the calculation for several temperatures.
    4. Computes energy, magnetization, specific heat,
       and magnetic susceptibility.

This is a classical thermal model, not a quantum-decoherence
simulation. A 1D Ising chain has no finite-temperature phase
transition in the thermodynamic limit.
"""

import os
import numpy as np
import matplotlib.pyplot as plt


print("=== Module 3: 1D Ising Model — Metropolis Monte Carlo ===")


# ============================================================
# 1. MODEL PARAMETERS
# ============================================================

N_SPINS = 50

J = 1.0

K_B = 1.0

# Temperatures that we will investigate.
TEMPERATURES = np.linspace(0.5, 4.0, 15)

# Number of Monte Carlo sweeps used to let the system
# reach thermal equilibrium.
EQUILIBRATION_SWEEPS = 1000

# Number of sweeps used to collect measurements.
MEASUREMENT_SWEEPS = 3000

# We do not need to measure after every sweep.
SAMPLE_INTERVAL = 10

# Fixed random seed makes the experiment reproducible.
rng = np.random.default_rng(42)


# ============================================================
# 2. TOTAL ENERGY
# ============================================================

def total_energy(spins, J=1.0):
    """
    Calculate the total energy of a 1D Ising chain.

    We use open boundary conditions:

        E = -J * sum(s_i * s_{i+1})

    Example:

        spins = [+1, +1, -1, -1]

    Interactions are:

        +1 * +1
        +1 * -1
        -1 * -1
    """

    interactions = spins[:-1] * spins[1:]

    return -J * np.sum(interactions)


# ============================================================
# 3. MAGNETIZATION
# ============================================================

def magnetization(spins):
    """
    Calculate the average magnetization per spin.

        m = (1/N) * sum(s_i)
    """

    return np.mean(spins)


# ============================================================
# 4. ONE METROPOLIS SPIN-FLIP ATTEMPT
# ============================================================

def metropolis_step(spins, temperature, J=1.0, rng=None):
    """
    Attempt to flip one randomly selected spin.

    The spin changes:

        s_i -> -s_i

    The energy difference is:

        dE = E_new - E_old

    If:

        dE <= 0

    the move is always accepted.

    If:

        dE > 0

    the move is accepted with probability:

        exp(-dE / (k_B*T))
    """

    if rng is None:
        rng = np.random.default_rng()

    N = len(spins)

    # Select a random spin.
    i = rng.integers(0, N)

    old_spin = spins[i]

    # --------------------------------------------------------
    # Calculate the sum of neighbouring spins.
    # --------------------------------------------------------

    neighbor_sum = 0

    # Left neighbour exists?
    if i > 0:
        neighbor_sum += spins[i - 1]

    # Right neighbour exists?
    if i < N - 1:
        neighbor_sum += spins[i + 1]

    # --------------------------------------------------------
    # Energy change caused by flipping the spin.
    #
    # dE = 2 J s_i (s_left + s_right)
    # --------------------------------------------------------

    dE = 2.0 * J * old_spin * neighbor_sum

    # --------------------------------------------------------
    # Metropolis acceptance rule.
    # --------------------------------------------------------

    # Energetically favourable move.
    if dE <= 0:

        spins[i] = -old_spin

        return True

    # Energetically unfavourable move.
    probability = np.exp(
        -dE / (K_B * temperature)
    )

    if rng.random() < probability:

        spins[i] = -old_spin

        return True

    return False


# ============================================================
# 5. ONE MONTE CARLO SWEEP
# ============================================================

def monte_carlo_sweep(spins, temperature, J=1.0, rng=None):
    """
    Perform N spin-flip attempts.

    Since there are N spins, one sweep corresponds to
    approximately one attempted update per spin.
    """

    accepted = 0

    for _ in range(len(spins)):

        if metropolis_step(
            spins,
            temperature,
            J,
            rng
        ):

            accepted += 1

    # Return the fraction of accepted moves.
    return accepted / len(spins)


# ============================================================
# 6. SIMULATION AT ONE TEMPERATURE
# ============================================================

def simulate_temperature(
    temperature,
    N=N_SPINS,
    J=J,
    equilibration_sweeps=EQUILIBRATION_SWEEPS,
    measurement_sweeps=MEASUREMENT_SWEEPS,
    sample_interval=SAMPLE_INTERVAL,
    rng=None,
):
    """
    Run the complete Monte Carlo simulation at one temperature.

    Returns:

        energy per spin
        average absolute magnetization
        specific heat
        magnetic susceptibility
        acceptance rate
    """

    if rng is None:
        rng = np.random.default_rng()

    # --------------------------------------------------------
    # Initial spin configuration
    # --------------------------------------------------------

    # Each spin is randomly chosen as -1 or +1.
    spins = rng.choice(
        [-1, 1],
        size=N
    ).astype(float)

    # ========================================================
    # A. EQUILIBRATION
    # ========================================================

    for _ in range(equilibration_sweeps):

        monte_carlo_sweep(
            spins,
            temperature,
            J,
            rng
        )

    # ========================================================
    # B. MEASUREMENT
    # ========================================================

    energy_samples = []

    magnetization_samples = []

    accepted_moves = 0

    attempted_moves = 0

    for sweep in range(measurement_sweeps):

        acceptance = monte_carlo_sweep(
            spins,
            temperature,
            J,
            rng
        )

        accepted_moves += acceptance * N

        attempted_moves += N

        # Sample only every few sweeps.
        if sweep % sample_interval == 0:

            energy_samples.append(
                total_energy(
                    spins,
                    J
                )
            )

            magnetization_samples.append(
                magnetization(spins)
            )

    # Convert lists to NumPy arrays.
    energy_samples = np.asarray(
        energy_samples
    )

    magnetization_samples = np.asarray(
        magnetization_samples
    )

    # ========================================================
    # C. THERMAL AVERAGES
    # ========================================================

    mean_energy = np.mean(
        energy_samples
    )

    mean_energy_squared = np.mean(
        energy_samples ** 2
    )

    mean_magnetization = np.mean(
        magnetization_samples
    )

    mean_magnetization_squared = np.mean(
        magnetization_samples ** 2
    )

    # Energy per spin.
    mean_energy_per_spin = (
        mean_energy / N
    )

    # We use |m| because the magnetization can switch
    # between positive and negative values.
    mean_abs_magnetization = np.mean(
        np.abs(
            magnetization_samples
        )
    )

    # ========================================================
    # D. SPECIFIC HEAT
    # ========================================================

    # Fluctuation formula:

    # C =
    #     (<E²> - <E>²)
    #     ----------------
    #          N k_B T²

    specific_heat = (
        (
            mean_energy_squared
            - mean_energy ** 2
        )
        / (
            N
            * K_B
            * temperature ** 2
        )
    )

    # ========================================================
    # E. MAGNETIC SUSCEPTIBILITY
    # ========================================================

    # chi =
    #
    #       N(<m²> - <m>²)
    #       ----------------
    #             k_B T

    susceptibility = (
        N
        * (
            mean_magnetization_squared
            - mean_magnetization ** 2
        )
        / (
            K_B
            * temperature
        )
    )

    # ========================================================
    # F. ACCEPTANCE RATE
    # ========================================================

    acceptance_rate = (
        accepted_moves
        / attempted_moves
    )

    return {
        "energy_per_spin": mean_energy_per_spin,

        "abs_magnetization":
            mean_abs_magnetization,

        "specific_heat":
            specific_heat,

        "susceptibility":
            susceptibility,

        "acceptance_rate":
            acceptance_rate,
    }


# ============================================================
# 7. RUN THE TEMPERATURE SWEEP
# ============================================================

energy_results = []

magnetization_results = []

specific_heat_results = []

susceptibility_results = []

acceptance_results = []


print("\nRunning temperature sweep...\n")


for temperature in TEMPERATURES:

    results = simulate_temperature(
        temperature=temperature,
        rng=rng
    )

    energy_results.append(
        results["energy_per_spin"]
    )

    magnetization_results.append(
        results["abs_magnetization"]
    )

    specific_heat_results.append(
        results["specific_heat"]
    )

    susceptibility_results.append(
        results["susceptibility"]
    )

    acceptance_results.append(
        results["acceptance_rate"]
    )

    print(
        f"T = {temperature:.2f} | "
        f"E/N = {results['energy_per_spin']:.4f} | "
        f"|M| = {results['abs_magnetization']:.4f} | "
        f"C = {results['specific_heat']:.4f} | "
        f"chi = {results['susceptibility']:.4f}"
    )


# ============================================================
# 8. CONVERT RESULTS TO NUMPY ARRAYS
# ============================================================

energy_results = np.asarray(
    energy_results
)

magnetization_results = np.asarray(
    magnetization_results
)

specific_heat_results = np.asarray(
    specific_heat_results
)

susceptibility_results = np.asarray(
    susceptibility_results
)

acceptance_results = np.asarray(
    acceptance_results
)


# ============================================================
# 9. SAVE FIGURES
# ============================================================

# Save the figures in the same folder as this Python file.

script_directory = os.path.dirname(
    os.path.abspath(__file__)
)


def save_plot(
    filename,
    ylabel,
    title,
    values
):
    """
    Create and save a temperature-dependence plot.
    """

    plt.figure(
        figsize=(8, 5)
    )

    plt.plot(
        TEMPERATURES,
        values,
        marker="o"
    )

    plt.xlabel(
        "Temperature T"
    )

    plt.ylabel(
        ylabel
    )

    plt.title(
        title
    )

    plt.grid(True)

    path = os.path.join(
        script_directory,
        filename
    )

    plt.savefig(
        path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    return path


# ------------------------------------------------------------
# Energy
# ------------------------------------------------------------

energy_path = save_plot(
    "ising_energy_vs_temperature.png",

    "Energy per spin E/N",

    "1D Ising Model: Energy vs Temperature",

    energy_results
)


# ------------------------------------------------------------
# Magnetization
# ------------------------------------------------------------

magnetization_path = save_plot(
    "ising_magnetization_vs_temperature.png",

    "Average |magnetization|",

    "1D Ising Model: Magnetization vs Temperature",

    magnetization_results
)


# ------------------------------------------------------------
# Specific heat
# ------------------------------------------------------------

specific_heat_path = save_plot(
    "ising_specific_heat_vs_temperature.png",

    "Specific heat per spin",

    "1D Ising Model: Specific Heat vs Temperature",

    specific_heat_results
)


# ------------------------------------------------------------
# Susceptibility
# ------------------------------------------------------------

susceptibility_path = save_plot(
    "ising_susceptibility_vs_temperature.png",

    "Magnetic susceptibility",

    "1D Ising Model: Susceptibility vs Temperature",

    susceptibility_results
)


# ============================================================
# 10. FINAL MESSAGE
# ============================================================

print(
    "\n=== Module 3 completed successfully ==="
)

print(
    "\nSaved figures:"
)

print(
    f" -> {energy_path}"
)

print(
    f" -> {magnetization_path}"
)

print(
    f" -> {specific_heat_path}"
)

print(
    f" -> {susceptibility_path}"
)

print(
    "\nImportant:"
)

print(
    "The 1D Ising model has no finite-temperature "
    "phase transition in the thermodynamic limit."
)