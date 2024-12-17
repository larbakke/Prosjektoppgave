import { SimulationDetails } from './interfaces';


export async function fetchSimulations() {
    try {
        const res = await fetch('http://localhost:5000/api/simulations');
        if (!res.ok) {
            throw new Error(`Error fetching simulations: ${res.statusText}`);
        }
        return await res.json();
    } catch (error) {
        console.error(error);
        return [];
    }
}

export async function runSimulation(startPosition: string, antennaCenter: string) {
    try {
        const res = await fetch('http://localhost:5000/api/simulate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                start_position: startPosition,
                antenna_center: antennaCenter,
            }),
        });

        if (!res.ok) {
            throw new Error(`Error running simulation: ${res.statusText}`);
        }

        return await res.json();
    } catch (error) {
        console.error(error);
        return null;
    }
}

export async function testBackend() {
    try {
        console.log('testBackend');
        const res = await fetch('http://localhost:5000/api/test');
        if (!res.ok) {
            throw new Error(`Error testing backend: ${res.statusText}`);
        }
        return await res.json();
    } catch (error) {
        console.error(error);
        return { error: "Unable to connect to the backend." };
    }
}

export async function fetchAvailableSimulations() {
    try {
        const res = await fetch('http://localhost:5000/api/simulation-ids');
        if (!res.ok) {
            throw new Error(`Error fetching available simulations: ${res.statusText}`);
        }
        return await res.json();
    } catch (error) {
        console.error(error);
        return [];
    }
}


export async function fetchSimulationById(simulationId: number): Promise<SimulationDetails | null> {
    try {
        const res = await fetch(`http://localhost:5000/api/simulations/${simulationId}`);
        if (!res.ok) {
            throw new Error(`Error fetching simulation ${simulationId}: ${res.statusText}`);
        }
        return await res.json() as SimulationDetails;
    } catch (error) {
        console.error(error);
        return null;
    }
}
