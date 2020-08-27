import pygame
import math

class MissileView(object):
	missileImg = pygame.image.load('rsc/missile.png')

	def __init__(self, missile):
		self.missile = missile
		self.missileImg = pygame.transform.scale(MissileView.missileImg, (self.missile.width, self.missile.height))

	def draw(self, display):
		gwidth, gheight = display.get_size()
		rx = self.missile.x - self.missile.plane.x + gwidth/2
		ry = self.missile.y - self.missile.plane.y + gheight/2

		mImg = pygame.transform.rotate(self.missileImg, 360 * self.missile.angle / (2 * math.pi))
		rect = mImg.get_rect(center=(rx, ry))
		display.blit(mImg, rect.topleft)