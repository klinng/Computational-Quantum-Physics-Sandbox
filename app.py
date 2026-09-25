"""
Unified Computational & Quantum Physics Laboratory

Streamlit front-end for Modules 1–5 of the project.
The calculations are kept inside this application so the UI does not
execute the original script files (which also generate their portfolio plots).
"""

import numpy as np
import scipy.linalg as la
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import streamlit as st


st.set_page_config(
    page_title="Computational & Quantum Physics Lab",
    page_icon="🌌",
    layout="wide",
)


# -----------------------------------------------------------------------------
# Shared helpers
# -----------------------------------------------------------------------------


def pauli_matrices():
    sx = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    sy = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
    sz = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    return sx, sy, sz


def tensor_operator(op, site, n_spins):
    identity = np.eye(2, dtype=complex)
    result = np.array([[1.0]], dtype=complex)
    for i in range(n_spins):
        result = np.kron(result, op if i == site else identity)
    return result


# -----------------------------------------------------------------------------
# Module 1 — Matrix Engine
# -----------------------------------------------------------------------------


def matrix_engine(n_points=50):
    x = np.linspace(0.0, 2.0 * np.pi, n_points)
    dx = x[1] - x[0]
    x_operator = np.diag(x)
    d_operator = (
        np.diag(np.ones(n_points - 1), 1)
        - np.diag(np.ones(n_points - 1), -1)
    ) / (2.0 * dx)
    psi = np.sin(x)
    numerical_derivative = d_operator @ psi
    exact_derivative = np.cos(x)
    error = np.max(np.abs(numerical_derivative - exact_derivative))
    return x, x_operator, d_operator, psi, numerical_derivative, exact_derivative, error


# -----------------------------------------------------------------------------
# Module 2 — Particle in a Box
# -----------------------------------------------------------------------------


def quantum_box(n_points=100, n_states=3, length=1.0):
    x_full = np.linspace(0.0, length, n_points + 2)
    dx = x_full[1] - x_full[0]
    x = x_full[1:-1]

    main = -2.0 * np.ones(n_points)
    off = np.ones(n_points - 1)
    d2 = np.diag(main) + np.diag(off, 1) + np.diag(off, -1)
    hamiltonian = -0.5 * d2 / dx**2

    energies, states = la.eigh(hamiltonian)
    n_states = min(n_states, n_points)

    states = states[:, :n_states].copy()
    selected_energies = energies[:n_states].copy()

    for i in range(n_states):
        norm = np.sqrt(np.trapezoid(np.abs(states[:, i]) ** 2, x))
        states[:, i] /= norm

    analytical = np.array(
        [(n**2 * np.pi**2) / (2.0 * length**2) for n in range(1, n_states + 1)]
    )
    relative_error = np.abs((selected_energies - analytical) / analytical)
    return x, hamiltonian, selected_energies, states, analytical, relative_error


# -----------------------------------------------------------------------------
# Module 3 — Classical 1D Ising / Metropolis Monte Carlo
# -----------------------------------------------------------------------------


