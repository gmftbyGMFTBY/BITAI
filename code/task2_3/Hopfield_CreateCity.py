#!/usr/bin/python3
# Author : GMFTBY
# Time   : 2017.1.19

# This script try to extract the message of the cities from the file or 
# Created randomly

from numpy import random

def CreateCity(GetNum):
    # create the dataset randomly, it just for test
    cityNum = GetNum
    city = []
    for i in range(cityNum):
        temp = []
        for j in range(2):
           temp.append(random.randint(0, 350))
        city.append(temp)
    return city

def readfile(filename):
    # read the dataset from the TSPLIB such as berlin52.tsp, it is the real one
    # The Hopfield Net is not work well for the large dataset such as berlin52.tsp
    cities = []
    with open(filename, 'r') as f:
        dimension = 0
        for index, line in enumerate(f.readlines()):
            if 'EOF' in line : break
            if index == 3 : 
                dimension = int(line[11:-1].strip())
                print('Problem\'s dimension is %d' % dimension)
            if index >= 6 :
                content = list(map(float, line.split()))[1:]
                cities.append(content)
        print('%d cities / %d dimension' % (len(cities), dimension))
    return cities

if __name__ == "__main__":
    # just for test
    print(CreateCity(5))
    print(readfile('../DATA/berlin52.tsp'))
