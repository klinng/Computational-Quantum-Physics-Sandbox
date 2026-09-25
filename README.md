# 🌌 Computational & Quantum Physics Sandbox

> An interactive computational physics project connecting numerical linear algebra, quantum mechanics, statistical mechanics, quantum many-body physics, and open quantum systems.

**🚀 Live interactive app:** https://klinng-computational-quantum-physics-sandbox-app-a4dcep.streamlit.app/

A modular computational physics project exploring numerical methods, quantum mechanics, statistical mechanics, quantum many-body systems, and open quantum dynamics.

The project is organized as a progressive sequence of computational modules, moving from basic numerical operators to quantum systems, Monte Carlo methods, exact diagonalization, and density-matrix dynamics.

---

## 🚀 Project Overview

| Module | Topic | Main Method |
|---|---|---|
| **Module 1** | Matrix Engine | Numerical operators & finite differences |
| **Module 2** | Quantum Solver | Finite-difference Schrödinger equation |
| **Module 3** | Thermal Bath | Metropolis Monte Carlo / Classical Ising model |
| **Module 4** | Quantum Ising Model | Pauli operators & exact diagonalization |
| **Module 5** | Open Quantum Systems | Density matrices & Lindblad dynamics |

A unified Streamlit application is included at the root of the repository, allowing the different computational experiments to be explored from one interface.

### ⚡ Quick Start

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd Computational-Quantum-Physics-Sandbox
pip install -r requirements.txt
streamlit run app.py
```

The main entry point is the root-level `app.py`. The individual module folders contain the underlying computational work.


---

# 🧭 Project Roadmap

```text
Numerical Mathematics
        │
        ▼
Module 1 — Matrix Engine
        │
        ▼
Module 2 — Quantum Solver
        │
        ▼
Module 3 — Classical Statistical Mechanics
        │
        ▼
Module 4 — Quantum Many-Body Physics
        │
        ▼
Module 5 — Open Quantum Systems
        │
        ▼
