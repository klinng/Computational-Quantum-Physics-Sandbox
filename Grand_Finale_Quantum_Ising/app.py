import streamlit as st
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

# Set up the web page title and header
st.set_page_config(page_title="Quantum Ising Sandbox", layout="wide")
st.title("🌌 Master 1: Quantum Ising Dashboard")
st.markdown("Interact with the sliders below to explore how temperature and magnetic fields cause **Quantum Decoherence**.")

# 1. INTERACTIVE SIDEBAR SLIDERS (User Inputs)
st.sidebar.header("🎛️ Simulation Controls")
N_spins = st.sidebar.slider("Number of Quantum Spins (Qubits)", min_value=2, max_value=5, value=4)
g_field = st.sidebar.slider("Transverse Magnetic Field (Quantum Tunneling)", min_value=0.0, max_value=3.0, value=1.0, step=0.1)
max_temp = st.sidebar.slider("Maximum Thermal Bath Temperature", min_value=1.0, max_value=10.0, value=5.0, step=0.5)

# 2. CORE PHYSICS CALCULATIONS (Integrated Modules 1, 2, & 3)
dim = 2**N_spins
Sz = np.array([[1, 0], [0, -1]])
Sx = np.array([[0, 1], [1, 0]])

def get_tensor_op(op, site, N):
    op_list = [np.eye(2)] * N
    op_list[site] = op
    res = op_list[0]
    for i in op_list[1:]:
        res = np.kron(res, i)
    return res

H_interaction = np.zeros((dim, dim))
H_transverse_field = np.zeros((dim, dim))

for i in range(N_spins):
    next_neighbor = (i + 1) % N_spins
    H_interaction -= np.dot(get_tensor_op(Sz, i, N_spins), get_tensor_op(Sz, next_neighbor, N_spins))
    H_transverse_field -= g_field * get_tensor_op(Sx, i, N_spins)

Hamiltonian = H_interaction + H_transverse_field
energy_levels, wavefunctions = la.eigh(Hamiltonian)

# Sweep the thermal bath scale based on user's max temperature slider
temperatures = np.linspace(0.1, max_temp, 100)
magnetization_order = []
quantum_entropy_proxy = []

for T in temperatures:
    beta = 1.0 / T
    boltzmann_weights = np.exp(-beta * (energy_levels - energy_levels[0]))
    partition_function = np.sum(boltzmann_weights)
    probabilities = boltzmann_weights / partition_function
    
    total_order = 0.0
    for state_idx in range(dim):
        wave = wavefunctions[:, state_idx]
        state_magnetization = np.dot(wave.T, np.dot(get_tensor_op(Sz, 0, N_spins), wave))
        total_order += np.abs(state_magnetization) * probabilities[state_idx]
        
    magnetization_order.append(total_order)
    quantum_entropy_proxy.append(-np.sum(probabilities * np.log(probabilities + 1e-15)))

# 3. DISPLAY DIAGNOSTICS & METRICS LIVE ON THE WEB PAGE
col1, col2, col3 = st.columns(3)
col1.metric("Hilbert Space Size", f"{dim}x{dim} States")
col2.metric("Ground State Energy (E_0)", f"{energy_levels[0]:.4f}")
col3.metric("First Excited State (E_1)", f"{energy_levels[1]:.4f}")

# 4. RENDER DUAL CURVES VISUAL LIVE
st.subheader("📈 Thermodynamic System Collapse Curves")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
ax1.plot(temperatures, magnetization_order, color='darkorange', linewidth=2.5)
ax1.set_ylabel("Quantum Alignment (Order)")
ax1.grid(True, alpha=0.3)

ax2.plot(temperatures, quantum_entropy_proxy, color='teal', linewidth=2.5, linestyle='--')
ax2.set_xlabel("Thermal Bath Temperature (T)")
ax2.set_ylabel("System Entropy (S)")
ax2.grid(True, alpha=0.3)

plt.tight_layout()
st.pyplot(fig)
