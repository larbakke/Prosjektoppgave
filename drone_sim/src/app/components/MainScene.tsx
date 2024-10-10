'use client';

import { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import CameraControls from './CameraControls';
import Slope from './Slope';
import Drone from './Drone';
import AvalancheBeacon from './AvalancheBeacon';

const MainScene = () => {
  const mountRef = useRef<HTMLDivElement>(null);
  const [camera, setCamera] = useState<THREE.PerspectiveCamera | null>(null);
  const [renderer, setRenderer] = useState<THREE.WebGLRenderer | null>(null);
  const [scene] = useState(new THREE.Scene());  // Create the Three.js scene

  // Slope properties
  const slopeProps = {
    width: 100,
    height: 200,
    angle: -90+35,  // 35 degree slope
    color: 0x8B4513,  // Brown
    scene,  // Pass the scene object to Slope
  };

  useEffect(() => {
    const width = mountRef.current?.clientWidth || window.innerWidth;
    const height = mountRef.current?.clientHeight || window.innerHeight;

    // Create a camera
    const newCamera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    newCamera.position.set(0, 100, 300);  // Position camera above and looking toward slope
    newCamera.lookAt(0, 50, 100);
    setCamera(newCamera);

    // Create the renderer
    const newRenderer = new THREE.WebGLRenderer();
    newRenderer.setSize(width, height);
    mountRef.current?.appendChild(newRenderer.domElement);
    setRenderer(newRenderer);

    // Add a light
    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(50, 50, 50).normalize();
    scene.add(light);  // Add light to scene

    // Add a ground plane (flat reference)
    const groundGeometry = new THREE.PlaneGeometry(500, 500);
    const groundMaterial = new THREE.MeshStandardMaterial({ color: 0x808080, side: THREE.DoubleSide });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;  // Make it flat
    scene.add(ground);  // Add ground to scene

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      newRenderer.render(scene, newCamera);
    };
    animate();

    // Cleanup on unmount
    return () => {
      mountRef.current?.removeChild(newRenderer.domElement);
    };
  }, [scene]);

  return (
    <div ref={mountRef} style={{ width: '100vw', height: '100vh' }}>
      {camera && renderer && (
        <>
          <CameraControls camera={camera} renderer={renderer} />
          <Slope {...slopeProps} />  {/* Pass scene and slope properties */}
          <Drone scene={scene} />  {/* Pass scene to Drone */}
          <AvalancheBeacon scene={scene} depth={1} />  {/* Pass scene and depth to Beacon */}
        </>
      )}
    </div>
  );
};

export default MainScene;
