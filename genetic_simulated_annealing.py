from random import uniform, randint
from math import ceil
from heapq import heappushpop, heappush
from threading import Thread, Lock
from visualizer import Visualizer
from time import sleep

'''
Search algorithm based on Genetic algorithm alongside Simulated Annealing
technique, designed to efficiently search through n^k variations.
'''

class Variation():

    def __init__(self, k, n, problem, problem_dict, random_genome):
        self.k = k
        self.n = n
        self.problem = problem
        self.problem_dict = problem_dict
        if random_genome:
            self.genome = [randint(1, self.n) for _ in range(k)]
            self.fitness = self.calculate_fitness()
        else:
            self.genome = []
            self.fitness = 0.0

    def calculate_fitness(self):
        '''
        This is the 'brain' of the Genetic Algorithm.

        Time complexity is 2*O(n) in the average case. For explanation see 'create_problem_dict'
        documentation.
        '''
        fitness = 0.0
        problem_dict_copy = self.problem_dict.copy()

        for i in range(self.k):
            if self.genome[i] == self.problem[i]:

                if problem_dict_copy[self.genome[i]] > 0:
                    fitness += 1.0
                else:
                    fitness += 0.25

                problem_dict_copy[self.genome[i]] -= 1
            elif self.genome[i] in problem_dict_copy and problem_dict_copy[self.genome[i]] > 0:

                fitness += 0.75
                problem_dict_copy[self.genome[i]] -= 1

        return fitness


def transform_problem_to_numerical(k, problem, num_symbols_map):
    numerical_problem = k * [1]

    for i in range(k):
        numerical_problem[i] = num_symbols_map[problem[i]]

    return numerical_problem


def create_problem_dict(k, problem):
    '''
    Dictionary representation of the problem where value is the number of
    times a key was found in the problem and the key is each problem's symbol.

    For dictionary creation we need 2*O(k) time. Every time we call 'calculate_fitness'
    function, we make a copy of our problem_dict so we can alter that copy without
    affecting our main problem_dict because we need it as it is. That adds another O(k)
    for dict copying. All in all it's 4*O(k) to calculate fitness value for the 1st time.
    Every time after the 1st one, it's 2*O(k) in the average case - worst case O(k^2).

    Without problem as dictionary, our time complexity for fitness function would have been
    O(k^2) because in the worst case scenario our ELIF statement in 'calculate_fitness' would
    always be True and we would need to go through whole problem to check the 'IN' part.
    '''
    problem_dict = {problem[i]: 0 for i in range(k)}
    for i in range(k):
        problem_dict[problem[i]] += 1

    return problem_dict

def elitism(elitism_rate, population_size):
    '''
    Creates min heap used for keeping track of our elite genomes.

    Elitism rate determines the size of the min heap.
    '''

    num_of_elites = ceil((elitism_rate * 1.0 * population_size))
    # this check is a fix for 'index out of bounds' error that can occurs when going
    # 2 by 2 through population with odd number of elements (see 'new_population[i+1] = child_2' line)
    if (population_size - num_of_elites) % 2 == 1:
        num_of_elites += 1

    elites = []
    if num_of_elites == 0:
        return None, 0
    else:
        for i in range(num_of_elites):
            # first value in a tuple is fitness, second value is genome
            heappush(elites, (0.0, []))
        return elites, num_of_elites

def tournament_selection(population_size, population, tournament_size):
    '''
    Tournament plays out tournament_size times and the winner is the genome that
    has the best fitness.
    '''

    index = -1
    max_fitness = 0
    for i in range(tournament_size):
        j = randint(0, population_size - 1)
        if population[j][0] > max_fitness:
            index = j
            max_fitness = population[j][0]

    return population[index]


def roulette_selection(population_size, population, tournament_size):
    '''
    Roulette selection gets tourament_size number of genomes, calculates probability
    of each one and then 'spins the wheel' to see who's the lucky winner.

    For speed purposes, there won't be any sorting so the first genome that qualifies
    will be the chosen one.

    Firstly we choose a bunch of genomes and sum up their fitness. After that we calculate
    probability to be chosen for each genome as 'all_prev_probs + current_genome_fitness / total_fitness'.
    '''

    fitness_sum = 0.0
    tournament_winners = []
    for _ in range(tournament_size):
        # 'winner' is a list and not a tuple because we will need to update 3rd item
        # and tuples are immutable
        winner = [population[randint(0, population_size - 1)], 0.0]
        fitness_sum += winner[0][0]
        tournament_winners.append(winner)

    winner_prob = uniform(0.0, 1.0)
    probability = 0.0

    for i in range(tournament_size):
        tournament_winners[i][1] = probability + tournament_winners[i][0][0] / fitness_sum
        probability = tournament_winners[i][1]
        if winner_prob < tournament_winners[i][1]:
            return tournament_winners[i][0]

