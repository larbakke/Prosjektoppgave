from typing import List, Optional
from position import Position, Measurement  # Assuming Position and Measurement are properly defined
from slope import Slope
from transmittAntenna import TransmittAntenna
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(BASE_DIR, "simulation.db")

def initialize_database():
    """
    Initialize the SQLite database with tables for simulations, slopes, and transmitt_antennas.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Table for simulation metadata
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            slope_id INTEGER,
            transmitt_antenna_id INTEGER,
            FOREIGN KEY (slope_id) REFERENCES slopes (id),
            FOREIGN KEY (transmitt_antenna_id) REFERENCES transmitt_antennas (id)
        )
    """)

    # Table for slopes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS slopes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            width REAL NOT NULL,
            height REAL NOT NULL,
            angle REAL NOT NULL,
            normal_vector_x REAL NOT NULL,
            normal_vector_y REAL NOT NULL,
            normal_vector_z REAL NOT NULL,
            transmitt_antenna_id INTEGER,
            FOREIGN KEY (transmitt_antenna_id) REFERENCES transmitt_antennas (id)
        )
    """)

    # Table for transmitt antennas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transmitt_antennas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            position_x REAL NOT NULL,
            position_y REAL NOT NULL,
            position_z REAL NOT NULL,
            position_pitch REAL NOT NULL,
            position_yaw REAL NOT NULL,
            position_roll REAL NOT NULL,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            power REAL NOT NULL,
            frequency REAL NOT NULL,
            gain REAL NOT NULL,
            azimuth REAL NOT NULL,
            beamwidth REAL NOT NULL,
            polarization TEXT NOT NULL,
            pattern TEXT NOT NULL
        )
    """)

    # Create the simulation_results table to store final simulation results
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS simulation_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            simulation_id INTEGER NOT NULL,
            start_position TEXT NOT NULL,
            antenna_center TEXT NOT NULL,
            final_position TEXT NOT NULL,
            steps INTEGER NOT NULL,
            FOREIGN KEY (simulation_id) REFERENCES simulations (id)
        )
    """)

    # Create the drone_paths table to store the trajectory, including rotations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drone_paths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            simulation_id INTEGER NOT NULL,
            timestamp REAL NOT NULL,
            x REAL NOT NULL,
            y REAL NOT NULL,
            z REAL NOT NULL,
            pitch REAL NOT NULL,
            yaw REAL NOT NULL,
            roll REAL NOT NULL,
            FOREIGN KEY (simulation_id) REFERENCES simulations (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drone_measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            simulation_id INTEGER NOT NULL,
            timestamp REAL NOT NULL,
            x REAL NOT NULL,
            y REAL NOT NULL,
            z REAL NOT NULL,
            pitch REAL NOT NULL,
            yaw REAL NOT NULL,
            roll REAL NOT NULL,
            signal_strength REAL NOT NULL,
            signal_direction REAL NOT NULL,
            FOREIGN KEY (simulation_id) REFERENCES simulations (id)
        )
    """)

    conn.commit()
    conn.close()

def create_simulation(description: str, slope_id: Optional[int] = None, transmitt_antenna_id: Optional[int] = None) -> int:
    """
    Create a simulation and return its ID.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO simulations (description, slope_id, transmitt_antenna_id)
        VALUES (?, ?, ?)
    """, (description, slope_id, transmitt_antenna_id))

    simulation_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return simulation_id


