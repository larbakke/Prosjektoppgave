% Constants
M = 1;  % Dipole moment (arbitrary unit, normalize later)
f = 457e3;  % Frequency in Hz
omega = 2 * pi * f;  % Angular frequency
mu0 = 4 * pi * 1e-7;  % Permeability of free space (H/m)
eps0 = 8.854e-12;  % Permittivity of free space (F/m)

% Simulation parameters
depth = 1;  % Depth of source in meters
x = linspace(-10, 10, 100);  % X-axis points
y = linspace(-10, 10, 100);  % Y-axis points
[X, Y] = meshgrid(x, y);  % 2D grid for simulation

% Calculate radial distance to each point on the grid
R = sqrt(X.^2 + Y.^2 + depth^2);  % 3D distance from source

% Magnetic field components in free space (near field equations)
Hr = (M ./ (2 * pi * R.^3)) .* (depth ./ R);  % Radial component
Htheta = (M ./ (4 * pi * R.^3)) .* sqrt(X.^2 + Y.^2) ./ R;  % Angular component

% Resultant field magnitude
H = sqrt(Hr.^2 + Htheta.^2);

% Visualization
figure;
contourf(X, Y, H, 20);
colorbar;
title('Magnetic Field Intensity');
xlabel('X (m)');
ylabel('Y (m)');
