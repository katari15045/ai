import pickle
import gym
import gym_maze
from gym import envs
from random import randint
from random import random

class env_state:
	q_value = 0
	reward = 0

class Main:
	
	gamma = 0.9 #discount rate
	learning_rate = 0.9
	alpha = 0.9 #exploration rate
	games = 20
	steps = 300
	actions = 4
	goal_state = [4, 4]
	state_1 = "2,2"
	state_2 = "3,3"
	manhattan_dists_file = "manhattan_dists.csv"
	q_data_file = "q_data.pkl"

	@staticmethod
	def main():
		# Training the model
		rewards_sum, games_steps, alphas, action_arr_1, action_arr_2 = Main.q_learning(False, "maze-sample-5x5-v0", False)
		Main.state_analysis(action_arr_1, action_arr_2)
		avg_steps = sum(games_steps)/len(games_steps)
		print("===========================================================================")
		print("Sum of Rewards in the last game to reach goal state: " + str(rewards_sum))
		print("Steps taken to reach goal state: " + str(games_steps))
		print("Average steps taken: " + str(avg_steps))
		print("Exploration Rate in each game: " + str(alphas))

		# testing on a new grid
		Main.q_data = Main.load_pickle(Main.q_data_file)
		Main.q_learning(False, "maze-random-5x5-v0", True)
		#Main.display_available_envs()

	@staticmethod
	def q_learning(display, maze_name, test):
		# pre processing
		if(test == False):
				Main.q_data = dict()
		else:
			Main.games = 1
		Main.manhattan_dists = []
		games_steps = []
		alphas = []
		action_arr_1_2d = []
		action_arr_2_2d = []
		# start
		env = gym.make(maze_name)
		count_games = 1
		while(count_games <= Main.games):
			#print("(alpha, gamma, learning_rate) : " + str(Main.alpha) + ", " + str(Main.gamma) + ", " + str(Main.learning_rate))
			alphas.append(round(Main.alpha, 3))
			count_steps = 1
			rewards_sum = 0
			action_arr_1 = []	
			action_arr_2 = []
			new_state = env.reset()
			new_state[0] = int(new_state[0])
			new_state[1] = int(new_state[1])
			#while(count_steps <= Main.steps):
			while(0 != 1):
				#Main.print_q_data(new_state, before=True)
				if(display == True):
					env.render()
				#action = env.action_space.sample()
				#action = Main.random_action(new_state)
				action = Main.best_action(new_state)	
				# Analysing 2 states
				new_state_str = Main.state_to_str(new_state)
				if(new_state_str == Main.state_1):
					action_arr_1.append(action)
				elif(new_state_str == Main.state_2):
					action_arr_2.append(action)
				old_state = []
				for num in new_state:
					old_state.append(num)
				new_state, reward, game_over, log = env.step(action)
				if(count_games == Main.games):
					if(count_steps == 1):
						print("Reward: " + str(reward))
					Main.manhattan_dists.append(Main.manhattan_dist(new_state))
				rewards_sum = rewards_sum+reward
				Main.q_data[Main.state_to_str(old_state)][action].reward = reward
				#print("action: " + str(action))
				#print("new_state: " + str(new_state))
				Main.update_q_data(old_state, action, reward, new_state)
				#Main.print_q_data(new_state, before=False)
				if(game_over):
					games_steps.append(count_steps)
					if(count_steps == 2000):
						print("Couldn't reach goal state!")
					else:
						print("Game " + str(count_games) + " Over! In " + str(count_steps) + " steps.")
					break
				count_steps = count_steps+1
			count_games = count_games+1
			Main.alpha = Main.alpha*0.30
			action_arr_1_2d.append(action_arr_1)
			action_arr_2_2d.append(action_arr_2)
		env.close()
		Main.save_manhattan_dists()
		if(test == False):
			Main.dump_pickle(Main.q_data, Main.q_data_file)
		return rewards_sum, games_steps, alphas, action_arr_1_2d, action_arr_2_2d

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
		max_q = Main.q_data[new_state][max_q_action].q_value
		Main.q_data[old_state][action].q_value = Main.learning_rate*(reward + (Main.gamma * max_q))

	@staticmethod
	def manhattan_dist(cur_state):
		x_dist = abs(cur_state[0] - Main.goal_state[0])
		y_dist = abs(cur_state[1] - Main.goal_state[1])
		return x_dist + y_dist	

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

	@staticmethod
	def state_analysis(actions_1, actions_2):
		Main.write_to_csv(actions_1, "state_analysis_1.csv", Main.state_1)
		Main.write_to_csv(actions_2, "state_analysis_2.csv", Main.state_2)

	@staticmethod
	def write_to_csv(data, filename, state):
		book = open(filename, "w")
		state_arr = state.split(",")
		row = state_arr[0]
		col = state_arr[1]
		book.write("Actions selected at state " + str(row) + "|" + str(col) + "\n")
		ind = 0
		while(ind < len(data)):
			action = data[ind]
			action = str(action)
			action = action.replace(",", "|")
			book.write(str(action) + "\n")
			ind = ind+1
		book.close()

	@staticmethod
	def dump_pickle(data, filename):
		book = open(filename, "wb")
		pickle.dump(data, book)
		book.close()

	@staticmethod
	def load_pickle(filename):
		book = open(filename, "rb")
		data = pickle.load(book)
		book.close()
		return data

Main.main()