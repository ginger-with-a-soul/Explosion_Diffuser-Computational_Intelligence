import pygame
from pygame import Vector2
from os import environ
import tkinter as tk
from copy import copy
from math import sin, cos, radians
from random import uniform
from time import sleep

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

	def draw_rect(self, row_coord, col_coord, color):
		pygame.draw.rect(self.surface, color,
						 pygame.Rect(row_coord, col_coord, self.cell_size, self.cell_size), 0, 9)

	def draw_grid(self):
		position = 0
		for col in range(self.col_num):
			col_coord = self.margin_size + col * self.spacing + col * self.cell_size
			for row in range(self.row_num):

				row_coord = self.margin_size + row * self.spacing + row * self.cell_size

				if position == self.current_position and position == self.problem_position:
					self.draw_rect(row_coord, col_coord, TEAL)
				elif position == self.current_position:
					self.draw_rect(row_coord, col_coord, GREEN)
				elif position == self.problem_position:
					self.draw_rect(row_coord, col_coord, RED)
				else:
					self.draw_rect(row_coord, col_coord, BLACK)
				position += 1


class Field:

	def __init__(self, surface, num_rows, k):
		self.surface = surface
		self.num_rows = num_rows
		self.solutions = []
		self.starting_positions = []
		self.init_solutions(k)

	def init_solutions(self, k):
		cols = self.num_rows
		for r in range(self.num_rows):
			starting_x = 200 - 15 * (cols - 1)
			for c in range(cols):
				x = starting_x + 30 * c
				y = HEIGHT - 30 - r * 30
				self.solutions.append(Solution(x, y, 0, k, self.surface))
				self.starting_positions.append(Solution(x, y, 0, k, self.surface))
			cols -= 1

	def draw_field(self, ready_to_unleash, search_is_done):
		# draws the 'problem' square
		pygame.draw.rect(self.surface, RED, pygame.Rect(191, 40, 40, 40), 0, 10)
		running = False
		for s in self.solutions:
			running |= s.running

		running &= ready_to_unleash


		if running and not search_is_done:
			for s in self.solutions:
				upper_vertex = s.vertexes[3]
				# checks to see if the *pointy* part of the solutions model is out of bounds or if it hit the solutions rectangle, and stops it in its tracks if it is/did
				if upper_vertex[0] <= 0 or \
				   upper_vertex[0] >= WIDTH or \
				   upper_vertex[1] <= 0 or \
				   upper_vertex[1] >= HEIGHT or \
				   ((upper_vertex[0] >= 191 and upper_vertex[0] <= 231) and
						(upper_vertex[1] <= 80 and upper_vertex[1] >= 40)):
					s.running = False
					s.draw_solution()
				else:
					s.update_vertex_positions()
					s.draw_solution()
					# the fitness of the solution is the best possible thus solution flies straight to the goal. EVERYTHING IS COMMENTED OUT BECAUSE IT SEEMS LIKE CONSTANT USAGE OF ROTATION DRIVES OUR VECTOR TO 0 THUS REDUCING SPEED TO 0
					dice_throw_1 = uniform(0, 1)
					dice_throw_2 = uniform(0, 1)
					if s.precision == 1.0:
						...
					elif s.precision > 0.9:
						...
					elif s.precision > 0.8:
						if dice_throw_1 <= 0.04:
							s.rotate_solution(3)
						if dice_throw_2 <= 0.03:
							s.rotate_solution(-3)
					elif s.precision > 0.65:
						if dice_throw_1 <= 0.05:
							s.rotate_solution(5)
						if dice_throw_2 <= 0.05:
							s.rotate_solution(-5)
					elif s.precision > 0.5:
						if dice_throw_1 <= 0.07:
							s.rotate_solution(7)
						if dice_throw_2 <= 0.07:
							s.rotate_solution(-7)
					else:
						if dice_throw_1 <= 0.08:
							s.rotate_solution(9)
						if dice_throw_2 <= 0.08:
							s.rotate_solution(-9)

		else:
			for s in self.starting_positions:
				s.draw_solution()

		if not running and not search_is_done:
			ready_to_unleash = False
			for i in range(len(self.solutions)):

				self.solutions[i].x = copy(self.starting_positions[i].x)
				self.solutions[i].y = copy(self.starting_positions[i].y)
				self.solutions[i].fitness = copy(self.starting_positions[i].fitness)
				self.solutions[i].forward_vector = copy(self.starting_positions[i].forward_vector)
				self.solutions[i].vertexes = copy(self.starting_positions[i].vertexes)
				self.solutions[i].acceleration = copy(self.starting_positions[i].acceleration)
				self.solutions[i].precision = self.solutions[i].calculate_precision()
			ready_to_unleash = True

		return running


