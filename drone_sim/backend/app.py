from flask import Flask, request, jsonify
from flask_cors import CORS
from db import db
from models import SimulationResult

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

@app.route('/api/simulations', methods=['GET'])
def get_simulations():
    """Fetch all simulation results."""
    results = SimulationResult.query.all()
    return jsonify([result.to_dict() for result in results])

@app.route('/api/simulate', methods=['POST'])
def simulate():
    """Simulate drone and store results."""
    data = request.json
    start_position = data.get('start_position')
    antenna_center = data.get('antenna_center')

    final_position = antenna_center  # Simplistic placeholder logic
    steps = 10  # Placeholder for the number of steps

    result = SimulationResult(
        start_position=start_position,
        antenna_center=antenna_center,
        final_position=final_position,
        steps=steps
    )
    db.session.add(result)
    db.session.commit()

    return jsonify(result.to_dict()), 201

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'message': 'Hello, World!'})

@app.route('/api/config', methods=['GET'])
def get_scene_config():
    """Returns the configuration for the 3D scene."""
    return jsonify({
        "camera": {
            "position": [0, 100, 300],
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
            "startPosition": [0, 100, 0],
        },
        "beacon": {
            "depth": 1
        }
    })


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



