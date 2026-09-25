# 🧪 Computational Quantum Physics Sandbox

> **Explore physics with code, simulations, and interactive visualizations.**

A hands-on computational physics project combining **numerical methods, quantum mechanics, statistical mechanics, quantum many-body physics, and open quantum systems** in one interactive application.

🚀 **[Launch the Live App](https://klinng-computational-quantum-physics-sandbox-app-a4dcep.streamlit.app/)**  
💻 **[View the GitHub Repository](https://github.com/klinng/Computational-Quantum-Physics-Sandbox)**

---

## 🌌 What is this project?

This project is a collection of five computational physics modules.

Each module takes a physical idea, turns it into mathematics, implements it numerically, and visualizes the result.

**Physics → Mathematics → Code → Simulation → Visualization**

---

## 🧩 The 5 Modules

### 1️⃣ Matrix Engine

Explore basic numerical operators on a one-dimensional spatial grid.

- 📍 Spatial grids
- 🔢 Position operators
- ∂ Finite-difference derivatives
- 📈 Numerical vs analytical derivatives

For example:

$$
\psi(x) = \sin(x)
$$

and

$$
\frac{d\psi}{dx} = \cos(x)
$$

The numerical derivative is compared with the analytical result.

---

### 2️⃣ Quantum Solver ⚛️

Solve the **one-dimensional infinite square well** using finite differences.

The Hamiltonian is

$$
H = -\frac{1}{2}\frac{d^2}{dx^2}
$$

The analytical energy levels are

$$
E_n = \frac{n^2\pi^2}{2L^2}
$$

You can explore:

- ⚛️ Hamiltonian construction
- 🧮 Numerical eigenvalues
- 🌊 Quantum eigenstates
- 📊 Energy spectra
- 📐 Numerical vs analytical errors

---

### 3️⃣ Thermal Bath 🔥

Simulate the **classical 1D Ising model** using Metropolis Monte Carlo.

Spins are

$$
s_i = \pm 1
$$

with energy

$$
E = -J\sum_i s_i s_{i+1}
$$

Explore how the system changes with temperature and other simulation parameters.

You can study:

- 🌡️ Temperature
- 🧲 Magnetization
- ⚡ Energy
- 🔥 Specific heat
- 📊 Magnetic susceptibility
- 🎲 Monte Carlo sampling

The implementation uses **open boundary conditions**.

---

### 4️⃣ Quantum Ising Model ⚛️🧲

Move from classical spins to a quantum many-body system.

The transverse-field Ising Hamiltonian is

$$
H =
-J\sum_i \sigma_i^z\sigma_{i+1}^z
-g\sum_i \sigma_i^x
$$

The model is built using **Pauli matrices and tensor products**, then solved by exact diagonalization.

Explore:

- 🧩 Many-body Hilbert spaces
- σ Pauli operators
- 🔢 Exact diagonalization
- 📈 Energy spectrum
- ⚡ Energy gap
- 🧲 Magnetization
- 🌡️ Thermal energy
- 🔥 Heat capacity
- 📊 Entropy

The implementation uses **periodic boundary conditions**.

---

### 5️⃣ Open Quantum Systems 🌊

Explore what happens when a quantum system interacts with its environment.

The density matrix follows the Lindblad equation:

$$\frac{d\rho}{dt} = -i[H,\rho] + \sum_k \left( L_k\rho L_k^\dagger - \frac{1}{2}\left\{L_k^\dagger L_k,\rho\right\} \right)$$

For the pure-dephasing model:

$$L = \sqrt{\gamma}\,\sigma_z$$
You can visualize:

- 🌀 Density-matrix evolution
- 💫 Quantum coherence
- 📊 Populations
- 🧭 Bloch-vector components
- 🔵 Purity
- 📈 Von Neumann entropy
- ✅ Trace preservation
- 🧪 Analytical validation

The current implementation focuses on **pure dephasing with $g=0$**.

---

# 🎛️ One Interactive App

All five modules are accessible from one Streamlit application.

### 🔬 Explore

**Matrix Engine**  
→ Numerical operators and derivatives

**Quantum Solver**  
→ Particle in a box and quantum eigenstates

**Thermal Bath**  
→ Classical Ising Monte Carlo

**Quantum Ising Model**  
→ Quantum many-body physics

**Open Quantum Systems**  
→ Density matrices and decoherence

---

## 🚀 Run it yourself

### 1. Clone the project

```bash
git clone https://github.com/klinng/Computational-Quantum-Physics-Sandbox.git
cd Computational-Quantum-Physics-Sandbox
```

### 2. Install the dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Start the application

```bash
python -m streamlit run app.py
```

Then open the local address shown by Streamlit in your browser.

---

## 📁 Project Structure

```text
Computational-Quantum-Physics-Sandbox/
│
├── app.py
├── requirements.txt
├── README.md
│
├── Module_1_Matrix_Engine/
│
├── Module_2_Quantum_Solver/
│
├── Module_3_Thermal_Bath/
│
├── Module_4_Quantum_Ising_Model/
│
└── Module_5_Open_Quantum_Systems/
```

Some earlier implementations are kept in the module folders as historical versions.

---

## 🧪 Validation

The project compares numerical results with analytical or expected physical behavior where appropriate.

Examples include:

- ✔️ Finite-difference derivative accuracy
- ✔️ Infinite-square-well energy comparison
- ✔️ Ising-model observables
- ✔️ Quantum Ising exact diagonalization
- ✔️ Density-matrix trace preservation
- ✔️ Pure-dephasing analytical behavior

---

## 🧠 What you can learn

This project connects several important ideas in computational physics:

| Topic | Example |
|---|---|
| 🔢 Numerical methods | Finite differences |
| ⚛️ Quantum mechanics | Infinite square well |
| 🔥 Statistical mechanics | Classical Ising model |
| 🧲 Quantum many-body physics | Transverse-field Ising model |
| 🌊 Open quantum systems | Lindblad dynamics |
| 🧮 Linear algebra | Eigenvalue problems |
| 🎲 Monte Carlo | Metropolis algorithm |
| 📊 Visualization | Matplotlib + Streamlit |

---

## 🎯 The idea behind the project

The goal is simple:

> **Take physics equations and turn them into working computational experiments.**

You can change parameters, run simulations, inspect numerical results, and compare them with analytical physics.

This makes the repository useful as both a **learning project** and a **computational physics sandbox**.

---

## 🚀 Live Demo

**Try the full application here:**

👉 **[Computational Quantum Physics Sandbox](https://klinng-computational-quantum-physics-sandbox-app-a4dcep.streamlit.app/)**

Have fun exploring the physics! ⚛️
