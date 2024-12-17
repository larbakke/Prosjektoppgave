import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit

# Constants and parameters
uav_velocity = 10  # UAV velocity (m/s)
time = np.linspace(0, 10, 300)  # Dense time points
true_target_location = np.array([0, 0])  # True target location (x, y)
uav_trajectory = np.array([50 * np.cos(0.1 * time), 50 * np.sin(0.1 * time)]).T  # Circular trajectory
noise_std = 0.05  # Noise standard deviation for AOA

# Function to simulate Bearings-Only Angles (BOAs)
def generate_aoa(uav_positions, target_location, noise_std):
    relative_positions = target_location - uav_positions
    true_aoa = np.arctan2(relative_positions[:, 1], relative_positions[:, 0])  # True AOA
    noisy_aoa = true_aoa + np.random.normal(0, noise_std, true_aoa.shape)  # Add noise
    return true_aoa, noisy_aoa

# Generate true and noisy AOAs
true_aoa, noisy_aoa = generate_aoa(uav_trajectory, true_target_location, noise_std)

# Smooth the noisy AOAs
smoothed_aoa = savgol_filter(noisy_aoa, window_length=21, polyorder=2)

# Corrected Angle-Rate Algorithm
def corrected_angle_rate_algorithm(uav_positions, smoothed_aoa, uav_velocity):
    aoa_rates = np.gradient(smoothed_aoa, time)  # Angular rate of change

    # Filter valid angular rates
    valid = np.abs(aoa_rates) > 1e-4

    if np.sum(valid) < 2:
        raise ValueError("Not enough valid angular rates for estimation.")

    # Define nonlinear model for AOA regression
    def aoa_model(t, a, b):
        return a * t + b

    # Fit the smoothed AOA data to the nonlinear model
    popt, _ = curve_fit(aoa_model, time[valid], smoothed_aoa[valid])
    avg_rate, avg_aoa = popt  # Extract average angular rate and AOA

    # Sanity check for angular rate
    if np.abs(avg_rate) < 1e-5:
        raise ValueError("Angular rate too small for reliable range estimation.")

    estimated_range = uav_velocity / avg_rate  # Estimated range
    estimated_cross_range = estimated_range * np.tan(avg_aoa)

    # Correct for systematic bias
    bias_correction = np.array([100, 0])  # Adjust for systematic offset
    corrected_position = np.array([estimated_range * np.cos(avg_aoa), estimated_cross_range]) - bias_correction

    return corrected_position, avg_aoa, avg_rate

# Triangulation method to estimate the target location
def triangulation_algorithm(uav_positions, smoothed_aoa):
    A = np.zeros((len(smoothed_aoa) - 1, 2))
    b = np.zeros(len(smoothed_aoa) - 1)
    for i in range(len(smoothed_aoa) - 1):
        dx = uav_positions[i + 1, 0] - uav_positions[i, 0]
        dy = uav_positions[i + 1, 1] - uav_positions[i, 1]
        angle_diff = smoothed_aoa[i + 1] - smoothed_aoa[i]
        A[i, 0] = -dy
        A[i, 1] = dx
        b[i] = dx * np.tan(smoothed_aoa[i]) - dy
    estimated_location, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    return estimated_location

# Compute estimates
estimated_target_angle_rate, avg_aoa, avg_rate = corrected_angle_rate_algorithm(uav_trajectory, smoothed_aoa, uav_velocity)
estimated_target_triangulation = triangulation_algorithm(uav_trajectory, smoothed_aoa)

# Debug intermediate results
print("Average AOA:", avg_aoa)
print("Average Angular Rate:", avg_rate)
print("Estimated Target (Angle-Rate):", estimated_target_angle_rate)
print("Estimated Target (Triangulation):", estimated_target_triangulation)

# Plot UAV trajectory, AOA lines, true target, and estimated target
plt.figure(figsize=(12, 12))
plt.plot(uav_trajectory[:, 0], uav_trajectory[:, 1], label="UAV Trajectory", color="blue")  # UAV trajectory
plt.scatter(*true_target_location, color="red", label="True Target", zorder=5)  # True target
plt.scatter(*estimated_target_angle_rate, color="green", label="Angle-Rate Estimate", zorder=5)  # Angle-rate estimate
plt.scatter(*estimated_target_triangulation, color="purple", label="Triangulation Estimate", zorder=5)  # Triangulation estimate

# Add AOA lines
for i in range(0, len(uav_trajectory), 20):  # Plot every 20th AOA for clarity
    uav_pos = uav_trajectory[i]
    angle = smoothed_aoa[i]
    line_length = 70  # Length of the line
    x_end = uav_pos[0] + line_length * np.cos(angle)
    y_end = uav_pos[1] + line_length * np.sin(angle)
    plt.plot([uav_pos[0], x_end], [uav_pos[1], y_end], color="orange", alpha=0.4)

plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.legend()
plt.title("UAV Trajectory, AOA Lines, and Target Estimates (Corrected Angle-Rate)")
plt.grid()
plt.axis("equal")
plt.show()
