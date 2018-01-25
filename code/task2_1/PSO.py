#!/usr/bin/python3
# Author : GMFTBY
# Time   : 2017.1.15

# The PSO Algorithm for the TSP Problem
# For my algorithm in the frame of the PSO, I allow that the exchange steps canbe changed dynamically in the period of the optimizing.

import glob
import numpy as np
import random

# this variable is just for the comparation at the last
global_max = np.inf

def find_exchenger(X, Y):
    # calculate the exchange between the X and Y
    # return the list of the tuple for exchange
    current = 0
    length  = len(X)
    YY = list(Y.copy())

    exchanger = []

    while current != length:
        x_c     = X[current]    # the current element
        y_c     = YY.index(x_c)    # the index of the x_c in the YY
        if y_c != current:
            # need to change
            exchanger.append((y_c, current))

            # debug for YY
            YY[y_c], YY[current] = YY[current], YY[y_c]
        current += 1

    # debug for YY
    # print('check for the same YY and X', YY, X)
    # Inorder to make the program right, the return must have the value, so I add the [0, 0] to the result
    if exchanger == [] : 
        exchanger.append([0, 0])
    return exchanger

def exchange(X, Y):
    # this fucntion try to change the solution X with the operator Y
    # the change will hold on for the X 
    # The X is a ndarray(1) of the solution and the Y is a list of the tuple which contain e the exchange index for two elements
    for i in Y:
        x, y = i
        X[x], X[y] = X[y], X[x]
    return 

class agent:
    def __init__(self, idnumber, dimension, start_exchange_length, cities_map):
        # the exchange stragites promise that the result is right
        self.id = idnumber
        self.dimension = dimension
        self.solution  = np.array(range(1, self.dimension + 1))
        self.start_exchange_length = start_exchange_length

        # random solution for the agent
        np.random.shuffle(self.solution)

        # random exchange operator for the agent (PSO)
        self.exchange = []
        for i in range(start_exchange_length):
            self.exchange.append(list(np.random.choice(range(dimension), 2)))
        self.exchange = np.array(self.exchange)

        # pbset
        self.pbest = self.calculate(cities_map)
        self.pbest_origin = self.solution.copy()    # it must be the copy for the solution

        # current solution
        self.current = self.pbest

        # print('Init for the agent %d is over !' % self.id)
        # may want to print something to debug
        # pass

    def move(self):
        # change the solution
        exchange(self.solution, self.exchange)
        '''
        if len(self.exchange) > self.start_exchange_length:
            mask = sorted(random.sample(range(len(self.exchange)), self.start_exchange_length))
            self.exchange = self.exchange[mask]
        '''
        # print('agent %d has chenged the solution !' % self.id)

    def calculate(self, cities_map):
        # calculate the result for this agent's solution and return 
        s = 0
        for i in range(self.dimension - 1):
            s += cities_map[self.solution[i] - 1, self.solution[i + 1] - 1]
        s += cities_map[self.solution[-1] - 1, self.solution[0] - 1]
        return s

    def find_pbest(self, cities_map):
        result = self.calculate(cities_map)
        if result < self.pbest:
            self.pbest = result
            self.pbest_origin = self.solution.copy()    # it must be the copy
        

