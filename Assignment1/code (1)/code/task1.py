"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the base Algorithm class that all algorithms should inherit
from. Here are the method details:
    - __init__(self, num_arms, horizon): This method is called when the class
        is instantiated. Here, you can add any other member variables that you
        need in your algorithm.
    
    - give_pull(self): This method is called when the algorithm needs to
        select an arm to pull. The method should return the index of the arm
        that it wants to pull (0-indexed).
    
    - get_reward(self, arm_index, reward): This method is called just after the 
        give_pull method. The method should update the algorithm's internal
        state based on the arm that was pulled and the reward that was received.
        (The value of arm_index is the same as the one returned by give_pull.)

We have implemented the epsilon-greedy algorithm for you. You can use it as a
reference for implementing your own algorithms.
"""

import numpy as np
import math
# Hint: math.log is much faster than np.log for scalars

class Algorithm:
    def __init__(self, num_arms, horizon):
        self.num_arms = num_arms
        self.horizon = horizon
    
    def give_pull(self):
        raise NotImplementedError
    
    def get_reward(self, arm_index, reward):
        raise NotImplementedError

# Example implementation of Epsilon Greedy algorithm
class Eps_Greedy(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # Extra member variables to keep track of the state
        self.eps = 0.1
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
    
    def give_pull(self):
        if np.random.random() < self.eps:
            return np.random.randint(self.num_arms)
        else:
            return np.argmax(self.values)
    
    def get_reward(self, arm_index, reward):
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value


# START EDITING HERE
# You can use this space to define any helper functions that you need
def binarysearch(p,u,t):
    c = 3 # constant 
    precision = 1e-3
    begin = p
    end = 1  # since q lies in [p,1]
    rhs = (math.log(t)+c*math.log(math.log(t)))/u # right hand side of the equation
    mid = (begin+end)/2
    
    while np.abs(begin-end)>precision:
        # print(1-p,1-mid)
        kl = p*math.log((p*1000)/(mid*1000)+1e-9) + (1-p)*math.log(((1-p)*1000)/((1-mid)*1000)+1e-9) # kl divergence
        if (kl > rhs): # if kl > rhs, then q is too small
            end = mid
        else:
            begin = mid # if kl < rhs, then q is too large
        mid = (begin+end)/2
    return mid
    
# END EDITING HERE

class UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.t = -1
        self.u = np.zeros(num_arms)
        self.p = np.zeros(num_arms)
        self.ucb = np.zeros(num_arms)
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        self.t += 1
        if(self.t < self.num_arms):
            return self.t
        else:
            return np.argmax(self.ucb)
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.u[arm_index] += 1
        n = self.u[arm_index]
        p_old = self.p[arm_index]
        p_new = ((n - 1) / n) * p_old + (1 / n) * reward
        self.p[arm_index] = p_new
        if(self.t >= self.num_arms):
            for i in range(self.num_arms):
                self.ucb[i] = self.p[i] + math.sqrt((2*math.log(self.t))/self.u[i])        
        # END EDITING HERE

class KL_UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.t = -1
        self.p = np.zeros(num_arms)
        self.u = np.zeros(num_arms)
        self.kl_ucb = np.zeros(num_arms)
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        if(self.t < self.num_arms):
            return self.t
        else:
            return np.argmax(self.kl_ucb)
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.t += 1
        self.u[arm_index] += 1
        n = self.u[arm_index]
        p_old = self.p[arm_index]
        p_new = ((n - 1) / n) * p_old + (1 / n) * reward
        self.p[arm_index] = p_new
        
        if(self.t >= self.num_arms):
            for i in range(self.num_arms):
                self.kl_ucb[i] = binarysearch(self.p[i],self.u[i],self.t)
        
        # END EDITING HERE


class Thompson_Sampling(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.s = np.zeros(num_arms)
        self.f = np.zeros(num_arms)
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        temp = np.zeros(self.num_arms)
        for i in range(self.num_arms):
            temp[i] = np.random.beta(self.s[i]+1,self.f[i]+1)
        return np.argmax(temp)
        
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        if(reward == 1):
            self.s[arm_index]+=1
        else:
            self.f[arm_index]+=1
            
        # END EDITING HERE