class Solution:

	def __init__(self, x, y, fitness, k, surface):
		self.surface = surface
		self.x = x
		self.y = y
		self.fitness = fitness
		self.k = k
		self.forward_vector = (Vector2(202, 60) - Vector2(self.x, self.y)).normalize()
		self.acceleration = 6
		self.running = False
		self.vertexes = []
		self.initiate_vertexes()
		self.precision = self.calculate_precision()

	def calculate_precision(self):
		precision = float(self.fitness / self.k)
		if precision < 0.5:
			precision = 0.5

		# initially `aims` the solution based on the precision
		coin_flip = uniform(0, 1)

		if precision == 1.0:
			...
		elif precision > 0.9:
			if coin_flip <= 0.5:
				self.rotate_solution(6)
			else:
				self.rotate_solution(-6)
		elif precision > 0.8:
			if coin_flip <= 0.5:
				self.rotate_solution(17)
			else:
				self.rotate_solution(-17)
		elif precision > 0.65:
			if coin_flip <= 0.5:
				self.rotate_solution(42)
			else:
				self.rotate_solution(-42)
		elif precision > 0.5:
			if coin_flip <= 0.5:
				self.rotate_solution(60)
			else:
				self.rotate_solution(-60)
		else:
			self.rotate_solution(180)


		self.draw_solution()
		return precision

	def initiate_vertexes(self):
		left_vertex = [self.x, self.y]
		middle_vertex = [self.x + 11, self.y - 10]
		right_vertex = [self.x + 22, self.y]
		upper_vertex = [self.x + 11, self.y - 25]
		self.vertexes.append(left_vertex)
		self.vertexes.append(middle_vertex)
		self.vertexes.append(right_vertex)
		self.vertexes.append(upper_vertex)

	def draw_solution(self):
		pygame.draw.polygon(self.surface, GREEN, [self.vertexes[0], self.vertexes[1], self.vertexes[2], self.vertexes[3]], 0)

	def update_vertex_positions(self):
		'''
		This function changes the position of our solutions model by adding appropriate x and y coordinate change to the current x and y coordinates of each vertex.
		'''
		for v in self.vertexes:

			self.forward_vector.normalize_ip()
			change_x = self.acceleration * self.forward_vector.x
			change_y = self.acceleration * self.forward_vector.y

			v[0] += change_x
			v[1] += change_y



	def rotate_solution(self, angle):
		angle = radians(angle)
		# the rotation is done around the upper_vertex and that is self.vertex[3]
		rotated_vertexes = []
		c = cos(angle)
		s = sin(angle)

		self.forward_vector.rotate_ip_rad(angle)

		for vertex in self.vertexes:

			tmp_point = vertex[0] - self.vertexes[3][0], vertex[1] - self.vertexes[3][1]
			tmp_point = tmp_point[0] * c - tmp_point[1] * s, \
				tmp_point[0] * s + tmp_point[1] * c
			tmp_point = tmp_point[0] + self.vertexes[3][0], tmp_point[1] + self.vertexes[3][1]

			rotated_vertexes.append(list(tmp_point))

		self.vertexes = rotated_vertexes[:]


class Visualizer:
	def __init__(self, caption, mode, k):
		self.done = False
		self.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.NOFRAME, vsync=1)
		pygame.display.set_caption(caption)
		self.clock = pygame.time.Clock()
		self.FPS = 30
		self.field = None
		self.grid = None
		self.mode = mode
		# used to signal visualizer that a new wave of units can be set off
		self.ready_to_unleash = False
		if self.mode == "gen_algo":
			self.field = Field(self.surface, 5, k)
		elif self.mode == "brute_algo":
			self.grid = Grid(self.surface, 10, 16, 35, 5, 7)
		# 'done' flag is used for the loop, if we were to use that as an indicator, when we set this flag to True when a solution gets to the goal, our window would close immediately and we don't want that. This flag is just used to indicate when can we start another generation in genetic algorithm
		self.running = False

	def run(self, search_is_done):
		while not self.done:
			self.surface.fill(BLUISH)

			for event in pygame.event.get():
				if event.type == pygame.QUIT or \
						(event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					self.done = True

			if self.mode == 'brute_algo':
				self.grid.draw_grid()
			elif self.mode == 'gen_algo':
				self.running = self.field.draw_field(self.ready_to_unleash, search_is_done)

			pygame.display.flip()
			self.clock.tick(self.FPS)

		pygame.quit()

	def close(self):
		pygame.quit()
