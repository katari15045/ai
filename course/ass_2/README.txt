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

2. Before expanding any node, make sure current_node's parent has a constraint, else, pruning is not possible; consider the nearest ancestor from the current node, that has constraints; for pruning to be possible, the constraints of parent_node and the nearest ancestor node should be disjoint sets. For example, consider, parent has at most -4 and the nearest ancestor has constraints at least 3; [-infinity, -4] and [3, infinity] are disjoint sets i.e they never satisfy each other. So, don't expand the node - prune the tree. If the constraints of overlap, then you MUST expand the current node; time complexity in finding the farthest ancestor with constraints from current node is O(Depth of tree); in most cases, depth is less when compared with no. of nodes.

3. When it is User's turn, he/she tries to maximize the cost i.e given a child, user makes 'at least' constraint. Computer minimizes the cost of a node, given the cost of a child node, computer makes 'at most' constraint.

4. When ever you assign a cost to a node, update the constraint of it's parent.

5. Instead of just overriding the parent's cost who has at least constraint, update only if the new value is more than the existing one; when parent has at most constraint, update only if new value is less than the old value
