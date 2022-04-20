from random import randint, randrange
from collections import defaultdict


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


class ClimbingGame(Environment):
    def __init__(self):
        Environment.__init__(self, [0, 1], ['A', 'B', 'C'], 0)
        self.rewards = {('A', 'A'): 11, ('A', 'B'): -30, ('A', 'C'): 0,
                        ('B', 'A'): -30, ('B', 'B'): 7, ('B', 'C'): 6,
                        ('C', 'A'): 0, ('C', 'B'): 0, ('C', 'C'): 5, }
        self.terminal_states = 1

    def respond_to_action(self, action):
        """
        Updates the current the state for a given action.
        Returns reward, new_state
        """

        reward = self.rewards[action]

        return reward, 1

    def get_new_state(self, action, state=None):
        """
        Returns the new state (x, y) for a given action.
        """
        return 1

    def isTerminalState(self, state):
        return state == 1


class Boutilier(Environment):
    def __init__(self, k):
        Environment.__init__(self, [1, 2, 3, 4, 5, 6, 7], ['a', 'b'], 1)

        self.rewards = defaultdict(lambda: 0)
        self.rewards[4] = 11
        self.rewards[5] = 6
        self.rewards[6] = 7

        # {4: 11, 5: k, 6: 7}
        # self.k = k

        self.agent1_action = None
        self.agent2_action = None

        self.terminal_states = [4, 5, 6, 7]

    def respond_to_action(self, action):
        """
        Updates the current the state for a given action.
        Returns reward, new_state
        """

        new_state = self.get_new_state(action)
        reward = self.rewards[new_state]

        self.current_state = new_state

        # if self.current_state == 1:
        #     self.agent1_action = action[0]
        #     self.agent2_action = action[1]
        #     if self.agent1_action == 'a':
        #         new_state = 2
        #         reward = 0
        #     elif self.agent1_action == 'b':
        #         new_state = 3
        # elif self.current_state == 2:
        #     if (self.agent1_action == 'a') and (self.agent2_action == 'a') and (action[0] == 'b') and (action[1] == 'b'):
        #         new_state = 4
        #         reward = 11
        #     elif (self.agent1_action == 'a') and (self.agent2_action == 'b') and (action[0] == 'b') and (action[1] == 'a'):
        #         new_state = 5
        #         reward = self.k
        #     else:
        #         new_state = 7
        #         reward = 0
        # elif self.current_state == 3:
        #     new_state = 6
        #     reward = 7

        return reward, new_state

    def get_new_state(self, action, state=None):
        if self.current_state == 1:
            self.agent1_action = action[0]
            self.agent2_action = action[1]
            if self.agent1_action == 'a':
                new_state = 2
            elif self.agent1_action == 'b':
                new_state = 3
        elif self.current_state == 2:
            if (self.agent1_action == 'a') and (self.agent2_action == 'a') and (action[0] == 'b') and (action[1] == 'b'):
                new_state = 4
            elif (self.agent1_action == 'a') and (self.agent2_action == 'b') and (action[0] == 'b') and (action[1] == 'a'):
                new_state = 5
            else:
                new_state = 7
        elif self.current_state == 3:
            new_state = 6

        return new_state

    def isTerminalState(self, state):
        return state in self.terminal_states


class Predator(Environment):
    # WORK IN PROGRESS
    def __init__(self, n, start_state, terminal_states):
        search_space = []
        for i in range(n * n):
            x = i // n
            y = i % n
            search_space.append((x, y))
        Environment.__init__(self, search_space, [
            'left', 'right', 'up', 'down', 'stay'], start_state)
        self.prey = (randrange(0, n), randrange(0, n))
        while(1):
            self.pred1 = (randrange(0, n), randrange(0, n))
            if (self.pred1 != self.prey):
                break
        while(1):
            self.pred2 = (randrange(0, n), randrange(0, n))
            if (self.pred2 != self.prey) and (self.pred2 != self.pred1):
                break

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
            x -= 1
        elif(action == 'right'):
            x += 1
        elif(action == 'up'):
            y -= 1
        elif(action == 'down'):
            y += 1
        elif(action == 'stay'):
            pass
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


class GridWorld(Environment):
    def __init__(self, n, start_state, terminal_states):
        """
        Initializes a GridWorld environment, whose search space is a list of tuples from the range (0, n-1) to... (n-1, n-1) and whose
        action space is the list ["left", "right", "up", "down"].
        start_state: a tuple in the search_space that is the start_state for the agent.
        terminal_states: a list of tuples in the search space that represent the terminal states for the environment.
        """
        search_space = []
        for i in range(n * n):
            x = i // n
            y = i % n
            search_space.append((x, y))
        Environment.__init__(self, search_space, [
                             'left', 'right', 'up', 'down'], start_state)
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
            x -= 1
        elif(action == 'right'):
            x += 1
        elif(action == 'up'):
            y -= 1
        elif(action == 'down'):
            y += 1
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