Unified Interactive Application
```

The goal is not to simulate one single physical system, but to build a small computational physics environment covering several important numerical techniques.

---

# 📦 Modules

## 1️⃣ Module 1 — Matrix Engine

The first module introduces numerical operators represented as matrices.

### Main concepts

- Spatial discretization
- Position operators
- Finite-difference derivatives
- Numerical differentiation
- Comparison between numerical and analytical derivatives
- Matrix-based representation of physical operators

For example, a wavefunction can be represented on a spatial grid and differentiated numerically using a finite-difference matrix.

For a test function

$$
\psi(x) = \sin(x),
$$

the analytical derivative is

$$
\frac{d\psi}{dx} = \cos(x).
$$

---

# 2️⃣ Module 2 — Quantum Solver

Module 2 uses numerical operators to solve the one-dimensional infinite square well.

The Hamiltonian is

$$
H =
-\frac{1}{2}\frac{d^2}{dx^2}.
$$

The discretized Schrödinger equation becomes

$$
H\psi_n = E_n\psi_n.
$$

### The module calculates

- Hamiltonian matrix
- Numerical eigenvalues
- Numerical eigenstates
- Normalized wavefunctions
- Analytical energy levels
- Relative errors

For an infinite square well of width $L$,

$$
E_n =
\frac{n^2\pi^2}{2L^2}.
$$

The numerical solution is compared with this analytical result.

---

# 3️⃣ Module 3 — Thermal Bath

Module 3 introduces statistical mechanics through the one-dimensional classical Ising model.

The system consists of spins

$$
s_i = \pm1.
$$

The Hamiltonian is

$$
E =
-J\sum_i s_i s_{i+1}.
$$

The system is simulated using the **Metropolis Monte Carlo algorithm**.

### The simulation calculates

- Energy
- Magnetization
- Energy fluctuations
- Specific heat
- Magnetic susceptibility
- Temperature-dependent observables

The simulation supports a reproducible random seed for numerical experiments.

### Physical note

The one-dimensional Ising model does not exhibit a finite-temperature phase transition in the thermodynamic limit.

---

# 4️⃣ Module 4 — Quantum Transverse-Field Ising Model

Module 4 extends the Ising model into the quantum regime.

The Hamiltonian is

$$
H =
-J\sum_i \sigma_i^z\sigma_{i+1}^z
-g\sum_i\sigma_i^x.
$$

Here,

- $J$ is the interaction strength,
- $g$ is the transverse-field strength,
- $\sigma^x$ and $\sigma^z$ are Pauli matrices.

The many-body Hilbert space is constructed using tensor products of single-spin operators.

### Main computational techniques

- Pauli matrices
- Tensor products
- Many-body Hilbert spaces
- Exact diagonalization
- Eigenvalue problems
- Ground-state analysis
- Thermal states

### The module calculates

- Energy spectrum
- Ground-state energy
- First excited-state energy
- Energy gap
- Longitudinal magnetization $M_z$
- Transverse magnetization $M_x$
- Thermal energy
- Heat capacity
- Partition function
- Gibbs/Shannon entropy

The model uses periodic boundary conditions.

---

# 5️⃣ Module 5 — Open Quantum Systems

Module 5 introduces density matrices and open quantum dynamics.

The state is represented by a density matrix

$$
\rho.
$$

The evolution is described using the Lindblad master equation:

$$
\frac{d\rho}{dt}
=
-i[H,\rho]
+
\sum_k
\left(
L_k\rho L_k^\dagger
-\frac{1}{2}
\{L_k^\dagger L_k,\rho\}
\right).
$$

The current implementation focuses on a **pure-dephasing** example with

$$
L =
\sqrt{\gamma}\sigma_z.
$$

### The module studies

- Density matrices
- Lindblad evolution
- Quantum coherence
- Population dynamics
- Bloch-vector components
- Purity
- Von Neumann entropy
- Trace preservation
- Numerical vs analytical dephasing

For pure dephasing, the populations remain constant while the off-diagonal coherence decays.

---

# 🖥️ Unified Interactive Application

The repository includes a root-level:

```text
app.py
```

This is the main interactive Streamlit application and the recommended entry point for the project.

It provides access to the computational experiments through one interface.

### Available sections

**Module 1**
- Spatial grid
- Position operator
- Numerical derivative
- Analytical derivative
- Numerical error

**Module 2**
- Particle-in-a-box parameters
- Hamiltonian
- Energy spectrum
- Numerical eigenstates
- Analytical energy levels
- Relative errors

**Module 3**
- Number of spins
- Temperature
- Coupling strength
- Monte Carlo steps
- Random seed
- Energy
- Magnetization
- Specific heat
- Susceptibility

**Module 4**
- Number of spins
- Coupling $J$
- Transverse field $g$
- Energy spectrum
- Energy gap
- Magnetization
- Thermal observables
- Entropy

**Module 5**
- Dephasing rate
- Time evolution
- Density matrix
- Coherence
- Populations
- Bloch vector
- Purity
- Von Neumann entropy
- Trace preservation
- Analytical validation

---

# 🗂️ Repository Structure

```text
Computational-Quantum-Physics-Sandbox/
│
├── app.py
├── README.md
├── requirements.txt
│
├── Module_1_Matrix_Engine/
│   └── ...
│
├── Module_2_Quantum_Solver/
│   ├── ...
│   └── quantum_solver_old.py
│
├── Module_3_Thermal_Bath/
│   ├── ...
│   └── thermal_bath_old.py
│
├── Module_4_Quantum_Ising_Model/
│   ├── quantum_ising.py
│   ├── quantum_ising_finale_old.py
│   └── app.py
│
└── Module_5_Open_Quantum_Systems/
    └── Open_Qunatum_system.py
