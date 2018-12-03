import gym
import gym_maze
from gym import envs
from random import randint

class Main:
	
	games = 1
	steps = 300
	gamma = 0.3
	actions = 4
	goal_state = [4, 4]
	manhattan_dists_file = "manhattan_dists.csv"

	@staticmethod
	def main():
		# pre processing
		Main.q_data = dict()
		Main.manhattan_dists = []
		# start
		env = gym.make("maze-sample-5x5-v0")
		count_games = 1
		while(count_games <= Main.games):
			count_steps = 1
			new_state = env.reset()
			new_state[0] = int(new_state[0])
			new_state[1] = int(new_state[1])
			#while(count_steps <= Main.steps):
			while(0 != 1):
				Main.print_q_data(new_state, before=True)
				env.render()
				#action = env.action_space.sample()
				#action = Main.random_action(new_state)
				action = Main.best_action(new_state)
				Main.manhattan_dists.append(Main.manhattan_dist(new_state))
				old_state = []
				for num in new_state:
					old_state.append(num)
				new_state, reward, game_over, log = env.step(action)
				print("action: " + str(action))
				print("new_state: " + str(new_state))
				Main.update_q_data(old_state, action, reward, new_state)
				Main.print_q_data(new_state, before=False)
				if(game_over):
					Main.manhattan_dists.append(Main.manhattan_dist(new_state))
					print("Game " + str(count_games) + " Over! In " + str(count_steps) + " steps.")
					break
				count_steps = count_steps+1
			count_games = count_games+1
		env.close()
		Main.save_manhattan_dists()

	@staticmethod
	def best_action(state):
		state = Main.state_to_str(state)
		if(Main.q_data.get(state) == None):
			Main.add_state_to_q_data(state)
			return randint(0, Main.actions-1)
		else:
			return Main.action_with_max_q(state)
	
	@staticmethod
	def random_action(state):
		state = Main.state_to_str(state)
		if(Main.q_data.get(state) == None):
			Main.add_state_to_q_data(state)
		return randint(0, Main.actions-1)

	@staticmethod
	def update_q_data(old_state, action, reward, new_state):
		old_state = Main.state_to_str(old_state)
		new_state = Main.state_to_str(new_state)
		if(Main.q_data.get(new_state) == None):
			Main.add_state_to_q_data(new_state)
		max_q_action = Main.action_with_max_q(new_state)
		max_q = Main.q_data[new_state][max_q_action]
		Main.q_data[old_state][action] = reward + (Main.gamma * max_q)		

	@staticmethod
	def manhattan_dist(cur_state):
		x_dist = abs(cur_state[0] - Main.goal_state[0])
		y_dist = abs(cur_state[1] - Main.goal_state[1])
		return x_dist + y_dist	

	# Given a state, it returns an action with max q value
	@staticmethod
	def action_with_max_q(state):
		actions_ = Main.q_data[state]
		max_q = max(actions_)
		max_q_action = Main.q_data[state].index(max_q)
		return max_q_action

	@staticmethod
	def add_state_to_q_data(state):
		# Generate a zero-initialized action_array
		action_array = []
		count = 1
		while(count <= Main.actions):
			action_array.append(0)
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

	@staticmethod
	def save_manhattan_dists():
		book = open(Main.manhattan_dists_file, "w")
		book.write("Step (Just before step k),Manhattan Distance\n")
		ind = 0
		while(ind < len(Main.manhattan_dists)):
			manhattan_dist_ = Main.manhattan_dists[ind]
			book.write(str(ind+1) + "," + str(manhattan_dist_) + "\n")
			ind = ind+1
		book.close()

	@staticmethod
	def display_available_envs():
		list_ = envs.registry.all()
		for obj in list_:
			print(obj)

Main.main()
