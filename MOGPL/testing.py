import numpy as np
import gurobipy as gp
from gurobipy import GRB
import matplotlib.pyplot as plt
from BFS import BFS

# Directions for BFS
advance_directions = {
    0: (0, -1),  # North
    1: (1, 0),   # East
    2: (0, 1),   # South
    3: (-1, 0)   # West
}

def generate_grid_with_gurobi(M, N, P):
    weights = np.random.randint(0, 1001, size=(M, N))
    model = gp.Model("grid_obstacles")
    x = model.addVars(M, N, vtype=GRB.BINARY, name="x")

    # Total obstacles
    model.addConstr(gp.quicksum(x[i,j] for i in range(M) for j in range(N)) == P)

    # Row/column constraints
    max_row_obs = int(2 * P / M)
    max_col_obs = int(2 * P / N)
    for i in range(M):
        model.addConstr(gp.quicksum(x[i,j] for j in range(N)) <= max_row_obs)
    for j in range(N):
        model.addConstr(gp.quicksum(x[i,j] for i in range(M)) <= max_col_obs)

    # No 101 in rows/columns
    for i in range(M):
        for j in range(N-2):
            model.addConstr(x[i,j] + x[i,j+2] <= 1)
    for j in range(N):
        for i in range(M-2):
            model.addConstr(x[i,j] + x[i+2,j] <= 1)

    # Minimize total weight
    model.setObjective(gp.quicksum(weights[i,j]*x[i,j] for i in range(M) for j in range(N)), GRB.MINIMIZE)
    model.optimize()

    grid = np.zeros((M, N), dtype=int)
    for i in range(M):
        for j in range(N):
            if x[i,j].X > 0.5:
                grid[i,j] = 1
    return grid

def visualize_grid(grid, start, goal, path=None):
    M, N = grid.shape
    display = np.copy(grid)
    display[start[0], start[1]] = 8  # Start
    display[goal[0], goal[1]] = 9    # Goal

    plt.figure(figsize=(6,6))
    plt.imshow(display, cmap="Greys", origin="upper")

    if path:
        # Plot path as red arrows
        x, y = start[1], start[0]
        for action in path:
            dx, dy = advance_directions[action] if isinstance(action, int) else (0,0)
            plt.arrow(x, y, dx*0.8, dy*0.8, color='red', head_width=0.3, length_includes_head=True)
            x += dx
            y += dy

    plt.title("Grid (start=8, goal=9, obstacles=1)")
    plt.show()

def generate_and_solve():
    M = int(input("Enter number of rows (M): "))
    N = int(input("Enter number of columns (N): "))
    P = int(input("Enter number of obstacles (P): "))

    grid = generate_grid_with_gurobi(M, N, P)
    print("Generated grid:")
    print(grid)

    start_row = int(input("Start row: "))
    start_col = int(input("Start col: "))
    start_orientation = int(input("Start orientation (0=N,1=E,2=S,3=W): "))
    goal_row = int(input("Goal row: "))
    goal_col = int(input("Goal col: "))

    start_pos = (start_col, start_row, start_orientation)
    goal_pos = (goal_col, goal_row)

    path = BFS(grid, start_pos, goal_pos)  # Make sure your BFS is imported
    if path is None:
        print("No path found!")
    else:
        print("Path found:", path)
    
    visualize_grid(grid, start_pos, goal_pos, path)

# Run everything
generate_and_solve()
