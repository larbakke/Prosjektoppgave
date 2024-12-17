Prosjektoppgave med TS og Python backend


The simulations consists of 2 parts:
PoseEstimation:
    contains python scripts of triangulation with angle of arival, and an experimental angle rate algorithm found in 

drone_sim is a very basic environment built on a a Next.js framwork with TypeScript and a Python backend. To run the environment:
make sure to have node, npm and python installed. 

run the backend:

    head into the backend:
    cd drone_sim/backend

    install dependecies:
    pip install -r requirements.txt

    run a simulation:
    python ./main.py

    run the backend server:
    python ./app.py

run the headder on localhost (might be required to run from terminal as admin):

    Head into drone_sim:
    cd drone_sim

    install dep:
    npm install

    run the frontend:
    npm run dev
