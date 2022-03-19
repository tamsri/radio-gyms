
class Box:
    min_bound = None
    max_bound = None
    triangles = []
    childLeft = None
    childRight = None

    def __init__(self, triangles):
        pass

    def isIntersect(self, ray):

        return -1