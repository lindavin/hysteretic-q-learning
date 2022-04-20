from agent import TDLearner
import numpy as np

class HystereticQLearner(TDLearner):
	def __init__(self, environment, get_exploration_rate, get_learning_rate, get_discount_rate, get_decrease_rate, policy=None):
		TDLearner.__init__(self, environment, get_exploration_rate,
						   get_learning_rate, get_discount_rate)
		self.q_values = None
		self.get_decrease_rate = get_decrease_rate
		self.init_action_values()

		if(policy == None):
			from policy import epsilon_greedy
			self.policy = epsilon_greedy(get_exploration_rate)
		else:
			self.policy = policy

	def get_q_value(self, state, action):
		return self.q_values[state][action]

	def get_max_q_value(self, state):
		return max(self.q_values[state].values())

	def set_q_value(self, state, action, new_value):
		self.q_values[state][action] = new_value

	def update(self, state, action_taken, new_state, reward, t = None):
		# TODO Hysteretic QLearner
		self.accumulated_reward += reward
		old_action_value = self.get_q_value(state, action_taken)
		delta = reward + self.get_discount_rate(t)*(self.get_max_q_value(new_state)) - old_action_value
		new_action_value = old_action_value + delta*(self.get_learning_rate(t) if delta >= 0 else self.get_decrease_rate(t))
		self.set_q_value(state, action_taken, new_action_value)

	def init_action_values(self):
		if(not(hasattr(self, "q_values")) or self.q_values != None):
			import warnings
			warnings.warn("Overriding Q-Values....")

		state_action_values = {}
		environment = self.environment
		for state in environment.get_state_space():
			temp = {}
			action_space = environment.get_action_space()
			possible_actions = action_space if not callable(action_space) else action_space(state)
			for action in possible_actions:
				temp[action] = 0
			state_action_values[state] = temp
		self.q_values = state_action_values

	def action_selection(self, state=None, possible_actions=None, *args, print_actions=False, **kwargs):
		action_space = self.environment.get_action_space()
		temp = action_space if not callable(action_space) else action_space(state)
		possible_actions = possible_actions if possible_actions is not None else temp
  
		action_values = np.zeros(len(possible_actions))

		for i, action in enumerate(possible_actions):
			action_values[i] = self.q_values[state][action]
		if(print_actions):
			print("possible_actions: {}".format(possible_actions))
			print("action_values: {}".format(action_values))
		return self.policy(possible_actions, action_values, *args, **kwargs)
