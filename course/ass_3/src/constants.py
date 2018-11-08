class Constants:
	iter_ = 10
	tot_cities = 7
	tot_ants = 1
	# new_pheromone = (old_pheromone(1-pherm_evap_rate)) + (q/tour_distance)
	q = 4010
	max_dist = 4000
	pherm_evap_rate = 0.1
	alpha_pherm = 0.4
	beta_visibility = 0.6
	init_pherm = 1
	vis_base = "vis/"