def selection(tournament_mode, population_size, population, tournament_size):
    if tournament_mode:
        parent_1 = tournament_selection(population_size, population, tournament_size)
        parent_2 = tournament_selection(population_size, population, tournament_size)
    else:
        parent_1 = roulette_selection(population_size, population, tournament_size)
        parent_2 = roulette_selection(population_size, population, tournament_size)

    return parent_1, parent_2

def crossover(k, n, parent_1_genome, parent_2_genome, problem, problem_dict):
    '''
    This is the uniform type of crossover - for each gene a coin is tossed to see which
    child gets whose gene.
    '''

    child_1 = Variation(k, n, problem, problem_dict, False)
    child_2 = Variation(k, n, problem, problem_dict, False)

    for i in range(k):
        p = uniform(0.0, 1.0)
        if p < 0.5:
            child_1.genome.append(parent_1_genome[i])
            child_2.genome.append(parent_2_genome[i])
        else:
            child_1.genome.append(parent_2_genome[i])
            child_2.genome.append(parent_1_genome[i])

    child_1.fitness = child_1.calculate_fitness()
    child_2.fitness = child_2.calculate_fitness()

    return child_1, child_2


def mutation(child_1, child_2, mutation_chance):
    for i in range(child_1.k):
        p = uniform(0.0, 1.0)
        if p < mutation_chance:
            child_1.genome[i] = randint(1, child_1.n)

        p = uniform(0.0, 1.0)
        if p < mutation_chance:
            child_2.genome[i] = randint(1, child_1.n)

    child_1.fitness = child_1.calculate_fitness()
    child_2.fitness = child_2.calculate_fitness()

    return (child_1.fitness, child_1.genome), (child_2.fitness, child_2.genome)

def symbolical_problem(k, numerical_problem, num_symbols_map, solution):
    '''
    Converts our numerical representation of the problem into symbolical.
    '''
    symbolical = []

    for i in range(k):
        for (key, value) in num_symbols_map.items():
            if value == solution[i]:
                symbolical.append(key)

    return symbolical


def simulated_annealing(genome, iterations, n, k, problem, problem_dict):
    '''
    Simulated annealing tries to improve current best genome by replacing a random gene of that
    genome with another random gene from the problem set.
    If the newly created genome is better than the original one, it will be sent back and added
    to the population. This results in faster convergence towards a solution (or a local max).
    If the newly created genome is not better than the original one, there is a chance that the
    new genome will be chosen despite being worse in regards to it's fitness. Because of this
    our convergence might be able to avoid a local maximum. In my implementation, the new genome
    will be added to the elites only if it's better than the worst elite.
    '''

    new_genome = Variation(k, n, problem, problem_dict, False)
    # this line of code is really important because new_genome.genome = genome[1] would create a reference to the genome[1] so any changes would reflect on both. Doing it this way we create a shallow copy to genome[1]. This caused a bug that I've been searching for literally 8 - 12 hours. Guess what mistake I won't make ever again...
    new_genome.genome = genome[1][:]
    new_genome.fitness = genome[0]
    current = Variation(k, n, problem, problem_dict, False)
    current.genome = genome[1][:]
    current.fitness = genome[0]
    maximum_genome = genome[1][:]
    maximum_fitness = genome[0]

    for i in range(iterations):
        current.genome = new_genome.genome[:]
        current.genome[randint(0, k - 1)] = randint(1, n)

        current.fitness = current.calculate_fitness()

        if current.fitness > new_genome.fitness:
            new_genome.genome = current.genome[:]
            new_genome.fitness = current.fitness
            # this if check should be removed if we want to return a genome that can be worse than the one we started with
            if maximum_fitness < current.fitness:
                print(f'SA IMPROVEMENT!\nOld genome: {maximum_fitness, maximum_genome}\nNew genome: {current.fitness, current.genome}')
                maximum_genome = current.genome[:]
                maximum_fitness = current.fitness
        else:
            p = 1.0 / (i + 1)**0.5
            q = uniform(0, 1)
            if p > q:
                new_genome.genome = current.genome[:]
                new_genome.fitness = current.fitness

    return (maximum_fitness, maximum_genome)
    # return (new_genome.fitness, new_genome.genome)


