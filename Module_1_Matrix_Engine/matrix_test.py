import os
import numpy as np
import matplotlib.pyplot as plt

print("=== The Matrix Engine: Complete Portfolio Framework ===")

# 1. Create a fine grid of 50 space points for calculations
N = 50
spatial_grid = np.linspace(0, 2 * np.pi, N)
dx = spatial_grid[1] - spatial_grid[0]  # Exact step spacing calculation

# 2. Build BOTH Physical Operators as Computational Matrices
X_operator = np.diag(spatial_grid)  # x_psi = X_operator @ psi
D_operator = (
    np.diag(np.ones(N-1), 1)
    - np.diag(np.ones(N-1), -1)
) / (2.0 * dx)  # DERIVATIVE OPERATOR (D)

# 3. Define a Physical State: A Quantum Wavefunction Psi = sin(x)
psi = np.sin(spatial_grid)

# 4. Let the Matrix calculate the derivative automatically!
calculated_derivative = np.dot(D_operator, psi)

# 5. Define the folder path to save everything safely inside Module 1
script_directory = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------
# 📊 GRAPH 1: The Position Operator Matrix
# ----------------------------------------------------
plt.figure(figsize=(6, 5))
plt.imshow(X_operator[:10, :10], cmap='Blues')
plt.title("Position Operator Matrix Grid (Slice 10x10)")
plt.colorbar(label="Position Value (meters)")
pos_graph_path = os.path.join(script_directory, "matrix_position_grid.png")
plt.savefig(pos_graph_path)
plt.close()

# ----------------------------------------------------
# 📊 GRAPH 2: The Derivative Operator Matrix 
# ----------------------------------------------------
plt.figure(figsize=(6, 5))
plt.imshow(D_operator[:10, :10], cmap='RdBu')
plt.title("Derivative Operator Matrix Grid (Slice 10x10)")
plt.colorbar(label="Operator Weight")
deriv_graph_path = os.path.join(script_directory, "matrix_derivative_grid.png")
plt.savefig(deriv_graph_path)
plt.close()

# ----------------------------------------------------
# 🌊 GRAPH 3: The Physical Wave Result
# ----------------------------------------------------
plt.figure(figsize=(8, 5))
plt.plot(spatial_grid, psi, label=r"Original Wave ($\psi = \sin(x)$)", color="blue", linewidth=2)
plt.plot(spatial_grid, calculated_derivative, label=r"Matrix Derivative ($d\psi/dx \approx \cos(x)$)", color="red", linestyle="--", linewidth=2)
plt.title("Matrix Engine: Deriving a Quantum Wavefunction")
plt.xlabel("Position (x)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend()
wave_graph_path = os.path.join(script_directory, "wavefunction_derivative_plot.png")
plt.savefig(wave_graph_path)
plt.close()

print(f"\nSuccess! All three isolated files have been saved in your module folder:")
print(f"-> 🟦 Position Matrix Graph: matrix_position_grid.png")
print(f"-> 🟥 Derivative Matrix Graph: matrix_derivative_grid.png")
print(f"-> 📈 Physical Wave Graph: wavefunction_derivative_plot.png")
