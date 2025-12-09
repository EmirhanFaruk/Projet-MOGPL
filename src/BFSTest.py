import numpy as np
import matplotlib.pyplot as plt
import os


from BFS import BFS, visualize_path
from GenerateGrid import generate_grid
from Time import now, elapsed, current_time_hms
from SaveGraph import save_graph_and_results
from ImportGraph import read_input_file



def generate_test_grid(size=10, wall_num=10, n=10):
    """
    Generate multiple test grids with specified size and wall percentage, n times and return them in a list.
    """
    grids = []
    for _ in range(n):
        grid, start_pos, goal_pos = generate_grid(M=size, N=size, wall_num=wall_num)
        grids.append((grid, start_pos, goal_pos))
    return grids


def test_BFS_on_multiple_grids(size=10, wall_num=10, n=10, output_time=""):
    """
    Test BFS algorithm on multiple generated grids.
    """
    if output_time == "":
        output_time = current_time_hms()
    graphs = []
    results = []
    counter = 0
    while counter < n: # We don't count unsolvable grids, so no for loop
        test_grid, start_pos, goal_pos = generate_test_grid(size, wall_num, 1)[0] # Generate a test grid

        start = now() # Start timer
        result = BFS(test_grid, start_pos, goal_pos) # Run BFS

        if result is None: # If no path found, we skip this grid
            continue

        length = len(result)
        result.insert(0, length) # Insert path length at the start of the result

        results.append((elapsed(start), result)) # Store time and result
        
        graphs.append((test_grid, start_pos, goal_pos)) # Store the graph to save later
        counter += 1

    save_graph_and_results(graphs, [result[1] for result in results], output_dir=f"saved_graphs/{output_time}/", file_time=output_time)
    return results, output_time






def show_pos_in_grid(grid, start_pos, goal_pos):
    display_grid = np.array(grid, copy=True)
    x, y, _ = start_pos
    display_grid[y][x] = 8  # Mark the start position with an 8
    x, y = goal_pos
    display_grid[y][x] = 9  # Mark the goal position with a 9
    print(display_grid)
    return display_grid


def ask_save(grid, start_pos, goal_pos, result):
    """
    Asks user if they want to save the graph and the result, then does what user wants.
    """
    if result is None:
        print("No path to save.")
        return

    choice = input("Save this grid and result? (y/n): ").strip().lower()
    if choice != "y":
        print("Not saved.")
        return

    # Folder name based on timestamp
    file_time = current_time_hms()
    output_dir = f"saved_graphs/manual_{file_time}/"
    os.makedirs(output_dir, exist_ok=True)

    graph_list = [(grid, start_pos, goal_pos)]
    results = [result]  # result is [length, action1, action2, ...]

    save_graph_and_results(graph_list=graph_list, results=results, output_dir=output_dir, file_time=file_time)

    print(f"Saved to folder: {output_dir}")
    print("Files created:")
    print(f"  - {output_dir}{file_time}_graph.txt")
    print(f"  - {output_dir}{file_time}_results.txt")


def do_single_test(M, N, wall_num):
    grid, start_pos, goal_pos = generate_grid(M, N, wall_num=wall_num)
    print(grid)
    print("Start position:", start_pos)
    print("Goal position:", goal_pos)
    show_pos_in_grid(grid, start_pos, goal_pos)

    result = BFS(grid, start_pos, goal_pos)
    length = len(result)
    result.insert(0, length) # Insert path length at the start of the result
    if result:
        path = result
        print("Path found:", path[1:])
        print("Number of explored nodes:", path[0])
    else:
        print("No path found")
    
    ask_save(grid, start_pos, goal_pos, result)




# TEST BY SIZE


def test_by_size():
    output_time = current_time_hms() # for the name for the saved graph file
    for i in range(10, 51, 10): # Test it with different grid sizes
        results, _ = test_BFS_on_multiple_grids(size=i, wall_num=10, n=10, output_time=output_time)
        avg_time = sum([res[0] for res in results]) / len(results) # Get average time

        #print(f"Results: {results}")
        print(f"Average time for BFS on {len(results)} grids of size {i}x{i} with {i} walls: {avg_time:.6f} seconds.")



def plot_performance_for_size():
    """
    Makes a plot to show the performance by size of the grid.
    """
    sizes = list(range(10, 51, 10))
    times = []
    output_time = current_time_hms()
    for i in sizes:
        results, output_time = test_BFS_on_multiple_grids(size=i, wall_num=i, n=10, output_time=output_time)
        avg_time = sum([res[0] for res in results]) / len(results)
        times.append(avg_time)

    plt.plot(sizes, times, marker='o')
    plt.title('BFS Performance on Different Grid Sizes with the Wall Number Same as Size')
    plt.xlabel('Grid Size (N x N)')
    plt.ylabel('Average Time (seconds)')
    plt.grid(True)
    plt.show()
    return output_time


