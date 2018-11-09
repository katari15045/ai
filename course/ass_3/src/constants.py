class Constants:
	iter_ = 2
	tot_cities = 6
	tot_ants = 6
	# new_pheromone = (old_pheromone(1-pherm_evap_rate)) + (q/tour_distance)
	q = 4001
	max_dist = 4000
	pherm_evap_rate = 0.1
	alpha_pherm = 0.9
	beta_visibility = 1.3
	init_pherm = 1
	vis_base = "vis/"
	# only when random=False is passed to Aco.move_ant()
	start_city = 0