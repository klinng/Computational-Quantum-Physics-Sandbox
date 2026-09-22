import numpy as np
import matplotlib.pyplot as plt

print("=== Module 1: The Matrix Engine (With Plotting) ===")

# 1. Set up a fine grid representing time (0 to 2 seconds, 100 steps)
time_grid = np.linspace(0, 2, 100)
dt = time_grid[1] - time_grid[0]  # The tiny spacing between points

# 2. Physics Equation: Position of a falling particle over time: y(t) = 0.5 * g * t^2
g = 9.81  # Gravity constant (m/s^2)
position = 0.5 * g * time_grid**2

# 3. Compute the Derivative (Velocity) using Finite Differences
velocity = np.diff(position) / dt

# 4. Generate and Save the Visual Graph Chart
# Note: velocity has 99 points because np.diff reduces the size by 1, so we use time_grid[1:]
plt.plot(time_grid[1:], velocity, label="Calculated Velocity (m/s)", color="blue", linewidth=2)
plt.title("Particle Velocity Over Time (Numerical Simulation)")
plt.xlabel("Time (seconds)")
plt.ylabel("Velocity (m/s)")
plt.grid(True)
plt.legend()

# Save the plot as an image file in your project folder
plt.savefig("velocity_plot.png")
print("Simulation successful! Visual chart saved as 'velocity_plot.png'")
