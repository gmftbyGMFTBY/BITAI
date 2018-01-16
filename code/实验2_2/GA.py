#!/usr/bin/python3
# Author : GMFTBY
# Time   : 2017.1.16

'''
The GA ALgorithm for the TSP Question, use the TSPLIB Dataset

Link : 
    1. https://www.cnblogs.com 
    2. https://wiki.org

Generate Algorithm:
    1. Init the swam for the Question, decide the size of the swarm (Y) 
    2. Decide the fittness function for the agent in the swarm (Y)
    3. Decide the number of the Max-Iteration and init the current time
       Or decide the terminations. (N)
    4. Select Operator : 
        1. Create the FG(Father Group) to generate the new agents
        2. Select the SG(Surviver Group) to create the next generations
        P.S : Use the possibility to execute the Select Operator
    5. Generat Operator :
        1. Combination : Near 0.9
            The core for the Algorithm and the result
        2. Mutation    : Near 0.1
            The core operator for search the solution in the State Space
            Escape the Local Optimization
'''

import numpy as np
import random
import time
import dataset

# The point to the best agent in the history
point = True

def fittness(agent, cities_map):
    # this function calculate the fittness for the agent
    s = 0
    for i in range(agent.dimension - 1):
        s += cities_map[agent.solution[i] - 1, agent.solution[i + 1] - 1]
    return s

class agent:
    def __init__(self, dimension, cities_map, solution = None):
        self.dimension = dimension
        if solution == None:
            self.solution = np.arange(1, dimension + 1)
            # Init the agent for the swarm
            np.random.shuffle(self.solution)
        else:
            self.solution = solution.copy()    # Must be the copy
        self.fittness = fittness(self, cities_map)
    def get_fittness(self):
        return self.fittness
    
def check(sol1, sol2):
    # this function try to check and fix two solution and return the right ans
    # fix the sol1 and return sol1 !! fuck !! do not need to return 
    for i in range(len(sol1)):
        num = sol1.index(i)
        if num > 1 :
            pass

def init_swarm(size, dimension, cities_map):
    # Init the swarm for the GA
    swarm = set()
    for i in range(size):
        swarm.add(agent(dimension, cities_map))
    return swarm

def generate(agent_1, agent_2, alpha):
    # This function use two father to generate the new agent 
    
    # ---- Combination alpha % ---- #
    
    if random.random() < alpha : 
        # Possibility to combination
        pause_sol_1 = agent_1.solution.copy()
        pause_sol_2 = agent_2.solution.copy()
        # Step 1 : randomly choose **two** point to combination
        f, l = sorted(random.sample(range(agent_1.dimension - 1), 2))
        # switch 
        pause_sol_1[f + 1: l + 1], pause_sol_2[f + 1: l + 1] \
                   = pause_sol_2[f + 1: l + 1], pause_sol_1[f + 1: l + 1]
        # check pause_sol_1
        check(pause_sol_1, pause_sol_2)
        # check_pause_sol_2
        check(pause_sol_2, pause_sol_1)
    
    # ---- Mutation ---- #
    
    

if __name__ == "__main__":
    map = dataset.create_map('../DATA/berlin52.tsp')
    print(map)