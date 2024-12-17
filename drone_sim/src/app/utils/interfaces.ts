export interface SimulationDetails {
    simulation: {
      id: number;          // Unique identifier for the simulation
      description: string; // A description of the simulation
    };
    slope: {
      width: number;       // Width of the slope
      height: number;      // Height of the slope
      angle: number;       // Angle of the slope
      color: number;       // Hexadecimal color representation
    };
    antenna: {
        azimuth: number,
        beamwidth: number,
        frequency: number,
        gain: number,
        name: string,
        pattern: string,
        polarization: string,
        position: {
                x: number, 
                y: number,
                z: number, 
                pitch: number,
                yaw: number,
                roll: number, 
            }
        power: number,
        type: string,                // Radius of the antenna's effective range
    };
    drone_path: Array<{
        position: {
            x: number, 
            y: number,
            z: number, 
            pitch: number,
            yaw: number,
            roll: number,
        },
        timestamp: number,
    }>; // Array of 3D coordinates representing the drone's path
    drone_measurements: Array<number>;          // Array of measurements taken by the drone at each step
    result: {
      final_position: [number, number, number]; // Final position of the drone
      steps: number;                           // Number of steps in the simulation
    };
  }
  


  export interface SceneConfig {
    camera: {
      position: [number, number, number];
      lookAt: [number, number, number];
    };
    slope: {
      width: number;
      height: number;
      angle: number;
      color: number;
    };
    light: {
      position: [number, number, number];
      color: number;
      intensity: number;
    };
    ground: {
      size: number;
      color: number;
    };
    drone: {
      startPosition: [number, number, number];
    };
    beacon: {
      depth: number;
    };
  }