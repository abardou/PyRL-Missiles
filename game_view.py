import pygame
from plane_view import PlaneView

class GameView(object):
	def __init__(self, game, background_color=(145, 219, 212)):
		self.game = game
		self.background_color = background_color

		self.missile_manager = self.game.missile_manager
		self.plane_view = PlaneView(self.game.plane, self.game.width, self.game.height)

	def draw(self, display):
		display.fill(self.background_color)

		self.missile_manager.draw(display)
		self.plane_view.draw(display)
