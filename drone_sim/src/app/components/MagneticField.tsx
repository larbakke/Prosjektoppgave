import * as THREE from 'three';
import { useEffect, useRef, useState } from 'react';

interface MagneticField2DProps {
  orientation: number;  // Angle to rotate the beacon
}

const MagneticField2D = ({ orientation }: MagneticField2DProps) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const [scene] = useState(new THREE.Scene());

  useEffect(() => {
    const width = mountRef.current?.clientWidth || window.innerWidth;
    const height = mountRef.current?.clientHeight || window.innerHeight;

    // Create the renderer
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(width, height);
    mountRef.current?.appendChild(renderer.domElement);

    // Create a 2D camera (orthographic)
    const camera = new THREE.OrthographicCamera(-150, 150, 30, -30, 0.1, 1000);
    camera.position.set(0, 0, 100);  // Set above looking at the 2D plane
    camera.lookAt(0, 0, 0);

    // Create material for field lines
    const lineMaterial = new THREE.LineBasicMaterial({ color: 0x000000 });

    // Create magnetic field pattern (contours)
    const fieldGroup = new THREE.Group();
    const numLines = 25;
    for (let i = 0; i < numLines; i++) {
      const fieldLine = new THREE.Geometry();
      const angleOffset = (i / numLines) * Math.PI * 2;

      // Generate a field line (using a basic dipole equation)
      for (let x = -150; x <= 150; x += 5) {
        const r = Math.sqrt(x * x + 10 * 10);  // Distance from the beacon center
        const theta = Math.atan2(10, x) + angleOffset + orientation;  // Include orientation

        // Dipole magnetic field equation approximation
        const fieldStrength = (1 / Math.pow(r, 3)) * Math.cos(theta);
        const y = fieldStrength * 10;  // Scale field strength to get y-coordinates

        fieldLine.vertices.push(new THREE.Vector3(x, y, 0));  // Add point to the line
      }

      // Create line
      const line = new THREE.Line(fieldLine, lineMaterial);
      fieldGroup.add(line);
    }

    scene.add(fieldGroup);  // Add all field lines to the scene

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      renderer.render(scene, camera);
    };
    animate();

    // Cleanup on unmount
    return () => {
      mountRef.current?.removeChild(renderer.domElement);
    };
  }, [orientation, scene]);

  return <div ref={mountRef} style={{ width: '100%', height: '100%' }}></div>;
};

export default MagneticField2D;