```

Older implementations are retained where applicable so that the evolution of the project can be followed. The root-level `app.py` is the main application entry point; the older Module 4 `app.py` is retained as part of the module history.

---

## 📝 GitHub Preview

This README uses standard GitHub Markdown. Equations use GitHub-supported math delimiters, so they render as mathematical expressions in the repository preview rather than appearing as raw LaTeX commands. Code blocks remain code blocks intentionally so installation commands and the repository structure are easy to copy.

# 🛠️ Technologies

The project is built primarily with Python and uses:

- Python
- NumPy
- SciPy
- Matplotlib
- Streamlit

### NumPy

Used for arrays, matrices, linear algebra, tensor products, and numerical calculations.

### SciPy

Used for eigenvalue problems, numerical integration, differential equations, and scientific algorithms.

### Matplotlib

Used for wavefunction plots, energy spectra, Monte Carlo observables, quantum dynamics, and numerical comparisons.

### Streamlit

Used for the unified interactive scientific application.

---

# ⚙️ Installation

Clone the repository:

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd Computational-Quantum-Physics-Sandbox
```

Create a virtual environment:

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Unified Application

From the project root:

```bash
streamlit run app.py
```

The Streamlit application will start locally and provide access to the different modules.

---

# 🧪 Numerical Validation

The project includes comparisons between numerical and analytical results.

### Module 1

Numerical derivative vs analytical derivative.

### Module 2

Numerical energy levels vs

$$
E_n =
\frac{n^2\pi^2}{2L^2}.
$$

### Module 3

Monte Carlo observables and statistical fluctuations.

### Module 4

Exact diagonalization of the many-body Hamiltonian and consistency checks on the spectrum.

### Module 5

Numerical Lindblad evolution compared with analytical pure-dephasing behavior.

These comparisons help verify the numerical implementations rather than relying only on visual output.

---

# 🔬 Scientific Scope

The project covers several major areas of computational physics:

```text
Linear Algebra
      │
      ├── Matrix operators
      └── Eigenvalue problems
             │
             ▼
       Quantum Mechanics
             │
             ├── Schrödinger equation
             └── Quantum Ising model
             │
             ▼
   Statistical Mechanics
             │
             └── Monte Carlo / Ising model
             │
             ▼
   Open Quantum Systems
             │
             └── Density matrices / Lindblad dynamics
```

This provides a computational introduction to several techniques used in theoretical and computational physics.

---

# 📊 What This Project Demonstrates

- Numerical linear algebra
- Matrix representations of physical operators
- Finite-difference methods
- Eigenvalue problems
- Numerical differential equations
- Quantum-mechanical simulations
- Monte Carlo methods
- Statistical mechanics
- Tensor-product Hilbert spaces
- Exact diagonalization
- Density matrices
- Lindblad master equations
- Scientific visualization
- Interactive scientific applications
- Python-based computational workflows

---

# 🔭 Future Development

Possible future improvements include:

- Higher-order finite-difference schemes
- Additional quantum potentials
- Larger Ising systems
- Improved Monte Carlo sampling
- Additional quantum spin models
- Sparse matrix implementations
- Larger-scale exact diagonalization
- Additional Lindblad operators
- Dissipative quantum dynamics
- Multi-qubit open systems
- Automated numerical tests
- More extensive analytical validation
- Cleaner separation between physics engines and user interface

---

# 📌 Current Status

### Implemented

- [x] Module 1 — Matrix Engine
- [x] Module 2 — Quantum Solver
- [x] Module 3 — Classical Ising Monte Carlo
- [x] Module 4 — Quantum Transverse-Field Ising Model
- [x] Module 5 — Open Quantum Systems
- [x] Unified Streamlit application
- [x] Numerical visualization
- [x] Analytical/numerical comparisons
- [x] Public project documentation

### Future work

- [ ] Larger-scale simulations
- [ ] More automated testing
- [ ] Additional physical models
- [ ] Further architectural refactoring

---

# 📚 Project Philosophy

The project follows a simple principle:

> Build the physics numerically, verify it analytically where possible, and make the results observable.

Each module introduces a new computational technique while building toward more advanced physical models.

The unified application brings these experiments together into a single interactive environment.

---

# 👨‍💻 Author

Developed as a computational physics project combining numerical methods, quantum mechanics, statistical mechanics, and open quantum systems.