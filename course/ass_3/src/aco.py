from constants import Constants
from graph import Graph
from random import randint

# Graph is fully connected
class Aco:

	@staticmethod
	def start():
		Graph.init()
		count = 1
		while(count <= Constants.iter_):
			Aco.epoch()
			Graph.draw(Constants.vis_base + str(count) + ".png")
			count = count+1

	@staticmethod
	def epoch():
		count = 1
		while(count <= Constants.tot_ants):
			Aco.move_ant()
			count = count+1

	@staticmethod
	def move_ant():
		# The cities are appended based on the visiting order, which, gives the edges too
		visited_cities = []
		# Randomly select start node
		start_city = randint(0, Constants.tot_cities-1)
		cur_city = start_city
		tour_dist = 0
		# Visit all the nodes
		while(True):
			visited_cities.append(cur_city)
			next_city_, dist_ = Aco.next_city(cur_city, visited_cities)
			tour_dist = tour_dist+dist_
			if(next_city_ == -1):
				break
			cur_city = next_city_
		# Update Pheromone of those edges which are visited by the ant
		ind = 0
		while(ind < (len(visited_cities)-1)):
			city_1 = visited_cities[ind]
			city_2 = visited_cities[ind+1]
			cur_pheromone = Graph.edge(city_1, city_2).pheromone
			Graph.edge(city_1, city_2).pheromone = ((1-Constants.pherm_evap_rate)*cur_pheromone) + (Constants.q/tour_dist)
			ind = ind+1

	@staticmethod
	def next_city(cur_city, visited_cities):
		if(len(visited_cities) == Constants.tot_cities):
			return -1, -1
		city = 0
		max_proba = -1
		next_city_ = -1
		proba_list = []
		dist_list = []
		while(city < Constants.tot_cities):
			if(city != cur_city and city not in visited_cities):
				proba, dist = Aco.get_proba_cum_dist(cur_city, city)
				proba_list.append(proba)
				dist_list.append(dist)
			else:
				proba_list.append(-1)
				dist_list.append(-1)
			city = city+1
		# Choose the city with max proba
		max_proba = max(proba_list)
		# Check if there is more that 1 city with max proba
		count = 0
		for proba in proba_list:
			if(proba == max_proba):
				count = count+1
		# If yes, choose the city with max_proba and min_dist
		if(count > 1):
			ind = 0
			min_dist = max(dist_list)
			min_city = -1
			while(ind < len(dist_list)):
				cur_dist = dist_list[ind]
				cur_proba = proba_list[ind]
				if(cur_proba == max_proba):
					if(cur_dist < min_dist):
						min_dist = cur_dist
						min_city = ind
				ind = ind+1
			return min_city, min_dist
		else:
			next_city_ = proba_list.index(max_proba)
			dist_ = dist_list[next_city_]
			return next_city_, dist_

	@staticmethod
	def  get_proba_cum_dist(start_city, end_city):
		# Note: only numerator is calculated, because, during comparision, denominator is always same.
		pheromone = Graph.edge(start_city, end_city).pheromone
		dist = Graph.edge(start_city, end_city).len_
		proba = (pheromone ** Constants.alpha_pherm)*((1/dist) ** Constants.beta_visibility)
		return proba, dist
