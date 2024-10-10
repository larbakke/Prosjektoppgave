'use client';  // Ensure this is a Client Component

import { useEffect, useRef } from 'react';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import * as THREE from 'three';

const CameraControls = ({ camera, renderer }) => {
  const controlsRef = useRef<any>(null);

  useEffect(() => {
    if (!camera || !renderer) return;

    // Initialize controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controlsRef.current = controls;

    // Optional: Set control parameters
    controls.enableDamping = true;  // Smooth camera motion
    controls.dampingFactor = 0.05;  // Damping factor (optional)
    controls.screenSpacePanning = false;  // Prevent panning in screen space (optional)
    controls.minDistance = 50;  // Minimum zoom distance
    controls.maxDistance = 500;  // Maximum zoom distance
    controls.maxPolarAngle = Math.PI / 2;  // Limit vertical movement (optional)

    // Cleanup on unmount
    return () => controls.dispose();
  }, [camera, renderer]);

  return null;  // This component doesn't render anything visible
};

export default CameraControls;
