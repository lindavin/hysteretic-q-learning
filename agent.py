import numpy as np
import random
from environment import Environment


class Agent:
	def __init__(self, environment: Environment):
		self.accumulated_reward = 0
		self.environment = environment
		self.action = None
	
	def update(self, state, reward, t):
		self.accumulated_reward += reward

	def action_selection(self, state=None, t=None, possible_actions=None):
		pass

class RandomAgent(Agent):
	def __init__(self, environment):
		Agent.__init__(self, environment)
	
	def action_selection(self, state, t=None, possible_actions=None):
		return random.choice(self.environment.action_space)
	

class TDLearner(Agent):
	def __init__(self, environment, get_exploration_rate, get_learning_rate, get_discount_rate):
		Agent.__init__(self, environment)
		self.get_learning_rate = get_learning_rate
		self.get_discount_rate = get_discount_rate
		self.get_exploration_rate = get_exploration_rate

class QLearner(TDLearner):
	def __init__(self, environment, get_exploration_rate, get_learning_rate, get_discount_rate, policy=None):
		TDLearner.__init__(self, environment, get_exploration_rate, get_learning_rate, get_discount_rate)
		self.q_values = None
		self.init_action_values()
		if(policy == None):
			from policy import epsilon_greedy
			self.policy = epsilon_greedy(get_exploration_rate)

	def init_action_values(self):
		if(not(hasattr(self, "q_values")) or self.q_values != None):
			import warnings
			warnings.warn("Overriding Q-Values....")

		state_action_values = {}
		for state in self.environment.get_state_space():
			temp = {}
			for action in self.environment.action_space:
				temp[action] = 0
			state_action_values[state] = temp
		self.q_values = state_action_values

	def action_selection(self, state, t):
		action_space = self.environment.action_space
		action_values = np.zeros(len(action_space))
		for i, action in enumerate(action_space):
			action_values[i] = self.q_values[state][action]
		action = self.policy(action_space, action_values, t)
		self.action = action
		return action

	def get_q_value(self, state, action):
		return self.q_values[state][action]

	def get_max_q_value(self, state):
		return max(self.q_values[state].values())

	def set_q_value(self, state, action, new_value):
		self.q_values[state][action] = new_value

	def update(self, new_state, reward, t):
		previous_state = self.environment.previous_state
		action = self.action
		self.accumulated_reward += reward
		q_value = self.get_q_value(previous_state, action)
		target = reward + self.get_discount_rate(t) * self.get_max_q_value(new_state)
		self.set_q_value(previous_state, action, q_value + self.get_learning_rate(t) * (target - q_value))