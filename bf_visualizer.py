import pygame
from os import environ

# TRIES to reposition the visualizer window
environ['SDL_VIDEO_WINDOW_POS'] = str(950) + ',' + str(40)


WIDTH = 422
HEIGHT = 675


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


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

				if position == self.problem_position:
					pygame.draw.rect(self.surface, RED,
                                    pygame.Rect(row_coord, col_coord, self.cell_size, self.cell_size), 0, 6)
				elif position == self.current_position:
					pygame.draw.rect(self.surface, GREEN,
                                            pygame.Rect(row_coord, col_coord, self.cell_size, self.cell_size), 0, 6)
				else:
					pygame.draw.rect(self.surface, BLACK, \
                                            pygame.Rect(row_coord, col_coord, self.cell_size, self.cell_size), 1, 6)
				position += 1



class Visualizer:
	def __init__(self):
		self.done = False
		self.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.NOFRAME, vsync=1)
		pygame.display.set_caption('Brute-Force algorithm')
		self.clock = pygame.time.Clock()
		self.FPS = 60
		self.grid = Grid(self.surface, 10, 16, 35, 5, 7)

	def run(self):
		print(self.grid.problem_position)
		while not self.done:
			self.surface.fill(WHITE)

			for event in pygame.event.get():
				if event.type == pygame.QUIT or \
    	                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					self.done = True

			self.grid.draw_grid()

			pygame.display.flip()
			self.clock.tick(self.FPS)

		pygame.quit()

	def close(self):
		pygame.quit()
