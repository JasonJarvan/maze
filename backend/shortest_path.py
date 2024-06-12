from collections import deque

def find_shortest_path(maze, start, end):
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