def classical_ising_sweep(
    n_spins=30,
    j=1.0,
    t_min=0.5,
    t_max=4.0,
    n_temperatures=12,
    equilibration_sweeps=300,
    measurement_sweeps=1000,
    sample_interval=10,
    seed=42,
):
    rng = np.random.default_rng(seed)
    temperatures = np.linspace(t_min, t_max, n_temperatures)

    energy_results = []
    magnetization_results = []
    heat_results = []
    susceptibility_results = []
    acceptance_results = []

    for temperature in temperatures:
        spins = rng.choice([-1.0, 1.0], size=n_spins)

        def attempt_flip():
            i = rng.integers(0, n_spins)
            neighbor_sum = 0.0
            if i > 0:
                neighbor_sum += spins[i - 1]
            if i < n_spins - 1:
                neighbor_sum += spins[i + 1]
            d_e = 2.0 * j * spins[i] * neighbor_sum
            if d_e <= 0.0 or rng.random() < np.exp(-d_e / temperature):
                spins[i] *= -1.0
                return True
            return False

        for _ in range(equilibration_sweeps):
            for _ in range(n_spins):
                attempt_flip()

        energies = []
        magnetizations = []
        accepted = 0
        attempted = 0

        for sweep in range(measurement_sweeps):
            for _ in range(n_spins):
                accepted += int(attempt_flip())
                attempted += 1

            if (sweep + 1) % sample_interval == 0:
                energy = -j * np.sum(spins[:-1] * spins[1:])
                magnetization = np.mean(spins)
                energies.append(energy)
                magnetizations.append(magnetization)

        energies = np.asarray(energies)
        magnetizations = np.asarray(magnetizations)
        mean_e = np.mean(energies)
        mean_e2 = np.mean(energies**2)
        mean_m = np.mean(magnetizations)
        mean_m2 = np.mean(magnetizations**2)

        energy_results.append(mean_e / n_spins)
        magnetization_results.append(np.mean(np.abs(magnetizations)))
        heat_results.append((mean_e2 - mean_e**2) / (n_spins * temperature**2))
        susceptibility_results.append(
            n_spins * (mean_m2 - mean_m**2) / temperature
        )
        acceptance_results.append(accepted / attempted if attempted else 0.0)

    return {
        "temperatures": temperatures,
        "energy": np.asarray(energy_results),
        "magnetization": np.asarray(magnetization_results),
        "heat_capacity": np.asarray(heat_results),
        "susceptibility": np.asarray(susceptibility_results),
        "acceptance": np.asarray(acceptance_results),
    }


# -----------------------------------------------------------------------------
# Module 4 — Quantum Transverse-Field Ising Model
# -----------------------------------------------------------------------------


def quantum_ising(n_spins=4, j=1.0, g=1.0, temperatures=None):
    if temperatures is None:
        temperatures = np.linspace(0.1, 5.0, 80)

    sx, _, sz = pauli_matrices()
    dim = 2**n_spins
    h_interaction = np.zeros((dim, dim), dtype=complex)
    h_field = np.zeros((dim, dim), dtype=complex)
    mz_operator = np.zeros((dim, dim), dtype=complex)
    mx_operator = np.zeros((dim, dim), dtype=complex)

    sz_ops = [tensor_operator(sz, i, n_spins) for i in range(n_spins)]
    sx_ops = [tensor_operator(sx, i, n_spins) for i in range(n_spins)]

    for i in range(n_spins):
        h_interaction -= j * (sz_ops[i] @ sz_ops[(i + 1) % n_spins])
        h_field -= g * sx_ops[i]
        mz_operator += sz_ops[i]
        mx_operator += sx_ops[i]

    mz_operator /= n_spins
    mx_operator /= n_spins
    hamiltonian = h_interaction + h_field
    energies, states = la.eigh(hamiltonian)

    mz_eigen = np.real(np.einsum("ij,ji->i", states.conj().T @ mz_operator, states))
    mx_eigen = np.real(np.einsum("ij,ji->i", states.conj().T @ mx_operator, states))

    thermal_energy = []
    thermal_mz = []
    thermal_mx = []
    heat_capacity = []
    entropy = []

    shifted = energies - energies[0]

    for temperature in temperatures:
        weights = np.exp(-shifted / temperature)
        probabilities = weights / np.sum(weights)
        avg_e = np.sum(probabilities * energies)
        avg_e2 = np.sum(probabilities * energies**2)
        thermal_energy.append(avg_e)
        thermal_mz.append(np.sum(probabilities * mz_eigen))
        thermal_mx.append(np.sum(probabilities * mx_eigen))
        heat_capacity.append((avg_e2 - avg_e**2) / temperature**2)
        entropy.append(-np.sum(probabilities * np.log(probabilities + 1e-15)))

    return {
        "hamiltonian": hamiltonian,
        "energies": energies,
        "states": states,
        "energy_gap": energies[1] - energies[0],
        "ground_mz": mz_eigen[0],
        "ground_mx": mx_eigen[0],
        "temperatures": np.asarray(temperatures),
        "thermal_energy": np.asarray(thermal_energy),
        "thermal_mz": np.asarray(thermal_mz),
        "thermal_mx": np.asarray(thermal_mx),
        "heat_capacity": np.asarray(heat_capacity),
        "entropy": np.asarray(entropy),
    }


