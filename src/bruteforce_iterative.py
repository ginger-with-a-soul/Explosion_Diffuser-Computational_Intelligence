from visualizer import Visualizer
from threading import Thread
import baseconv
from time import sleep


'''
Iterative bruteforce algorithm for generating all
variations that are k long using n different symbols
'''

def generate_all(k, n, output_label, mainwindow, problem, num_symbols_map, progress, done_flag):
    '''
    Generates all variations starting from all 1s. Variations are
    changed from back to front.
    Converts problem into [int] representation used for comparison
    with out current variation via fitness function.
    Every time a better variation is found, it gets printed to UI.
    Stops search when match is found.
    '''
    visualizer = Visualizer("Brute-force algorithm", "brute_algo", k)
    grid = visualizer.grid
    total_variations = n ** k
    current_variation_number = 0
    progress_percentage = 0.0

    progress_step = 100.0 / (grid.col_num * grid.row_num)

    numerical_problem = k * [1]

    for i in range(k):
        numerical_problem[i] = num_symbols_map[problem[i]]

    # calculates the ordinal number of my problem variation so that I can place it on a tile in UI
    number = [numerical_problem[i]-1 for i in range(len(numerical_problem))]
    problem_position = int(baseconv.base(tuple(number), n, 10, string=True)) + 1
    problem_position = int(((problem_position * 100.0) / (total_variations*1.0)) / progress_step)
    visualizer.grid.problem_position = problem_position

    if not visualizer.running:
        # starts the 'run' function from the visualization part
        Thread(target=visualizer.run, args=[done_flag[0]], daemon=True).start()
        visualizer.running = True
    else:
        return


    current_variation = k * [1]
    current_best_fitness = 0

    exists_next_variation = True
    while(exists_next_variation):
        current_variation_number += 1

        progress_percentage = (current_variation_number * 100.0) / (total_variations*1.0)
        if progress_percentage >= progress_step:
            progress_step += 100.0 / (grid.col_num * grid.row_num)
            grid.current_position += 1

        new_fitness = fitness(k, current_variation, numerical_problem)
        if(new_fitness > current_best_fitness):

            back_to_symbolical = []
            current_best_fitness = new_fitness
            progress(current_best_fitness * 100.0 / k)

            for i in range(k):
                for (key, value) in num_symbols_map.items():
                    if value == current_variation[i]:
                        back_to_symbolical.append(key)

            output_label['text'] = back_to_symbolical
            mainwindow.update()

            if(current_best_fitness == k):
                done_flag[0] = True
                visualizer.draw_end_text = True
                return

        index = k - 1
        while(index >= 0 and current_variation[index] == n):
            current_variation[index] = 1
            index -= 1

        if index < 0:
            exists_next_variation = False
        else:
            current_variation[index] += 1



def fitness(k, solution, problem):
    fit = 0
    for i in range(k):
        if solution[i] == problem[i]:
            fit += 1

    return fit
