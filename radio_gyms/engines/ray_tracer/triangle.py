import numpy as np
from typing import Tuple
from numpy.typing import NDArray
from ...utils.constants import EPSILON


class Triangle:
    pointA: NDArray = None
    pointB: NDArray = None
    pointC: NDArray = None
    normal: NDArray = None
    edgeA: NDArray = None
    edgeB: NDArray = None

    def __init__(self, triangle: Tuple[NDArray, NDArray, NDArray]):
        self.pointA = triangle[0]
        self.pointB = triangle[1]
        self.pointC = triangle[2]
        self.edgeA = self.pointB - self.pointA
        self.edgeB = self.pointC - self.pointA
        self.normal = np.cross(self.edgeA, self.edgeB)
        self.normal = self.normal / np.sqrt(np.sum(self.normal ** 2))

    def isIntersect(self, ray: Tuple[NDArray, NDArray]) -> float:
        ray_pos = ray[0]
        ray_dir = ray[1]
        h = np.cross(ray_dir, self.edgeB)
        a = np.dot(self.edgeA, h)
        if a > -EPSILON and a < EPSILON:
            return -1
        f = 1.0 / float(a)
        s = ray_pos - self.pointA
        u = f * np.dot(s, h)
        if u < 0 or u > 1:
            return -1
        q = np.cross(s, self.edgeA)
        v = f * np.dot(ray_dir, q)
        if v < 0 or u + v > 1:
            return -1
        distance = f * np.dot(self.edgeB, q)
        if distance > EPSILON:
            return distance
        return -1
