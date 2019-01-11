q_data = []
discount_factor = 0.9
exploration_rate = 0.9
learning_rate = 0.9
games = 30

main()
	count = 1
	while(count <= games)
		# In each game, model is trained by updating q_data
		q_learning()
		count = count+1

q_learning()
	new_state = initial_state
	while true
		action = next_action(new_state)
		old_state = new_state
		new_state, reward, game_over = take_action(action)
		q_data[old_state][action].reward =reward
		if(new_state not in q_data)
			add new_state to q_data
		max_q_action = action with max_q from new_state #if q_values are not present, select the action randomly
		max_q = q_data[new_state][max_q_action].q_value
		q_data[old_state][action].q_value = learning_rate*( reward+(discount_factor*max_q) )
		if(game_over == True)
			return
		exploration_rate = exploration_rate*0.30


next_action(state)
	if(state not in q_data)
		add state to q_data
		randomly choose action & return
	rand = random()
	if(rand <= exploration_rate)
		randomly choose action & return
	return action with max_q_value among all possible actions from state


