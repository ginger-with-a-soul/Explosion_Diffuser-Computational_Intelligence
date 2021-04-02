import os
import pygubu
import tkinter as tk
import tkinter.ttk as ttk
import psutil  # multi-platform library for system resource usage tracking
from random import choices
from string import ascii_lowercase  # used to generate a list of available symbols
import bruteforce_iterative as bf
import genetic_simulated_annealing as gsa
import threading # threading in Python does not work line in other programming languages (Google GIL). I've implemented threading because I need faster context switching for the UI and Visualization drawing

PROJECT_PATH = os.path.dirname(__file__)
PROJECT_UI = os.path.join(PROJECT_PATH, "ui.ui")


class UiApp:
    def __init__(self):

        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('mainwindow')
        builder.connect_callbacks(self)

        self.theme()

        self.initialize_variables()

        self.initialize_flags()

        self.show_resource_usage()

        self.bind_validation()

    def initialize_variables(self):
        self.k = 5
        self.n = 5
        self.population_size = 500
        self.elitism = 0.1
        self.mutation_rate = 0.03
        self.problem = ''
        self.available_symbols = list(ascii_lowercase) + [str(i) for i in range(10)]
        # numerical symbols represent a map of available symbols where keys are numbers used for checking current best solution in algorithms that generate variations with numbers only. Key values start with 1 because our variations start with all 1s and not 0s
        self.available_symbols_numerical = {self.available_symbols[i - 1]: i for i in range(1, len(self.available_symbols) + 1)}
        self.output_label = self.builder.get_object('label_current_best')
        self.progress_tracker = self.builder.get_object('label_percentage_tracker')
        self.current_solution = ''
        self.builder.get_variable('algo_group').set('1')
        self.builder.get_variable('gene_group').set('1')
        self.progress_bar = self.builder.get_object('progressbar')
        self.timer_variable = 0.0
        self.timer_label = self.builder.get_object('label_time')
        # timer_reference is used to store reference to the timer's after function so we can call after_cancel function later
        self.timer_reference = None

    def initialize_flags(self):
        '''
        Initializes flags used to communicate frontend and backend states.
        Initially, size, number, genetic and tournamet flags are True because
        they have a valid default state.
        '''


        self.DONE_FLAG = [True] # it's a list because it needs to be mutable to be sent to threads
        self.MUTATION_FLAG = True
        self.PROBLEM_FLAG = False
        self.SIZE_FLAG = True
        self.START_FLAG = False
        self.NUMBER_FLAG = True
        self.BRUTEFORCE_FLAG = True
        self.MONTECARLO_FLAG = False
        self.GENETIC_FLAG = False
        self.ROULETTE_FLAG = False
        self.TOURNAMENT_FLAG = True
        self.POPULATION_SIZE_FLAG = True
        self.ELITISM_FLAG = True

    def theme(self):
        # root.tk.call locates the theme package and selects styles we wish
        # to use from that package
        self.theme_abs_path = os.path.abspath('awthemes-10.2.1')
        self.mainwindow.tk.call('lappend', 'auto_path', self.theme_abs_path)
        self.mainwindow.tk.call('package', 'require', 'awdark')
        self.mainwindow.tk.call('package', 'require', 'awlight')
        # to change the style we need to create an instance of 'Style' class
        self.style = ttk.Style(self.mainwindow)
        self.style.theme_use('awdark')
        # self.style.theme_use('awlight')

    def brute_force_callback(self):
        self.clear_problem_entry()
        self.BRUTEFORCE_FLAG = True
        self.GENETIC_FLAG = not self.BRUTEFORCE_FLAG
        self.MONTECARLO_FLAG = not self.BRUTEFORCE_FLAG

    def monte_carlo_callback(self):
        self.clear_problem_entry()
        self.MONTECARLO_FLAG = True
        self.GENETIC_FLAG = not self.MONTECARLO_FLAG
        self.BRUTEFORCE_FLAG = not self.MONTECARLO_FLAG

    def genetic_algorithm_callback(self):
        self.clear_problem_entry()
        self.GENETIC_FLAG = True
        self.MONTECARLO_FLAG = not self.GENETIC_FLAG
        self.BRUTEFORCE_FLAG = not self.GENETIC_FLAG

    def roulette_selection_callback(self):
        self.ROULETTE_FLAG = True
        self.TOURNAMENT_FLAG = not self.ROULETTE_FLAG

    def tournament_selection_callback(self):
        self.TOURNAMENT_FLAG = True
        self.ROULETTE_FLAG = not self.TOURNAMENT_FLAG

    def generate_problem_callback(self):
        '''
        Initializes the problem we want to solve.

        It firstly selects a list of available symbols for variation
        to use based on n. After that it randomly chooses k elements from
        the list of available symbols. Finally, it concatenates them and
        when printing it in the entry box, adds a blank after each symbol
        for readabillity purposes.
        '''

        self.PROBLEM_FLAG = True
        # resets the progress bar
        self.progress(value=0)

        # clears current solution label
        self.output_label['text'] = ''

        entry_field = self.builder.get_object('entry_problem')
        entry_field.delete("0", "end")

        self.problem = ''.join(choices(self.available_symbols[0:self.n], k=self.k))

        entry_field.insert(0, ' '.join(self.problem))


    def start_callback(self):
        self.START_FLAG = self.DONE_FLAG[0] & self.NUMBER_FLAG & self.PROBLEM_FLAG & self.SIZE_FLAG & (self.BRUTEFORCE_FLAG | self.MONTECARLO_FLAG | self.GENETIC_FLAG)

        if self.START_FLAG:
            self.DONE_FLAG[0] = False
            self.timer_variable = 0.0
            self.timer()
            if self.BRUTEFORCE_FLAG:
                # daemon parameter True indicates that our threads stop when we close the main program
                threading.Thread(target=bf.generate_all, args=[self.k, self.n, self.output_label,self.mainwindow, self.problem, self.available_symbols_numerical, self.progress, self.DONE_FLAG], daemon=True).start()
            elif self.MONTECARLO_FLAG:
                ...
            else:
                if self.POPULATION_SIZE_FLAG & self.ELITISM_FLAG & self.MUTATION_FLAG:
                    if self.TOURNAMENT_FLAG:
                        threading.Thread(target=gsa.search, args = [self.k, self.n, self.population_size, self.mutation_rate, self.elitism, self.output_label, self.mainwindow, self.problem, self.available_symbols_numerical, self.progress, self.TOURNAMENT_FLAG, self.DONE_FLAG], daemon=True).start()
                    else:
                        threading.Thread(target=gsa.search, args=[self.k, self.n, self.population_size, self.mutation_rate, self.elitism, self.output_label, self.mainwindow, self.problem, self.available_symbols_numerical, self.progress, self.TOURNAMENT_FLAG, self.DONE_FLAG], daemon=True).start()

    def change_theme_callback(self):
        if self.style.theme_use() == 'awdark':
            self.style.theme_use('awlight')
        else:
            self.style.theme_use('awdark')

    def show_resource_usage(self):
        self.builder.get_variable('cpu_usage').set(psutil.cpu_percent())
        self.builder.get_variable('memory_usage').set(psutil.virtual_memory().percent)
        # updates usage stats every 1000ms
        self.mainwindow.after(1000, self.show_resource_usage)


    def timer(self):
        self.timer_variable += 1
        self.timer_label['text'] = int(self.timer_variable)
        self.timer_reference = self.mainwindow.after(1000, self.timer)

    def bind_validation(self):
        '''
        Binds entry fields with their tkinter objects and
        enables user input validation for those objects.
        '''

        entry_input_size = self.builder.get_object('entry_input_size')
        entry_variation_size = self.builder.get_object('entry_input_num_of_symbols')
        entry_mutation_rate = self.builder.get_object('entry_mutation_rate')
        entry_problem = self.builder.get_object('entry_problem')
        entry_elitism = self.builder.get_object('entry_elitism')
        entry_population_size = self.builder.get_object('entry_population_size')

        self.register_validation(tk.Entry(entry_input_size), self.input_size_validate_callback)
        self.register_validation(tk.Entry(entry_variation_size), self.input_number_validate_callback)
        self.register_validation(tk.Entry(entry_mutation_rate), self.mutation_rate_validate_callback)
        self.register_validation(tk.Entry(entry_problem), self.random_problem_validate_callback)
        self.register_validation(tk.Entry(entry_elitism), self.elitism_validate_callback)
        self.register_validation(tk.Entry(entry_population_size), self.population_size_validate_callback)

    def register_validation(self, entry, callback):
        '''
        Registers validation function (binds each variable to its
        validate function).
        '''
        # reg is the name of our callback function
        reg = entry.register(callback)
        entry.config(validate="focusout", validatecommand=(reg, '% P'))

    def input_size_validate_callback(self):

        self.clear_problem_entry()

        try:
            self.k = int(self.builder.get_variable('input_size').get())
        except ValueError:
            self.SIZE_FLAG = False
            return False

        if self.k < 1 or self.k > 21:
            self.SIZE_FLAG = False
            return False
        else:
            self.SIZE_FLAG = True
            return True

    def input_number_validate_callback(self):

        self.clear_problem_entry()

        try:
            self.n = int(self.builder.get_variable('input_number').get())
        except ValueError:
            self.NUMBER_FLAG = False
            return False

        if self.n < 1 or self.n > 36:
            self.NUMBER_FLAG = False
            return False
        else:
            self.NUMBER_FLAG = True
            return True

    def mutation_rate_validate_callback(self):

        # catches if entry field is empty (default 0% mutation rate)
        try:
            self.mutation_rate = (float(self.builder.get_variable('mutation_rate').get())) / 100.0
        except ValueError:
            self.MUTATION_FLAG = False
            return False

        if(self.mutation_rate < 0 or self.mutation_rate > 100):
            self.MUTATION_FLAG = False
            return False
        else:
            self.MUTATION_FLAG = True
            return True

    def population_size_validate_callback(self):

        try:
            self.population_size = int(self.builder.get_variable('population_size').get())
        except ValueError:
            self.POPULATION_SIZE_FLAG = False
            return False

        if(self.population_size < 1 or self.population_size > 10000):
            self.POPULATION_SIZE_FLAG = False
            return False
        else:
            self.POPULATION_SIZE_FLAG = True
            return True

    def elitism_validate_callback(self):

        try:
            self.elitism = (float(self.builder.get_variable('elitism').get())) / 100.0
        except ValueError:
            self.ELITISM_FLAG = False
            return False

        if(self.elitism < 0.01 or self.elitism > 1):
            self.ELITISM_FLAG = False
            return False
        else:
            self.ELITISM_FLAG = True
            return True

    def random_problem_validate_callback(self):
        '''
        Gets problem string and then removes any space characters that are
        added when generating a problem or inputing it.
        Checks validity of our problem and sets PROBLEM_FLAG accordingly.
        '''

        self.problem = (self.builder.get_variable('random_problem').get()).replace(' ', '')

        self.progress(value=0)

        size = len(self.problem)

        if size == 0:
            self.PROBLEM_FLAG = False
            return False

        self.k = size
        input_size = self.builder.get_object('entry_input_size')
        input_size.delete('0', 'end')
        input_size.insert(0, size)

        for i in self.problem:
            if i not in self.available_symbols:
                self.PROBLEM_FLAG = False
                return False

        self.PROBLEM_FLAG = True
        return True

    def clear_problem_entry(self):
        problem = self.builder.get_object('entry_problem')
        self.output_label['text'] = ''
        problem.delete('0', 'end')
        self.PROBLEM_FLAG = False

    def progress(self, value=0):
        self.progress_bar['value'] = value
        self.progress_tracker['text'] = int(value)

    def run(self):
        self.mainwindow.mainloop()
