def one_hot(state):
	"""
	Convertit l'état du jeu en une représentation one-hot.

	Args:
		state (list): L'état actuel du jeu représenté par une liste d'entiers.

	Returns:
		list: L'état du jeu converti en représentation one-hot.

	"""
	current_state = []

	for square in state:
		if square == 0:
			current_state.append(1)
			current_state.append(0)
			current_state.append(0)
		elif square == 1:
			current_state.append(0)
			current_state.append(1)
			current_state.append(0)
		elif square == -1:
			current_state.append(0)
			current_state.append(0)
			current_state.append(1)

	return current_state
