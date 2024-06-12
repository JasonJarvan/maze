from flask import Flask, jsonify, request
from flask_cors import CORS
from bokeh.plotting import figure
from bokeh.embed import json_item
from maze import generate_maze
from shortest_path import find_shortest_path

app = Flask(__name__)
CORS(app)


@app.route('/generate_maze', methods=['GET'])
def generate_maze_route():
    maze, start, end, path_length = generate_maze(10, 10)
    plot = figure(width=400, height=400)
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            color = "red" if cell == 1 else "white"
            if (i, j) == start:
                color = "blue"
            elif (i, j) == end:
                color = "black"
            plot.rect(x=j, y=i, width=1, height=1, color=color)
    item = json_item(plot)
    return jsonify({
        'plot': item,
        'start': start,
        'end': end,
        'path_length': path_length
    })


@app.route('/solve_maze', methods=['POST'])
def solve_maze_route():
    data = request.json
    maze = data['maze']
    start = tuple(data['start'])
    end = tuple(data['end'])
    user_path_length = data['path_length']
    shortest_path = find_shortest_path(maze, start, end)

    if shortest_path is None:
        return jsonify({'message': 'No path exists.', 'correct': False})

    correct_length = len(shortest_path)

    if correct_length == user_path_length:
        return jsonify({'message': 'Correct!', 'correct': True})
    else:
        return jsonify({'message': f'Incorrect. The correct path length is {correct_length}.', 'correct': False})


@app.route('/get_hint', methods=['POST'])
def get_hint_route():
    data = request.json
    maze = data['maze']
    start = tuple(data['start'])
    end = tuple(data['end'])
    shortest_path = find_shortest_path(maze, start, end)

    if shortest_path is None:
        return jsonify({'message': 'No path exists.', 'path': None})

    directions = []
    for i in range(1, len(shortest_path)):
        dx = shortest_path[i][0] - shortest_path[i - 1][0]
        dy = shortest_path[i][1] - shortest_path[i - 1][1]
        if dx == 1:
            directions.append('D')
        elif dx == -1:
            directions.append('U')
        elif dy == 1:
            directions.append('R')
        elif dy == -1:
            directions.append('L')

    return jsonify({'path': ''.join(directions)})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=50190, debug=True)
