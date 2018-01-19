#!/usr/bin/python3
# Author : GMFTBY
# Time   : 2017.1.19

# tanh is used for the equlation function

from math import tanh
import random

class HopfieldNet:
    def __init__(self, matrix):
        # matrix is the cities_map of the TSP Problem
        
        # the punishment coordinates of the HNN
        self.a = 500
        self.b = 500
        self.c = 200
        self.d = 300
        
        self.u0 = 0.02
        self.timestep = 0.000001
        
        # distances is the cities_map
        self.distances = matrix
        # the dimension of the problem
        self.size = len(matrix)
        
        # Init the neure for the Hopfield Network
        self.inputs = self.init_inputs()

    def init_inputs(self):
        # Init the neure, and uniform the init state of each neure
        base = 1 / (self.size ** 2)
        init = []
        for x in range(0, self.size):
            row = []
            for y in range(0, self.size):
                row.append(base + random.uniform(- base / 10, base / 10))
            init.append(row)
        return init

    def activation(self, input):
        # return the state of the neure
        #   1. Big than the sigmoid thread, active
        #   2. Small than the sigmoid thread, None
        sigm = 0.5 * (1 + tanh(input / self.u0))
        activ = 0 if sigm < 0.2 else sigm
        activ = 1 if sigm > 0.8 else activ
        return activ

    def get_a(self, city, position):
        sum = 0.0
        for pos in range(0, self.size):
            sum += self.activation(self.inputs[city][pos])
        sum -= self.activation(self.inputs[city][position])
        return sum * self.a

    def get_b(self, mainCity, position):
        sum = 0.0
        for city in range(0, self.size):
            sum += self.activation(self.inputs[city][position])
        sum -= self.activation(self.inputs[mainCity][position])
        return sum * self.b

    def get_c(self):
        sum = 0.0
        for city in range(0, self.size):
            for pos in range(0, self.size):
                sum += self.activation(self.inputs[city][pos])
        sum -= self.size + 5
        return sum * self.c

    def get_d(self, mainCity, position):
        sum = 0.0
        for city in range(0, self.size):
            sum += self.distances[mainCity][city] \
                   * (self.activation(self.inputs[city][(position + 1) % self.size])
                      + self.activation(self.inputs[city][(position - 1) % self.size]))

        return sum * self.d

    def get_new_state(self, city, pos):
        # use the state before to change the next state
        new_state = -self.inputs[city][pos]
        new_state -= self.get_a(city, pos)
        new_state -= self.get_b(city, pos)
        new_state -= self.get_c()
        new_state -= self.get_d(city, pos)
        return new_state

    def update(self):
        # update the Hopfield Network
        statesChange = []

        for city in range(0, self.size):
            row = []
            for pos in range(0, self.size):
                row.append(self.timestep * self.get_new_state(city, pos))
            statesChange.append(row)

        for city in range(0, self.size):
            for pos in range(0, self.size):
                self.inputs[city][pos] += statesChange[city][pos]


    def EnergyToAddress(self):
        activations = []
        for x in range(0, self.size):
            row = []
            for y in range(0, self.size):
                act = self.activation(self.inputs[x][y])
                sign = 1 if act > 0.75 else 0
                row.append(sign)
            activations.append(row)

        return activations

    def HopfieldValidTest(self, array):
        # Test the valid of the result
        #   1. Valid   : True
        #   2. Unvalid : False
        
        # Test for the row
        for row in range(self.size):
            column_sum = 0.0
            for column in range(self.size):
                column_sum += array[row][column]
            if column_sum != 1:
                return False
            else:
                continue
            
        # Test for the column
        for column in range(self.size):
            row_sum = 0.0
            for row in range(self.size):
                row_sum += array[row][column]
            if row_sum != 1:
                return False
            else:
                continue
            
        return True

if __name__ == "__main__":
    instance = HopfieldNet([[1,2],[2,1]])
    print(instance.EnergyToAddress())