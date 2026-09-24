import os
import numpy as np
import matplotlib.pyplot as plt

print("=== Module 3: The Thermal Bath (Full Explanatory Framework) ===")

# 1. SIMULATION PARAMETERS & GRID INITIALIZATION
N_spins = 50      # Number of microscopic magnets (spins) in a 1D chain
T = 0.5           # Low Temperature of the thermal bath (forces order)
N_steps = 10000   # Number of individual thermal agitation attempts

# Initialize a random chaotic state (High-Temperature chaos)
spins = np.random.choice([-1, 1], size=N_spins)
initial_spins = spins.copy()  # Backup the original chaos to plot later

print(f"\n1. Statistical System Setup:")
print(f"   -> Spin Chain Length: {N_spins} nodes")
print(f"   -> Target Temperature (T): {T} (Cooled Bath)")
print(f"   -> Initial Random State Grid:\n      {initial_spins}")

# 2. ENERGY CALCULATOR (The 1D Ising Model Rule)
def calculate_energy(spin_array):
    # Neighbors pointing in the SAME direction (+1*+1 or -1*-1) give -1 energy (Stable)
    # Neighbors pointing in OPPOSITE directions (+1*-1) give +1 energy (Unstable/High Energy)
    interactions = spin_array[:-1] * spin_array[1:]
    return -1.0 * np.sum(interactions)

initial_energy = calculate_energy(initial_spins)
print(f"\n2. Initial System Energy calculated: {initial_energy:.2f}")

# 3. METROPOLIS-HASTINGS MONTE CARLO LOOP
print(f"\n3. Simulating Heat Exchange with the Thermal Bath...")
energy_history = []  # Track energy at every step to plot later

current_energy = initial_energy
for step in range(N_steps):
    # Save current energy history snapshot
    energy_history.append(current_energy)
    
    # Step A: Pick a completely random magnet index in our chain
    idx = np.random.randint(0, N_spins)
    
    # Step B: Temporarily flip it to check the physics change
    spins[idx] *= -1
    new_energy = calculate_energy(spins)
    
    # Step C: Compute the Energy Difference (Delta E)
    dE = new_energy - current_energy
    
    # Step D: Apply the Thermodynamic Acceptance Rule
    if dE <= 0:
        # If flipping lowers the energy, nature accepts it instantly!
        current_energy = new_energy
    else:
        # If flipping RAISES the energy, it can only happen by a random thermal kick.
        # This chance is determined by the Boltzmann factor: exp(-dE/T)
        probability_threshold = np.exp(-dE / T)
        if np.random.rand() < probability_threshold:
            # A lucky thermal fluctuation accepted the higher energy state!
            current_energy = new_energy
        else:
            # Too cold! The thermal bath rejects the change. Flip it back!
            spins[idx] *= -1

final_energy = current_energy
print(f"   -> Thermal simulation complete over {N_steps} iterations.")
print(f"   -> Final Optimized System Energy: {final_energy:.2f}")
print(f"   -> Final Organized State Grid:\n      {spins}")

# 4. EXPORTING THE ENTIRE VISUAL PORTFOLIO
script_directory = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------
# 📊 GRAPH 1 & 2: Before & After Spin States (State Alignment)
# ----------------------------------------------------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 4))
# Red blocks = Spin Up (+1), Blue blocks = Spin Down (-1)
ax1.imshow(initial_spins.reshape(1, -1), cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
ax1.set_title("Initial Hot Chaotic State (Random Magnets)")
ax1.get_yaxis().set_visible(False)

ax2.imshow(spins.reshape(1, -1), cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
ax2.set_title(f"Final Cooled State (Aligned by Thermal Bath at T = {T})")
ax2.get_yaxis().set_visible(False)

plt.tight_layout()
state_plot_path = os.path.join(script_directory, "thermal_evolution_plot.png")
plt.savefig(state_plot_path)
plt.close()

# ----------------------------------------------------
# 📈 GRAPH 3: Thermodynamic Energy Minimization Path
# ----------------------------------------------------
plt.figure(figsize=(8, 4))
plt.plot(energy_history, color='purple', linewidth=1.5)
plt.title("Thermodynamics in Action: System Energy Minimization")
plt.xlabel("Monte Carlo Simulation Steps")
plt.ylabel("Total System Energy (E)")
plt.grid(True, alpha=0.3)

energy_plot_path = os.path.join(script_directory, "energy_minimization_plot.png")
plt.savefig(energy_plot_path)
plt.close()

print(f"\nSuccess! Both isolated files have been saved in your module folder:")
print(f"-> 🟥 Spin State Comparison: thermal_evolution_plot.png")
print(f"-> 📈 Energy Minimization Path: energy_minimization_plot.png")
