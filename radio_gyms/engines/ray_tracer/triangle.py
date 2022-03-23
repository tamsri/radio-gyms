import numpy as np

from typing import Tuple
from numpy.typing import NDArray

from ...utils import VecNorm
from ...utils.constants import EPSILON


class Triangle:
    pointA: NDArray = None
    pointB: NDArray = None
    pointC: NDArray = None
    normal: NDArray = None
    edgeA: NDArray = None
    edgeB: NDArray = None
    min_x: float = None
    max_x: float = None
    min_y: float = None
    max_y: float = None
    min_z: float = None
    max_z: float = None

    def __init__(self, a: NDArray, b: NDArray, c: NDArray):
        self.pointA = a
        self.pointB = b
        self.pointC = c
        self.edgeA = self.pointB - self.pointA
        self.edgeB = self.pointC - self.pointA
        self.normal = VecNorm(np.cross(self.edgeA, self.edgeB))
        self.min_x = min([a[0], b[0], c[0]])
        self.min_y = min([a[1], b[1], c[1]])
        self.min_z = min([a[2], b[2], c[2]])
        self.max_x = max([a[0], b[0], c[0]])
        self.max_y = max([a[1], b[1], c[1]])
        self.max_z = max([a[2], b[2], c[2]])

    def is_intersect(self, ray: Tuple[NDArray, NDArray]) -> float:
        ray_pos: NDArray = ray[0]
        ray_dir: NDArray = ray[1]

        h = np.cross(ray_dir, self.edgeB)
        a = np.dot(self.edgeA, h)
        if -EPSILON < a < EPSILON:
            return -1
        f = 1.0 / float(a)
        s = ray_pos - self.pointA
        u = f * np.dot(s, h)
        if u < 0 or u > 1:
            return -1

        q = np.cross(s, self.edgeA)
        v = f * np.dot(ray_dir, q)
        if v < 0 or (u + v) > 1:
            return -1

        distance = f * np.dot(self.edgeB, q)
        if distance > EPSILON:
            return distance
        return -1
