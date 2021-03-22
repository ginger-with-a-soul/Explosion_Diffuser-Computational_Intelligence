'''
Iterative bruteforce algorithm for generating all 
variations that are k long using n different symbols
'''

def generate_all(k, n, output_label, mainwindow, problem, num_symbols_map, progress):
    '''
    Generates all variations starting from all 1s. Variations are
    changed from back to front.
    Converts problem into [int] representation used for comparison
    with out current variation via fitness function.
    Every time a better variation is found, it gets printed to UI.
    Stops search when match is found.
    '''
    numerical_problem = k * [1]

    for i in range(k):
        numerical_problem[i] = num_symbols_map[problem[i]]

    current_variation = k * [1]
    current_best_fitness = 0

    exists_next_variation = True
    while(exists_next_variation):

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
                break

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
