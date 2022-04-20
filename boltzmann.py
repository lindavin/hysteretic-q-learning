from math import e
from scipy.constants import k
import numpy as np
from decimal import Decimal

# Q is list of the estimated value of choosing each action
# T is the system temperature
def boltzmann_distribution(Q, T):
    # Populate array of action selection probabilities    
    #P = []
    #for i in range(len(Q)):
    #    P[i] = e**(Q[i]/(k*T))
    
    # DOn't know python does this work
    P = Q
    # Decimal to avoid overflow errors
    # P[:] = [(Decimal(e)**(Decimal(x)/(Decimal(k)*Decimal(T)))) for x in P]
    # Remove k constant to again avoid overflow errors
    P[:] = [(Decimal(e)**(Decimal(x)/(Decimal(T)))) for x in P]
    print("P1: {}".format(P))
    # Calculate canonical partition function, divide all probabilities by it so sum <= 1
    CPF = sum(P)
    print("CPF: {}".format(CPF))
    P[:] = [Decimal(x) / Decimal(CPF) for x in P]
    print("P2: {}".format(P))

    return P                    # Return array of probabilities

# A is list of actions, Q is estimated value of each action, T is system temperature
def selection(A, Q, T):
    print("calling boltzmann")
    return np.random.choice(A, p=boltzmann_distribution(Q, T))