import numpy as np

print("=== Module 1: The Matrix Engine ===")

# 1. Set up a fine grid representing time (0 to 2 seconds, 100 steps)
time_grid = np.linspace(0, 2, 100)
dt = time_grid[1] - time_grid[0]  # The tiny spacing between points

# 2. Physics Equation: Position of a falling particle over time: y(t) = 0.5 * g * t^2
g = 9.81  # Gravity constant (m/s^2)
position = 0.5 * g * time_grid**2

# 3. Compute the Derivative (Velocity) using Finite Differences
# Velocity is change in position divided by change in time (dy/dt)
velocity = np.diff(position) / dt

print(f"Simulation successful over {len(time_grid)} grid points!")
print(f"Final calculated velocity at 2 seconds: {velocity[-1]:.2f} m/s")
print(velocity)
