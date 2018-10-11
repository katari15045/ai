from node import node

'''
Assumptions:
	1st Player: X - user
	2nd Player: O - computer
	Grid: dim x dim matrix
'''

class main:
	grid = [['X', 'O', 'X'], ['O', 'X', 'O'], ['O', 'X', 'X']]
	node_ = node(grid)
	is_complete_, player = node_.is_complete()
	print(str(is_complete_) + " : " + player)

main()