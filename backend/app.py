from flask import Flask, render_template, request, jsonify
from maze import generate_maze, solve_maze, get_path_length
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import Rect, ColumnDataSource

app = Flask(__name__)


@app.route('/')
def index():
    maze, start, end = generate_maze(10, 10)
    script, div = render_maze(maze, start, end)
    return render_template('index.html', script=script, div=div, maze=maze, start=start, end=end)


@app.route('/check_path', methods=['POST'])
def check_path():
    data = request.get_json()
    maze = data['maze']
    start = tuple(data['start'])  # 转换为元组
    end = tuple(data['end'])  # 转换为元组
    user_length = int(data['length'])

    solution, path_length = solve_maze(maze, start, end)
    if solution:
        correct = (user_length == path_length)
        message = "Correct!" if correct else f"Incorrect! The correct length is {path_length}."
    else:
        correct = False
        message = "No path exists."

    return jsonify(correct=correct, message=message)


@app.route('/get_hint', methods=['POST'])
def get_hint():
    data = request.get_json()
    maze = data['maze']
    start = tuple(data['start'])  # 转换为元组
    end = tuple(data['end'])  # 转换为元组

    solution, path_length, directions = solve_maze(maze, start, end, hint=True)
    if solution:
        script, div = render_maze(maze, start, end, directions=directions)
        hint = ''.join(directions)
    else:
        script, div = render_maze(maze, start, end)
        hint = "No path exists."

    return jsonify(script=script, div=div, hint=hint)


def render_maze(maze, start, end, directions=None):
    plot = figure(x_range=(0, 10), y_range=(0, 10), plot_width=400, plot_height=400)
    plot.rect(x='x', y='y', width=1, height=1, source=ColumnDataSource(data=dict(x=[], y=[])), fill_color='red')

    # Draw maze
    for i, row in enumerate(maze):
        for j, val in enumerate(row):
            if val == 1:
                plot.rect(x=[j + 0.5], y=[9.5 - i], width=1, height=1, color="red")

    # Draw start and end
    plot.rect(x=[start[1] + 0.5], y=[9.5 - start[0]], width=1, height=1, color="blue")
    plot.rect(x=[end[1] + 0.5], y=[9.5 - end[0]], width=1, height=1, color="black")

    # Draw path if hint is given
    if directions:
        x, y = start
        for move in directions:
            if move == 'D':
                y += 1
            elif move == 'U':
                y -= 1
            elif move == 'L':
                x -= 1
            elif move == 'R':
                x += 1
            plot.rect(x=[x + 0.5], y=[9.5 - y], width=1, height=1, color="green")

    script, div = components(plot)
    return script, div


if __name__ == '__main__':
    app.run(port=50190, debug=True)
