'use client';

import * as THREE from 'three';
import { useEffect, useRef, useState } from 'react';

interface BeaconProps {
  scene: THREE.Scene;
  depth: number; // Burial depth in meters
}

const AvalancheBeacon = ({ scene, depth }: BeaconProps) => {
  const beaconRef = useRef<THREE.Mesh | null>(null);
  const [fieldLines, setFieldLines] = useState<THREE.Group | null>(null);

  useEffect(() => {
    // Create the beacon model (a small cube)
    const beaconGeometry = new THREE.BoxGeometry(1, 1, 1);
    const beaconMaterial = new THREE.MeshStandardMaterial({ color: 0xff0000 }); // Red beacon
    const beaconMesh = new THREE.Mesh(beaconGeometry, beaconMaterial);

    // Set beacon position based on depth (negative Y axis for burial)
    beaconMesh.position.set(0, -depth, 0);

    // Add beacon to the scene
    scene.add(beaconMesh);
    beaconRef.current = beaconMesh;

    // Create magnetic field lines
    const fieldGroup = new THREE.Group(); // Group to hold all field lines
    const numLines = 20; // Number of field lines to represent the magnetic field

    for (let i = 0; i < numLines; i++) {
      const angle = (i / numLines) * Math.PI * 2; // Distribute lines in a circle around the beacon

      // Create the field lines (curved lines representing magnetic flux)
      const points = [];
      const radius = 40; // Radius of the field lines
      for (let t = 0; t < Math.PI; t += 0.1) {
        const x = radius * Math.sin(t) * Math.cos(angle);
        const y = radius * Math.cos(t); // Height of the line (change with burial depth)
        const z = radius * Math.sin(t) * Math.sin(angle);
        points.push(new THREE.Vector3(x, y - depth, z)); // Adjust height by burial depth
      }

      const geometry = new THREE.BufferGeometry().setFromPoints(points);
      const material = new THREE.LineBasicMaterial({ color: 0x00ff00 }); // Green for field lines
      const line = new THREE.Line(geometry, material);

      fieldGroup.add(line); // Add line to the group
    }

    scene.add(fieldGroup); // Add field lines to the scene
    setFieldLines(fieldGroup);

    // Cleanup when the component is unmounted
    return () => {
      if (beaconRef.current) scene.remove(beaconRef.current);
      if (fieldGroup) scene.remove(fieldGroup);
    };
  }, [depth, scene]);

  return null; // The beacon and field are part of the 3D scene, not JSX
};

export default AvalancheBeacon;
