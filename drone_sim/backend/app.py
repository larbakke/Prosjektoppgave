from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from db import *

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simulation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

@app.route('/api/simulations', methods=['GET'])
def get_simulations():
    """
    Fetch all simulation metadata (ID and description).
    """
    try:
        conn = db.engine.connect()
        simulations = conn.execute("SELECT id, description FROM simulations").fetchall()
        return jsonify([{"id": sim[0], "description": sim[1]} for sim in simulations]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/simulations/<int:simulation_id>', methods=['GET'])
def get_simulation_details(simulation_id):
    """
    Fetch full details of a specific simulation, including slope, antenna, path, and measurements.
    """
    try:
        simulation_data = get_simulation_full_details(simulation_id)
        if "error" in simulation_data:
            return jsonify(simulation_data), 404
        return jsonify(simulation_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/simulate', methods=['POST'])
def simulate():
    """
    Simulate a drone and store the results.
    Expects:
    {
        "description": "Simulation description",
        "start_position": {...},
        "antenna_center": {...},
        "steps": 10
    }
    """
    try:
        data = request.json
        description = data.get('description')
        start_position = data.get('start_position')
        antenna_center = data.get('antenna_center')
        steps = data.get('steps', 10)

        if not description or not start_position or not antenna_center:
            return jsonify({"error": "Missing required fields"}), 400

        conn = db.engine.connect()
        conn.execute("""
            INSERT INTO simulations (description) VALUES (?)
        """, (description,))
        simulation_id = conn.execute("SELECT last_insert_rowid()").scalar()

        conn.execute("""
            INSERT INTO simulation_results (simulation_id, start_position, antenna_center, final_position, steps)
            VALUES (?, ?, ?, ?, ?)
        """, (
            simulation_id,
            str(start_position),
            str(antenna_center),
            str(antenna_center),  # Simplistic final position placeholder
            steps
        ))
        conn.close()

        return jsonify({"message": "Simulation created", "simulation_id": simulation_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/test', methods=['GET'])
def test():
    """
    Test API endpoint.
    """
    return jsonify({'message': 'Hello, World!'}), 200

@app.route('/api/config', methods=['GET'])
def get_scene_config():
    """
    Returns the configuration for the 3D scene.
    """
    return jsonify({
        "camera": {
            "position": [200, 100, 300],
            "lookAt": [0, 50, 100]
        },
        "slope": {
            "width": 100,
            "height": 200,
            "angle": -90 + 35,  # 35 degrees
            "color": 0x8B4513  # Brown
        },
        "light": {
            "position": [50, 50, 50],
            "color": 0xffffff,
            "intensity": 1
        },
        "ground": {
            "size": 500,
            "color": 0x808080
        },
        "drone": {
            "startPosition": [40, 10, 175],
        },
        "beacon": {
            "depth": 1
        }
    }), 200

@app.route('/api/simulation-ids', methods=['GET'])
def get_simulation_ids():
    """
    API endpoint to fetch all available simulation IDs and descriptions.
    """
    try:
        simulations = fetch_simulation_ids_and_descriptions()
        return jsonify(simulations), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        initialize_database()  # Ensures tables are created
    app.run(debug=True)
