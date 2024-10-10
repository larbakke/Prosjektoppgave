% Constants
M = 1;  % Dipole moment (arbitrary unit, normalize later)
f = 457e3;  % Frequency in Hz
omega = 2 * pi * f;  % Angular frequency
mu0 = 4 * pi * 1e-7;  % Permeability of free space (H/m)
eps0 = 8.854e-12;  % Permittivity of free space (F/m)

% Simulation parameters
depth = 1;  % Depth of source in meters
x = linspace(-10, 10, 50);  % X-axis points
y = linspace(-10, 10, 50);  % Y-axis points
z = linspace(-10, 10, 50);  % Z-axis points
[X, Y, Z] = meshgrid(x, y, z);  % 3D grid for simulation

% Calculate radial distance to each point in 3D space
R = sqrt(X.^2 + Y.^2 + Z.^2);  % 3D distance from source at the origin

% Magnetic field components in free space (near field equations)
Hr = (M ./ (2 * pi * R.^3)) .* (depth ./ R);  % Radial component in 3D
Htheta = (M ./ (4 * pi * R.^3)) .* sqrt(X.^2 + Y.^2 + Z.^2) ./ R;  % Angular component in 3D

% Resultant field magnitude
H = sqrt(Hr.^2 + Htheta.^2);

% 3D Visualization
figure;
% Create a slice plot to visualize the magnetic field in 3D
slice(X, Y, Z, H, 0, 0, 0);  % Slice at the origin for better visibility
colorbar;
title('3D Magnetic Field Intensity');
xlabel('X (m)');
ylabel('Y (m)');
zlabel('Z (m)');
shading interp;  % Smooth shading
