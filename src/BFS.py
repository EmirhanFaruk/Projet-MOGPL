import numpy as np

from State import State


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
        if 0 <= x < len(grid[0]) - 1 and 0 <= y < len(grid) - 1:
            in_a_wall = any(grid[y + dy][x + dx] == 1 for dx, dy in wall_collision_directions)
            return not in_a_wall
    return False

def advance(state, action, grid):
    """
    Advances the state forward by the specified action amount if the path is valid. Returns the new state.
    """
    advance_num = advance_action[action]

    can_advance = True # Assume True unless proven otherwise
    for i in range(1, advance_num):
        x = state.x + (i * advance_directions[state.o][0])
        y = state.y + (i * advance_directions[state.o][1])
        can_advance = can_advance and valid_position(x, y, grid)
    
    if can_advance:
        new_x = state.x + (advance_num * advance_directions[state.o][0])
        new_y = state.y + (advance_num * advance_directions[state.o][1])
        return State(new_x, new_y, state.o, state, action)

def turn(state, action):
    """
    Turns the state left or right based on the action. Returns the new state.
    """
    new_o = (state.o + (1 if action == "D" else -1)) % 4
    return State(state.x, state.y, new_o, state, action)

def perform_action(current_state, action, grid):
    """
    Performs the given action on the current state and returns the resulting new state. None if the action is invalid.
    """
    if action in ["D", "G"]:
        return turn(current_state, action)
    elif action in ["a1", "a2", "a3"]:
        return advance(current_state, action, grid)
    return None

def BFS(grid, start_pos, goal_pos):
    """
    Performs a breadth-first search on the grid to find a path from the start position and orientation to the goal position.
    Returns a list of actions to reach the goal, or None if no path is found.
    """
    start_x, start_y, start_o = start_pos
    goal_x, goal_y = goal_pos
    start_state = State(start_x, start_y, start_o)
    queue = [start_state]
    visited = set()
    visited.add((start_x, start_y, start_o))

    while queue:
        current_state = queue.pop(0)

        # Check if we reached the goal
        if current_state.x == goal_x and current_state.y == goal_y:
            path = [] # Reconstruct path
            while current_state.parent is not None:
                path.append(current_state.action)
                current_state = current_state.parent
            return path[::-1]  # Return reversed path

        # Generate possible actions (move forward(1, 2 or 3), turn left, turn right)
        for action in ["a1", "a2", "a3", "D", "G"]:
            new_state = perform_action(current_state, action, grid)
            # If the new state is valid and not visited, add it to the queue
            if new_state and (new_state.x, new_state.y, new_state.o) not in visited:
                visited.add((new_state.x, new_state.y, new_state.o))
                queue.append(new_state)

    return None  # No path found