from typing import List
from agent import Agent
from environment import Environment
from math import e

# system_temperature should NOT be None if it will be used in the agent#action_selection method.


def simulate_task(agents: List[Agent], task: Environment, t=0, system_temperature=None, timesteps=1000, update_agents=True, return_acc_reward=False):
    state = task.start_state() if callable(task.start_state) else task.start_state
    
    T = system_temperature

    def action_lambda(a: Agent, s, T, idx):
        #         print("agent {}".format(idx))
        return a.action_selection(s, None, T)

    while not task.isTerminalState(state) and t < timesteps:
        acc_reward = 0
#         actions = tuple((lambda a: a.action_selection(state, None, T), agents))
        actions = tuple((action_lambda(agent, state, T, idx)
                        for idx, agent in enumerate(agents)))
        if(T is not None):
            T = T * 0.99
            # T = T * (e**(-0.003))
        reward, new_state = task.respond_to_action(actions)
        if(return_acc_reward):
            acc_reward += reward
#         print("reward: {}".format(reward))
        if(update_agents):
            # allows us to perform a greedy trial to evaluate agents
            agents[0].update(state, actions[0], new_state, reward)  # , t)
            agents[1].update(state, actions[1], new_state, reward)  # , t)

        state = new_state
        t += 1
    if(return_acc_reward):
        return t, T, acc_reward
    else:
        return t, T

def find_greedy_action_for_state(agent, state):
    return max(agent.q_values[state], key=agent.q_values[state].get)