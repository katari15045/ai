
Assumptions:
------------
-> Ant is smart enough to not visit a node that it has already visited in the same tour.
-> Ant knows how many nodes it has visited, how many nodes to visit, so that, it comes out of the tour, when all nodes are visited.
-> Every city is connected to every other city; if you want to disconnect 2 cities, give a huge weight (distance) to the edge connecting both the cities.

Approach
--------
-> Tour of an ant: it randomly selects a city to start with. It then selects the neighbour with the highest probability (depends on pheromone_in_the_path and visibility_of_the_path (1 / length_of_path)). If there are multiple nodes with same probability, it selects a node with minimum distance. While selecting a node, an ant makes sure that it doesn't select a node that has already been visited. If it visits all the nodes (visited_nodes = total_nodes), it immediately exits from its tour.
-> All the ants make the above tour. Upon exiting from a tour, each ant updates the pheromone of all the edges that it has travelled through, using the formula - new_pheromone = (old_pheromone(1-pherm_evap_rate)) + (q/tour_distance) --- 1 iteration
-> This is repeated 'k' times i.e 'k' iterations

Observations:
-------------
All the examples given in the parenthesis like 10, 100, 1, 0.9, 0.1 etc are tested for 5-7 cities; the defenitions of low, average, high might change with no. of cities, but, the low, medium, high principles, still hold.

-> Very high pheromone_evaporation_rate (0.9) gives bad results i.e doesn't make ants to follow any specific path (all the learning is evaporated); conversely, low (0.1) pheromone_evaporation_rate is ideal to make ants to learn about shorter paths more quickly.
-> High no. of ants (100) or high no. of iterations is required for good results; the former gives quick results than the latter. However, low # of ants (1) and low # of iterations (1) gives bad results (almost no learning). Average no. of ants (10) and average no. of iterations (10) gives good results too.
-> Very low values of 'q (new_pheromone = [old_pheromone[1-pherm_evap_rate]] + [q/tour_distance])' yields bad results; a 'q' which is at least as big as 'max value of distance between any city' would give good results.
-> Less no. of cities (<= 5): would get acceptable results with less ants (1) and less iterations (1); high no. of cities (7) need more ants or more no. of iterations to get acceptable results.

Conclusion
----------
To get good results, make pheromone_evaporation_rate low (0.1), 'have as many ants as possible (>= 10) or high no. of iterations (1 of these 2 - ants, iterations would be enough)', high 'q'.
