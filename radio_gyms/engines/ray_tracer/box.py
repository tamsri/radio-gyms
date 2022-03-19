from typing import Sequence, Tuple
import numpy as np
from numpy.typing import NDArray
from .triangle import Triangle
from ...utils.constants import MAX_FLT, MIN_FLT


class Box:
    min_bound: NDArray = None
    max_bound: NDArray = None
    triangles: Sequence[Triangle] = None
    child_left: 'Box' = None
    child_right: 'Box' = None

    def __init__(self, triangles: Sequence[Triangle]):
        self.triangles = triangles
        min_x, min_y, min_z = MAX_FLT, MAX_FLT, MAX_FLT
        max_x, max_y, max_z = MIN_FLT, MIN_FLT, MAX_FLT

        for triangle in self.triangles:
            x_list = [triangle.pointA[0], triangle.pointB[0], triangle.pointC[0]]
            y_list = [triangle.pointA[1], triangle.pointB[1], triangle.pointC[1]]
            z_list = [triangle.pointA[2], triangle.pointB[2], triangle.pointC[2]]
            min_x, max_x = min(x_list), max(x_list)
            min_y, max_y = min(y_list), max(y_list)
            min_z, max_z = min(z_list), max(z_list)

        self.min_bound = np.array([min_x, min_y, min_z])
        self.max_bound = np.array([max_x, max_y, max_z])

    def is_intersect(self, ray: Tuple[NDArray, NDArray]) -> bool:
        """
        check if the input ray intersects with the box
        Algorithm: "fast branchless raybounding box intersection"
        :param ray:
        :return: true/false
        """
        ray_pos: NDArray = ray[0]
        ray_dir: NDArray = ray[1]
        min_bound_check = (self.min_bound - ray_pos) * ray_dir
        max_bound_check = (self.max_bound - ray_pos) * ray_dir
        t1, t3, t5 = min_bound_check
        t2, t4, t6 = max_bound_check
        t_min = max( max( min(t1, t2), min(t3, t4)), min(t5, t6))
        t_max = min( min( max(t1, t2), max(t3, t4)), max(t5, t6))
        return t_max >= t_min
