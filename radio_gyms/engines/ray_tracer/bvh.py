
from typing import Sequence, Tuple, List
from numpy.typing import NDArray

from .triangle import Triangle
from ...utils.constants import MAX_FLT
from .box import Box

class BVH:
    root: Box = None
    def __init__(self, triangles: Sequence[Triangle]):
        self.root = Box(triangles)
        BVH.makeChildren(self.root, 0)

    def is_intersect(self, ray: Tuple[NDArray, NDArray])->float:
        hot_boxes = [self.root]
        hit_once = False
        nearest_hit = MAX_FLT

        while len(hot_boxes) != 0:
            current_box = hot_boxes.pop(0)

            if current_box.is_intersect(ray):
                continue

            if current_box.alone:
                current_hit = current_box.triangles[0].isIntersect(ray)
                if current_hit >= 0:
                    nearest_hit = min(nearest_hit, current_hit)
                    hit_once = True
                continue

            if current_box.child_left != None:
                hot_boxes.append(current_box.child_left)
            if current_box.child_right != None:
                hot_boxes.append(current_box.child_right)
        if hit_once:
            return nearest_hit
        return -1

    @staticmethod
    def makeChildren(root: Box, level):
        k: int = level%3

        if k == 0:
            root.triangles.sort(key=lambda tri: min([tri.pointA[0], tri.pointB[0], tri.pointC[0]]))
        elif k == 1:
            root.triangles.sort(key=lambda tri: min([tri.pointA[1], tri.pointB[1], tri.pointC[1]]))
        elif k == 2:
            root.triangles.sort(key=lambda tri: min([tri.pointA[2], tri.pointB[2], tri.pointC[2]]))

        middle_index = len(root.triangles)
        left_triangles = root.triangles[:middle_index]
        right_triangles = root.triangles[middle_index:]
        n_left = len(left_triangles)
        n_right = len(right_triangles)
        level += 1

        if n_left != 0:
            root.child_left = Box(left_triangles)
            if n_right > 1:
                BVH.makeChildren(root.child_left, level)
        if n_right != 0:
            root.child_right = Box(right_triangles)
            if n_right > 1:
                BVH.makeChildren(root.child_right, level)