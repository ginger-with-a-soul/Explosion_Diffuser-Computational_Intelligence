import os
import pygubu
import tkinter as tk
import tkinter.ttk as ttk
import psutil  # multi-platform library for system resource usage tracking
from random import choices


PROJECT_PATH = os.path.dirname(__file__)
PROJECT_UI = os.path.join(PROJECT_PATH, "ui.ui")


class UiApp:
    def __init__(self):

        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('mainwindow')
        builder.connect_callbacks(self)

        # variable initialization
        self.k = 5
        self.n = 5
        self.problem = ''

        
        #root.tk.call locates the theme package and selects styles we wish #to use from that package
        self.theme_abs_path = os.path.abspath('awthemes-10.2.1')
        self.mainwindow.tk.call('lappend', 'auto_path', self.theme_abs_path)
        self.mainwindow.tk.call('package', 'require', 'awdark')
        self.mainwindow.tk.call('package', 'require', 'awlight')
        #to change the style we need to create an instance of 'Style' class
        self.style = ttk.Style(self.mainwindow)
        self.style.theme_use('awdark')
        #self.style.theme_use('awlight')

        self.show_resource_usage()

        #connects edit fields with their events (focus out, focus in, etc.)
        self.bind_variables()

    def brute_force_callback(self):
        pass

    def monte_carlo_callback(self):
        pass

    def genetic_algorithm_callback(self):
        pass

    def generate_problem_callback(self):
        '''
        Initializes a problem we want to solve

        Firstly generates a list of available symbols for variation to use based on n ([1, n]).
        After that it chooses randomly k elements from the list of the available symbols.
        Finally, it concatenates them and when printing in the entry box, adds a blank after
        each symbol for readabillity purposes
        '''
        entry_field = self.builder.get_object('entry_problem')
        entry_field.delete("0", "end")
        
        available_symbols = [str(x + 1) for x in range(self.n)]
        self.problem = ''.join(choices(available_symbols, k = self.k))
        print(self.problem)
        
        
        entry_field.insert(0, ' '.join(self.problem))

    def random_problem_validate_callback(self):
        pass

    def current_best_solution_validate_callback(self):
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

    def bind_variables(self):
        self.entry_input_size = self.builder.get_object('entry_input_size')
        self.entry_variation_size = self.builder.get_object('entry_input_num_of_symbols')
        self.entry_input_size.bind("<FocusOut>", self.get_size_input)
        self.entry_variation_size.bind("<FocusOut>", self.get_variation_size_input)

    def get_size_input(self, event):
        self.k = int(self.builder.get_variable('input_size').get())
    
    def get_variation_size_input(self, event):
        self.n = int(self.builder.get_variable('input_number').get())
        
    def run(self):
        self.mainwindow.mainloop()
