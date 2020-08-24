import math
from tools import update_angle, rotated_rectangle_points_list

class Plane(object):
	def __init__(self, speed=40, rspeed=2*math.pi, width=51, height=50):
		"""Initialize the plane

		Args:
				speed (int, optional): the speed of the plane, in pixels per sec. Defaults to 40.
				rspeed (float, optional): the rotational speed of the plane, in radians per sec. Defaults to 2*math.pi.
				width (int, optional): the width of the plane, in pixels
				height (int, optional): the height of the plane, in pixels
		"""
		self.x = 0
		self.y = 0
		self.speed = speed
		self.rspeed = rspeed
		self.angle = 1.5 * math.pi
		self.width = width
		self.height = height
		self.alive = True

	def reset(self):
		self.x = 0
		self.y = 0
		self.angle = 1.5 * math.pi
		self.alive = True

	def update(self, rotation, sdt):
		"""Update the logical state of the plane

		Args:
				rotation (int): 1 for anti-clockwise rotation, -1 for clockwise rotation, 0 for no rotation
				sdt (int): time interval in seconds since the last logical update
		"""
		self.x += sdt * self.speed * math.cos(self.angle)
		self.y -= sdt * self.speed * math.sin(self.angle)
		self.angle = update_angle(self.angle, rotation * sdt * self.rspeed)
		print(sdt)

	def as_points_list(self):
		return rotated_rectangle_points_list(self.x, self.y, self.width, self.height, self.angle)