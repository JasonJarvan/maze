from flask import Flask, render_template, request, jsonify
from maze import generate_maze, solve_maze
from bokeh.embed import components
from bokeh.plotting import figure, ColumnDataSource

app = Flask(__name__)

def visualize_maze(maze, start, end):
    width, height = len(maze[0]), len(maze)
    data = {'x': [], 'y': [], 'color': []}
    for i in range(height):
        for j in range(width):
            data['x'].append(j)
            data['y'].append(height - i - 1)
            if (i, j) == start:
                data['color'].append('blue')
            elif (i, j) == end:
                data['color'].append('black')
            else:
                data['color'].append('white' if maze[i][j] == 0 else 'red')
    source = ColumnDataSource(data)
    plot = figure(plot_width=400, plot_height=400, x_range=(0, width), y_range=(0, height))
    plot.rect('x', 'y', 0.9, 0.9, source=source, color='color', line_color='black')
    return plot

@app.route('/')
def home():
    maze, start, end, shortest_path = generate_maze(10, 10)
    plot = visualize_maze(maze, start, end)
    script, div = components(plot)
    return render_template('index.html', script=script, div=div, start=start, end=end, maze=maze)

@app.route('/check_path', methods=['POST'])
def check_path():
    data = request.get_json()
    length = data.get('length')
    start = tuple(data.get('start'))
    end = tuple(data.get('end'))
    maze = data.get('maze')
    correct_length, path = solve_maze(maze, start, end)
    if length == correct_length:
        return jsonify({'result': 'correct', 'path': path})
    else:
        return jsonify({'result': 'incorrect', 'path': path})

@app.route('/hint', methods=['POST'])
def hint():
    data = request.get_json()
    start = tuple(data.get('start'))
    end = tuple(data.get('end'))
    maze = data.get('maze')
    _, path = solve_maze(maze, start, end)
    if path:
        return jsonify({'path': path})
    else:
        return jsonify({'path': 'No path found'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=50190, debug=True)
