from plane import Plane
from missile_manager import MissileManager
import time

class Game(object):
	def __init__(self, width=800, height=1000):
		self.width = width
		self.height = height
		self.start_time = None
		self.duration = None

		self.reset()

	def reset(self):
		self.plane = Plane()
		self.missile_manager = MissileManager()
		self.start_time = None
		self.duration = None

	def update(self):
		t = time.time()
		sdt = t - self.last_update
		self.plane.update(0, sdt)
		self.missile_manager.update(self.plane, self.height, sdt)

		self.last_update = t

	def start(self):
		self.start_time = time.time()
		self.missile_manager.start(self.plane, self.height)
		self.last_update = self.start_time
	
	def end(self):
		self.duration = time.time() - self.start_time