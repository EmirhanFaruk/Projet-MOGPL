from Time import current_time_hms
import os

advance_directions = {
    0: "nord",  # North
    1: "est",   # East
    2: "sud",   # South
    3: "ouest"   # West
}

def grid_to_string(grid):
    """
    Convert a grid represented in a numpy array to a string format.
    """
    lines = ["".join(["0 " if grid[i, j] == 0 else "1 " for j in range(grid.shape[1])]) for i in range(grid.shape[0])]
    lines.insert(0, f"{grid.shape[0]} {grid.shape[1]}")
    return '\n'.join(lines)

def graph_to_string(grid, start_pos, goal_pos):
    """
    Convert the graph representation of a grid, along with start and goal positions, to a string format.
    """
    grid_str = grid_to_string(grid)
    start_str = f"{start_pos[0]} {start_pos[1]}"
    goal_str = f"{goal_pos[0]} {goal_pos[1]}"
    return f"{grid_str}\n{start_str} {goal_str} {advance_directions[start_pos[2]]}\n0 0"

def save_graph_to_file(grid, start_pos, goal_pos, filename):
    """
    Save the graph representation of a grid to a file.
    """
    with open(filename, 'w') as f:
        grs = graph_to_string(grid, start_pos, goal_pos)
        f.write(grs)

def save_graph_list_to_file(graph_list, output_dir=""):
    """
    Save a list of graph representations each in seperate files. Output_dir will have "../" at the start. If not specified, defaults to 'saved_graphs/'.
    """
    file_time = current_time_hms()
    if output_dir and not output_dir.endswith('/'):
        output_dir += '/'
    output_dir = "../" + output_dir
    if output_dir == "../":
        output_dir = '../saved_graphs/'
    os.makedirs(output_dir, exist_ok=True)
    for i, (grid, start_pos, goal_pos) in enumerate(graph_list):
        file_path = f"{output_dir}{file_time}_graph_{len(grid)}x{len(grid[0])}_{(i+1):02}.txt"
        save_graph_to_file(grid, start_pos, goal_pos, file_path)



def results_to_string(result):
    return " ".join(str(el) for el in result)


def save_result_to_file(result, filename):
    """
    Save the results of BFS searches to a file.
    """
    with open(filename, 'w') as f:
        f.write(f"{results_to_string(result)}\n")


def save_graph_and_results(graph_list, results, output_dir=""):
    """
    Save both the graph representations and the results of BFS searches to files.
    """
    file_time = current_time_hms()
    if output_dir and not output_dir.endswith('/'):
        output_dir += '/'
    output_dir = "../" + output_dir
    if output_dir == "../":
        output_dir = '../saved_graphs/'
    os.makedirs(output_dir, exist_ok=True)
    path = f"{output_dir}{file_time}"
    for i, (grid, start_pos, goal_pos) in enumerate(graph_list):
        graph_name = f"{len(grid)}x{len(grid[0])}_{(i+1):02}"
        graph_file_path = f"{path}_graph_{graph_name}.txt"
        results_file_path = f"{path}_results_{graph_name}.txt"
        save_graph_to_file(grid, start_pos, goal_pos, graph_file_path)
        save_result_to_file(results[i][1], results_file_path)