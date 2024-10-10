% Soil parameters for half-space model
epsilon_r_soil = 8;  % Relative permittivity of soil
sigma_soil = 1e-3;  % Conductivity in S/m
epsilon_c_soil = eps0 * epsilon_r_soil - 1j * sigma_soil / omega;  % Complex permittivity

% Half-space correction (simplified reflection coefficient)
reflection_coefficient = (mu0 - sqrt(mu0 * epsilon_c_soil)) / (mu0 + sqrt(mu0 * epsilon_c_soil));

% Adjust the magnetic field strength in the half-space model
H_half_space = H * abs(reflection_coefficient);

% Visualization of half-space model
figure;
contourf(X, Y, H_half_space, 20);
colorbar;
title('Half-Space Magnetic Field Intensity');
xlabel('X (m)');
ylabel('Y (m)');
