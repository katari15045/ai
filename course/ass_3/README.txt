1. To run the code, "cd src/" and type "python main.py" on cmd; if your system uses Python2 for "python main.py", run it with "python3 main.py"

2. To make ants to select a particular node at the start of a tour (instead of random selection), pass "random=False" to the method "Aco.move_ant()" and set the "start_city" (0 to n-1, for n cities) accordingly in "constants.py"; default behaviour: random=True

3. To print the output on the console, pass "verbose=False" to "Aco.start()" method; default behaviour: verbose=False

4. Network Diagrams (src/vis/*.png): the value on each edge represents the distance between 2 cities; the width of an edge represents the pheromone level along the path (wider the edge, more pheromone it has)