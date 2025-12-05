import numpy as np
from random import randint

def is_valid_wall_position(grid, x, y):
    rows, cols = grid.shape
    if x >= cols - 1 or x < 0 or y >= rows - 1 or y < 0:
        return False
    if np.any(grid[y:y+2, x:x+2] == 1):
        return False
    return True


wall_collision_directions = [
    (0, -1),  # North
    (0, 0),   # Center
    (-1, -1),   # South
    (-1, 0)   # West
]


def valid_position(x, y, grid):
    """
    Check if the coordinates are valid(not in a wall and inside the grid).
    """
    if grid is not None:
        if 0 <= x < len(grid[0]) - 1 and 0 <= y < len(grid) - 1:
            in_a_wall = any(grid[y + dy][x + dx] == 1 for dx, dy in wall_collision_directions)
            return not in_a_wall
    return False


def get_start_goal_positions(M, N, grid, min_distance=0):
    """
    Selects random start and goal positions on the grid ensuring they are not walls and meet the minimum distance requirement.
    """
    if min_distance == 0:
        min_distance = max(M, N) // 4
    
    start_x = randint(0, N - 1)
    start_y = randint(0, M - 1)
    while (not valid_position(start_x, start_y, grid)):
        start_x = randint(0, N - 1)
        start_y = randint(0, M - 1)
    start_o = randint(0, 3)

    goal_x = randint(0, N - 1)
    goal_y = randint(0, M - 1)
    while abs(goal_y - start_y) < min_distance or (not valid_position(goal_x, goal_y, grid)):
        goal_x = randint(0, N - 1)
        goal_y = randint(0, M - 1)

    return (start_x, start_y, start_o), (goal_x, goal_y)

def generate_grid(M=10, N=10, wall_num=10):
    """
    Generates a grid of given size with walls placed randomly based on wall_density.
    1 represents free space, and 0 represents a wall.
    """
    grid = np.zeros((M, N), dtype=int)
    
    for _ in range(wall_num):
        wall_pos = np.random.randint(0, M * N - 1)
        x = wall_pos % N
        y = wall_pos // N
        while not is_valid_wall_position(grid, x, y):
            wall_pos = np.random.randint(0, M * N - 1)
            x = wall_pos % N
            y = wall_pos // N
        grid[y][x] = 1
        
    
    start_pos, goal_pos = get_start_goal_positions(M, N, grid)

    return grid, start_pos, goal_pos