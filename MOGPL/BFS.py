import numpy as np

advance_action = {"a1": 1, "a2": 2, "a3": 3}
advance_directions = {
    0: (0, -1),  # North
    1: (1, 0),   # East
    2: (0, 1),   # South
    3: (-1, 0)   # West
}

wall_collision_directions = [
    (0, -1),  # North
    (0, 0),   # Center
    (-1, -1), # North-West
    (-1, 0)   # West
]


def valid_position(x, y, grid):
    """
    Check if the coordinates are valid(not in a wall and inside the grid).
    """
    if grid is not None:
        for dx, dy in wall_collision_directions:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < len(grid[0]) and 0 <= ny < len(grid)):
                return False  # outside grid
            if grid[ny][nx] == 1:
                return False  # wall
        return True
    return False


def advance(state, action, grid):
    """
    Advances the state forward by the specified action amount if the path is valid. Returns the new state.
    """
    advance_num = advance_action[action]
    dx, dy = advance_directions[state[2]]

    for i in range(1, advance_num + 1):
        x = state[0] + (i * dx)
        y = state[1] + (i * dy)
        if not valid_position(x, y, grid):
            return None
    
    new_x = state[0] + (advance_num * dx)
    new_y = state[1] + (advance_num * dy)
    return (new_x, new_y, state[2])

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
    start_x, start_y, start_o = start_state
    queue = [start_state]
    parents = {(start_x, start_y, start_o): None}
    visited = set()
    visited.add((start_x, start_y, start_o))

    while queue:
        current_state = queue.pop(0)

        # Check if we reached the goal
        if current_state[:2] == goal_state:
            path = [] # Reconstruct path
            last_state = current_state
            while parents[last_state] is not None:
                last_state, last_action = parents[last_state]
                path.append(last_action)
            return path[::-1]  # Return reversed path

        # Generate possible actions (move forward(1, 2 or 3), turn left, turn right)
        for action in ["a3", "a2", "a1", "D", "G"]:
            new_state = perform_action(current_state, action, grid)
            # If the new state is valid and not visited, add it to the queue
            if new_state and (new_state[0], new_state[1], new_state[2]) not in visited:
                visited.add((new_state[0], new_state[1], new_state[2]))
                parents[new_state] = (current_state, action)
                queue.append(new_state)
    
    #print(parents)
    #print(visited)

    return None  # No path found


def visualize_path(grid, start_state, goal_state, path):
    """
    Visualizes the path taken on the grid from start to goal.
    """
    visual_grid = np.array(grid, dtype=str)
    visual_grid[visual_grid == '0'] = '.'  # Free space
    visual_grid[visual_grid == '1'] = '#'  # Wall

    x, y, o = start_state
    visual_grid[y][x] = 'S'  # Start

    for action in path:
        new_state = perform_action((x, y, o), action, grid)
        if new_state:
            x, y, o = new_state
            visual_grid[y][x] = '*'  # Path

    gx, gy = goal_state
    visual_grid[gy][gx] = 'G'  # Goal

    x, y, o = start_state
    visual_grid[y][x] = 'S'  # Start

    for row in visual_grid:
        print(" ".join(row))