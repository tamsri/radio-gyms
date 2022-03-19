from typing import Sequence
from .triangle import Triangle

from .box import Box

class BVH:
    root: Box = None

    def __init__(self, triangles: Sequence[Triangle]):
        self.root = Box(triangles)
        BVH.makeChildren(self.root, 0)

    def isIntersect(self, ray):
        return -1

    @staticmethod
    def makeChildren(root, level):
        pass


