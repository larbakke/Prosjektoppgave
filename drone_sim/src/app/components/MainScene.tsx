'use client';

import { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import CameraControls from './CameraControls';
import Slope from './Slope';
import Drone from './Drone';
import AvalancheBeacon from './AvalancheBeacon';

interface SceneConfig {
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

const MainScene = () => {
  const mountRef = useRef<HTMLDivElement>(null);
  const [camera, setCamera] = useState<THREE.PerspectiveCamera | null>(null);
  const [renderer, setRenderer] = useState<THREE.WebGLRenderer | null>(null);
  const [scene] = useState(new THREE.Scene());
  const [config, setConfig] = useState<SceneConfig | null>(null);

  useEffect(() => {
    // Fetch configuration from backend
    const fetchConfig = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/config'); // Adjust backend URL if needed
        const data = await response.json();
        setConfig(data);
      } catch (error) {
        console.error('Failed to fetch scene config:', error);
      }
    };
    fetchConfig();
  }, []);

  useEffect(() => {
    if (!config) return; // Wait until config is loaded

    const width = mountRef.current?.clientWidth || window.innerWidth;
    const height = mountRef.current?.clientHeight || window.innerHeight;

    // Create and position the camera
    const newCamera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    newCamera.position.set(...config.camera.position);
    newCamera.lookAt(...config.camera.lookAt);
    setCamera(newCamera);

    // Create the renderer
    const newRenderer = new THREE.WebGLRenderer();
    newRenderer.setSize(width, height);
    mountRef.current?.appendChild(newRenderer.domElement);
    setRenderer(newRenderer);

    // Add light to the scene
    const light = new THREE.DirectionalLight(config.light.color, config.light.intensity);
    light.position.set(...config.light.position).normalize();
    scene.add(light);

    // Add a ground plane
    const groundGeometry = new THREE.PlaneGeometry(config.ground.size, config.ground.size);
    const groundMaterial = new THREE.MeshStandardMaterial({ color: config.ground.color, side: THREE.DoubleSide });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2; // Make it flat
    scene.add(ground);

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
  }, [config, scene]);

  if (!config) return <div>Loading...</div>; // Show a loading indicator while fetching config

  return (
    <div ref={mountRef} style={{ width: '100vw', height: '100vh' }}>
      {camera && renderer && (
        <>
          <CameraControls camera={camera} renderer={renderer} />
          <Slope {...config.slope} scene={scene} />
          <Drone scene={scene} startPosition={config.drone.startPosition} />
          <AvalancheBeacon scene={scene} depth={config.beacon.depth} />
        </>
      )}
    </div>
  );
};

export default MainScene;
