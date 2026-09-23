import os
import numpy as np
import matplotlib.pyplot as plt

print("=== The Matrix Engine in Action (Module 1 Isolated) ===")

# 1. Create a fine grid of 50 space points
N = 50
spatial_grid = np.linspace(0, 2 * np.pi, N)
dx = spatial_grid[1] - spatial_grid[0]  # Exact step spacing calculation

# 2. Build the Derivative Matrix Operator (The 0.5 and -0.5 stripes)
D_operator = (np.diag(np.ones(N-1), 1) - np.diag(np.ones(N-1), -1)) / (2.0 * dx)

# 3. Define a Physical State: A Quantum Wavefunction Psi = sin(x)
psi = np.sin(spatial_grid)

# 4. Let the Matrix calculate the derivative automatically!
calculated_derivative = np.dot(D_operator, psi)

# 5. Generate the Visual Chart
plt.figure(figsize=(8, 5))
plt.plot(spatial_grid, psi, label=r"Original Wave ($\psi = \sin(x)$)", color="blue", linewidth=2)
plt.plot(spatial_grid, calculated_derivative, label=r"Matrix Derivative ($d\psi/dx \approx \cos(x)$)", color="red", linestyle="--", linewidth=2)
plt.title("Matrix Engine: Deriving a Quantum Wavefunction")
plt.xlabel("Position (x)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend()

# 6. Module Isolation Layer: Force the image to save INSIDE the script's folder
script_directory = os.path.dirname(os.path.abspath(__file__))
output_image_path = os.path.join(script_directory, "wavefunction_derivative_plot.png")

# Save the plot securely to its own module space
plt.savefig(output_image_path)
print(f"\nSimulation successful! Visual chart isolated inside: \n-> {output_image_path}")
