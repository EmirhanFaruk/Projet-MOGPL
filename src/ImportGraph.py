import numpy as np

directions = {
    "nord": 0,  # North
    "est": 1,   # East
    "sud": 2,   # South
    "ouest": 3   # West
}

def read_input_file(filename):
    """
    Reads the input file and returns a list of problem instances.
    Each instance is a tuple: (grid, start_pos, goal_pos, start_orientation)
    """
    instances = []

    with open(filename, 'r', encoding='utf-8') as f:
        while True:
            # Read grid size
            line = f.readline().strip()
            if line == "0 0" or line == "": # As a safety if forgot to put 0 0 at the end
                break
            M_N = line.split()
            M = int(M_N[0])
            N = int(M_N[1])

            # Read the grid
            grid = []
            for _ in range(M):
                row_str = f.readline().strip().split()
                row = [int(x) for x in row_str]
                grid.append(row)
            grid = np.array(grid, dtype=int)

            # Read start/goal + orientation
            last_line = f.readline().strip().split()
            D1 = int(last_line[1])
            D2 = int(last_line[0])
            F1 = int(last_line[3])
            F2 = int(last_line[2])
            orientation = directions[last_line[4].lower()]  # e.g., "nord", "sud", "est", "ouest"

            start_pos = (D1, D2, orientation)
            goal_pos = (F1, F2)

            instances.append((grid, start_pos, goal_pos))

    return instances
