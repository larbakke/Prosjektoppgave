'use client';

import * as THREE from 'three';
import { useEffect, useRef, forwardRef, useImperativeHandle } from 'react';
import { testBackend } from '../utils/api';

interface DroneProps {
  scene: THREE.Scene;
  startPosition: [number, number, number];
}

const Drone = forwardRef(({ scene, startPosition }: DroneProps, ref) => {
  const droneRef = useRef<THREE.Mesh | null>(null);
  const speed = 1; // Movement speed
  const rotationSpeed = 0.02; // Rotation speed

  const keyState: { [key: string]: boolean } = {
    ArrowUp: false,
    ArrowDown: false,
    ArrowLeft: false,
    ArrowRight: false,
    w: false,
    a: false,
    s: false,
    d: false,
    t: false,
  };

  useEffect(() => {
    const droneGeometry = new THREE.BoxGeometry(5, 5, 5);
    const droneMaterial = new THREE.MeshStandardMaterial({ color: 0x0000ff });
    const droneMesh = new THREE.Mesh(droneGeometry, droneMaterial);

    droneMesh.position.set(...startPosition);
    droneMesh.rotation.set(0, 0, 0);

    scene.add(droneMesh);
    droneRef.current = droneMesh;

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key in keyState) {
        keyState[event.key] = true;
      }
    };

    const handleKeyUp = (event: KeyboardEvent) => {
      if (event.key in keyState) {
        keyState[event.key] = false;
        console.log('Position:', droneRef.current?.position);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    const animateDrone = async () => {
      if (!droneRef.current) return;

      const position = droneRef.current.position;
      const rotation = droneRef.current.rotation;

      if (keyState.ArrowUp) position.y += speed;
      if (keyState.ArrowDown) position.y -= speed;

      if (keyState.ArrowLeft) rotation.y += rotationSpeed;
      if (keyState.ArrowRight) rotation.y -= rotationSpeed;

      if (keyState.w) {
        position.x -= speed * Math.sin(rotation.y);
        position.z -= speed * Math.cos(rotation.y);
      }
      if (keyState.s) {
        position.x += speed * Math.sin(rotation.y);
        position.z += speed * Math.cos(rotation.y);
      }

      if (keyState.a) {
        position.x -= speed * Math.cos(rotation.y);
        position.z += speed * Math.sin(rotation.y);
      }
      if (keyState.d) {
        position.x += speed * Math.cos(rotation.y);
        position.z -= speed * Math.sin(rotation.y);
      }

      if (keyState.t) {
        console.log('Testing backend...');
        const res = await testBackend();
        console.log(res);
      }
      requestAnimationFrame(animateDrone);
    };

    animateDrone();

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
      if (droneRef.current) scene.remove(droneRef.current);
    };
  }, [scene, startPosition]);

  // Expose the moveDrone function and the drone's THREE.Mesh via ref
  useImperativeHandle(ref, () => ({
    moveDrone: (targetPosition: [number, number, number], duration: number) => {
      if (!droneRef.current) {
        console.error('Drone mesh is not initialized!');
        return;
      }

      const start = droneRef.current.position.clone();
      const target = new THREE.Vector3(...targetPosition);
      const startTime = performance.now();

      const animate = (time: number) => {
        const elapsed = time - startTime;
        const t = Math.min(elapsed / duration, 1); // Clamp t between 0 and 1

        // Interpolate position
        droneRef.current?.position.lerpVectors(start, target, t);

        if (t < 1) {
          requestAnimationFrame(animate);
        } else {
          console.log('Drone reached target position:', targetPosition);
        }
      };

      requestAnimationFrame(animate);
    },
    get current() {
      return droneRef.current;
    },
  }));

  return null;
});

export default Drone;
