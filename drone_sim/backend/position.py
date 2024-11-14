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
    

class Measurement:
    def __init__(self, position: Position, signal_strength: float, signal_direction: float, timestamp: float):
        self.position = position
        self.signal_strength = signal_strength
        self.signal_direction = signal_direction   #signal direction is the angle of the signal from the drone's current rotation and position in yaw axis
        self.timestamp = timestamp