def log_position(simulation_id: int, timestamp: float, position: Position):
    """
    Log a drone position at a given timestamp to the database, including rotation.
    :param simulation_id: ID of the simulation this position is part of.
    :param timestamp: The simulated time when the position was recorded.
    :param position: The Position object representing the drone's position and rotation.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO drone_paths (simulation_id, timestamp, x, y, z, pitch, yaw, roll)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (simulation_id, timestamp, position.x, position.y, position.z,
          position.pitch, position.yaw, position.roll))

    conn.commit()
    conn.close()

def log_measurement(simulation_id: int, measurement: Measurement):
    """
    Log a drone position at a given timestamp to the database, including rotation.
    :param simulation_id: ID of the simulation this position is part of.
    :param timestamp: The simulated time when the position was recorded.
    :param position: The Position object representing the drone's position and rotation.
    """

    position = measurement.position
    timestamp = measurement.timestamp
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO drone_measurements (simulation_id, timestamp, x, y, z, pitch, yaw, roll, signal_strength, signal_direction)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (simulation_id, timestamp, position.x, position.y, position.z,
          position.pitch, position.yaw, position.roll, measurement.signal_strength, measurement.signal_direction))

    conn.commit()
    conn.close()

def log_simulation_result(simulation_id: int, start_position: Position, antenna_center: Position, final_position: Position, steps: int):
    """
    Log the final results of a simulation, storing positions as strings for readability.
    :param simulation_id: ID of the simulation.
    :param start_position: Starting Position object of the drone.
    :param antenna_center: Antenna center Position object.
    :param final_position: Final Position object of the drone.
    :param steps: Total steps taken in the simulation.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO simulation_results (simulation_id, start_position, antenna_center, final_position, steps)
        VALUES (?, ?, ?, ?, ?)
    """, (simulation_id, str(start_position.getStep()), str(antenna_center.getStep()), 
          str(final_position.getStep()), steps))

    conn.commit()
    conn.close()

def get_simulation_path(simulation_id: int) -> List[Position]:
    """
    Retrieve the path of a simulation by its ID, returning a list of Position objects.
    :param simulation_id: ID of the simulation.
    :return: List of Position objects in chronological order.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, x, y, z, pitch, yaw, roll
        FROM drone_paths
        WHERE simulation_id = ?
        ORDER BY timestamp ASC
    """, (simulation_id,))
    path = [
        Position(x=row[1], y=row[2], z=row[3], pitch=row[4], yaw=row[5], roll=row[6])
        for row in cursor.fetchall()
    ]

    conn.close()
    return path

def get_simulation_result(simulation_id: int) -> Optional[dict]:
    """
    Retrieve the final results of a simulation by its ID.
    :param simulation_id: ID of the simulation.
    :return: A dictionary with simulation results or None if not found.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT start_position, antenna_center, final_position, steps
        FROM simulation_results
        WHERE simulation_id = ?
    """, (simulation_id,))
    result = cursor.fetchone()

    conn.close()
    if result:
        return {
            "start_position": eval(result[0]),  # Safely convert the string back to Position object
            "antenna_center": eval(result[1]),
            "final_position": eval(result[2]),
            "steps": result[3]
        }
    return None

def list_simulations() -> List[dict]:
    """
    List all simulations with their IDs and descriptions.
    :return: A list of dictionaries with simulation metadata.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, description FROM simulations
    """)
    simulations = [{"id": row[0], "description": row[1]} for row in cursor.fetchall()]

    conn.close()
    return simulations

import numpy as np

def add_slope(slope: Slope, transmitt_antenna_id: Optional[int] = None) -> int:
    """
    Add a slope to the database and return its ID.
    """
    angle = slope.angle
    width = slope.width
    height = slope.height
    normal_vector = np.array([np.sin(np.radians(angle)), 0, np.cos(np.radians(angle))])
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO slopes (width, height, angle, normal_vector_x, normal_vector_y, normal_vector_z, transmitt_antenna_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (width, height, angle, normal_vector[0], normal_vector[1], normal_vector[2], transmitt_antenna_id))

    slope_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return slope_id

def add_transmitt_antenna(antenna: TransmittAntenna) -> int:
    """
    Add a transmitt antenna to the database and return its ID.
    """
    position = antenna.position
    name = antenna.name
    type_ = antenna.type
    power = antenna.power
    frequency = antenna.frequency
    gain = antenna.gain
    azimuth = antenna.azimuth
    beamwidth = antenna.beamwidth
    polarization = antenna.polarization
    pattern = antenna.pattern

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transmitt_antennas (position_x, position_y, position_z, position_pitch, position_yaw, position_roll,
                                        name, type, power, frequency, gain, azimuth, beamwidth, polarization, pattern)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (position.x, position.y, position.z, position.pitch, position.yaw, position.roll, name, type_,
          power, frequency, gain, azimuth, beamwidth, polarization, pattern))

    antenna_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return antenna_id




def get_simulation_full_details(simulation_id: int) -> dict:
    """
    Retrieve all details of a simulation to recreate it in the frontend.
    :param simulation_id: ID of the simulation.
    :return: A dictionary containing slope, antenna, path, measurements, and results.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Get simulation metadata
    cursor.execute("""
        SELECT description, slope_id, transmitt_antenna_id
        FROM simulations
        WHERE id = ?
    """, (simulation_id,))
    simulation = cursor.fetchone()
    if not simulation:
        conn.close()
        return {"error": "Simulation not found"}

    description, slope_id, antenna_id = simulation

    # Get slope details
    slope = None
    if slope_id:
        cursor.execute("""
            SELECT width, height, angle, normal_vector_x, normal_vector_y, normal_vector_z, transmitt_antenna_id
            FROM slopes
            WHERE id = ?
        """, (slope_id,))
        slope_row = cursor.fetchone()
        if slope_row:
            slope = {
                "width": slope_row[0],
                "height": slope_row[1],
                "angle": slope_row[2],
                "normal_vector": (slope_row[3], slope_row[4], slope_row[5]),
                "transmitt_antenna_id": slope_row[6]
            }

    # Get antenna details
    antenna = None
    if antenna_id:
        cursor.execute("""
            SELECT position_x, position_y, position_z, position_pitch, position_yaw, position_roll,
                   name, type, power, frequency, gain, azimuth, beamwidth, polarization, pattern
            FROM transmitt_antennas
            WHERE id = ?
        """, (antenna_id,))
        antenna_row = cursor.fetchone()
        if antenna_row:
            antenna = {
                "position": {
                    "x": antenna_row[0],
                    "y": antenna_row[1],
                    "z": antenna_row[2],
                    "pitch": antenna_row[3],
                    "yaw": antenna_row[4],
                    "roll": antenna_row[5],
                },
                "name": antenna_row[6],
                "type": antenna_row[7],
                "power": antenna_row[8],
                "frequency": antenna_row[9],
                "gain": antenna_row[10],
                "azimuth": antenna_row[11],
                "beamwidth": antenna_row[12],
                "polarization": antenna_row[13],
                "pattern": antenna_row[14]
            }

    # Get drone path
    cursor.execute("""
        SELECT timestamp, x, y, z, pitch, yaw, roll
        FROM drone_paths
        WHERE simulation_id = ?
        ORDER BY timestamp ASC
    """, (simulation_id,))
    drone_path = [
        {
            "timestamp": row[0],
            "position": {
                "x": row[1],
                "y": row[2],
                "z": row[3],
                "pitch": row[4],
                "yaw": row[5],
                "roll": row[6]
            }
        }
        for row in cursor.fetchall()
    ]

    # Get drone measurements
    cursor.execute("""
        SELECT timestamp, x, y, z, pitch, yaw, roll, signal_strength, signal_direction
        FROM drone_measurements
        WHERE simulation_id = ?
        ORDER BY timestamp ASC
    """, (simulation_id,))
    drone_measurements = [
        {
            "timestamp": row[0],
            "position": {
                "x": row[1],
                "y": row[2],
                "z": row[3],
                "pitch": row[4],
                "yaw": row[5],
                "roll": row[6]
            },
            "signal_strength": row[7],
            "signal_direction": row[8]
        }
        for row in cursor.fetchall()
    ]

    # Get simulation results
    cursor.execute("""
        SELECT start_position, antenna_center, final_position, steps
        FROM simulation_results
        WHERE simulation_id = ?
    """, (simulation_id,))
    simulation_result = cursor.fetchone()
    result = None
    if simulation_result:
        result = {
            "start_position": eval(simulation_result[0]),
            "antenna_center": eval(simulation_result[1]),
            "final_position": eval(simulation_result[2]),
            "steps": simulation_result[3]
        }

    conn.close()

    # Construct full simulation details
    return {
        "simulation": {
            "id": simulation_id,
            "description": description
        },
        "slope": slope,
        "antenna": antenna,
        "drone_path": drone_path,
        "drone_measurements": drone_measurements,
        "result": result
    }
