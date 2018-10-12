to do
-----
0. carefully observe the grids printed for 2x2 tic tac toe; if it's X turn, consider only those configs where X is inserted; many unnecessary configs are being produced
1. node.py -> update_cost(): propagate the cost modification from the current_node (leaf) to it's ancestors, till root node; note that, user's turn is at alternate levels of the tree; maintain a var in every node mentioning whose turn it is.