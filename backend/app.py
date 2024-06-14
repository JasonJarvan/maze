from flask import Flask, jsonify, request
from maze import Maze

app = Flask(__name__)

@app.route('/generate', methods=['GET'])
def generate_maze():
    maze = Maze()
    maze.save_maze()
    solution = maze.solve_maze()
    return jsonify({"path": solution, "length": len(solution) if solution else 0})

@app.route('/validate', methods=['POST'])
def validate_path():
    data = request.json
    user_length = data.get('length')
    maze = Maze()
    solution = maze.solve_maze()
    if user_length == len(solution):
        return jsonify({"result": "correct"})
    else:
        return jsonify({"result": "incorrect"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=50190, debug=True)
