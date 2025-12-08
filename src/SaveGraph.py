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
    return f"{grid_str}\n{start_str} {goal_str} {advance_directions[start_pos[2]]}\n"

    
def save_graph_list_to_file(instances, filename):
    """
    Save the graph representation of a grid to a file.
    """
    # If file exists, remove trailing "0 0" (EOF marker)
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        # Remove LAST line only if it is exactly "0 0"
        if lines and lines[-1].strip() == "0 0":
            lines = lines[:-1]  # drop the EOF marker
            with open(filename, 'w') as f:
                f.writelines(lines)
    
    with open(filename, 'a') as f:
        for grid, start_pos, goal_pos in instances:
            grs = graph_to_string(grid, start_pos, goal_pos) # Get graph as a string
            f.write(grs) # Write the graph in the file
        f.write("0 0\n")  # End of file indicator
        


def results_to_string(result):
    return " ".join(str(el) for el in result)


def save_result_list_to_file(results, filename):
    """
    Save the results of BFS searches to a file.
    """
    with open(filename, 'a') as f:
        for result in results:
            f.write(f"{results_to_string(result)}\n")


def save_graph_and_results(graph_list, results, output_dir="", file_time=""):
    """
    Save both the graph representations and the results of BFS searches to files.
    """
    if not file_time:
        file_time = current_time_hms()
    if output_dir and not output_dir.endswith('/'):
        output_dir += '/'
    output_dir = "../" + output_dir
    if output_dir == "../":
        output_dir = '../saved_graphs/'
    os.makedirs(output_dir, exist_ok=True)
    path = f"{output_dir}{file_time}"

    graph_file_path = f"{path}_graph.txt"
    save_graph_list_to_file(graph_list, graph_file_path)
    results_file_path = f"{path}_results.txt"
    save_result_list_to_file(results, results_file_path)