# -----------------------------------------------------------------------------
# Module 5 — Open Quantum System / Lindblad dephasing
# -----------------------------------------------------------------------------


def open_quantum_system(gamma=0.5, g=0.0, t_end=10.0, n_times=400):
    hbar = 1.0
    sx, sy, sz = pauli_matrices()
    hamiltonian = -(g / 2.0) * sx
    collapse = np.sqrt(gamma) * sz

    psi_initial = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2.0)
    rho_initial = np.outer(psi_initial, psi_initial.conj())
    times = np.linspace(0.0, t_end, n_times)

    def commutator(a, b):
        return a @ b - b @ a

    def anticommutator(a, b):
        return a @ b + b @ a

    def rhs(_, vector):
        rho = vector.reshape(2, 2)
        unitary = -1j / hbar * commutator(hamiltonian, rho)
        dissipative = (
            collapse @ rho @ collapse.conj().T
            - 0.5 * anticommutator(collapse.conj().T @ collapse, rho)
        )
        return (unitary + dissipative).flatten()

    solution = solve_ivp(
        rhs,
        (0.0, t_end),
        rho_initial.flatten(),
        t_eval=times,
        method="RK45",
        rtol=1e-9,
        atol=1e-11,
    )
    if not solution.success:
        raise RuntimeError(solution.message)

    rho_series = []
    populations_0 = []
    populations_1 = []
    coherence = []
    bloch_x = []
    bloch_y = []
    bloch_z = []
    purity = []
    entropy = []
    traces = []

    for column in solution.y.T:
        rho = column.reshape(2, 2)
        rho = 0.5 * (rho + rho.conj().T)
        rho_series.append(rho)
        populations_0.append(np.real(rho[0, 0]))
        populations_1.append(np.real(rho[1, 1]))
        coherence.append(np.abs(rho[0, 1]))
        bloch_x.append(np.real(np.trace(rho @ sx)))
        bloch_y.append(np.real(np.trace(rho @ sy)))
        bloch_z.append(np.real(np.trace(rho @ sz)))
        purity.append(np.real(np.trace(rho @ rho)))
        eigenvalues = np.clip(np.linalg.eigvalsh(rho).real, 0.0, None)
        nz = eigenvalues[eigenvalues > 1e-14]
        entropy.append(float(-np.sum(nz * np.log(nz))) if len(nz) else 0.0)
        traces.append(np.real(np.trace(rho)))

    initial_coherence = coherence[0]
    analytical = initial_coherence * np.exp(-2.0 * gamma * times)
    max_error = float(np.max(np.abs(np.asarray(coherence) - analytical))) if g == 0 else None

    return {
        "times": times,
        "rho_series": rho_series,
        "population_0": np.asarray(populations_0),
        "population_1": np.asarray(populations_1),
        "coherence": np.asarray(coherence),
        "analytical_coherence": analytical,
        "bloch_x": np.asarray(bloch_x),
        "bloch_y": np.asarray(bloch_y),
        "bloch_z": np.asarray(bloch_z),
        "purity": np.asarray(purity),
        "entropy": np.asarray(entropy),
        "trace": np.asarray(traces),
        "max_error": max_error,
        "rho_final": rho_series[-1],
    }


# -----------------------------------------------------------------------------
# Plot helpers
# -----------------------------------------------------------------------------


def show_matrix(matrix, title, max_size=20):
    fig, ax = plt.subplots(figsize=(6, 5))
    displayed = matrix[:max_size, :max_size]
    image = ax.imshow(np.real(displayed), aspect="auto")
    ax.set_title(title)
    ax.set_xlabel("Index")
    ax.set_ylabel("Index")
    fig.colorbar(image, ax=ax)
    st.pyplot(fig, clear_figure=True)


# -----------------------------------------------------------------------------
# UI
# -----------------------------------------------------------------------------

st.title("🌌 Computational & Quantum Physics Laboratory")
st.markdown(
    "Explore the five computational-physics modules through one interactive interface. "
    "Each page runs the numerical model directly rather than displaying pre-generated figures."
)

