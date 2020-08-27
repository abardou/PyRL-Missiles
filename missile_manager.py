from missile import Missile
from missile_view import MissileView
from tools import polygons_intersect
import time
import numpy as np

class MissileManager(object):
	def __init__(self, plane, spawn_time=4, min_speed=390):
		self.plane = plane
		self.spawn_time = spawn_time
		self.min_speed = min_speed
		self.last_spawn = None
		self.missiles = []
		self.missile_views = []
		self.ncollisions = None
		self.plane_destroyed = False

		self.reset()

	def reset(self):
		self.last_spawn = None
		self.missiles = []
		self.ncollisions = None
		self.plane_destroyed = False

	def start(self, height):
		self.missiles = [Missile(self.plane.x, self.plane.y - height/2, self.plane)]
		self.missile_views = [MissileView(self.missiles[0])]
		self.last_spawn = time.time()

	def update(self, width, height, sdt):
		# Check for missiles to delete
		self.ncollisions = 0

		to_delete = []
		for i,m in enumerate(self.missiles):
			if m.speed < self.min_speed:
				to_delete.append(i)

		# Check for missiles collision
		for i in range(len(self.missiles)):
			if i not in to_delete:
				# Collision with other missile
				for j in range(i+1, len(self.missiles)):
					if j not in to_delete and polygons_intersect(self.missiles[i].as_points_list(), self.missiles[j].as_points_list()):
						to_delete.append(i)
						to_delete.append(j)
						self.ncollisions += 1

				# Collision with plane
				if i not in to_delete and polygons_intersect(self.missiles[i].as_points_list(), self.plane.as_points_list()):
					self.plane_destroyed = True
					self.plane.alive = False
		
		self.missiles = [m for i,m in enumerate(self.missiles) if i not in to_delete]
		self.missile_views = [m for i,m in enumerate(self.missile_views) if i not in to_delete]

		# Missile update
		for i,m in enumerate(self.missiles):
			m.update(sdt)

		# Missile spawn
		t = time.time()
		if t - self.last_spawn > self.spawn_time:
			self.missiles.append(Missile(np.random.uniform(self.plane.x - width/2, self.plane.x + width/2), self.plane.y - height/2, self.plane))
			self.missile_views.append(MissileView(self.missiles[-1]))

			self.last_spawn = t

	def draw(self, display):
		for mv in self.missile_views:
			mv.draw(display)