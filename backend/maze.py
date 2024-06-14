import random
from collections import deque

def generate_maze(width, height):
    maze = [[random.choice([0, 1]) for _ in range(width)] for _ in range(height)]
    start = (random.randint(0, height-1), random.randint(0, width-1))
    end = (random.randint(0, height-1), random.randint(0, width-1))
    while start == end or maze[start[0]][start[1]] == 1 or maze[end[0]][end[1]] == 1:
        start = (random.randint(0, height-1), random.randint(0, width-1))
        end = (random.randint(0, height-1), random.randint(0, width-1))
    shortest_path = bfs(maze, start, end)
    return maze, start, end, shortest_path

def bfs(maze, start, end):
    queue = deque([(start, 0, "")])
    visited = set()
    directions = {'D': (1, 0), 'U': (-1, 0), 'R': (0, 1), 'L': (0, -1)}
    while queue:
        (x, y), length, path = queue.popleft()
        if (x, y) == end:
            return length, path
        for direction, (dx, dy) in directions.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), length + 1, path + direction))
    return None, None

def solve_maze(maze, start, end):
    correct_length, path = bfs(maze, start, end)
    return correct_length, path
