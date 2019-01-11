import pickle
import gym
import gym_maze
from gym import envs
from random import randint
from random import random
from matplotlib import pyplot

class env_state:
	q_value = 0
	reward = 0

class Main:
	
	gamma = 0.9 #discount rate
	learning_rate = 0.9
	alpha = 0.9 #exploration rate
	games = 20
	actions = 4

	@staticmethod
	def main():
		Main.q_data = dict()
		Main.q_learning("maze-sample-5x5-v0")
	
	@staticmethod
	def q_learning(maze_name):
		games_steps = []
		env = gym.make(maze_name)
		count_games = 1
		while(count_games <= Main.games):
			count_steps = 1
			new_state = env.reset()
			new_state[0] = int(new_state[0])
			new_state[1] = int(new_state[1])
			while(0 != 1):
				if(count_games == Main.games):
					env.render()
					filename = str(count_steps) + ".png"
					pyplot.imshow(env.render())
					pyplot.savefig(filename)
				action = Main.best_action(new_state)	
				new_state_str = Main.state_to_str(new_state)
				old_state = []
				for num in new_state:
					old_state.append(num)
				new_state, reward, game_over, log = env.step(action)
				Main.q_data[Main.state_to_str(old_state)][action].reward = reward
				Main.update_q_data(old_state, action, reward, new_state)
				if(game_over):
					if(count_steps == 2000):
						print("Couldn't reach goal state!")
					else:
						print("Game " + str(count_games) + " Over! In " + str(count_steps) + " steps.")
					break
				count_steps = count_steps+1
			count_games = count_games+1
			Main.alpha = Main.alpha*0.30
		env.close()

	@staticmethod
	def best_action(state):
		state = Main.state_to_str(state)
		if(Main.q_data.get(state) == None):
			Main.add_state_to_q_data(state)
			return randint(0, Main.actions-1)
		# Considering exploration rate, generate a random number in range [0, 1)
		rand = random()
		if(rand <= Main.alpha):		
			return randint(0, Main.actions-1)
		return Main.action_with_max_q(state)
	
	@staticmethod
	def update_q_data(old_state, action, reward, new_state):
		old_state = Main.state_to_str(old_state)
		new_state = Main.state_to_str(new_state)
		if(Main.q_data.get(new_state) == None):
			Main.add_state_to_q_data(new_state)
		max_q_action = Main.action_with_max_q(new_state)
		max_q = Main.q_data[new_state][max_q_action].q_value
		Main.q_data[old_state][action].q_value = Main.learning_rate*(reward + (Main.gamma * max_q))

	# Given a state, it returns an action with max q value
	@staticmethod
	def action_with_max_q(state):
		env_state_objs_ = Main.q_data[state]
		ind = 0
		max_q = -99
		max_ind = -1
		while(ind < len(env_state_objs_)):
			num = env_state_objs_[ind].q_value
			if(num != 0 and num>max_q):
				max_q = num
				max_ind = ind
			ind = ind+1
		if(max_q == -99):
			max_q_action = randint(0, Main.actions-1)
		else:
			max_q_action = max_ind
		return max_q_action

	@staticmethod
	def add_state_to_q_data(state):
		# Generate a zero-initialized action_array
		action_array = []
		count = 1
		while(count <= Main.actions):
			obj = env_state()
			action_array.append(obj)
			count = count+1
		Main.q_data[state] = action_array

	# Converts the list [int_1, int_2] to the string "int_1,int_2"
	@staticmethod
	def state_to_str(state):
		return str(int(state[0])) + "," + str(int(state[1]))	

	@staticmethod
	def print_q_data(cur_state, before):
		if(before == True):
			print("====================================")
		cur_state = Main.state_to_str(cur_state)
		print("current state: " + str(cur_state))
		for key_, value_ in Main.q_data.items():
			print(key_ + ": " + str(value_))
		if(before == False):
			print("====================================")

Main.main()
