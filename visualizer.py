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

	def __init__(self, surface, num_solutions):
		self.surface = surface
		self.num_solutions = num_solutions
		self.solutions = []

	def draw_field(self):
		# draws the 'problem' square
		pygame.draw.rect(self.surface, RED, pygame.Rect(186, 50, 50, 50), 0, 0)

class Solution:

	def __init__(self, x, y, fitness):
		self.x = x
		self.y = y
		self.fitness = fitness


class Visualizer:
	def __init__(self):
		self.done = False
		self.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.NOFRAME, vsync=1)
		pygame.display.set_caption('Brute-Force algorithm')
		self.clock = pygame.time.Clock()
		self.FPS = 60
		self.grid = Grid(self.surface, 10, 16, 35, 5, 7)
		self.field = Field(self.surface, 6)
		self.mode = None

	def run(self):
		while not self.done:
			self.surface.fill(BLUISH)

			for event in pygame.event.get():
				if event.type == pygame.QUIT or \
    	                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					self.done = True

			if self.mode == 'GRID':
				self.grid.draw_grid()
			elif self.mode == 'FIELD':
				self.field.draw_field()

			pygame.display.flip()
			self.clock.tick(self.FPS)

		pygame.quit()

	def close(self):
		pygame.quit()
