import random
from bokeh.plotting import figure
from bokeh.io import output_file, save
import numpy as np


class Maze:
    def __init__(self, size=10):
        self.size = size
        self.grid = np.zeros((size, size), dtype=bool)
        self.start = (0, 0)
        self.end = (size - 1, size - 1)
        self.generate_maze()

    def generate_maze(self):
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i, j] = random.choice([True, False])
        self.grid[self.start] = False
        self.grid[self.end] = False

    def solve_maze(self):
        # Use DFS to find the path from start to end
        stack = [(self.start, "")]
        visited = set()
        directions = [(1, 0, "D"), (0, 1, "R"), (-1, 0, "U"), (0, -1, "L")]

        while stack:
            (current, path) = stack.pop()
            if current in visited:
                continue
            visited.add(current)

            if current == self.end:
                return path

            for d in directions:
                next_cell = (current[0] + d[0], current[1] + d[1])
                if (0 <= next_cell[0] < self.size and 0 <= next_cell[1] < self.size and not self.grid[next_cell]):
                    stack.append((next_cell, path + d[2]))

        return None

    def render_maze(self):
        p = figure(x_range=(0, self.size), y_range=(0, self.size), plot_width=400, plot_height=400)
        p.grid.visible = False
        p.axis.visible = False

        for i in range(self.size):
            for j in range(self.size):
                color = "red" if self.grid[i, j] else "white"
                p.rect(x=[j + 0.5], y=[self.size - i - 0.5], width=1, height=1, color=color)

        p.rect(x=[self.start[1] + 0.5], y=[self.size - self.start[0] - 0.5], width=1, height=1, color="blue")
        p.rect(x=[self.end[1] + 0.5], y=[self.size - self.end[0] - 0.5], width=1, height=1, color="black")

        return p

    def save_maze(self):
        p = self.render_maze()
        output_file("/mnt/data/maze.html")
        save(p)


# Example usage
maze = Maze()
maze.save_maze()
