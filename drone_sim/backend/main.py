from db import (
    initialize_database,
    create_simulation,
    log_position,
    log_simulation_result,
    log_measurement,
    add_slope,
    add_transmitt_antenna,
)
from slope import Slope
from drone import Drone
from position import Position
from preDefPath import PreDefPath
from transmittAntenna import TransmittAntenna

def run_simulation():
    """
    Simulates a drone's movement on a slope and stores the results in the database.
    """
    # Step 1: Initialize the database
    initialize_database()

    # Step 2: Define the slope and drone
    transmittAntenna = TransmittAntenna(1, Position(0, 0, 0, 0, 0, 0), "Transmitter", "Omni", 10, 2.4, 5, 0, 360, "Vertical", "Pattern")
    slope = Slope(width=100, height=200, angle=35, transmittAntenna=transmittAntenna)


    # Step 3: Create a new simulation entry
    simulation_description = "Simulation of drone movement on a 35-degree slope."
    antenna_id = add_transmitt_antenna(transmittAntenna)
    slope_id = add_slope(slope, antenna_id)
    simulation_id = create_simulation(simulation_description, slope_id, antenna_id)
    print(f"Created simulation with ID: {simulation_id}")

    #Initialize drone
    start_position = Position(0, 0, 5, 0, 0, 0)
    drone = Drone(
        start_position=start_position,
        speed_limit=10.0,
        rot_speed_limit=30.0,
        slope=slope,
        simulation_id=simulation_id,
        antenna_range=100,
    )

    # Step 4: Simulate drone movements
    # Create a path for the drone to follow
    path_positions = [
        Position(0, 0, 10, 0, 0, 0),
        Position(0, 0, 20, 0, 15, 0),
        Position(20, 0, 10, 0, 30, 0),
        Position(30, 10, 10, 0, 45, 0),
    ]
    path = PreDefPath(path_positions)
    drone.addPath(path)

    time_step = 0.05

    if drone.followPath(d_time=time_step):
        print("Successe! Drone reached the end of the path.")


    # Step 5: Log everythoing to the database

    for position, timestamp in drone.positionHist:
        log_position(simulation_id, timestamp, position)

    for measurement in drone.measurements:
        log_measurement(simulation_id, measurement)

    log_simulation_result(
        simulation_id,
        start_position,
        slope.transmittAntenna.position,
        drone.position,
        len(drone.positionHist),
    )

    print("\nSimulation complete. Results stored in the database.")

if __name__ == "__main__":
    print('\n\n**************************\nStarting simulation...\n**************************\n\n')
    run_simulation()
    print('\n\n**************************\nSimulation complete.\n**************************\n\n')
