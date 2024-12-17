import numpy as np
import matplotlib.pyplot as plt

# Constants
M = 1  # Magnetic moment (arbitrary unit)
epsilon0 = 8.854e-12  # Vacuum permittivity
mu0 = 4 * np.pi * 1e-7  # Vacuum permeability
sigma_snow = 3e-6  # Snow conductivity (S/m)
epsilon_r_snow = 4  # Relative permittivity of snow
sigma_soil = 1e-3  # Soil conductivity (S/m)
epsilon_r_soil = 8  # Relative permittivity of soil
depth = 1  # Depth of the transmitter (meters)
freq = 457e3  # Frequency of avalanche transceiver (Hz)

# Grid for the field visualization
x = np.linspace(-60, 60, 400)
z = np.linspace(-10, 30, 200)
X, Z = np.meshgrid(x, z)

# Function to compute the magnetic field intensity at (x, z)
def magnetic_field_intensity(M, x, z, depth):
    r = np.sqrt(x**2 + (z - depth)**2)
    theta = np.arctan2(z - depth, x)
    Hr = M / (2 * np.pi * r**3) * np.cos(theta)
    Htheta = M / (4 * np.pi * r**3) * np.sin(theta)
    H = np.sqrt(Hr**2 + Htheta**2)
    return H

# Compute the magnetic field over the grid
H = magnetic_field_intensity(M, X, Z, depth)

# Create the plot
plt.figure(figsize=(8, 6))
plt.contourf(X, Z, H, levels=100, cmap='inferno')
plt.colorbar(label="Magnetic Field Intensity")
plt.title("Magnetic Field Intensity of Avalanche Transceiver")
plt.xlabel("X Distance (m)")
plt.ylabel("Z Depth (m)")
plt.streamplot(X, Z, np.cos(np.arctan2(Z - depth, X)), np.sin(np.arctan2(Z - depth, X)), color='white')

# plt.gca().invert_yaxis()  # Invert depth axis for better visualization
plt.show()
