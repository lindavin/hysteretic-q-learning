from random import randint, randrange, random, sample, choice


class Environment:
    def __init__(self, search_space, action_space, start_state):
        self.search_space = search_space
        self.action_space = action_space
        self.previous_state = start_state
        self.current_state = start_state
        self.start_state = start_state

    #
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


class ClimbingGame(Environment):
    def __init__(self, part_stochastic=False, full_stochastic=False):
        Environment.__init__(self, [0, 1], ['A', 'B', 'C'], 0)

        if full_stochastic:
            self.rewards = {('A', 'A'): (10, 12), ('A', 'B'): (5, -65), ('A', 'C'): (8, -8),
                            ('B', 'A'): (5, -65), ('B', 'B'): (14, 0), ('B', 'C'): (12, 0),
                            ('C', 'A'): (8, -8), ('C', 'B'): (12, 0), ('C', 'C'): (10, 0)}

        elif part_stochastic:
            self.rewards = {('A', 'A'): (11,), ('A', 'B'): (-30,), ('A', 'C'): (0,),
                            ('B', 'A'): (-30,), ('B', 'B'): (14, 0), ('B', 'C'): (6,),
                            ('C', 'A'): (0,), ('C', 'B'): (0,), ('C', 'C'): (5,)}
        else:
            self.rewards = {('A', 'A'): 11, ('A', 'B'): -30, ('A', 'C'): 0,
                            ('B', 'A'): -30, ('B', 'B'): 7, ('B', 'C'): 6,
                            ('C', 'A'): 0, ('C', 'B'): 0, ('C', 'C'): 5}

        self.stochastic = part_stochastic or full_stochastic

        self.terminal_states = [1]

    def respond_to_action(self, action):
        """
        Updates the current the state for a given action.
        Returns reward, new_state
        """

        if self.stochastic:
            reward_tuple = self.rewards[action]
            reward = reward_tuple[randrange(0, len(reward_tuple))]
        else:
            reward = self.rewards[action]

        return reward, self.get_new_state(action)

    # Returns the new state (x, y) for a given action.
    def get_new_state(self, action, state=None):

        if state is None:
            state = self.current_state

        assert state == 0
        return 1

    def isTerminalState(self, state):
        return state in self.terminal_states


class PenaltyGame(Environment):
    def __init__(self, k):
        Environment.__init__(self, [0, 1], ['A', 'B', 'C'], 0)

        self.rewards = {('A', 'A'): 10, ('A', 'B'): 0, ('A', 'C'): k,
                        ('B', 'A'): 0, ('B', 'B'): 2, ('B', 'C'): 0,
                        ('C', 'A'): k, ('C', 'B'): 0, ('C', 'C'): 10, }

        self.terminal_states = [1]

    def respond_to_action(self, action):
        """
        Updates the current the state for a given action.
        Returns reward, new_state
        """

        reward = self.rewards[action]

        return reward, self.get_new_state(action)

    # Returns the new state (x, y) for a given action.
    def get_new_state(self, action, state=None):

        if state is None:
            state = self.current_state

        assert state == 0
        return 1

    def isTerminalState(self, state):
        return state in self.terminal_states


class Boutilier(Environment):
    def __init__(self, k, part_stochastic=False):
        Environment.__init__(self, [1, 2, 3, 4, 5, 6, 7], ['a', 'b'], 1)

        if part_stochastic:
            self.rewards = {1: (0,), 2: (0,), 3: (0,),
                            4: (11,), 5: (k,), 6: (0, 14)}
        else:
            self.rewards = {1: 0, 2: 0, 3: 0,
                            4: 11, 5: k, 6: 7}

        self.stochastic = part_stochastic
        self.terminal_states = [4, 5, 6]

    def respond_to_action(self, action):
        """
        Updates the current the state for a given action.
        Returns reward, new_state
        """

        new_state = self.get_new_state(action)

        if self.stochastic:
            reward_tuple = self.rewards[new_state]
            reward = reward_tuple[randrange(0, len(reward_tuple))]
        else:
            reward = self.rewards[new_state]

        self.current_state = new_state

        return reward, new_state

    def get_new_state(self, action, state=None):

        if state is None:
            state = self.current_state

        if state == 1:
            if action[0] == 'a':
                new_state = 2
            else:
                new_state = 3
        elif state == 2:
            if action[0] == action[1]:
                new_state = 4
            else:
                new_state = 5
        elif state == 3:
            new_state = 6
        else:
            print("Unexpected case!!!")

        return new_state

    def isTerminalState(self, state):
        return state in self.terminal_states


# Predator game helpers
def bound_coordinate(x):
    return ((x+4) % 10)-4

    # if (x < -4):
    #     dif = -4 - x
    #     assert dif == 1, f"dif is greater than 1, got: {dif}"
    #     return 5
    # elif (x > 5):
    #     dif = x - 5
    #     assert dif == 1, f"dif is greater than 1, got: {dif}"
    #     return -4
    # else:
    #     return x