with st.sidebar:
    st.header("🧭 Laboratory")
    page = st.radio(
        "Choose a module",
        [
            "🏠 Overview",
            "🧮 Module 1 — Matrix Engine",
            "⚛️ Module 2 — Quantum Solver",
            "🌡️ Module 3 — Classical Ising",
            "🧲 Module 4 — Quantum Ising",
            "🌊 Module 5 — Open Quantum System",
        ],
    )


if page == "🏠 Overview":
    st.subheader("From numerical matrices to open quantum dynamics")
    st.write(
        "This application brings together the current Modules 1–5 into a single "
        "interactive laboratory. The modules remain physically distinct, but share "
        "the same computational progression: discretization → operators → Hamiltonians "
        "→ statistical ensembles → density-matrix dynamics."
    )

    cols = st.columns(5)
    cards = [
        ("Module 1", "Numerical operators", "Finite differences and matrix representations."),
        ("Module 2", "Quantum mechanics", "Particle-in-a-box Hamiltonian and eigenstates."),
        ("Module 3", "Statistical physics", "Metropolis Monte Carlo for a classical Ising chain."),
        ("Module 4", "Many-body quantum", "Transverse-field Ising model and Gibbs ensemble."),
        ("Module 5", "Open quantum", "Density matrices and Lindblad dephasing."),
    ]
    for col, (name, title, description) in zip(cols, cards):
        with col:
            st.markdown(f"### {name}")
            st.markdown(f"**{title}**")
            st.caption(description)

    st.info(
        "The current application is the integration layer. The next engineering step "
        "is to move the reusable physics functions into a shared core package and add tests."
    )


elif page == "🧮 Module 1 — Matrix Engine":
    st.header("🧮 Module 1 — Matrix Engine")
    st.write("Represent a position operator and a finite-difference derivative as matrices.")
    n_points = st.slider("Grid points", 20, 150, 50, 5)
    x, x_op, d_op, psi, numerical, exact, error = matrix_engine(n_points)

    c1, c2 = st.columns(2)
    with c1:
        show_matrix(x_op, "Position operator")
    with c2:
        show_matrix(d_op, "Derivative operator")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x, psi, label=r"$\psi(x)=\sin(x)$")
    ax.plot(x, numerical, "--", label="Matrix derivative")
    ax.plot(x, exact, ":", label=r"Exact $\cos(x)$")
    ax.set_xlabel("x")
    ax.set_ylabel("Value")
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig, clear_figure=True)
    st.metric("Maximum absolute derivative error", f"{error:.3e}")


elif page == "⚛️ Module 2 — Quantum Solver":
    st.header("⚛️ Module 2 — 1D Quantum Particle in a Box")
    st.write("Solve the dimensionless Schrödinger equation with a finite-difference Hamiltonian.")
    c1, c2, c3 = st.columns(3)
    with c1:
        n_grid = st.slider("Interior grid points", 30, 180, 100, 10)
    with c2:
        n_states = st.slider("Eigenstates", 1, 6, 3)
    with c3:
        box_length = st.slider("Box length L", 0.5, 3.0, 1.0, 0.1)

    x, h, energies, states, analytical, errors = quantum_box(n_grid, n_states, box_length)
    c1, c2, c3 = st.columns(3)
    c1.metric("Ground-state energy", f"{energies[0]:.6f}")
    c2.metric("Analytical ground state", f"{analytical[0]:.6f}")
    c3.metric("Ground-state relative error", f"{errors[0]:.3e}")

    show_matrix(h, "Hamiltonian matrix (20 × 20 slice)")

    fig, ax = plt.subplots(figsize=(10, 5))
    for i in range(len(energies)):
        density = np.abs(states[:, i]) ** 2
        scaled = density / np.max(density) * max(energies[-1] * 0.25, 1.0)
        ax.plot(x, scaled + energies[i], label=f"n={i+1}")
    ax.set_xlabel("x")
    ax.set_ylabel("Energy + scaled probability density")
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig, clear_figure=True)

    st.dataframe(
        {
            "n": np.arange(1, len(energies) + 1),
            "Numerical energy": energies,
            "Analytical energy": analytical,
            "Relative error": errors,
        },
        use_container_width=True,
    )


