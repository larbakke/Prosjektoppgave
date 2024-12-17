import { SimulationDetails } from './interfaces';
import * as THREE from 'three';

export function runSimulation(simulationData: SimulationDetails, droneRef: { current: THREE.Mesh | null }) {
    if (droneRef.current) {
        for (let i = 0; i < simulationData.drone_path.length; i++) {
            droneRef.current.moveDrone([simulationData.drone_path[i].position.x, simulationData.drone_path[i].position.y, simulationData.drone_path[i].position.z], 20000);
        }
        // droneRef.current.moveDrone([simulationData.drone_path[0].position.x, simulationData.drone_path[0].position.y, simulationData.drone_path[0].position.z], 2000);
      }
}
  
    // Define the dummy point for the drone to move to
//   const dummyPoint = new THREE.Vector3(10, 20, 30); // Example position (10, 20, 30)
//   console.log('Running simulation:', simulationData);
//   if (!droneRef.current) {
//     console.error('Drone reference is null!');
//     return;
//   }

//   // Get the starting position of the drone
//   console.log('Drone starting position:', droneRef);
//   const startPosition = droneRef.current.position.clone();
//   const animationDuration = 2000; // Animation duration in milliseconds
//   const startTime = performance.now();

//   const animate = (time: number) => {
//     if (!droneRef.current) return;

//     // Calculate the elapsed time as a fraction of the total duration
//     const elapsed = time - startTime;
//     const t = Math.min(elapsed / animationDuration, 1); // Clamp t between 0 and 1

//     // Linearly interpolate between the start and dummy point
//     droneRef.current.position.lerpVectors(startPosition, dummyPoint, t);

//     // If the animation is not complete, request the next frame
//     if (t < 1) {
//       requestAnimationFrame(animate);
//     } else {
//       console.log('Drone reached the dummy point:', dummyPoint);
//     }
//   };

//   // Start the animation loop
//   requestAnimationFrame(animate);
// }
