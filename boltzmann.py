from math import e
from scipy.constants import k
import numpy as np
from decimal import Decimal

# Q is list of the estimated value of choosing each action
# T is the system temperature
def boltzmann_distribution(Q, T):
    highInf = 0
    highInfIndex = -1
    # Check if any/multiple expected values would result in infinity, remember the highest
    for i,x in enumerate(Q):
        if e**(x/T) == np.Infinity and x > highInf:
            highInf = x
            highInfIndex = i

    if highInf != 0 and highInfIndex != -1:
        P[:] = 0
        P[highInfIndex] = 1
        return P

    P = [e**(x/T) for x in Q]
    # Calculate canonical partition function, divide all probabilities by it so sum <= 1
    CPF = sum(P)
    P[:] = [x / CPF for x in P]

    return P                    # Return array of probabilities

# A is list of actions, Q is estimated value of each action, T is system temperature
def selection(A, Q, T):
    return np.random.choice(A, p=boltzmann_distribution(Q, T))