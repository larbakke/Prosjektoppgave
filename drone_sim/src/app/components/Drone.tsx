'use client';

import * as THREE from 'three';
import { useEffect, useRef } from 'react';

interface DroneProps {
  scene: THREE.Scene;
}

const Drone = ({ scene }: DroneProps) => {
  const droneRef = useRef<THREE.Mesh | null>(null);
  const speed = 1; // Movement speed
  const rotationSpeed = 0.02; // Rotation speed

  // Key state for movement and rotation
  const keyState: { [key: string]: boolean } = {
    ArrowUp: false,
    ArrowDown: false,
    ArrowLeft: false,
    ArrowRight: false,
    w: false,
    a: false,
    s: false,
    d: false,
  };

  useEffect(() => {
    // Create the drone geometry and material
    const droneGeometry = new THREE.BoxGeometry(5, 5, 5); // A small cube for the drone
    const droneMaterial = new THREE.MeshStandardMaterial({ color: 0x0000ff }); // Blue color for the drone
    const droneMesh = new THREE.Mesh(droneGeometry, droneMaterial);

    // Set the initial position and rotation
    droneMesh.position.set(0, 20, 0); // Starting position
    droneMesh.rotation.set(0, 0, 0); // Starting rotation

    // Add the drone to the scene
    scene.add(droneMesh);
    droneRef.current = droneMesh;

    // Keydown listener
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key in keyState) {
        keyState[event.key] = true;
      }
    };

    // Keyup listener
    const handleKeyUp = (event: KeyboardEvent) => {
      if (event.key in keyState) {
        keyState[event.key] = false;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    // Animate drone movement
    const animateDrone = () => {
      if (!droneRef.current) return;

      const position = droneRef.current.position;
      const rotation = droneRef.current.rotation;

      // Handle height (Y-axis) movement (ArrowUp, ArrowDown)
      if (keyState.ArrowUp) position.y += speed; // Move up
      if (keyState.ArrowDown) position.y -= speed; // Move down

      // Handle yaw rotation (ArrowLeft, ArrowRight)
      if (keyState.ArrowLeft) rotation.y += rotationSpeed; // Rotate left (yaw)
      if (keyState.ArrowRight) rotation.y -= rotationSpeed; // Rotate right (yaw)

      // Handle forward/backward movement (W, S)
      if (keyState.w) {
        position.x -= speed * Math.sin(rotation.y);
        position.z -= speed * Math.cos(rotation.y); // Move forward in direction of rotation
      }
      if (keyState.s) {
        position.x += speed * Math.sin(rotation.y);
        position.z += speed * Math.cos(rotation.y); // Move backward in direction of rotation
      }

      // Handle strafing movement (A, D)
      if (keyState.a) {
        position.x -= speed * Math.cos(rotation.y);
        position.z += speed * Math.sin(rotation.y); // Strafe left
      }
      if (keyState.d) {
        position.x += speed * Math.cos(rotation.y);
        position.z -= speed * Math.sin(rotation.y); // Strafe right
      }

      requestAnimationFrame(animateDrone); // Continue the animation loop
    };

    animateDrone(); // Start the animation

    return () => {
      // Cleanup event listeners and remove drone from the scene
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
      if (droneRef.current) scene.remove(droneRef.current); // Remove the drone on cleanup
    };
  }, [scene]);

  return null; // The drone is part of the 3D scene, not rendered as JSX
};

export default Drone;
