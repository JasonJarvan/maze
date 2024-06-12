import random

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import CDN


def generate_maze(width, height):
    maze = [[random.choice([0, 1]) for _ in range(width)] for _ in range(height)]
    start = (random.randint(0, height - 1), random.randint(0, width - 1))
    end = (random.randint(0, height - 1), random.randint(0, width - 1))
    maze[start[0]][start[1]] = 0
    maze[end[0]][end[1]] = 0
    path_length = find_shortest_path_length(maze, start, end)
    return maze, start, end, path_length

def visualize_maze(maze, start, end):
    plot = figure(width=400, height=400)
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            color = "red" if cell == 1 else "white"
            if (i, j) == start:
                color = "blue"
            elif (i, j) == end:
                color = "black"
            plot.rect(x=j, y=i, width=1, height=1, color=color)
    script, div = components(plot, CDN)
    return script, div

def find_shortest_path_length(maze, start, end):
    path = find_shortest_path(maze, start, end)
    return len(path) if path else -1

def find_shortest_path(maze, start, end):
    from collections import deque

    queue = deque([start])
    visited = set()
    visited.add(start)
    parent = {start: None}

    while queue:
        current = queue.popleft()
        if current == end:
            break
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if (0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]) and
                    neighbor not in visited and maze[neighbor[0]][neighbor[1]] == 0):
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    path = []
    if end in visited:
        step = end
        while step is not None:
            path.append(step)
            step = parent[step]
        path.reverse()

    return path
