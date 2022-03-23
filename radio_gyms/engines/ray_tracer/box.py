from typing import Sequence, Tuple, List
import numpy as np
from numpy.typing import NDArray
from .triangle import Triangle
from ...utils.constants import MAX_FLT, MIN_FLT
from ...utils import VecInv


class Box:
    min_bound: NDArray = None
    max_bound: NDArray = None
    triangles: List[Triangle] = None
    child_left: 'Box' = None
    child_right: 'Box' = None
    alone: bool = False

    def __init__(self, triangles: List[Triangle]):
        self.triangles = [triangle for triangle in triangles]
        if len(self.triangles) == 1:
            self.alone = True

        min_x, min_y, min_z = MAX_FLT, MAX_FLT, MAX_FLT
        max_x, max_y, max_z = MIN_FLT, MIN_FLT, MIN_FLT
        for triangle in self.triangles:
            min_x = min(min_x, triangle.min_x)
            min_y = min(min_y, triangle.min_y)
            min_z = min(min_z, triangle.min_z)
            max_x = max(max_x, triangle.max_x)
            max_y = max(max_y, triangle.max_y)
            max_z = max(max_z, triangle.max_z)
        self.min_bound = np.array([min_x, min_y, min_z])
        self.max_bound = np.array([max_x, max_y, max_z])

    def is_intersect(self, ray: Tuple[NDArray, NDArray]) -> bool:
        """
        check if the input ray intersects with the box

        :param ray:
        :return: true/false
        """
        # Optimized from the algorithm: "fast branch-less ray-bounding box intersection"
        ray_pos: NDArray = np.array(ray[0])
        ray_inv_dir: NDArray = VecInv(np.array(ray[1]))

        min_bound_check = (self.min_bound - ray_pos) * ray_inv_dir
        max_bound_check = (self.max_bound - ray_pos) * ray_inv_dir
        t1, t3, t5 = min_bound_check
        t2, t4, t6 = max_bound_check
        t_min = max(max(min(t1, t2), min(t3, t4)), min(t5, t6))
        t_max = min(min(max(t1, t2), max(t3, t4)), max(t5, t6))
        return t_max >= t_min
