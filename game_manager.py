from game import Game
from game_view import GameView
from ai import AI
import pygame
import numpy as np

class GameManager(object):
	def __init__(self, ai=False):
		pygame.init()
		self.ai = ai
		if self.ai:
			self.agent = AI()
		
		self.game = Game()
		self.game_view = GameView(self.game)

		self.gameDisplay = pygame.display.set_mode((self.game.width, self.game.height))
		pygame.display.set_caption('Missiles!')

		self.clock = pygame.time.Clock()

	def launch(self):
		stop = False
		ngames = 3
		game_count = 0

		while not stop:
			self.game.reset(game_count+1)
			self.game_view.reset()
			self.game.start()
			
			nframes = 2
			last_state = None
			last_score = None
			last_action = None
			frame_count = nframes - 1
			while self.game.plane.alive:
				for event in pygame.event.get():
					if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
						self.game.plane.alive = False
						stop = True

					elif not self.ai and event.type == pygame.KEYDOWN:
						if event.key == pygame.K_q:
							self.game.plane.alive = False
							stop = True
							break
						elif event.key == pygame.K_RIGHT:
							self.game.plane.set_rotation(-1)
						elif event.key == pygame.K_LEFT:
							self.game.plane.set_rotation(1)

					elif not self.ai and event.type == pygame.KEYUP:
						if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
							self.game.plane.set_rotation(0)
				
				self.game.update()
				self.game_view.draw(self.gameDisplay)
				pygame.display.update()

				# AI managing
				frame_count += 1
				if self.ai and (frame_count == nframes or not self.game.plane.alive):
					if last_state is None:
						last_state = np.asarray(self.game_view.as_matrix(self.gameDisplay))
					else:
						state = np.asarray(self.game_view.as_matrix(self.gameDisplay))
						# diff = state - last_state
						action = self.agent.action(state)
						self.game.plane.set_rotation(action)
						if last_score is not None:
							r = 0 if self.game.plane.alive else self.game.score
							self.agent.store_transition(last_state, last_action, r, state, not self.game.plane.alive)
						
						last_score = self.game.score
						last_action = action

					frame_count = 0

				self.clock.tick(45) # 45

			if self.ai:
				self.agent.experience_replay()
				if game_count % ngames == 0:
					self.agent.transfer_to_target_network()

			game_count += 1

		pygame.quit()