import math
from tools import update_angle, rotated_rectangle_points_list

class Plane(object):
	def __init__(self, speed=400, rspeed=1.8*math.pi, width=51, height=50):
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
		self.rotation = 0

	def reset(self):
		self.x = 0
		self.y = 0
		self.angle = 1.5 * math.pi
		self.alive = True
		self.rotation = 0

	def update(self, sdt):
		"""Update the logical state of the plane

		Args:
				sdt (int): time interval in seconds since the last logical update
		"""
		self.x += sdt * self.speed * math.cos(self.angle)
		self.y -= sdt * self.speed * math.sin(self.angle)
		self.angle = update_angle(self.angle, self.rotation * sdt * self.rspeed)

	def as_points_list(self):
		return rotated_rectangle_points_list(self.x, self.y, self.width, self.height, self.angle)

	def set_rotation(self, r):
		self.rotation = r