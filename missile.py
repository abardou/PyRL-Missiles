import math
from tools import update_angle, rotated_rectangle_points_list

class Missile(object):
	def __init__(self, x, y, speed=60, rspeed=2*math.pi, acc=-2.5, width=10, height=3):
		"""Initialize a missile

		Args:
				x (int): position of missile on x-axis
				y (int): position of missile on y-axis
				speed (int, optional): initial speed of missile in pixels per second. Defaults to 60.
				rspeed (float, optional): rotational speed of missile in radians per second. Defaults to 2*math.pi.
				acc (float, optional): acceleration of missile in pixels per second squared. Defaults to -3.
				width (int, optional): width of missile in pixels. Defaults to 10.
				height (int, optional): height of missile in pixels. Defaults to 3.
		"""
		self.x = x
		self.y = y
		self.speed = speed
		self.rspeed = rspeed
		self.acc = acc
		self.width = width
		self.height = height
		self.angle = 1.5 * math.pi

	def update(self, px, py, sdt):
		self.x += sdt * self.speed * math.cos(self.angle)
		self.y -= sdt * self.speed * math.sin(self.angle)
		self.speed += sdt * self.acc

		# New angle according to plane position
		angle_to_reach = math.acos((self.x - px) / math.sqrt((self.x - px) ** 2 + (self.y - py) ** 2))
		dangle = angle_to_reach - self.angle
		if dangle > math.pi:
			dangle = 2 * math.pi - dangle
		if dangle < -math.pi:
			dangle = 2 * math.pi + dangle
		self.angle = update_angle(self.angle, sdt * self.rspeed * math.copysign(1, dangle))

	def as_points_list(self):
		return rotated_rectangle_points_list(self.x, self.y, self.width, self.height, self.angle)