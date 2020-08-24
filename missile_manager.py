from missile import Missile
from tools import polygons_intersect
import time

class MissileManager(object):
	def __init__(self, spawn_time=4, min_speed=25):
		self.spawn_time = spawn_time
		self.min_speed = min_speed
		self.last_spawn = None
		self.missiles = []
		self.ncollisions = None
		self.plane_destroyed = False

		self.reset()

	def reset(self):
		self.last_spawn = None
		self.missiles = []
		self.ncollisions = None
		self.plane_destroyed = False

	def start(self, plane, height):
		self.missiles = [Missile(plane.x, plane.y - height/2)]
		self.last_spawn = time.time()

	def update(self, plane, height, sdt):
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
				if i not in to_delete and polygons_intersect(self.missiles[i].as_points_list(), plane.as_points_list()):
					self.plane_destroyed = True
					plane.alive = False
		
		self.missiles = [m for i,m in enumerate(self.missiles) if i not in to_delete]

		# Missile update
		for m in self.missiles:
			m.update(plane.x, plane.y, sdt)

		# Missile spawn
		if time.time() - self.last_spawn > self.spawn_time:
			self.missiles.append(Missile(plane.x, plane.y - height/2))

	def draw(self, display):
		pass