import exp from "constants";

export async function fetchSimulations() {
    const res = await fetch('http://localhost:5000/api/simulations');
    return await res.json();
}

export async function runSimulation(startPosition: string, antennaCenter: string) {
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
    return await res.json();
}


export async function testBackend() {
    console.log('testBackend');
    const res = await fetch('http://localhost:5000/api/test');
    return await res.json();
}