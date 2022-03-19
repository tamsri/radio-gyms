import numpy as np

EPSILON = 0.0000001

class Triangle:
    pointA = None
    pointB = None
    pointC = None

    def __init__(self, triangle):
        self.pointA = triangle[0]
        self.pointB = triangle[1]
        self.pointC = triangle[2]

    def isIntersect(self, ray):
        return -1