def random_pos():
    while(1):
        agent1 = (randrange(-4, 6), randrange(-4, 6))
        if (agent1 != (0, 0)):
            break

    while(1):
        agent2 = (randrange(-4, 6), randrange(-4, 6))
        if (agent2 != (0, 0)) and (agent2 != agent1):
            break

    return agent1, agent2


class Predator(Environment):
    def __init__(self):
        # Set up state space
        # Every possible coordinate combination
        state_space = []
        for x1 in range(-4, 6):
            for y1 in range(-4, 6):
                for x2 in range(-4, 6):
                    for y2 in range(-4, 6):
                        state_space.append(((x1, y1), (x2, y2)))

        # Give each predator a unique starting space
        self.agent1_pos, self.agent2_pos = random_pos()
        self.supportStates = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.captureCount = 0

        Environment.__init__(self, state_space, ['left', 'right', 'up', 'down', 'stay'],
                             (self.agent1_pos, self.agent2_pos))

    def resetCaptues(self):
        self.captureCount = 0

    def isTerminalState(self, state):
        pos1 = state[0]
        pos2 = state[1]

        return (pos1 == pos2) or (pos1 == (0, 0)) or (pos2 == (0, 0))

    # Returns the new state (x, y) for a given action.
    def get_new_state(self, action, state=None, mouse_move=False):

        # Chance to make a mistake with action or mouse moves
        if (random() < 0.8) or mouse_move:
            p1_action = action[0]
        else:
            p1_action = self.action_space[randint(0, 4)]

        if (random() < 0.8) or mouse_move:
            p2_action = action[1]
        else:
            p2_action = self.action_space[randint(0, 4)]

        # Get current state and break it into coordinates
        if(state == None):
            p1_state, p2_state = self.get_state()
        else:
            p1_state, p2_state = state
        x1, y1 = p1_state
        x2, y2 = p2_state

        # Move the first agent
        if(p1_action == 'left'):
            x1 = bound_coordinate(x1-1)
        elif(p1_action == 'right'):
            x1 = bound_coordinate(x1+1)
        elif(p1_action == 'up'):
            y1 = bound_coordinate(y1+1)
        elif(p1_action == 'down'):
            y1 = bound_coordinate(y1-1)
        elif(p1_action == 'stay'):
            pass
        else:
            raise ValueError("ERROR Unknown action: {}".format(action))

        # Move the second agent
        if(p2_action == 'left'):
            x2 = bound_coordinate(x2-1)
        elif(p2_action == 'right'):
            x2 = bound_coordinate(x2+1)
        elif(p2_action == 'up'):
            y2 = bound_coordinate(y2+1)
        elif(p2_action == 'down'):
            y2 = bound_coordinate(y2-1)
        elif(p2_action == 'stay'):
            pass
        else:
            raise ValueError("ERROR Unknown action: {}".format(action))

        return ((x1, y1), (x2, y2))

    # Updates the current the state for a given action.
    # Returns reward, new_state
    def respond_to_action(self, action):

        p1_state, p2_state = self.get_new_state(action)
        reward = 0
        # If terminal state, reset positions
        if self.isTerminalState((p1_state, p2_state)):
            if ((p1_state == (0, 0) and p2_state in self.supportStates) or
                    (p2_state == (0, 0) and p1_state in self.supportStates)):
                reward = 10
                self.captureCount += 1
                # print("CAPTURED")
            else:
                reward = -50

            p1_state, p2_state = random_pos()

        # If not terminal state, mouse might move
        elif (random() > 0.2):
            moves = []
            if not (p1_state == (1, 0)) or (p2_state == (1, 0)):
                moves.append('left')
            if not (p1_state == (-1, 0)) or (p2_state == (-1, 0)):
                moves.append('right')
            if not (p1_state == (0, -1)) or (p2_state == (0, -1)):
                moves.append('up')
            if not (p1_state == (0, 1)) or (p2_state == (0, 1)):
                moves.append('down')

            mouse_action = moves[randrange(0, len(moves))]
            p1_state, p2_state = self.get_new_state(
                (mouse_action, mouse_action), mouse_move=True)

        self.current_state = (p1_state, p2_state)
        return reward, (p1_state, p2_state)


def make_grid_space(n):
    arr = []
    for i in range(n):
        for j in range(n):
            arr.append((i,j))
            
    return arr

