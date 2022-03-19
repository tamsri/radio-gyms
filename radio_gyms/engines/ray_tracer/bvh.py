from .box import Box

class BVH:
    def __init__(self, triangles):
        self.root = Box(triangles)
        BVH.makeChildren(self.root, 0);

    def isIntersect(self, ray):
        return -1

    @staticmethod
    def makeChildren(root, level):
        pass


