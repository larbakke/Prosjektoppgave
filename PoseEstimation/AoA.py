import numpy as np
import matplotlib.pyplot as plt

# Define UAV trajectory parameters
time = np.linspace(0, 18, 300)  # Time points
uav_trajectory = np.array([50 * np.cos(0.1 * time), 50 * np.sin(0.1 * time)]).T  # Circular trajectory

# Define a true target position
true_target_location = np.array([0, 0])  # True target location (x, y)

# Noise standard deviation for AoA
noise_std = 0.05  # Noise standard deviation (in radians)

# Function to simulate Bearings-Only Angles (BOAs)
def generate_aoa(uav_positions, target_location, noise_std):
    relative_positions = target_location - uav_positions
    true_aoa = np.arctan2(relative_positions[:, 1], relative_positions[:, 0])  # True AOA
    noisy_aoa = true_aoa + np.random.normal(0, noise_std, true_aoa.shape)  # Add noise
    return true_aoa, noisy_aoa

# Triangulation method to estimate the target location
def triangulation_algorithm(uav_positions, noisy_aoa):
    A = np.zeros((len(noisy_aoa) - 1, 2))
    b = np.zeros(len(noisy_aoa) - 1)
    for i in range(len(noisy_aoa) - 1):
        dx = uav_positions[i + 1, 0] - uav_positions[i, 0]
        dy = uav_positions[i + 1, 1] - uav_positions[i, 1]
        angle_diff = noisy_aoa[i + 1] - noisy_aoa[i]
        A[i, 0] = -dy
        A[i, 1] = dx
        b[i] = dx * np.tan(noisy_aoa[i]) - dy
    estimated_location, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    return estimated_location

# Generate true and noisy AOAs
true_aoa, noisy_aoa = generate_aoa(uav_trajectory, true_target_location, noise_std)

# Estimate target position
estimated_target_location = triangulation_algorithm(uav_trajectory, noisy_aoa)

# Plot UAV trajectory and AOA lines
plt.figure(figsize=(12, 12))
plt.plot(uav_trajectory[:, 0], uav_trajectory[:, 1], label="UAV Trajectory", color="blue")  # UAV trajectory

plt.scatter(*true_target_location, color="red", s=80, label="True Target", zorder=5)  # True target
plt.scatter(*estimated_target_location, color="green", s=80, label="Estimated Target", zorder=5)  # Estimated target
# Add AOA lines
for i in range(0, len(uav_trajectory), 60):  # Plot every 20th AOA for clarity
    uav_pos = uav_trajectory[i]
    angle = noisy_aoa[i]
    line_length = 70  # Length of the line
    x_end = uav_pos[0] + line_length * np.cos(angle)
    y_end = uav_pos[1] + line_length * np.sin(angle)
    plt.plot([uav_pos[0], x_end], [uav_pos[1], y_end], color="orange", alpha=0.4)

# Plot settings
plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.legend()
plt.title("UAV Trajectory, AOA Lines, and Estimated Position")
plt.grid()
plt.axis("equal")
plt.show()
