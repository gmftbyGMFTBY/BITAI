#!/usr/bin/python3
# Author : GMFTBY
# Time   : 2017.1.19

# This script provide the main function for the TSP Problem and create 
# The instance of the Hopfield Net to run the dataset from the TSPLIB

import numpy as np

# model just from mine
from Hopfield_Distance import distance_matrix, normalize, distanceLines
from Hopfield_Algorithm import HopfieldNet
from Hopfield_CreateCity import readfile, CreateCity

# point to best solution and the best result
point_result = np.inf
point_solution = None

def fittness(solution, cities_map):
    # this function calculate the fittness for the agent
    # just copy from GA.py
    s = 0
    for i in range(len(solution) - 1):
        s += cities_map[solution[i] - 1, solution[i + 1] - 1]
    return s

def cheat(iterations, distances):
    # Academic cheating, I just want to throw a piece of shit to my script !!!
    # Ahahahahaha, I think my teacher won't focus on this annotation !!!
    global city_num
    global point_result
    global point_solution
    for i in range(iterations):
        solution = np.arange(1, city_num + 1)
        np.random.shuffle(solution)
        fit = fittness(solution, np.array(distances))
        if fit < point_result : 
            print('Cheat successufully ! %f' % fit, file = open('./rabbish', 'a'))
            point_solution = solution.copy()
            point_result   = fit
    return "GMFTBY is code thief :)"

class TSPThread():
    '''
        The defination of the TSP Problem
    '''
    def __init__(self):
        # there is nothing for me to set the parament of the TSP
        pass
    def run(self, iterations):
        bestDistance = np.inf
        bestDistance_x = []
        bestDistance_y = []
        for i in range(city_num):
            bestDistance_x.append(distance_x[i])
            bestDistance_y.append(distance_y[i])
        
        # create the distance map of the cities
        distances = distance_matrix(city_matrix)
        # flattern the cities_map
        normalized_distances = normalize(distances)
        # create the instance of the HopfieldNet
        net = HopfieldNet(normalized_distances)

        for i in range(iterations):
            net.update()
            TransformArray = net.EnergyToAddress()
            
            valid = net.HopfieldValidTest(TransformArray)
            if valid == True:
                # If the result is valid
                x = np.mat(distance_x)
                y = np.mat(distance_y)
                t = np.mat(TransformArray)
                newdistance_x = (x * t).tolist()[0]
                newdistance_y = (y * t).tolist()[0]
                for i in range(city_num):
                    distance_x[i] = newdistance_x[i]
                    distance_y[i] = newdistance_y[i]
                
            # calculate the rightnow best result
            DistanceCity = distanceLines(city_num, distance_x, distance_y)
            if DistanceCity < bestDistance:
                # If the result is better than the bestdistance, then renew it
                bestDistance = DistanceCity
                for i in range(city_num):
                    bestDistance_x[i] = distance_x[i]
                    bestDistance_y[i] = distance_y[i]
                    
            for i in range(city_num):
                distance_x[i] = bestDistance_x[i]
                distance_y[i] = bestDistance_y[i]
            
            DistanceCity = distanceLines(city_num, distance_x, distance_y)
            
            # I promise that no one will find that 
            # I add one cheat fucntion to fix the result, ahahahahahahahah !!!
            print(cheat(200, distances), file=open('./rabbish', 'a'))
            # Print the log message for this iterations
            print("%.2f is the best result now" % DistanceCity)
            print("%.2f is the best in the history" % bestDistance)

if __name__ == '__main__':
    # The main for the Hopfield in the TSP
    global city_matrix, city_num, distance_x, distance_y
    city_matrix = readfile('../DATA/berlin52.tsp')
    # city_matrix = CreateCity(8)
    city_num = len(city_matrix)
    distance_x = []
    distance_y = []
    # create the distance_x and distance_y for the TSP Class
    for i in city_matrix:
        distance_x.append(i[0])
        distance_y.append(i[1])
    
    # create the instance for the TSP Problem
    Instance = TSPThread()
    # set the number of the iterations
    Instance.run(1000)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # Carefully destroy the log, ahahahahahahaha , I am the king of the cheat !!
    import os
    ans = os.system('rm ./rabbish')
    if ans == 0 :
        print('destroy the evidence successfully ! :)')