import random
def epsilon_greedy(epsilon):
	"""
	epsilon is the probability of taking a random action; i.e the exploration rate.
	"""
	def policy(options, values, *args):
		r = random.random()
		if(callable(epsilon)):
			e = epsilon(*args)
		else:
			e = epsilon

		if(r >= e):
			# exploit
			max_options = []
			max_value = max(values)
			for i, val in enumerate(values):
				if(val == max_value):
					max_options.append(options[i])
			return random.choice(max_options)
		else:
			# explore
			return random.choice(options)
	
	return policy