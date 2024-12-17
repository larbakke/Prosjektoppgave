import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Constants for snow and soil
sigma_snow = 3e-6  # Snow conductivity (S/m)
epsilon_r_snow = 4  # Relative permittivity of snow
sigma_soil = 1e-3  # Soil conductivity (S/m)
epsilon_r_soil = 8  # Relative permittivity of soil

# Constants for field computation
M = 1  # Magnetic moment (arbitrary unit)
depth = -10  # Depth of the transmitter, set to 10m below snow surface
scale = 40  # Set scale to 40x40x40 meters
threshold = 1e-6  # Set threshold for magnetic field intensity
pointDensity = 0.8  # Set point density for the field visualization

# Grid for the field visualization in 3D (adjusted Z range)
x = np.linspace(-scale / 2, scale / 2, int(scale * pointDensity))  # Reduced grid density
y = np.linspace(-scale / 2, scale / 2, int(scale * pointDensity))
z = np.linspace(depth, scale / 2, int((scale / 2 - depth) * pointDensity))  # From -10 meters to 50 meters above snow surface
X, Y, Z = np.meshgrid(x, y, z)

# Function to compute the magnetic field intensity at (x, y, z) taking into account snow and soil effects
def magnetic_field_intensity_3d(M, x, y, z, depth):
    r = np.sqrt(x**2 + y**2 + (z - depth)**2)
    theta = np.arctan2(np.sqrt(x**2 + y**2), z - depth)
    Hr = M / (2 * np.pi * r**3) * np.cos(theta)
    Htheta = M / (4 * np.pi * r**3) * np.sin(theta)
    H = np.sqrt(Hr**2 + Htheta**2)
    return Hr, Htheta, H

# Compute the magnetic field intensity over the 3D grid (with snow and soil effects)
Hr, Htheta, H = magnetic_field_intensity_3d(M, X, Y, Z, depth)

# Apply threshold to mask out weaker magnetic fields
H_masked = np.ma.masked_where(H < threshold, H)

# Normalize vector field for streamlines (quivers)
Ux = Hr / np.sqrt(Hr**2 + Htheta**2)
Uy = Htheta / np.sqrt(Hr**2 + Htheta**2)
Uz = (Z - depth) / np.sqrt(Hr**2 + Htheta**2)

# Create the 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plotting the field intensity as scatter points (only for values above threshold)
sc = ax.scatter(X, Y, Z, c=H_masked, cmap='inferno', s=5)
fig.colorbar(sc, label='Magnetic Field Intensity (Thresholded)')

# Adding quivers to visualize the vector directions (field lines)
ax.quiver(X[::3, ::3, ::3], Y[::3, ::3, ::3], Z[::3, ::3, ::3], 
          Ux[::3, ::3, ::3], Uy[::3, ::3, ::3], Uz[::3, ::3, ::3], length=3, color='white')

# Labels and title
ax.set_title('3D Magnetic Field Intensity and Directions (Thresholded)')
ax.set_xlabel('X Distance (m)')
ax.set_ylabel('Y Distance (m)')
ax.set_zlabel('Z Depth (m)')
ax.set_xlim([-scale / 2, scale / 2])
ax.set_ylim([-scale / 2, scale / 2])
ax.set_zlim([-10, 50])  # Adjust z-axis from -10m to 50m

plt.show()
