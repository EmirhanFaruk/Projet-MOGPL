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

    for i in range(1, advance_num + 1):
        i = state[0] + (i * di)
        j = state[1] + (i * dj)
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

def BFS(grid, start_state, goal_state):
    """
    Performs a breadth-first search on the grid to find a path from the start position and orientation to the goal position.
    Returns a list of actions to reach the goal, or None if no path is found.
    """
    # Initialize queue(file, First In First Out), parents dictionnary and visited set
    start_i, start_j, start_o = start_state
    queue = [start_state]
    parents = {(start_i, start_j, start_o): None}
    visited = set()
    visited.add((start_i, start_j, start_o))

    while queue: # While queue is not empty
        current_state = queue.pop(0)

        # Check if we reached the goal
        if current_state[:2] == goal_state:
            path = [] # Path to return
            last_state = current_state
            while parents[last_state] is not None: # Build the path from parents dictionnary
                last_state, last_action = parents[last_state]
                path.append(last_action)
            return path[::-1]  # Return reversed path

        # Generate possible actions (move forward(1, 2 or 3), turn left, turn right)
        for action in ["a3", "a2", "a1", "D", "G"]:
            new_state = perform_action(current_state, action, grid)
            # If the new state is valid and not visited, add it to the queue
            if new_state and (new_state[0], new_state[1], new_state[2]) not in visited:
                visited.add((new_state[0], new_state[1], new_state[2])) # Add the state to the visited
                parents[new_state] = (current_state, action) # Add the state to parents
                queue.append(new_state)

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