import numpy as np
from random import randint

def is_valid_wall_position(grid, i, j):
    """
    Returns true if (i, j) location is 
    """
    rows, cols = grid.shape
    if j >= cols - 1 or j < 0 or i >= rows - 1 or i < 0:
        return False
    """
    if np.any(grid[y:y+2, x:x+2] == 1):
        return False
    """
    return True


wall_collision_directions = [
    (-1, 0),  # North
    (0, 0),   # Center
    (-1, -1),   # North-West
    (0, -1)   # West
]


def valid_position(i, j, grid):
    """
    Check if the coordinates are valid(not in a wall and inside the grid).
    """
    if grid is not None:
        if 0 <= j < len(grid[0]) and 0 <= i < len(grid):
            in_a_wall = any(grid[i + di][j + dj] == 1 for di, dj in wall_collision_directions)
            return not in_a_wall
    return False


def get_start_goal_positions(M, N, grid, min_distance=0):
    """
    Selects random start and goal positions on the grid ensuring they are not walls and meet the minimum distance requirement.
    """
    if min_distance == 0:
        min_distance = max(M, N) // 4
    
    start_i = randint(1, M - 1)
    start_j = randint(1, N - 1)
    while (not valid_position(start_i, start_j, grid)):
        start_i = randint(1, M - 1)
        start_j = randint(1, N - 1)
    start_o = randint(0, 3)

    goal_i = randint(1, M - 1)
    goal_j = randint(1, N - 1)
    while abs(goal_i - start_i) < min_distance or (not valid_position(goal_i, goal_j, grid)):
        goal_i = randint(1, M - 1)
        goal_j = randint(1, N - 1)

    return (start_i, start_j, start_o), (goal_i, goal_j)

def generate_grid(M=10, N=10, wall_num=10):
    """
    Generates a grid of given size with walls placed randomly based on wall_density.
    1 represents free space, and 0 represents a wall.
    """
    grid = np.zeros((M, N), dtype=int)
    
    for _ in range(wall_num):
        wall_pos = np.random.randint(0, M * N - 1)
        i = wall_pos // N
        j = wall_pos % N
        while not is_valid_wall_position(grid, i, j):
            wall_pos = np.random.randint(0, M * N - 1)
            i = wall_pos // N
            j = wall_pos % N
        grid[i][j] = 1
        
    
    start_pos, goal_pos = get_start_goal_positions(M, N, grid)

    return grid, start_pos, goal_pos