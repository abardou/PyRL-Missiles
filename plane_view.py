import pygame
import math

class PlaneView(object):
	planeImg = pygame.image.load('rsc/plane.png')

	def __init__(self, plane, gwidth, gheight):
		self.plane = plane
		self.gwidth = gwidth
		self.gheight = gheight

		self.planeImg = pygame.transform.scale(PlaneView.planeImg, (self.plane.width, self.plane.height))

	def draw(self, display):
		print(self.plane.x, self.plane.y)
		pImg = pygame.transform.rotate(self.planeImg, 360 * self.plane.angle / (2 * math.pi))
		rect = pImg.get_rect(center=(self.gwidth/2, self.gheight/2))
		display.blit(pImg, rect.topleft)