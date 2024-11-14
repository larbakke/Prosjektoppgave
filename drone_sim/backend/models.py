from typing import List, Optional
from position import Position, Measurement  # Assuming Position and Measurement are properly defined
import sqlite3

DATABASE_FILE = "simulation.db"

def initialize_database():
    """
    Initialize the SQLite database with tables for simulations, drone paths, and simulation results.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Create the simulations table to store simulation metadata
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL
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

def create_simulation(description: str) -> int:
    """
    Create a new simulation entry and return its ID.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO simulations (description)
        VALUES (?)
    """, (description,))
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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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