# TEST BY WALL NUMBER

def test_by_wall_number(size=20):
    output_time = current_time_hms()
    for i in range(10, 51, 10):
        results, output_time = test_BFS_on_multiple_grids(size=size, wall_num=i, n=10, output_time=output_time)
        avg_time = sum([res[0] for res in results]) / len(results)

        #print(f"Results: {results}")
        print(f"Average time for BFS on {len(results)} grids of size {size}x{size} with {i} walls: {avg_time:.6f} seconds.")


def plot_performance_for_wall_number(size=20):
    """
    Makes a plot to show the performance by the number of the walls existing in the grid.
    """
    wall_numbers = list(range(10, 51, 10))
    times = []
    lengths = []
    output_time = current_time_hms()
    for i in wall_numbers:
        results, output_time = test_BFS_on_multiple_grids(size=size, wall_num=i, n=100, output_time=output_time)
        avg_time = sum([res[0] for res in results]) / len(results)
        times.append(avg_time)

        avg_length = sum([len(res[1]) if res[1] is not None else 0 for res in results]) / len(results)
        lengths.append(avg_length)

    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.plot(wall_numbers, times, marker='o')
    plt.title('BFS Performance on Different Wall Numbers with the Grid size of ' + str(size) + 'x' + str(size))
    plt.xlabel('Wall Number')
    plt.ylabel('Average Time (seconds)')
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(wall_numbers, lengths, marker='o')
    plt.title(f'BFS Path Length vs Wall Number ({size}x{size})')
    plt.xlabel('Wall Number')
    plt.ylabel('Average BFS Path Length')
    plt.grid(True)

    plt.grid(True)
    plt.show()
    return output_time


# READ FROM A FILE

def test_read_file(filename):
    """
    Read from the given file name, then use bfs on the graph.
    """
    instance = read_input_file(filename)
    instance = instance[0]  # Get the first instance for testing
    print(f"instance: {instance}")
    result = BFS(instance[0], instance[1], instance[2])
    print(f"result: {len(result)} {result}")
    visualize_path(instance[0], instance[1], instance[2], result)



# TEST THE TEST FILE

def test_test_file():
    grid, start_pos, goal_pos = read_input_file("test.txt")[0]

    result = BFS(grid, start_pos, goal_pos)
    length = len(result)
    result.insert(0, length) # Insert path length at the start of the result
    if result:
        path = result
        print("Path found:", path[1:])
        print("Number of explored nodes:", path[0])
        visualize_path(grid, start_pos, goal_pos, path[1:])
    else:
        print("No path found.")




# MENU

def print_menu_choices():
    print("\n===== BFS GRID TEST MENU =====")
    print("1. Run a single test")
    print("2. Test by grid size")
    print("3. Plot performance by grid size")
    print("4. Test by wall number")
    print("5. Plot performance by wall number")
    print("6. Read and test a grid from file")
    print("7. Test the test file")
    print("0. Quit")
    print("================================\n")


def menu_single_test():
    try:
        M = int(input("Enter number of rows M: "))
        N = int(input("Enter number of columns N: "))
        wall_num = int(input("Enter number of walls: "))
        do_single_test(M, N, wall_num)
    except ValueError:
        print("Invalid input, expected numbers.")

def menu_test_by_size():
    test_by_size()

def menu_plot_by_size():
    output_time = plot_performance_for_size()
    print(f"Plots saved using timestamp: {output_time}")

def menu_test_by_wall_number():
    try:
        size = int(input("Enter fixed grid size: "))
        test_by_wall_number(size)
    except ValueError:
        print("Invalid input.")

def menu_plot_by_wall_number():
    try:
        size = int(input("Enter fixed grid size: "))
        output_time = plot_performance_for_wall_number(size)
        print(f"Plots saved using timestamp: {output_time}")
    except ValueError:
        print("Invalid input.")

def menu_test_from_file():
    filename = input("Enter file path: ")
    test_read_file(filename)

def menu_test_testfile():
    test_test_file()



def menu():
    while True:
        print_menu_choices()
        user_choice = input("Enter your choice: ")

        if user_choice == "1":
            menu_single_test()

        elif user_choice == "2":
            menu_test_by_size()

        elif user_choice == "3":
            menu_plot_by_size()

        elif user_choice == "4":
            menu_test_by_wall_number()

        elif user_choice == "5":
            menu_plot_by_wall_number()

        elif user_choice == "6":
            menu_test_from_file()

        elif user_choice == "7":
            menu_test_testfile()

        elif user_choice == "0":
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    menu()