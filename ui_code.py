import os
import pygubu
import tkinter as tk
import tkinter.ttk as ttk
import psutil  # multi-platform library for system resource usage tracking
from random import choices
from string import ascii_lowercase # used to generate a list of available symbols


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

        # variable initialization
        self.k = 5
        self.n = 5
        self.problem = ''
        self.available_symbols = list(ascii_lowercase) + [str(i) for i in range(10)]
        print(len(self.available_symbols))

        self.show_resource_usage()

        self.bind_validation()



    def theme(self):
        #root.tk.call locates the theme package and selects styles we wish #to use from that package
        self.theme_abs_path = os.path.abspath('awthemes-10.2.1')
        self.mainwindow.tk.call('lappend', 'auto_path', self.theme_abs_path)
        self.mainwindow.tk.call('package', 'require', 'awdark')
        self.mainwindow.tk.call('package', 'require', 'awlight')
        #to change the style we need to create an instance of 'Style' class
        self.style = ttk.Style(self.mainwindow)
        self.style.theme_use('awdark')
        #self.style.theme_use('awlight')


    def brute_force_callback(self):
        pass

    def monte_carlo_callback(self):
        pass

    def genetic_algorithm_callback(self):
        pass

    def generate_problem_callback(self):
        '''
        Initializes the problem we want to solve.

        It firstly selects a list of available symbols for variation
        to use based on n. After that it randomly chooses k elements from
        the list of available symbols. Finally, it concatenates them and
        when printing it in the entry box, adds a blank after each symbol
        for readabillity purposes.
        '''
        entry_field = self.builder.get_object('entry_problem')
        entry_field.delete("0", "end")
        
        self.problem = ''.join(choices(self.available_symbols[0:self.n], k = self.k))
        
        entry_field.insert(0, ' '.join(self.problem))


    def random_problem_validate_callback(self):
        pass

    def current_best_solution_validate_callback(self):
        pass

    def mutation_rate_validate_callback(self):
        pass

    def start_callback(self):
        pass

    def change_theme_callback(self):
        if self.style.theme_use() == 'awdark':
            self.style.theme_use('awlight')
        else:
            self.style.theme_use('awdark')


    def show_resource_usage(self):
        self.builder.get_variable('cpu_usage').set(psutil.cpu_percent())
        self.builder.get_variable('memory_usage').set(psutil.virtual_memory().percent)
        #updates usage stats every 1000ms
        self.mainwindow.after(1000, self.show_resource_usage)

    def bind_validation(self):
        '''
        Binds entry fields with their tkinter objects and
        enables user input validation for those objects.
        '''

        entry_input_size = self.builder.get_object('entry_input_size')
        entry_variation_size = self.builder.get_object('entry_input_num_of_symbols')

        
        self.register_validation(tk.Entry(entry_input_size), self.input_size_validate_callback)
        self.register_validation(tk.Entry(entry_variation_size), self.input_number_validate_callback)

    def register_validation(self, entry, callback):
        '''
        Registers validation function (binds each variable to its
        validate function).
        '''
        # reg is the name of our callback function
        reg = entry.register(callback)
        entry.config(validate = "focusout", validatecommand = (reg, '% P'))

    def input_size_validate_callback(self):
        self.k = int(self.builder.get_variable('input_size').get())
        if self.k < 1 or self.k > 16:
            return False
        else:
            return True

    def input_number_validate_callback(self):
        self.n = int(self.builder.get_variable('input_number').get())
        if self.n < 1 or self.n > 36:
            return False
        else:
            return True
        
    def run(self):
        self.mainwindow.mainloop()
