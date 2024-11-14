import numpy as np
from position import Position
from typing import Tuple

class TransmittAntenna:
    def __init__(self, id, position: Position, name, type, power, frequency, gain, azimuth, beamwidth, polarization, pattern):
        self.id = id
        self.position = position
        self.name = name
        self.type = type
        self.power = power
        self.frequency = frequency
        self.gain = gain
        self.azimuth = azimuth
        self.beamwidth = beamwidth
        self.polarization = polarization
        self.pattern = pattern
        self.antenna = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "power": self.power,
            "frequency": self.frequency,
            "gain": self.gain,
            "azimuth": self.azimuth,
            "beamwidth": self.beamwidth,
            "polarization": self.polarization,
            "pattern": self.pattern
        }

    def getAntenna(self):
        return self.antenna
    
    def getPosition(self):
        return self.position
    
    def read_signal(self, position: Position, range: int = 40) -> Tuple[float, float]:
        """Return the signal strength at the drone's current position."""
        d_dist = np.linalg.norm(np.array([self.position.x, self.position.y, self.position.z]) - np.array([position.x, position.y, position.z]))
        signal_strength = d_dist
        direction_vector = np.array([position.x, position.y, position.z]) - np.array([self.position.x, self.position.y, self.position.z])
        signal_direction = np.arctan2(direction_vector[1], direction_vector[0])

        # Check if the reading antenna is to far away from transmitter
        # if d_dist > range:
        #     signal_strength = None
        #     signal_direction = None

        return (signal_strength, signal_direction)