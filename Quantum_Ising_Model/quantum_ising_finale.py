import os
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

print("=== The Grand Finale: Fully Explanatory Quantum Ising Engine ===")

# 1. PHYSICS CONFIGURATION
N_spins = 4       # Number of quantum qubits (Matrix dimensions grow exponentially at 2^N)
g_field = 1.0     # Strength of the Quantum Transverse Field
temperatures = np.linspace(0.1, 5.0, 100)  # Thermal Bath temperature scale sweep

dim = 2**N_spins  # Hilbert space dimensionality = 16

# Fundamental Pauli Operators of Quantum Mechanics
Sz = np.array([[1, 0], [0, -1]])   # Measures Up/Down classical configuration
Sx = np.array([[0, 1], [1, 0]])   # Induces Left/Right quantum superposition tunneling

# Shorthand to expand operators across the multi-node quantum network
def get_tensor_op(op, site, N):
    op_list = [np.eye(2)] * N
    op_list[site] = op
    res = op_list[0]
    for i in op_list[1:]:
        res = np.kron(res, i)
    return res

# 2. CONSTRUCT OPERATOR MATRICES (Module 1 & 2 Concept)
H_interaction = np.zeros((dim, dim))
H_transverse_field = np.zeros((dim, dim))

for i in range(N_spins):
    next_neighbor = (i + 1) % N_spins
    H_interaction -= np.dot(get_tensor_op(Sz, i, N_spins), get_tensor_op(Sz, next_neighbor, N_spins))
    H_transverse_field -= g_field * get_tensor_op(Sx, i, N_spins)

# Complete Quantum Master Hamiltonian Matrix
Hamiltonian = H_interaction + H_transverse_field

print(f"\n[STEP 1] Matrix Operators Formed in Memory:")
print(f"   -> Quantum Hilbert Space Dimension: {dim}x{dim} states")
print(f"   -> Top-Left 4x4 Slice of the Raw Quantum Interaction Matrix [H_interaction]:")
print(H_interaction[:4, :4])
print(f"   -> Top-Left 4x4 Slice of the Quantum Field Operator Matrix [H_field]:")
print(H_transverse_field[:4, :4])

# 3. SOLVE INTERNAL QUANTUM STATES (Module 2 Engine)
energy_levels, wavefunctions = la.eigh(Hamiltonian)

print(f"\n[STEP 2] Schrödinger Equation Solved!")
print(f"   -> Ground State Energy (E_0): {energy_levels[0]:.4f} energy units")
print(f"   -> First Excited State Energy (E_1): {energy_levels[1]:.4f} energy units")

# 4. THERMAL BATH INTERACTION ENSEMBLE SWEEP (Module 3 Boltzmann Logic)
magnetization_order = []
quantum_entropy_proxy = []

for T in temperatures:
    beta = 1.0 / T
    # Compute Boltzmann factor probabilities over all 16 discrete quantum eigenstates
    boltzmann_weights = np.exp(-beta * (energy_levels - energy_levels[0]))
    partition_function = np.sum(boltzmann_weights)
    probabilities = boltzmann_weights / partition_function
    
    total_order = 0.0
    for state_idx in range(dim):
        wave = wavefunctions[:, state_idx]
        # Quantum expectation value measurement: <psi| Sz_0 |psi>
        state_magnetization = np.dot(wave.T, np.dot(get_tensor_op(Sz, 0, N_spins), wave))
        total_order += np.abs(state_magnetization) * probabilities[state_idx]
        
    magnetization_order.append(total_order)
    # Statistical Shannon Entropy calculation to measure decoherence intensity
    quantum_entropy_proxy.append(-np.sum(probabilities * np.log(probabilities + 1e-15)))

# 5. GENERATE THE COMPLETE FINALE VISUAL PACKAGE
script_directory = os.path.dirname(os.path.abspath(__file__))

# --- GRAPH 1: The Master Hamiltonian Operator Matrix Grid ---
plt.figure(figsize=(6, 5))
plt.imshow(Hamiltonian, cmap='seismic')
plt.title("Master Quantum Hamiltonian Matrix Grid [H]")
plt.colorbar(label="Energy State Matrix Weight")
matrix_path = os.path.join(script_directory, "quantum_hamiltonian_matrix_grid.png")
plt.savefig(matrix_path)
plt.close()

# --- GRAPH 2: Thermodynamics vs Quantum Alignment (The System Collapse) ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

ax1.plot(temperatures, magnetization_order, color='darkorange', linewidth=2.5)
ax1.set_title("Thermal Decoherence: Destruction of Quantum Order")
ax1.set_ylabel("Quantum Alignment")
ax1.grid(True, alpha=0.3)

ax2.plot(temperatures, quantum_entropy_proxy, color='teal', linewidth=2.5, linestyle='--')
ax2.set_title("Thermodynamic Chaos (Entropy Absorption from Bath)")
ax2.set_xlabel("Thermal Bath Temperature (T)")
ax2.set_ylabel("System Entropy (S)")
ax2.grid(True, alpha=0.3)

plt.tight_layout()
curves_path = os.path.join(script_directory, "quantum_decoherence_curves.png")
plt.savefig(curves_path)
plt.close()

print(f"\n[STEP 3] Execution successful! Visual assets locked into your module folder:")
print(f"   -> 🟥 Matrix Architecture: quantum_hamiltonian_matrix_grid.png")
print(f"   -> 📈 System Collapse Curves: quantum_decoherence_curves.png")
