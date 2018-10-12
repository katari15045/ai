to do
-----
1. node.py -> update_cost(): propagate the cost modification from the current_node (leaf) to it's ancestors, till root node; note that, user's turn is at alternate levels of the tree; maintain a var in every node mentioning whose turn it is.

2. To update ancestors' cost from leaf nodes, maintain a variable called 'no_of_children_updated' in each node; if len(children) == 'no_of_children_updated' then you can update the weight of parent; 

3. A node might have multiple parents i.e if you encounter duplicate grids then your child would be the existing grid (instead of expanding same grid multiple times, expand only once and point multiple nodes to that single expansion, in case of duplicates). while updating the weights of ancestors, some nodes' costs are not updated - those nodes whose children has a duplicate grid