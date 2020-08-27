from plane import Plane
from missile_manager import MissileManager
import time
import copy
import pprint

class Game(object):
	def __init__(self, width=400, height=600):
		self.width = width
		self.height = height
		self.start_time = None
		self.duration = None
		self.score = None
		self.game_count = 1

		self.reset()

	def reset(self, game_count=1):
		self.plane = Plane()
		self.missile_manager = MissileManager(self.plane)
		self.start_time = None
		self.duration = None
		self.score = None
		self.game_count = game_count

	def update(self):
		t = time.time()
		sdt = t - self.last_update
		self.plane.update(sdt)
		self.missile_manager.update(self.width, self.height, sdt)

		self.score += t - self.last_update + 10 * self.missile_manager.ncollisions

		self.last_update = t

	def start(self):
		self.start_time = time.time()
		self.missile_manager.start(self.height)
		self.last_update = self.start_time
		self.score = 0
	
	def end(self):
		self.duration = time.time() - self.start_time

	# def as_matrix(self, rad):
	# 	matrix = []
	# 	missiles = copy.deepcopy(self.missile_manager.missiles)
	# 	j = 0
	# 	while j * rad < self.height:
	# 		line = []
	# 		i = 0
	# 		while i * rad < self.width:
	# 			to_del = []
	# 			line.append(0)
	# 			for k,m in enumerate(missiles):
	# 				x = m.x - self.plane.x + self.width/2
	# 				y = m.y - self.plane.y + self.height/2
	# 				if x >= i * rad and x < (i+1) * rad and y >= j * rad and y < (j+1) * rad:
	# 					line[-1] += 1
	# 					to_del.append(k)

	# 			missiles = [m for m in missiles if k not in to_del]
	# 			i += 1

	# 		matrix.append(line)
	# 		j += 1

	# 	return matrix