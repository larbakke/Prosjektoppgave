class Position:
    """A class to represent a physical position and rotation in space."""
    def __init__(self, x: float, y: float, z: float, pitch: float, yaw: float, roll: float):
        self.x = x
        self.y = y
        self.z = z
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll

    def getStep(self):
        return (self.x, self.y, self.z, self.pitch, self.yaw, self.roll)
    
    def addDelta(self, dx=0, dy=0, dz=0, dpitch=0, dyaw=0, droll=0):
        return Position(self.x + dx, self.y + dy, self.z + dz, self.pitch + dpitch, self.yaw + dyaw, self.roll + droll)
    
    def __str__(self):
        return f"(x:{self.x}, y:{self.y}, z:{self.z}, p:{self.pitch}, yw:{self.yaw}, r:{self.roll})"
    
    def is_close(self, other, threshold=1e-5):
        """
        Compares this position with another position to see if they are the same within a given threshold.
        :param other: The other Position object to compare.
        :param threshold: The maximum allowable difference for each attribute.
        :return: True if all attributes are within the threshold, False otherwise.
        """
        if not isinstance(other, Position):
            raise TypeError("Can only compare with another Position object.")
        
        return (
            abs(self.x - other.x) <= threshold and
            abs(self.y - other.y) <= threshold and
            abs(self.z - other.z) <= threshold and
            abs(self.pitch - other.pitch) <= threshold and
            abs(self.yaw - other.yaw) <= threshold and
            abs(self.roll - other.roll) <= threshold
        )
    

class Measurement:
    def __init__(self, position: Position, signal_strength: float, signal_direction: float, timestamp: float):
        self.position = position
        self.signal_strength = signal_strength
        self.signal_direction = signal_direction   #signal direction is the angle of the signal from the drone's current rotation and position in yaw axis
        self.timestamp = timestamp
