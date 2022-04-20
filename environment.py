class Environment:
	def __init__(self, search_space, action_space, start_state):
		self.search_space = search_space
		self.action_space = action_space
		self.previous_state = start_state
		self.current_state = start_state
		self.start_state = start_state
	
	def respond_to_action(self, action):
		pass

	def get_search_space(self):
		return self.search_space

	def get_state_space(self):
		return self.search_space

	def get_action_space(self):
		return self.action_space

	def get_new_state(self, action):
		pass

	def get_reward(self, action):
		pass

	def get_state(self):
		return self.current_state
	
	def reset_state(self):
		self.previous_state = self.start_state
		self.current_state = self.start_state

class GridWorld(Environment):
	def __init__(self, n, start_state, terminal_states):
		"""
		Initializes a GridWorld environment, whose state space is a list of tuples from the range (0, n-1) to... (n-1, n-1) and whose
		action space is the list ["left", "right", "up", "down"].
		start_state: a tuple in the state_space that is the start_state for the agent.
		terminal_states: a list of tuples in the state space that represent the terminal states for the environment.
		"""
		state_space = []
		for i in range(n * n):
			x = i // n
			y = i % n
			state_space.append((x, y))
		Environment.__init__(self, state_space, ['left', 'right', 'up', 'down'], start_state)
		self.terminal_states = terminal_states
		self.n = n

	def respond_to_action(self, action):
		"""
		Updates the current the state for a given action.
		Returns reward, new_state
		"""
		self.previous_state = self.current_state
		new_state = self.get_new_state(action)
		if(new_state in self.terminal_states):
			reward = 1
		else:
			reward = -1
		self.current_state = new_state
		return reward, new_state

	def get_new_state(self, action, state=None):
		"""
		Returns the new state (x, y) for a given action.
		"""
		if(state == None):
			x, y = self.get_state()
		else:
			x, y = state
		if(action == 'left'):
			x-=1
		elif(action == 'right'):
			x+=1
		elif(action == 'up'):
			y-=1
		elif(action == 'down'):
			y+=1
		else:
			raise ValueError("ERROR Unknown action: {}".format(action))

		n = self.n

		if(x < 0):
			x = 0
		elif(x >= n):
			x = n - 1

		if(y < 0):
			y = 0
		elif(y >= n):
			y = n - 1

		return (x, y)
	
	def isTerminalState(self, state):
		return state in self.terminal_states