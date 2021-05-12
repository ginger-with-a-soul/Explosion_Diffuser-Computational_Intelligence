import pygame
from os import environ
import tkinter as tk

# TRIES to reposition the visualizer window
environ['SDL_VIDEO_WINDOW_POS'] = str(950) + ',' + str(0)

WIDTH = 422
HEIGHT = 675

BLACK = (20, 20, 23)
GRAY = (51, 56, 50)
WHITE = (218, 222, 217)
BLUISH = (56, 60, 71)
RED = (209, 35, 23)
GREEN = (18, 181, 9)
TEAL = (52, 227, 201)


class Grid:

	def __init__(self, surface, row_num, col_num, cell_size, margin_size, spacing):
		self.surface = surface
		self.row_num = row_num
		self.col_num = col_num
		self.cell_size = cell_size
		self.margin_size = margin_size
		self.spacing = spacing
		self.problem_position = 0
		self.current_position = 0

	def draw_grid(self):
		position = 0
		for col in range(self.col_num):
			col_coord = self.margin_size + col * self.spacing + col * self.cell_size
			for row in range(self.row_num):

				row_coord = self.margin_size + row * self.spacing + row * self.cell_size

				if position == self.current_position and position == self.problem_position:
					pygame.draw.rect(self.surface, TEAL,
                                    pygame.Rect(row_coord, col_coord, self.cell_size, self.cell_size), 0, 9)
				elif position == self.current_position:
					pygame.draw.rect(self.surface, GREEN,
                                    pygame.Rect(row_coord, col_coord, self.cell_size, self.cell_size), 0, 9)
				elif position == self.problem_position:
					pygame.draw.rect(self.surface, RED,
                                    pygame.Rect(row_coord, col_coord, self.cell_size, self.cell_size), 0, 9)
				else:
					pygame.draw.rect(self.surface, BLACK, \
                                            pygame.Rect(row_coord, col_coord, self.cell_size, self.cell_size), 0, 9)
				position += 1



class Field:

	def __init__(self, surface, num_rows):
		self.surface = surface
		self.num_rows = num_rows
		self.solutions = []
		self.starting_positions = []
		self.init_solutions()

	def init_solutions(self):
		cols = self.num_rows
		for r in range(self.num_rows):
			starting_x = 200 - 15 * (cols - 1)
			for c in range(cols):
				x = starting_x + 30 * c
				y = HEIGHT - 30 - r * 30
				self.solutions.append(Solution(x, y, 0, self.surface))
				self.starting_positions.append(Solution(x, y, 0, self.surface))
			cols -= 1

	def draw_field(self):
		# draws the 'problem' square
		pygame.draw.rect(self.surface, RED, pygame.Rect(186, 50, 50, 50), 0, 0)
		running = False
		for s in self.solutions:
			running = running or s.running

		if running:
			for s in self.solutions:
				# checks to see if the *pointy* part of the solutions model is out of bounds or if it hit the solutions rectangle, and stops it in its tracks if it is/did
				if s.upper_vertice[0] <= 0 or \
				   s.upper_vertice[0] >= WIDTH or \
				   s.upper_vertice[1] <= 0 or \
				   s.upper_vertice[1] >= HEIGHT or \
				   ((s.upper_vertice[0] >= 186 and s.upper_vertice[0] <= 236) and \
					(s.upper_vertice[1] <= 100 and s.upper_vertice[1] >= 50)):
					s.running = False
					s.update_vertice_positions(0, 0)
				else:
					s.update_vertice_positions(0, -s.speed)
		else:
			for s in self.starting_positions:
				s.update_vertice_positions(0, 0)

		if not running:
			for i in range(len(self.solutions)):
				self.solutions[i].x = self.starting_positions[i].x
				self.solutions[i].y = self.starting_positions[i].y
				self.solutions[i].fitness = self.starting_positions[i].fitness
				self.solutions[i].speed = self.starting_positions[i].speed

		return running


class Solution:

	def __init__(self, x, y, fitness, surface):
		self.surface = surface
		self.x = x
		self.y = y
		self.fitness = fitness
		self.speed = 10
		self.running = False
		self.update_vertice_positions(0, 0)

	def draw_solution(self):
		pygame.draw.polygon(self.surface, GREEN, [self.left_vertice, self.middle_vertice, self.right_vertice, self.upper_vertice], 0)

	def update_vertice_positions(self, x_change, y_change):
		'''
		This function changes the position of our solutions model by adding appropriate x and y coordinate change to our current x and y coordinates.
		'''
		self.x += x_change
		self.y += y_change
		self.left_vertice = (self.x, self.y)
		self.middle_vertice = (self.x + 11, self.y - 10)
		self.right_vertice = (self.x + 22, self.y)
		self.upper_vertice = (self.x + 11, self.y - 25)
		self.draw_solution()


class Visualizer:
	def __init__(self, caption, mode):
		self.done = False
		self.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.NOFRAME, vsync=1)
		pygame.display.set_caption(caption)
		self.clock = pygame.time.Clock()
		self.FPS = 60
		self.field = None
		self.grid = None
		self.mode = mode
		if self.mode == "gen_algo":
			self.field = Field(self.surface, 5)
		elif self.mode == "brute_algo":
			self.grid = Grid(self.surface, 10, 16, 35, 5, 7)
		# 'done' flag is used for the loop, if we were to use that as an indicator, when we set this flag to True when a solution gets to the goal, our window would close immediately and we don't want that. This flag is just used to indicate when can we start another generation in genetic algorithm
		self.running = False

	def run(self):
		while not self.done:
			self.surface.fill(BLUISH)

			for event in pygame.event.get():
				if event.type == pygame.QUIT or \
    	                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					self.done = True

			if self.mode == 'brute_algo':
				self.grid.draw_grid()
			elif self.mode == 'gen_algo':
				self.running = self.field.draw_field()

			pygame.display.flip()
			self.clock.tick(self.FPS)


		pygame.quit()

	def close(self):
		pygame.quit()
