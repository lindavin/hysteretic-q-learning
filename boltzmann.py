from math import e
from scipy.constants import k
import numpy as np

# Q is list of the estimated value of choosing each action
# T is the system temperature
def boltzman_distribution(Q, T):
    # Populate array of action selection probabilities    
    P = []
    for i in range(len(Q)):
        P[i] = e**(Q[i]/(k*T))
    
    # Calculate canonical partition function, divide all probabilities by it so sum <= 1
    CPF = sum(P)
    P[:] = [x / CPF for x in P]
    return P                    # Return array of probabilities

# A is list of actions, Q is estimated value of each action, T is system temperature
def selection(A, Q, T):
    return np.random.choice(A, p=boltzman_distribution(Q, T))