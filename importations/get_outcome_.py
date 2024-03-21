def get_outcome(state):
	total_reward = 0

	for i in range(0, 9):
		# Vérifie les lignes horizontales
		if i == 0 or i == 3 or i == 6:
			if state[i] == state[i + 1] and state[i] == state[i + 2]:
				total_reward = state[i]					
				break
			# Vérifie la diagonale de gauche à droite
			elif state[0] == state[4] and state[0] == state[8] and i == 0:
				total_reward = state[0]
				break
		# Vérifie les colonnes verticales
		if i < 3:
			if state[i] == state[i + 3] and state[i] == state[i + 6]:
				total_reward = state[i]					
				break
			# Vérifie la diagonale de droite à gauche
			elif state[2] == state[4] and state[2] == state[6] and i == 2:
				total_reward = state[2]
				break

	# Vérifie les lignes horizontales
	if (state[0] == state[1] == state[2]) and not state[0] == 0:
		total_reward = state[0]	
	elif (state[3] == state[4] == state[5]) and not state[3] == 0:
		total_reward = state[3]	
	elif (state[6] == state[7] == state[8]) and not state[6] == 0:
		total_reward = state[6]	
	# Vérifie les colonnes verticales
	elif (state[0] == state[3] == state[6]) and not state[0] == 0:
		total_reward = state[0]	
	# Vérifie les autres colonnes verticales
	elif (state[1] == state[4] == state[7]) and not state[1] == 0:
		total_reward = state[1]	
	elif (state[2] == state[5] == state[8]) and not state[2] == 0:
		total_reward = state[2]	
	# Vérifie les diagonales
	elif (state[0] == state[4] == state[8]) and not state[0] == 0:
		total_reward = state[0]	
	elif (state[2] == state[4] == state[6]) and not state[2] == 0:
		total_reward = state[2]

	return total_reward
