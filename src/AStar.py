import numpy as np

advance_action = {"a1": 1, "a2": 2, "a3": 3}
advance_directions = {
    0: (-1, 0),  # North
    1: (0, 1),   # East
    2: (1, 0),   # South
    3: (0, -1)   # West
}

wall_collision_directions = [
    (-1, 0),  # North
    (0, 0),   # Center
    (-1, -1), # North-West
    (0, -1)   # West
]


def valid_position(i, j, grid):
    """
    Check if the coordinates are valid(not in a wall and inside the grid).
    """
    if grid is not None:
        for di, dj in wall_collision_directions:
            ni, nj = i + di, j + dj
            if not (0 <= ni < len(grid) and 0 <= nj < len(grid[0])):
                return False  # outside grid
            if grid[ni][nj] == 1:
                return False  # wall
        return True
    return False


def advance(state, action, grid):
    """
    Advances the state forward by the specified action amount if the path is valid. Returns the new state.
    """
    advance_num = advance_action[action]
    di, dj = advance_directions[state[2]]

    for index in range(1, advance_num + 1):
        i = state[0] + (index * di)
        j = state[1] + (index * dj)
        if not valid_position(i, j, grid):
            return None
    
    new_i = state[0] + (advance_num * di)
    new_j = state[1] + (advance_num * dj)
    return (new_i, new_j, state[2])

def turn(state, action):
    """
    Turns the state left or right based on the action. Returns the new state.
    """
    new_o = (state[2] + (1 if action == "D" else -1)) % 4
    return (state[0], state[1], new_o)

def perform_action(current_state, action, grid):
    """
    Performs the given action on the current state and returns the resulting new state. None if the action is invalid.
    """
    if action in ["D", "G"]:
        return turn(current_state, action)
    elif action in ["a1", "a2", "a3"]:
        return advance(current_state, action, grid)
    return None

def heuristic(pos, goal):
    """Manhattan distance as heuristic."""
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

def A_star(grid, start_state, goal_state):
    """
    Performs a A* search on the grid to find a path from the start position and orientation to the goal position.
    Returns a list of actions to reach the goal, or None if no path is found.
    """
    open_list = [(start_state, 0, heuristic(start_state, goal_state))]  # (state, g, f)
    parents = {start_state: None}
    g_score = {start_state: 0}
    visited = set()

    while open_list:
        # Sort open_list by f (ascending) and pop first element
        open_list.sort(key=lambda x: x[2])
        current, g, f = open_list.pop(0)

        if current[:2] == goal_state:
            # Reconstruct path
            path = []
            last = current
            while parents[last] is not None:
                last, action = parents[last]
                path.append(action)
            return path[::-1]

        visited.add(current)

        for action in ["a3", "a2", "a1", "D", "G"]:
            neighbor = perform_action(current, action, grid)
            if neighbor and neighbor not in visited:
                tentative_g = g + 1  # Each action costs 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal_state)
                    open_list.append((neighbor, tentative_g, f_score))
                    parents[neighbor] = (current, action)

    return None  # No path found



def visualize_path(grid, start_state, goal_state, path):
    """
    Visualizes the path taken on the grid from start to goal.
    """
    visual_grid = np.array(grid, dtype=str)
    visual_grid[visual_grid == '0'] = '.'  # Free space
    visual_grid[visual_grid == '1'] = '#'  # Wall

    i, j, o = start_state
    visual_grid[i][j] = 'S'  # Start

    for action in path:
        new_state = perform_action((i, j, o), action, grid)
        if new_state:
            i, j, o = new_state
            visual_grid[i][j] = '*'  # Path

    gi, gj = goal_state
    visual_grid[gi][gj] = 'G'  # Goal

    i, j, o = start_state
    visual_grid[i][j] = 'S'  # Start

    for row in visual_grid:
        print(" ".join(row))