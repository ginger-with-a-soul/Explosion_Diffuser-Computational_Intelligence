from random import uniform, randint

'''
Search algorithm based on Genetic algorithm alongside Simulated Annealing
technique, designed to efficiently search through n^k variations.
'''

class Variation():

    def __init__(self, k, n, problem, problem_dict):
        self.k = k
        self.n = n
        self.genome = [randint(1, self.n) for _ in range(k)]
        self.problem = problem
        self.problem_dict = problem_dict
        self.fitness = self.calculate_fitness()

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

                if problem_dict_copy[self.genome[i]] == 0:
                    fitness += 0.5
                else:
                    fitness += 1.0

                problem_dict_copy[self.genome[i]] -= 1
            elif self.genome[i] in problem_dict_copy and problem_dict_copy[self.genome[i]] > 0:

                fitness += 0.5
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

    Without problem as dictionary, our time complexity for finess function would have been
    O(k^2) because in the worst case scenario our ELIF statement in 'calculate_fitness' would
    always be True and we would need to go through whole problem to check the 'IN' part.
    '''
    problem_dict = {problem[i]: 0 for i in range(k)}
    for i in range(k):
        problem_dict[problem[i]] += 1

    return problem_dict

def search(k, n, population_size, mutation_chance, elitism_rate, output_label, mainwindow, problem, num_symbols_map, progress, tournament_selection):

    numerical_problem = transform_problem_to_numerical(k, problem, num_symbols_map)
    problem_dict = create_problem_dict(k, numerical_problem)

    population = []
    new_population = []
    for variation in range(population_size):
        population.append(Variation(k, n, numerical_problem, problem_dict))