elif page == "🌡️ Module 3 — Classical Ising":
    st.header("🌡️ Module 3 — Classical 1D Ising Model")
    st.write("Metropolis Monte Carlo simulation with open boundary conditions.")
    c1, c2 = st.columns(2)
    with c1:
        n_spins = st.slider("Number of spins", 10, 80, 30, 5)
        equilibration = st.slider("Equilibration sweeps", 50, 800, 300, 50)
    with c2:
        measurements = st.slider("Measurement sweeps", 200, 2000, 1000, 100)
        n_temps = st.slider("Temperature points", 6, 20, 12)
    t_min = st.slider("Minimum temperature", 0.2, 2.0, 0.5, 0.1)
    t_max = st.slider("Maximum temperature", 2.0, 6.0, 4.0, 0.5)
    seed = st.number_input("Random seed", 0, 100000, 42)

    if t_max <= t_min:
        st.error("Maximum temperature must be greater than minimum temperature.")
    else:
        if st.button("▶ Run Monte Carlo", type="primary"):
            with st.spinner("Running the Metropolis simulation..."):
                result = classical_ising_sweep(
                    n_spins=n_spins,
                    t_min=t_min,
                    t_max=t_max,
                    n_temperatures=n_temps,
                    equilibration_sweeps=equilibration,
                    measurement_sweeps=measurements,
                    seed=int(seed),
                )
            st.session_state["ising_result"] = result

        result = st.session_state.get("ising_result")
        if result is not None:
            t = result["temperatures"]
            c1, c2 = st.columns(2)
            with c1:
                fig, ax = plt.subplots()
                ax.plot(t, result["energy"], marker="o")
                ax.set(xlabel="Temperature", ylabel="Energy per spin", title="Energy")
                ax.grid(True, alpha=0.3)
                st.pyplot(fig, clear_figure=True)
            with c2:
                fig, ax = plt.subplots()
                ax.plot(t, result["magnetization"], marker="o")
                ax.set(xlabel="Temperature", ylabel="|Magnetization|", title="Magnetization")
                ax.grid(True, alpha=0.3)
                st.pyplot(fig, clear_figure=True)

            c1, c2 = st.columns(2)
            with c1:
                fig, ax = plt.subplots()
                ax.plot(t, result["heat_capacity"], marker="o")
                ax.set(xlabel="Temperature", ylabel="Specific heat", title="Specific heat")
                ax.grid(True, alpha=0.3)
                st.pyplot(fig, clear_figure=True)
            with c2:
                fig, ax = plt.subplots()
                ax.plot(t, result["susceptibility"], marker="o")
                ax.set(xlabel="Temperature", ylabel="Susceptibility", title="Magnetic susceptibility")
                ax.grid(True, alpha=0.3)
                st.pyplot(fig, clear_figure=True)

            st.caption("The 1D classical Ising model has no finite-temperature phase transition in the thermodynamic limit.")


