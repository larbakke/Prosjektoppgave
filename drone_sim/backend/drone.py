import numpy as np
from preDefPath import PreDefPath
from slope import Slope
from position import Measurement, Position
from typing import List, Tuple

class Drone:
    def __init__(self, start_position: Position, speed_limit: float, rot_speed_limit: float, slope: Slope, simulation_id, antenna_range: int):
        """
        Represents a drone with a position, speed limit, and slope constraints.
        :param start_position: (x, y, z) tuple for the drone's starting position.
        :param speed_limit: Maximum speed (units per timestep).
        :param slope: The Slope object representing the search area.
        """
        self._position = start_position
        self.speed_limit = speed_limit
        self.rot_speed_limit = rot_speed_limit
        self.slope = slope
        self.simulation_id = simulation_id
        self._positionHist =  [(self._position, 0)]
        self._measurements = []
        self._antenna_range = antenna_range
        self._path = PreDefPath()

    def move(self, dx, dy, dz, dpitch, dyaw, droll, dt):
        """
        Move the drone by given deltas, respecting the speed limit and slope.
        :param dx: Change in x-axis.
        :param dy: Change in y-axis.
        :param dz: Change in z-axis.
        :param dpitch: Change in pitch.
        :param dyaw: Change in yaw.
        :param droll: Change in roll.
        :param dt: Change in time.
        """
        # Compute the distance and enforce speed limit
        displacement = np.array([dx, dy, dz])
        distance = np.linalg.norm(displacement)
        if distance/dt > self.speed_limit:
            print(f"Speed limit exceeded! Max allowed: {self.speed_limit}, Attempted: {distance}")
            displacement = displacement / distance * self.speed_limit  # Scale to speed limit

        

        # Update orientation
        # Compute the new orientation
        rot_displacement = np.array([dpitch, dyaw, droll])
        
        # Compute the rotational speed and enforce rotational speed limit
        rotation_speed = np.linalg.norm([dpitch, dyaw, droll])
        if rotation_speed/dt > self.rot_speed_limit:
            print(f"Rotational speed limit exceeded! Max allowed: {self.rot_speed_limit}, Attempted: {rotation_speed}")
            new_orientation = rot_displacement / rotation_speed * self.rot_speed_limit * dt  # Scale to speed limit

        # Update position
        new_position = self._position.addDelta(dx=displacement[0], dy=displacement[1], dz=displacement[2], dpitch=rot_displacement[0], dyaw=rot_displacement[1], droll=rot_displacement[2])
        

        # Check if the new position violates slope constraints
        if new_position.y < 0 or not self.slope.is_above(new_position):
            print(f"Invalid move! Drone cannot go beneath or through the slope. Current Position: {self._position}")
        else:
            self._position = new_position
            print(f"Drone moved t0 ", self._position)
            self._positionHist.append((self._position, dt + self._positionHist[-1][1]))

    @property
    def position(self) -> Position:
        """Return the current position of the drone."""
        return self._position
    
    @property
    def antenna_range(self) -> int:
        return self._antenna_range
    
    @property
    def positionHist(self) -> List[Tuple[Position, float]]:
        return self._positionHist
    
    @property
    def measurements(self) -> List[Measurement]:
        return self._measurements
    
    @property
    def path(self) -> PreDefPath:
        return self._path
    
    def addPath(self, path: PreDefPath):
        self._path.addPath(path.path)
    

    def flyTowards(self, position: Position, dt: float):
        """Move the drone towards a target position."""
        # Calculate the direction vector towards the target position
        direction = np.array([position.x - self._position.x, position.y - self._position.y, position.z - self._position.z])
        distance = np.linalg.norm(direction)
        
        # Normalize the direction vector
        if distance > 0:
            direction = direction / distance
        
        # Calculate the maximum distance we can travel in this timestep
        max_distance = self.speed_limit * dt
        
        # Calculate the actual distance to move
        move_distance = min(distance, max_distance)
        
        # Calculate the displacement
        displacement = direction * move_distance
        
        # Calculate the rotation needed to face the target position
        target_orientation = np.array([position.pitch, position.yaw, position.roll])
        current_orientation = np.array([self._position.pitch, self._position.yaw, self._position.roll])
        rot_direction = target_orientation - current_orientation
        rot_distance = np.linalg.norm(rot_direction)
        
        # Normalize the rotation direction vector
        if rot_distance > 0:
            rot_direction = rot_direction / rot_distance
        
        # Calculate the maximum rotation we can achieve in this timestep
        max_rot_distance = self.rot_speed_limit * dt
        
        # Calculate the actual rotation to apply
        rot_move_distance = min(rot_distance, max_rot_distance)
        
        # Calculate the rotational displacement
        rot_displacement = rot_direction * rot_move_distance
        
        # Move the drone
        self.move(displacement[0], displacement[1], displacement[2], rot_displacement[0], rot_displacement[1], rot_displacement[2], dt)


    def measureSignal(self) -> bool:
        """Return True if signal is detected. The detection will be addedd to the measurements list."""
        transmitter = self.slope.transmittAntenna
        signal_strength, signal_direction = transmitter.read_signal(self.position, self.antenna_range)
        if signal_strength is not None:
            measurement = Measurement(self.position, signal_strength, signal_direction, timestamp=0)
            self._measurements.append(measurement)
            return True
        return False
    
    def calculatePath(self):
        '''Calculate the best searchpath for covering the whole slope. Given the slope and the drone's position'''
        pass

    def followPath(self, d_time: float = 0.1):
        '''Follow the calculated path'''
        while not self.path.isComplete():
            self.flyTowards(self.path.getNext(), d_time)
            self.measureSignal()
                
        #finish the path
        return True

    
