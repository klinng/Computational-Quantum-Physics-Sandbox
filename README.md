# 🌌 Computational & Quantum Physics Journey (Master 1)

This project is an educational computational-physics sandbox developed alongside my first year of Master's studies in Physics. The ultimate goal is to turn mathematical and physical concepts from my coursework into numerical experiments through a progressive journey where each module builds the foundations for the next.

## 🗺️ Semester Roadmap

- [X] **Module 1: The Matrix Engine** (Aligned with: *Simulations numériques*)
  - Represent mathematical operators as computational matrices.
  - Discretize continuous problems onto numerical grids.
  - Approximate derivatives using finite-difference methods.
  - Build and manipulate matrices using NumPy to establish foundations for later physics simulations.

- [X] **Module 2: The Quantum State Solver** (Aligned with: *Mécanique quantique*)
  - Numerically solve the one-dimensional time-independent Schrödinger equation.
  - Construct a discretized Hamiltonian using finite differences to calculate energy eigenvalues and eigenstates.
  - Normalize numerical wavefunctions and visualize probability densities.
  - Compare numerical energy levels with the analytical solution of the infinite square well.

- [X] **Module 3: The Thermal Bath** (Aligned with: *Physique statistique*)
  - Study a classical one-dimensional Ising model using the Metropolis Monte Carlo algorithm.
  - Model thermal fluctuations, spin configurations, and Boltzmann statistics.
  - Estimate specific heat and magnetic susceptibility from energy and magnetization fluctuations.
  - *Note: This classical model does not exhibit a finite-temperature phase transition in the thermodynamic limit.*

- [X] **Module 4: The Quantum Spin Chain**
  - Merge the numerical linear-algebra foundations with quantum many-body physics by moving from the classical Ising model to its quantum counterpart.
  - Construct a quantum Hamiltonian in the many-body Hilbert space using Pauli operators.
  - Study the transverse-field Ising Hamiltonian:
    ```math
    H = -J\sum_i \sigma_i^z\sigma_{i+1}^z -g\sum_i \sigma_i^x
    ```
  - Calculate quantum energy eigenvalues/eigenstates and investigate how the external transverse field modifies the system.
  - Explore thermal occupation of quantum states and calculate quantum observables using the Gibbs distribution.

- [X] **🚀 Module 5: Open Quantum Systems & Time Dynamics (The Grand Finale)**
  - Extend quantum state evolution to open quantum systems coupled to an external environment.
  - Implement time-dependent wavepacket evolution and unitary unitary operators ($U(t) = e^{-iHt/\hbar}$).
  - Solve the Lindblad master equation for non-unitary density matrix dynamics ($\rho$):
    ```math
    \frac{d\rho}{dt} = -\frac{i}{\hbar}[H, \rho] + \sum_k \left( L_k \rho L_k^\dagger - \frac{1}{2} \{L_k^\dagger L_k, \rho\} \right)
    ```
  - Investigate quantum decoherence, dissipation, and bipartite entanglement entropy ($S = -\text{Tr}(\rho \ln \rho)$).

## 🧠 Core Competencies Demonstrated

* **Numerical Methods:** Finite-difference discretization, matrix representations, unitary time propagation, and eigenvalue/eigenvector solvers.
* **Statistical & Quantum Physics:** Monte Carlo sampling, thermal fluctuations, many-body Hilbert spaces, density matrix formalism, and open quantum systems.
* **Analysis:** Scientific visualization, interactive data analysis, and bridging theoretical physics with programming.

## 🛠️ Tech Stack

* **Language:** Python 3
* **Libraries:** NumPy (numerical arrays), SciPy (scientific solvers & sparse matrices), Matplotlib (visualization), Streamlit (interactive dashboards).

## 📁 Project Structure

```text
Computational-Quantum-Physics-Sandbox/
│
├── Module_1_Matrix_Engine/      # Grid discretization & finite differences
├── Module_2_Quantum_Solver/     # 1D Schrödinger equation solver
├── Module_3_Thermal_Bath/        # Classical Ising model & Monte Carlo
├── Module_4_Quantum_Ising/      # Many-body quantum spin chain
├── Module_5_Quantum_Systems/    # Open quantum dynamics & Lindblad master equation (Grand Finale)
│
├── README.md
└── requirements.txt

## 🎯 Long-Term Goal

To develop a stronger connection between theoretical physics, numerical methods, and programming. Future extensions will include advanced numerical methods, larger quantum systems, and computational projects connected to research-level physics and quantum computing.
