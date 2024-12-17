'use client';

import { useState, useEffect } from 'react';
import { fetchAvailableSimulations } from '../utils/api';

interface Simulation {
  id: number;
  description: string;
}

interface SimulationControlsProps {
  onPlay: (simulationId: number) => void;
}

const SimulationControls: React.FC<SimulationControlsProps> = ({ onPlay }) => {
  const [simulations, setSimulations] = useState<Simulation[]>([]);
  const [selectedSimulation, setSelectedSimulation] = useState<number | null>(null);

  // Fetch available simulations from the centralized API
  useEffect(() => {
    const loadSimulations = async () => {
      try {
        const data = await fetchAvailableSimulations();
        setSimulations(data);
        if (data.length > 0) {
          setSelectedSimulation(data[0].id); // Set the first simulation as default
        }
      } catch (error) {
        console.error('Failed to fetch simulations:', error);
      }
    };
    loadSimulations();
  }, []);

  const handlePlayClick = () => {
    if (selectedSimulation !== null) {
      onPlay(selectedSimulation);
    } else {
      alert('Please select a simulation first.');
    }
  };

  return (
    <div style={{ position: 'absolute', top: '20px', left: '20px', background: 'rgba(255, 255, 255, 0.8)', padding: '10px', borderRadius: '8px' }}>
      <h3>Select Simulation</h3>
      <select
        value={selectedSimulation || ''}
        onChange={(e) => setSelectedSimulation(Number(e.target.value))}
        style={{ marginBottom: '10px', width: '100%' }}
      >
        {simulations.map((sim) => (
          <option key={sim.id} value={sim.id}>
            {sim.description}
          </option>
        ))}
      </select>
      <button onClick={handlePlayClick} style={{ width: '100%', padding: '10px', background: '#007bff', color: 'white', border: 'none', borderRadius: '4px' }}>
        Play
      </button>
    </div>
  );
};

export default SimulationControls;
