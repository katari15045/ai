import gym
import gym_maze
from gym import envs

class Main:

	steps = 300
	games = 1

	@staticmethod
	def main():
		env = gym.make("maze-sample-5x5-v0")
		count_games = 1
		while(count_games <= Main.games):
			count_steps = 1
			old_state = env.reset()
			while(count_steps <= Main.steps):
				env.render()
				# Randomly chooses an action
				action = env.action_space.sample()
				if(count_steps != 1):
					old_state = new_state
				new_state, reward, game_over, log = env.step(action)
				if(game_over):
					print("Game " + str(count_games) + " Over! In " + str(count_steps) + " steps.")
					break
				count_steps = count_steps+1
			count_games = count_games+1
		env.close()

	@staticmethod
	def display_available_envs():
		list_ = envs.registry.all()
		for obj in list_:
			print(obj)

Main.main()

