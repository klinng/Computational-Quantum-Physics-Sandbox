import numpy as np
import matplotlib.pyplot as plt

print("=== Module 1: The Matrix Engine (True Matrix Construction) ===")

# 1. Discretize a spatial grid from 0 to 5 meters using only 6 points (to keep it readable)
N = 6
spatial_grid = np.linspace(0, 5, N)
print(f"\n1. Digital Grid Points (x):\n{spatial_grid}")

# 2. Construct the POSITION OPERATOR (X) as a diagonal matrix
# This is a true matrix where the grid values live on the main diagonal
X_operator = np.diag(spatial_grid)
print(f"\n2. Position Operator Matrix [X]:\n{X_operator}")

# 3. Construct a Finite Difference DERIVATIVE OPERATOR (D) Matrix
# This matrix will automatically compute differences between neighboring points
D_operator = (np.diag(np.ones(N-1), 1) - np.diag(np.ones(N-1), -1)) / 2.0
print(f"\n3. Numerical Derivative Matrix Operator [D]:\n{D_operator}")

# 4. Generate a quick visualization of our operators
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.imshow(X_operator, cmap='Blues')
plt.title("Position Operator Matrix Visual")
plt.colorbar()

plt.subplot(1, 2, 2)
plt.imshow(D_operator, cmap='RdBu')
plt.title("Derivative Operator Matrix Visual")
plt.colorbar()

# Save the real matrix visualization image
plt.savefig("matrix_operator_visualization.png")
print("\nSimulation successful! Matrix visuals saved as 'matrix_operator_visualization.png'")
