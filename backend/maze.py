import random
from collections import deque

def generate_maze(width, height):
    maze = [[1 if random.random() < 0.3 else 0 for _ in range(width)] for _ in range(height)]
    start = (0, 0)
    end = (height - 1, width - 1)
    maze[start[0]][start[1]] = 0
    maze[end[0]][end[1]] = 0
    return maze, start, end


def solve_maze(maze, start, end, hint=False):
    directions = ['U', 'D', 'L', 'R']
    dir_vectors = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

    # 将start和end从列表转换为元组
    start = tuple(start)
    end = tuple(end)

    queue = deque([(start, [])])
    visited = set()
    visited.add(start)

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            if hint:
                return True, len(path), path
            else:
                return True, len(path)

        for dir in directions:
            dx, dy = dir_vectors[dir]
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0 and (nx, ny) not in visited:
                queue.append(((nx, ny), path + [dir]))
                visited.add((nx, ny))

    if hint:
        return False, 0, []
    else:
        return False, 0

def get_path_length(maze, start, end):
    solution, path_length = solve_maze(maze, start, end)
    return path_length