elif page == "🧲 Module 4 — Quantum Ising":
    st.header("🧲 Module 4 — Quantum Transverse-Field Ising Model")
    st.write("Exact diagonalization of a periodic quantum spin chain and its Gibbs ensemble.")
    c1, c2, c3 = st.columns(3)
    with c1:
        n_spins = st.slider("Number of quantum spins", 2, 6, 4)
    with c2:
        j = st.slider("Ising coupling J", 0.0, 3.0, 1.0, 0.1)
    with c3:
        g = st.slider("Transverse field g", 0.0, 3.0, 1.0, 0.1)
    t_max = st.slider("Maximum temperature", 1.0, 10.0, 5.0, 0.5)
    n_temps = st.slider("Temperature points", 20, 150, 80, 10)

    result = quantum_ising(
        n_spins=n_spins,
        j=j,
        g=g,
        temperatures=np.linspace(0.1, t_max, n_temps),
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Hilbert dimension", f"{2**n_spins}")
    c2.metric("Ground energy", f"{result['energies'][0]:.5f}")
    c3.metric("First excited energy", f"{result['energies'][1]:.5f}")
    c4.metric("Energy gap", f"{result['energy_gap']:.5f}")

    show_matrix(result["hamiltonian"], "Quantum Ising Hamiltonian")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(np.arange(len(result["energies"])), result["energies"], marker=".")
    ax.set_xlabel("Eigenstate index")
    ax.set_ylabel("Energy")
    ax.set_title("Exact energy spectrum")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig, clear_figure=True)

    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots()
        ax.plot(result["temperatures"], result["thermal_mz"], label=r"$\langle M_z\rangle$")
        ax.plot(result["temperatures"], result["thermal_mx"], label=r"$\langle M_x\rangle$")
        ax.set(xlabel="Temperature", ylabel="Magnetization", title="Thermal magnetization")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig, clear_figure=True)
    with c2:
        fig, ax = plt.subplots()
        ax.plot(result["temperatures"], result["heat_capacity"], label="Heat capacity")
        ax.plot(result["temperatures"], result["entropy"], label="Gibbs entropy")
        ax.set(xlabel="Temperature", ylabel="Value", title="Thermodynamic response")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig, clear_figure=True)

    st.caption("The entropy shown here is the Gibbs/Shannon entropy of the energy-state probabilities; it is not a direct measure of dynamical decoherence.")


elif page == "🌊 Module 5 — Open Quantum System":
    st.header("🌊 Module 5 — Open Quantum System")
    st.write("Numerically integrate Lindblad dynamics for a single qubit.")
    c1, c2, c3 = st.columns(3)
    with c1:
        gamma = st.slider("Dephasing rate γ", 0.0, 2.0, 0.5, 0.05)
    with c2:
        g = st.slider("Hamiltonian strength g", 0.0, 2.0, 0.0, 0.05)
    with c3:
        t_end = st.slider("Final time", 1.0, 30.0, 10.0, 1.0)

    with st.spinner("Integrating the Lindblad master equation..."):
        result = open_quantum_system(gamma=gamma, g=g, t_end=t_end)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Final purity", f"{result['purity'][-1]:.5f}")
    c2.metric("Final entropy", f"{result['entropy'][-1]:.5f}")
    c3.metric("Final trace", f"{result['trace'][-1]:.8f}")
    c4.metric("Final coherence", f"{result['coherence'][-1]:.5f}")

    t = result["times"]
    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots()
        ax.plot(t, result["coherence"], label="Numerical |ρ₀₁|")
        if g == 0.0:
            ax.plot(t, result["analytical_coherence"], "--", label="Analytical dephasing")
        ax.set(xlabel="Time", ylabel="Coherence", title="Coherence decay")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig, clear_figure=True)
    with c2:
        fig, ax = plt.subplots()
        ax.plot(t, result["population_0"], label="Population |0⟩")
        ax.plot(t, result["population_1"], label="Population |1⟩")
        ax.set(xlabel="Time", ylabel="Population", title="Populations")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig, clear_figure=True)

    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots()
        ax.plot(t, result["bloch_x"], label="x")
        ax.plot(t, result["bloch_y"], label="y")
        ax.plot(t, result["bloch_z"], label="z")
        ax.set(xlabel="Time", ylabel="Bloch component", title="Bloch-vector dynamics")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig, clear_figure=True)
    with c2:
        fig, ax = plt.subplots()
        ax.plot(t, result["purity"], label="Purity")
        ax.plot(t, result["entropy"], label="Von Neumann entropy")
        ax.set(xlabel="Time", ylabel="Value", title="State properties")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig, clear_figure=True)

    if g == 0.0:
        st.success(f"Analytical pure-dephasing validation: maximum coherence error = {result['max_error']:.3e}")
    else:
        st.info("The analytical pure-dephasing curve is shown only when g = 0. With non-zero Hamiltonian dynamics, the simple validation formula from the original Module 5 no longer applies directly.")

    st.subheader("Final density matrix")
    st.dataframe(np.round(result["rho_final"], 6), use_container_width=True)


st.divider()
st.caption("Computational & Quantum Physics Sandbox — Modules 1–5 unified interactive laboratory")
