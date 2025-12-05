import numpy as np
from random import randint

def is_valid_wall_position(grid, x, y):
    rows, cols = grid.shape
    if x >= cols - 1 or x < 0 or y >= rows - 1 or y < 0:
        return False
    if np.any(grid[y:y+2, x:x+2] == 1):
        return False
    return True

def get_start_goal_positions(size, grid, min_distance=0):
    """
    Selects random start and goal positions on the grid ensuring they are not walls and meet the minimum distance requirement.
    """
    if min_distance == 0:
        min_distance = size // 4
    
    start_x = randint(0, size - 1)
    start_y = randint(0, size - 1)
    while grid[start_y][start_x] == 1:
        start_x = randint(0, size - 1)
        start_y = randint(0, size - 1)
    start_o = randint(0, 3)

    goal_x = randint(0, size - 1)
    goal_y = randint(0, size - 1)
    while abs(goal_y - start_y) < min_distance or grid[goal_y][goal_x] == 1:
        goal_x = randint(0, size - 1)
        goal_y = randint(0, size - 1)

    return (start_x, start_y, start_o), (goal_x, goal_y)

def generate_grid(size=10, wall_num=10):
    """
    Generates a grid of given size with walls placed randomly based on wall_density.
    1 represents free space, and 0 represents a wall.
    """
    grid = np.zeros((size, size), dtype=int)
    
    for _ in range(wall_num):
        wall_pos = np.random.randint(0, size * size - 1)
        x = wall_pos % size
        y = wall_pos // size
        while not is_valid_wall_position(grid, x, y):
            wall_pos = np.random.randint(0, size * size - 1)
            x = wall_pos % size
            y = wall_pos // size
        grid[y][x] = 1
        
    
    start_pos, goal_pos = get_start_goal_positions(size, grid)

    return grid, start_pos, goal_pos