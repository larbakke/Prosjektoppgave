% Orientation angles (0 for vertical, 45 degrees, and horizontal)
theta = [0, 45, 90];  % in degrees

for i = 1:length(theta)
    % Convert theta to radians
    angle = deg2rad(theta(i));
    
    % Update dipole moment direction for tilted source
    H_theta_tilted = Htheta * cos(angle) + Hr * sin(angle);
    
    % Visualization for each orientation
    figure;
    contourf(X, Y, H_theta_tilted, 20);
    colorbar;
    title(['Magnetic Field Intensity at ', num2str(theta(i)), '° Tilt']);
    xlabel('X (m)');
    ylabel('Y (m)');
end
