from typing import List
from agent import Agent
from environment import Environment

# system_temperature should NOT be None if it will be used in the agent#action_selection method.
def simulate_task(agents: List[Agent], task: Environment, t = 0, system_temperature = None):
    state = task.start_state
    T = system_temperature
    def action_lambda(a: Agent, s, T, idx):
#         print("agent {}".format(idx))
        return a.action_selection(s, None, T)
    
    while not task.isTerminalState(state):
        t += 1
#         actions = tuple((lambda a: a.action_selection(state, None, T), agents))
        actions = tuple((action_lambda(agent, state, T, idx) for idx, agent in enumerate(agents)))
        if(T is not None):
            T = T * 0.99
        reward, new_state = task.respond_to_action(actions)
#         print("reward: {}".format(reward))
        agents[0].update(state, actions[0], new_state, reward) #, t)
        agents[1].update(state, actions[1], new_state, reward) #, t)
        
        state = new_state
    return t, T
