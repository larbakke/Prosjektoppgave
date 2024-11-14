import numpy as np

from position import Position
from transmittAntenna import TransmittAntenna

class Slope:
    def __init__(self, width: float, height: float, angle: float, transmittAntenna: TransmittAntenna):
        """
        Represents a slope with given width, height, and angle of inclination.
        The slope is centered at the origin and inclined along the X-Z plane.
        """
        self.width = width
        self.height = height
        self.angle = angle  # Degrees
        self.normal_vector = self._calculate_normal()
        self._transmittAntenna = transmittAntenna

    @property
    def transmittAntenna(self) -> TransmittAntenna:
        return self._transmittAntenna

    def _calculate_normal(self):
        """Calculate the normal vector of the inclined plane."""
        radians = np.radians(self.angle)
        # Normal vector for a plane inclined in X-Z (no tilt in Y axis)
        return np.array([np.sin(radians), 0, np.cos(radians)])

    def is_above(self, position: Position) -> bool:
        """
        Check if a point is above the slope.
        :param position: (x, y, z) tuple representing the point's position.
        :return: True if the point is above the slope, False otherwise.
        """
        x= position.x
        y= position.y
        z= position.z

        if abs(x) > self.width / 2 or abs(z) > self.height / 2:
            return False  # Outside slope bounds, but not invalid
        # Check height relative to the slope plane
        slope_y = (x * np.tan(np.radians(self.angle)))
        return y >= slope_y
    
