'use client';

import * as THREE from 'three';
import { useEffect } from 'react';

interface SlopeProps {
  width: number;
  height: number;
  angle: number;  // in degrees
  color: number;  // hexadecimal color
  scene: THREE.Scene;  // Pass the scene from MainScene
}

const Slope = ({ width, height, angle, color, scene }: SlopeProps) => {
  useEffect(() => {
    // Create slope geometry and material
    const slopeGeometry = new THREE.PlaneGeometry(width, height, 32, 32);
    const slopeMaterial = new THREE.MeshStandardMaterial({ color, side: THREE.DoubleSide });
    const slopeMesh = new THREE.Mesh(slopeGeometry, slopeMaterial);

    // Rotate and position slope
    slopeMesh.rotation.x = THREE.MathUtils.degToRad(angle);
    slopeMesh.position.set(0, 50, 100); // Adjust position so it's visible in the camera's view

    // Add the slope mesh directly to the scene
    scene.add(slopeMesh);

    // Cleanup when the component unmounts (optional)
    return () => {
      scene.remove(slopeMesh);
    };
  }, [width, height, angle, color, scene]);

  return null;  // Nothing to render in JSX, this is just a 3D object
};

export default Slope;
