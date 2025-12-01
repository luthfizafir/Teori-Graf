import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
import os


filename = 'small.csv' 

plt.ion()   

def read_cities(filepath):
    '''
    Load a TSP dataset.
    '''
    if not os.path.exists(filepath):
        print(f"Error: The file '{filepath}' was not found in this folder.")
        print("Please ensure 'small.csv' is in the same directory as this script.")
        exit(1)
        
    cities = np.loadtxt(filepath, delimiter=',')
    return cities


def score_solution(cities, solution):
    '''
    Calculate the total distance traveled by the given solution.
    '''
    if len(solution) != len(cities):
        raise Exception(('Invalid solution: len(solution) is {}, ' + \
                'but it should be {}.').format(len(solution), len(cities)))

    if set(solution) != set(range(len(cities))):
        raise Exception('Invalid solution: The solution does not ' + \
                'visit each city exactly once!')

    ordered_cities = cities[solution]
    next_cities = np.roll(ordered_cities, -1, axis=0)
    distances = np.sqrt(np.sum((ordered_cities - next_cities)**2, axis=1))
    
    return np.sum(distances)


def create_figure():
    '''
    Creates a figure which `visualize_solution()` will draw onto.
    '''
    fig, axes = plt.subplots(1, 2, figsize=(15, 7))
    return fig, axes


def visualize_solution(cities, solution, fig=None, axes=None, block=True):
    '''
    Visualize the solution in a 2D plot.
    '''
    dist = score_solution(cities, solution) if len(solution) == len(cities) else float('NaN')

    if fig is None or axes is None:
        fig, axes = create_figure()
    ax1, ax2 = axes
    
    if not plt.fignum_exists(fig.number):
        return

    fig.suptitle('Total Distance: {:.4f}'.format(dist), fontsize=20)

    ax1.clear()
    ax1.set_title("Raw Cities")
    ax1.scatter(cities[:,0], cities[:,1])

    if len(solution) == len(cities):
        path = np.hstack((solution, solution[0]))  
    else:
        path = solution
    
    ax2.clear()
    ax2.set_title("Optimized Path")
    ax2.plot(cities[path,0], cities[path,1], 'b-')
    ax2.scatter(cities[:,0], cities[:,1], c='red', zorder=5)
    
    ax2.scatter(cities[path[0],0], cities[path[0],1], c='green', s=100, zorder=6, label='Start')

    if block:
        print(f"Done! Final Distance: {dist:.4f}")
        print("Close the plot window to exit.")
        plt.show(block=True)
    else:
        plt.pause(0.001)


def solve_nearest_neighbor(cities):
    """
    Greedy algorithm: always go to the nearest unvisited city.
    """
    N = len(cities)
    unvisited = set(range(1, N))
    current_city = 0
    solution = [0]

    while unvisited:
        best_dist = float('inf')
        nearest = None
        
        for candidate in unvisited:
            d = euclidean(cities[current_city], cities[candidate])
            if d < best_dist:
                best_dist = d
                nearest = candidate
        
        solution.append(nearest)
        unvisited.remove(nearest)
        current_city = nearest
        
    return np.array(solution)


def solve_2opt(cities, solution, callback=None):
    """
    Iteratively reverse segments of the path to untangle crossings.
    """
    best_solution = solution.copy()
    best_dist = score_solution(cities, best_solution)
    improved = True
    
    count = 0

    while improved:
        improved = False
        N = len(best_solution)
        
        for i in range(N - 1):
            for j in range(i + 1, N):
                if j - i == 1: continue 
                
                new_solution = best_solution.copy()
                new_solution[i:j] = best_solution[i:j][::-1] 
                
                new_dist = score_solution(cities, new_solution)
                
                if new_dist < best_dist:
                    best_dist = new_dist
                    best_solution = new_solution
                    improved = True
                    count += 1
                    
                    if callback and count % 2 == 0: 
                        callback(best_solution)
                    
                    break 
            if improved: break
            
    return best_solution


def tsp_solver_smart(cities, new_best_solution_func=None):
    '''
    Solver Logic:
    1. Greedy Nearest Neighbor
    2. 2-Opt Local Search
    '''
    print("Step 1: Calculating Greedy Nearest Neighbor...")
    initial_solution = solve_nearest_neighbor(cities)
    if new_best_solution_func:
        new_best_solution_func(initial_solution)
    
    print("Step 2: Optimizing with 2-Opt (Local Search)...")
    final_solution = solve_2opt(cities, initial_solution, new_best_solution_func)
    
    return final_solution


if __name__ == '__main__':
    
    cities = read_cities(filename)

    show_progress = True 

    if not show_progress:
        solution = tsp_solver_smart(cities)
        visualize_solution(cities, solution)
    else:
        fig, axes = create_figure()

        def visualize_wrapper(solution, is_final=False):
            dist = score_solution(cities, solution)
            print(f"{'FINAL' if is_final else 'Current'} Distance: {dist:.4f}")
            visualize_solution(cities, solution, fig, axes, block=is_final)

        solution = tsp_solver_smart(cities, visualize_wrapper)
        visualize_wrapper(solution, True)