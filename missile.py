import math
from tools import update_angle, rotated_rectangle_points_list

class Missile(object):
	def __init__(self, x, y, plane, speed=550, rspeed=1.2*math.pi, acc=-10, width=13, height=7):
		"""Initialize a missile

		Args:
				x (int): position of missile on x-axis
				y (int): position of missile on y-axis
				plane (Plane): the target plane
				speed (int, optional): initial speed of missile in pixels per second. Defaults to 60.
				rspeed (float, optional): rotational speed of missile in radians per second. Defaults to 2*math.pi.
				acc (float, optional): acceleration of missile in pixels per second squared. Defaults to -3.
				width (int, optional): width of missile in pixels. Defaults to 10.
				height (int, optional): height of missile in pixels. Defaults to 3.
		"""
		self.x = x
		self.y = y
		self.plane = plane
		self.speed = speed
		self.rspeed = rspeed
		self.acc = acc
		self.width = width
		self.height = height
		self.angle = 1.5 * math.pi

	def update(self, sdt):	
		self.x += sdt * self.speed * math.cos(self.angle)
		self.y -= sdt * self.speed * math.sin(self.angle)
		self.speed += sdt * self.acc

		# New angle according to plane position
		dxpm = self.plane.x - self.x
		dypm = self.y - self.plane.y
		dangle = update_angle(math.copysign(1, dypm) * math.acos(dxpm / math.sqrt(dxpm ** 2 + dypm ** 2)), -self.angle)

		if dangle > math.pi:
			dangle -= 2*math.pi
		
		mov_max = sdt * self.rspeed
		if abs(dangle) < abs(mov_max):
			shift = dangle
		else:
			shift = mov_max * math.copysign(1, dangle)
		self.angle = update_angle(self.angle, shift)

	def as_points_list(self):
		return rotated_rectangle_points_list(self.x, self.y, self.width, self.height, self.angle)