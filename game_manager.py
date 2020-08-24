from game import Game
from game_view import GameView
import pygame

class GameManager(object):
	def __init__(self):
		self.game = Game()
		self.game_view = GameView(self.game)

		pygame.init()
		self.gameDisplay = pygame.display.set_mode((self.game.width, self.game.height))
		pygame.display.set_caption('Missiles!')

		self.clock = pygame.time.Clock()

	def launch(self):
		self.game.start()
		
		while self.game.plane.alive:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.game.plane.alive = False
					break
			
			self.game.update()
			self.game_view.draw(self.gameDisplay)
			pygame.display.update()

			self.clock.tick(60)

		pygame.quit()