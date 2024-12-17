import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Constants and parameters
freq = 457e3  # Frequency of the avalanche beacon in Hz
mu_0 = 4 * np.pi * 1e-7  # Permeability of free space
c = 3e8  # Speed of light in m/s
wavelength = c / freq  # Wavelength of the signal
depth = 3  # Depth of the beacon (in meters)
max_range = 60  # Max range of the beacon in meters
snow_conductivity = 1e-6  # Snow conductivity (S/m)
soil_conductivity = 1e-3  # Soil conductivity (S/m)

# Create adjustable parameters
rotation_angle = np.deg2rad(45)  # Rotation angle of the antenna (in radians)
plot3D = True  # Set to True for 3D plot, False for 2D

# Define magnetic dipole model
def magnetic_field(r, theta, rotation_angle, depth):
    # Rotated dipole along a specific axis
    r_eff = np.sqrt(r**2 + depth**2)  # Effective distance considering burial
    theta_eff = theta + rotation_angle  # Apply rotation

    # Magnetic field components (simplified near-field model)
    B_r = (mu_0 / (2 * np.pi * r_eff**3)) * (2 * np.cos(theta_eff))
    B_theta = (mu_0 / (2 * np.pi * r_eff**3)) * np.sin(theta_eff)

    return B_r, B_theta

# Create a 2D/3D grid for plotting
def create_grid(plot3D):
    r = np.linspace(0.1, max_range, 200)  # Radial distances (in meters)
    theta = np.linspace(0, 2 * np.pi, 200)  # Angles (in radians)

    r_grid, theta = np.meshgrid(r, theta)
    
    if plot3D:
        z = np.linspace(-3, 80, 200)  # Heights (from -3m under snow to 50m)
        z_grid, r_grid = np.meshgrid(z, r)
        print(r_grid.shape, theta.shape, z_grid.shape)
        return r, theta, z_grid
    return r, theta, 0

# Plot 2D radiation pattern
def plot_2d(r, theta, B_r):
    plt.polar(theta, np.abs(B_r))
    plt.title('2D Radiation Pattern')
    plt.show()

# Plot 3D radiation pattern
def plot_3d(r, theta, z, B_r):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    
    print(x.shape, y.shape, z.shape, B_r.shape)
    ax.plot_surface(x, y, z, facecolors=plt.cm.viridis(np.abs(B_r)))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z (Height)')
    ax.set_title('3D Radiation Pattern')
    plt.show()

# Main function to update and visualize
def simulate_beacon(plot3D, rotation_angle, depth):
    r, theta, z = create_grid(plot3D)
    
    # Calculate the magnetic field for each point
    B_r, B_theta = magnetic_field(r, theta, rotation_angle, depth)
    
    if plot3D:
        plot_3d(r, theta, z, B_r)
    else:
        plot_2d(r, theta, B_r)

# Run simulation
simulate_beacon(plot3D, rotation_angle, depth)