class Predator2(Environment):
    def __init__(self, n = 10):
        state_space = []
        import math
        up_bound = math.floor(n/2)
        low_bound = math.floor(n/2) * 1
        if(n % 2 == 0):
            up_bound += 1
            low_bound += 1
        
        for x1 in range(-4, 6):
            for y1 in range(-4, 6):
                for x2 in range(-4, 6):
                    for y2 in range(-4, 6):
                        state_space.append(((x1, y1), (x2, y2)))
        self.agent1_pos, self.agent2_pos = random_pos()
        self.supportStates = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.captureCount = 0
        
        self.true_space = make_grid_space(10)
        self.current_true_state = self.get_new_true_state()
        
        
        Environment.__init__(self, state_space, ['left', 'right', 'up', 'down', 'stay'],
                             lambda: self.observe_state(self.get_new_start_state(True)))
        
    def get_new_start_state(self, set_self=False):
        new_state = self.get_new_true_state()
        if(set_self):
            self.current_true_state = new_state
        return new_state
    
    def observe_state(self, state=None):
        if state is not None:
            rel_state = self.process_states(*state)
        else:
            rel_state = self.process_states(*self.current_true_state)
        return rel_state[1], rel_state[2]
    
    def get_new_true_state(self):
        return [self.true_space[i] for i in sample(range(100), 3)]
    
    def update_ind_state(self, state, action):
        if(action == 'left'):
            return ((state[0]-1)%10, state[1])
        elif(action == 'right'):
            return ((state[0]+1)%10, state[1])
        elif(action == 'up'):
            return (state[0], (state[1] - 1)%10 )
        elif(action == 'down'):
            return (state[0], (state[1] + 1)%10 )
        elif(action == 'stay'):
            return state
        else:
            print("Unknown case!")
    
    def process_mouse_pred(self, mouse_state, single_pred_state):
        # returns the relative states        
        bound_x = (mouse_state[0] - 4, mouse_state[0] + 5)
        bound_y = (mouse_state[1] - 4, mouse_state[1] + 5)
        if(single_pred_state[0] in range(bound_x[0], bound_x[1] + 1)):
            rel_x = single_pred_state[0] - mouse_state[0]
        else:
            # print("x out")
            rel_x = ((single_pred_state[0] + 5) % 10) - ((mouse_state[0] + 5) % 10)
            
        if(single_pred_state[1] in range(bound_y[0], bound_y[1] + 1)):
            rel_y = single_pred_state[1] - mouse_state[1]
        else:
            # print("y out")
            rel_y = ((single_pred_state[1] + 5) % 10) - ((mouse_state[1] + 5) % 10)
        
        # sanity check
        if(rel_x not in range(-4, 6)):
            print("WARNING rel x not in correct bounds")
        if(rel_y not in range(-4, 6)):
            print("WARNING rel y not in correct bounds")
            
        return rel_x, rel_y
    
    def process_states(self, mouse_state, pred_one_state, pred_two_state):
        # returns the relative states        
        return (0,0), self.process_mouse_pred(mouse_state, pred_one_state), self.process_mouse_pred(mouse_state, pred_two_state)
    
    def isTerminalState(self, observable_state):
        # observable state is the two relative states
        if(observable_state[0] == observable_state[1]):
            return True
        
        return ((0, 0) == observable_state[0]) or ((0,0) == observable_state[1])

    
    def is_terminal_state(self, mouse_state, pred_one_state, pred_two_state):
        if(pred_one_state == pred_two_state):
            return True
        
        return (mouse_state == pred_one_state) or (mouse_state == pred_two_state)
    
    def resetCaptures(self):
        self.captureCount = 0
    
    def show_true_grid(self):
        import numpy as np
        grid = np.zeros((10, 10))
        mouse = self.current_true_state[0]
        pred1 = self.current_true_state[1]
        pred2 = self.current_true_state[2]
        grid[mouse[1]][mouse[0]] = -1 # mouse
        grid[pred1[1]][pred1[0]] = 1 # cat1
        grid[pred2[1]][pred2[0]]= 2 # cat2
        print(grid)
    
    def respond_to_action(self, action):
        true_pred_state  = [self.current_true_state[1], self.current_true_state[2]]
        mouse_true_state = self.current_true_state[0]
        
        if (random() >= 0.2): # predator game is stochastic 
            new_pred_state = [self.update_ind_state(state, action[i]) for i, state in enumerate(true_pred_state)]
        else:
            new_pred_state = [self.update_ind_state(state, choice(self.action_space)) for i, state in enumerate(true_pred_state)]
        
        rel_states = self.process_states(mouse_true_state, *new_pred_state)
        
        if(self.is_terminal_state(mouse_true_state, *new_pred_state)):
            # Don't update the environment state. State must reset.
            # need to distinguish crash and capture attempt for resets
            if(new_pred_state[0] == new_pred_state[1]):
                # crash!
                # print("Crash.")
                return -50, (rel_states[1], rel_states[2])
            else:
                # capture attempt
                if((rel_states[1] in self.supportStates) or (rel_states[2] in self.supportStates)):
                    # success! capture attempt with support!
                    self.captureCount += 1
                    # print("Captured!")
                    return 10, (rel_states[1], rel_states[2])
                # attempt without support!
                # print("Capture without suppport.")
                return -50, (rel_states[1], rel_states[2])
        
        # mouse moves after predators move
        if(random() >= 0.2):
            possible_new_states = []
            for action in ['left', 'right', 'up', 'down']:
                new_state = self.update_ind_state(mouse_true_state, action)
                if(new_state not in new_pred_state):
                    possible_new_states.append(new_state)
            new_mouse_state = choice(possible_new_states)
        else:
            new_mouse_state = mouse_true_state
        
        self.current_true_state = [new_mouse_state, *new_pred_state]
        rel_states = self.process_states(*self.current_true_state)
        
        return 0, (rel_states[1], rel_states[2])
    
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
        Environment.__init__(self, state_space, [
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