def search(k, n, population_size, mutation_chance, elitism_rate, output_label, mainwindow, problem, num_symbols_map, progress, tournament_selection_mode, done_flag):

    # the visualizing part
    visualizer = Visualizer("Genetic-Simulated annealing algorithm", "gen_algo", k)
    Thread(target=visualizer.run, args=[], daemon=True).start()


    numerical_problem = transform_problem_to_numerical(k, problem, num_symbols_map)
    problem_dict = create_problem_dict(k, numerical_problem)

    elites, num_of_elites = elitism(elitism_rate, population_size)
    num_of_generations = 1000
    tournament_size = 12

    simulated_annealing_temperature = 20
    # can't make this a touple because touples are immutable
    current_best_fitness = 0.0
    current_best_genome = []
    sa_fitness = 0.0
    sa_genome = []
    population = []
    new_population = []
    # after how many % of the generations where we don't have an improvement to our solution, will dynamic mutation chance kick in
    dynamic_mutation_rate = 0.05
    no_improvement_num = 0
    # used to store the original mutation_chance rate so we can restore it if and when needed
    initial_mutation_chance = mutation_chance
    # determines the increment by how much we want to increase our mutation_chance (current mutation_chance will be calculated as mutation_chance + mutation_chance*mutation_chance_increment - percentage increment) when the dynamic mutation kicks in
    mutation_chance_increment = 0.2

    # initial population generation
    for i in range(population_size):
        variation = Variation(k, n, numerical_problem, problem_dict, True)

        heappushpop(elites, (variation.fitness, variation.genome))

        population.append((variation.fitness, variation.genome))
        new_population.append((variation.fitness, variation.genome))

    for generation in range(num_of_generations):
        # check to see if we can unleash another set of solutions to be visualized or if the last set is still flying around on the screen
        if not visualizer.running:
            print("flicker")
            for s in visualizer.field.solutions:
                s.fitness = population[randint(0, population_size - 1)][0]
                s.precision = s.calculate_precision()
                s.running = True


        if generation == num_of_generations-1:
            done_flag[0] = True
            return

        for i in range(0, population_size, 2):

            parent_1, parent_2 = selection(tournament_selection_mode, population_size, population, tournament_size)

            child_1, child_2 = crossover(k, n, parent_1[1], parent_2[1], numerical_problem, problem_dict)

            child_1, child_2 = mutation(child_1, child_2, mutation_chance)

            heappushpop(elites, (child_1[0], child_1[1]))
            heappushpop(elites, (child_2[0], child_2[1]))

            for j in range(num_of_elites):
                if elites[j][0] > current_best_fitness:
                    no_improvement_num = 0
                    mutation_chance = initial_mutation_chance
                    current_best_genome = elites[j][1][:]
                    current_best_fitness = elites[j][0]

                    progress(current_best_fitness * 100.0 / k)
                    output_label['text'] = symbolical_problem(k, problem, num_symbols_map, current_best_genome)
                    mainwindow.update()

                    if elites[j][0] == k:
                        print(f'Solution {elites[j][1]} found in generation {generation}')
                        done_flag[0] = True
                        return

            sa_fitness, sa_genome = simulated_annealing((current_best_fitness, current_best_genome), simulated_annealing_temperature, n, k, numerical_problem, problem_dict)
            if sa_fitness > current_best_fitness or sa_genome != current_best_genome:
                no_improvement_num = 0
                heappushpop(elites, (sa_fitness, sa_genome))
                new_population[randint(0, population_size - 1)] = (sa_fitness, sa_genome)

            new_population[i] = child_1
            new_population[i + 1] = child_2

        print(f'Generation: {generation}\nCurrent best solution: {current_best_fitness, current_best_genome}\n')
        no_improvement_num += 1
        if no_improvement_num >= int(num_of_generations * dynamic_mutation_rate):
            mutation_chance += mutation_chance * mutation_chance_increment
            print(f'No improvement: {no_improvement_num} generations\nMutation chance increased to: {mutation_chance}')
            if mutation_chance > 0.3:
                # we will cap out our mutation_chance to 30%
                mutation_chance = 0.3


        population = new_population
