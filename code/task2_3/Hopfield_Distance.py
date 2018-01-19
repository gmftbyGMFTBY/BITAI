#!/usr/bin/python3
# Author : GMFTBY
# Time   : 2017.1.19

# Link of help:
#   1. https://github.com/ChaiPL
#   2. Fix lots of things of the repo's script and do not work well 

from math import sqrt
from typing import List, Tuple

def distance(p1, p2):
    return sqrt((p1[0]-p2[0]) ** 2 + (p1[1]-p2[1]) ** 2)

# create distance between the cities
def distance_matrix(coordinates : List[Tuple]):    
    matrix = []
    for cord1 in coordinates:
        row = []
        for cord2 in coordinates:
            row.append(distance(cord1, cord2))
        matrix.append(row)
    return matrix

def get_largest(matrix):
    largest = 0.0
    for x in range(0, len(matrix)):
        largest = largest if largest > max(matrix[x]) else max(matrix[x])
    return largest

# normalize the data into the [0, 1], flattern the data
def normalize(matrix):    #
    largest = get_largest(matrix)

    for x in range(0,len(matrix)):
        for y in range(0, len(matrix)):
            matrix[x][y] /= largest
    return matrix

# calculate the distance between two points
def distanceTwoPoints(x0, y0, x1, y1):
    return sqrt(pow((x1 - x0), 2) + pow((y1 - y0), 2))

# calculate the distances of a edge
def distanceLines(n, x, y):
    temp_distance = 0.0
    for i in range(n):
        start = i - 1
        end = i
        temp_distance += distanceTwoPoints(x[start], y[start], x[end], y[end])
    return temp_distance

if __name__ == "__main__":
    # ---- test for distance_mastrix ---- #
    print(distance_matrix([[1,1],[2,2]]))
    



