from typing import Sequence, Tuple, List
from numpy.typing import NDArray

from .triangle import Triangle
from ...utils.constants import MAX_FLT
from .box import Box


class BVH:
    root: Box = None

    def __init__(self, triangles: Sequence[Triangle]):
        self.root = Box(triangles)
        BVH.make_children(self.root, 0)

    def is_intersect(self, ray: Tuple[NDArray, NDArray]) -> float:
        hot_boxes = [self.root]
        hit_once = False
        nearest_hit = MAX_FLT

        while len(hot_boxes) != 0:
            current_box = hot_boxes.pop(0)

            if current_box.alone:
                current_hit = current_box.triangles[0].is_intersect(ray)
                if current_hit > 0:
                    nearest_hit = min(nearest_hit, current_hit)
                    hit_once = True
                continue

            if not current_box.is_intersect(ray):
                continue
            if current_box.child_left is not None:
                hot_boxes.append(current_box.child_left)
            if current_box.child_right is not None:
                hot_boxes.append(current_box.child_right)

        if hit_once:
            return nearest_hit
        return -1

    @staticmethod
    def make_children(parent: Box, level: int):
        k: int = level % 3
        ordered_triangles = []
        if k == 0:
            ordered_triangles = sorted(parent.triangles, key=lambda tri: tri.max_x, reverse=False)
        elif k == 1:
            ordered_triangles = sorted(parent.triangles, key=lambda tri: tri.max_y, reverse=False)
        elif k == 2:
            ordered_triangles = sorted(parent.triangles, key=lambda tri: tri.max_z, reverse=False)

        middle_index = int(len(ordered_triangles) / 2)
        left_triangles = ordered_triangles[:middle_index]
        right_triangles = ordered_triangles[middle_index:]

        n_left = len(left_triangles)
        n_right = len(right_triangles)

        level += 1
        if n_left != 0:
            parent.child_left = Box(left_triangles)
            if n_left > 1:
                BVH.make_children(parent.child_left, level)
        if n_right != 0:
            parent.child_right = Box(right_triangles)
            if n_right > 1:
                BVH.make_children(parent.child_right, level)

