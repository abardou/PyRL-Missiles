import pygame
from plane_view import PlaneView

class GameView(object):
	def __init__(self, game, background_color=(145, 219, 212)):
		self.game = game
		self.background_color = background_color

		self.missile_manager = self.game.missile_manager
		self.plane_view = PlaneView(self.game.plane, self.game.width, self.game.height)

		self.font = pygame.font.Font('rsc/HelveticaNeue.woff', 20)

	def reset(self):
		self.missile_manager = self.game.missile_manager
		self.plane_view = PlaneView(self.game.plane, self.game.width, self.game.height)

	def draw(self, display):
		display.fill(self.background_color)

		text = self.font.render('Game ' + str(self.game.game_count) + ' - Score: ' + str(round(self.game.score, 1)), True, (100, 100, 100))
		text_rec = text.get_rect()
		text_rec.topleft = (10, 10)
		display.blit(text, text_rec)

		self.missile_manager.draw(display)
		self.plane_view.draw(display)

	def as_matrix(self, display):
		return pygame.PixelArray(display).extract((0, 0, 0))