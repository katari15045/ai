to do
-----

Minimax
-------
1. node.py -> update_cost(): propagate the cost modification from the current_node (leaf) to it's ancestors, till root node; note that, user's turn is at alternate levels of the tree; maintain a var in every node mentioning whose turn it is.

2. To update ancestors' cost from leaf nodes, maintain a variable called 'no_of_children_updated' in each node; if len(children) == 'no_of_children_updated' then you can update the weight of parent; 

3. A node might have multiple parents i.e if you encounter duplicate grids then your child would be the existing grid (instead of expanding same grid multiple times, expand only once and point multiple nodes to that single expansion, in case of duplicates). while updating the weights of ancestors, some nodes' costs are not updated - those nodes whose children has a duplicate grid; maintain multiple parents for each node; parent, other_parents.

Alpha Beta Pruning
------------------
1. Each node of the tree has 2 constraints - at_least and at_most; also maintain 2 booleans - at_least_valid, at_most_valid; this is because you should not mistakenly assume the default values of at_least and at_most as real constraints.

2. Before expanding any node, check if it's parent and grand parent (both) have constarints; if yes, for example, consider, parent has at most -4 and grand parent has at least 3; [-infinity, -4] and [3, infinity] are disjoint sets i.e they never satisfy each other. So, don't expand the node - prune the tree. If at least one of parent and grand parent doesn't have any constraint, then you SHOULD expand the current node. Also, if the constraints of parent and grand parent overlap, then you MUST expand the current node.

3. When it is User's turn, he/she tries to maximize the cost i.e given a child, user makes 'at least' constraint. Computer minimizes the cost of a node, given the cost of a child node, computer makes 'at most' constraint.

4. When ever you assign a cost to a node, update the constraint of it's parent.