class swarm:
    def __init__(self, dimensions, dimension, start_exchange_length, cities_map, ab):
        # dimensions is the number of the agent in the PSO
        # alpha is the exchenger possibility for the pbset, and beta is for gbest
        global global_max
        self.dimensions = dimensions
        self.dimension  = dimension
        self.agents     = []
        self.ab         = ab
        # create the agents for the swarm
        for i in range(self.dimensions):
            self.agents.append(agent(i, dimension, start_exchange_length, cities_map))
        self.gbest      = np.inf
        self.gbest_id   = -1
        self.find_gbest()    # init the gbest and the gbest_id
        global_max = self.gbest     # save the first result into the global var

        print("Init for swarm is over !")
        # may want to print something for debuging 
    
    def find_gbest(self):
        for i in range(self.dimensions):
            if self.gbest > self.agents[i].pbest:
                # renew the gbest abd the 
                self.gbest_id = self.agents[i].id
                self.gbest    = self.agents[i].pbest

    def change_agent(self, agent):
        # change all the agent in the swarm once
        # find the exchanger from pbest and gbest
        # may be the [[0, 0]]
        pbest_influence = np.array(find_exchenger(agent.pbest_origin, agent.solution))
        # may be very larger !!
        gbest_influence = np.array(find_exchenger(self.agents[self.gbest_id].pbest_origin , agent.solution))

        # print(pbest_influence, len(pbest_influence))
        # print(gebst_influence, len(gbest_influence))
        alpha = np.random.random()
        
        # Ignore the [] for the length_pbest_influence
        # length_pbest_influence = max(int(len(pbest_influence) * alpha), 1)
        # length_gbest_influence = max(int(len(gbest_influence) * (1 - alpha)),  1)
    
        try:
            # the parament for balancing the alpha and beta 
            # If alpha > 0.5 : attend to search the gbest more
            # Else : attend to search the pbest more
            # self.ab = 0.42 - 10971 / 1000, 200, 10
            if alpha > self.ab : 
                length_pbest_influence = min(agent.start_exchange_length, len(pbest_influence))
                pmask = sorted(random.sample(range(len(pbest_influence)), \
                                             length_pbest_influence))
                agent.exchange = np.concatenate((pbest_influence[pmask], \
                                                 agent.exchange), axis = 0)
            else:
                length_gbest_influence = min(agent.start_exchange_length, len(gbest_influence))
                pmask = sorted(random.sample(range(len(gbest_influence)), \
                                             length_gbest_influence))
                agent.exchange = np.concatenate((gbest_influence[pmask], \
                                                 agent.exchange), axis = 0)
            mask = sorted(random.sample(range(len(agent.exchange)), \
                                        agent.start_exchange_length))
            agent.exchange = agent.exchange[mask]
        except Exception as e:
            # show the debug message 
            print(e)
            exit(1)

        agent.move()
        # print('Move for agent %d is over !' % agent.id)
        return

    def change_swarm(self, i, cities_map):
        # change the gbest and pbest for the swarm
        for index in range(len(self.agents)):
            self.change_agent(self.agents[index])    # change the agent
            self.agents[index].find_pbest(cities_map)          # agent renew the pbest
        self.find_gbest()                            # swam renew the gbest
        # print('The change in the loop %d is over !' % i ,end = '\r')
        return self.gbest, self.agents[self.gbest_id].pbest_origin


def ECU_2D(x1, y1, x2, y2):
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        
def create_map(filename):
    cities = []
    with open(filename, 'r') as f:
        dimension = 0
        for index, line in enumerate(f.readlines()):
            if 'EOF' in line : break
            if index == 3 : 
                dimension = int(line[11:-1].strip())
                print('Problem\'s dimension is %d' % dimension)
            if index >= 6 :
                content = tuple(map(float, line.split()))
                cities.append(content)
        print('%d cities / %d dimension' % (len(cities), dimension))
    cities_number = len(cities)
    cities_map = np.zeros([cities_number, cities_number])
    # create the distance map for the cities
    # this sentence may be very slow
    for i in range(cities_number):
        for j in range(cities_number):
            if j == i : continue
            else:
                cities_map[i, j] = ECU_2D(cities[i][1], cities[i][2], \
                        cities[j][1] ,cities[j][2])
    print('The distance map has been created !')
    # return the distance ndarray
    return cities_map, dimension

def run(cities_map, dimension, times, dimensions, length, ab):
    # run one test file in tsplib ('./DATA/berlin52.tsp' / ...)
    
    # Get the paraments 
    # times = int(input('The number of the iterations : '))
    # dimensions = int(input('The size of the swarm : '))
    # the length influence the result, because the length is toolarge may cause
    # cause the result too unstable, but the result is too small cause that
    # converging is too slow, but we can add the iterations times to fix this disadvantages
    # length = int(input('The size of the vel\'s length : '))
    # ab     = float(input('The alpha & beta param for balancing : '))

    # create the swarm, 1000, 200, 10
    global swarm
    global global_result
    swarm_instance = swarm(dimensions, dimension, length, cities_map, ab)
    for i in range(times):
        j, k = swarm_instance.change_swarm(i, cities_map)
        yield i, j, k
        # print('Calculating ... %f' % (i / times, ), end='\r')
    # print('The iteration is over ! And we get the gbest solution !')
    # print('The best solution is from %d agent' % swarm_instance.gbest_id)
    # print('Before iteration : %f, after iteration : %f' % (global_max, swarm_instance.gbest))
    # print('Time cost %f' % round(end - begin, 2))
    
    # Reninit the global_max
    # return swarm_instance.gbest

if __name__ == "__main__":
    # Do not waste the time for fix the paraments of the iterations and size of swarm
    # And the start_exchange_length But it actually worth ? and effecient ? 
    # test for debuging , easy test
    
    min_ab     = -1
    min_result = np.inf
    cities_map, dimension = create_map('../DATA/berlin52.tsp')
    result = run(cities_map, dimension, 1000, 200, 10, ab)
    for i in result:
        print(i)
    
    # 1000, 200, 10, 0.42, 10 times solve the avg
    '''
    opt = np.inf
    for i in range(10):
        opt = min(run('./DATA/berlin52.tsp', 1000, 200, 10, 0.42), opt)
    print("0.42(opt) :", opt)
    '''
