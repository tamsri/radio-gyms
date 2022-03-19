from ...utils import ObjToTriangles
from .bvh import BVH

class Tracer:

    def __init__(self, object_file_path):
        """
        Initialize Map for Ray Tracer
        :param object_file_path:
        """
        triangles = ObjToTriangles(object_file_path)
        self.map = BVH(triangles)

    def traceOutdoor(self, tx_pos, rx_pos):
        """
        Trace the possible ray paths from tx_pos to rx_pos in outdoor scenario (open sky)
        :param tx_pos: Transmitting Position
        :param rx_pos: Receiving Position
        :return: Outdoor Tracing Result
        """
        result = {
            "direct": True,
            "reflections": [],
            "knifeEdges": []
        }
        if self.directPath(tx_pos, rx_pos):
            result["direct"] = True
        else:
            result["direct"] = False
            result["knifeEdges"] = self.traceKnifeEdges(tx_pos, rx_pos)

        result['reflections'] = self.traceReflections(tx_pos, rx_pos)
        return result

    def directPath(self, tx_pos, rx_pos):
        """
        Check Direct Path
        :param tx_pos: Transmitting Position
        :param rx_pos: Receiving Position
        :return: true if tx_pos and rx_pos are in line-of-sight.
        """
        return False

    def traceReflections(self, tx_pos, rx_pos, max_bounce=3):
        """
        Trace Reflection Points
        :param tx_pos: Transmitting Position
        :param rx_pos: Receiving Position
        :return: reflection points
        """

        return []

    def traceKnifeEdges(self, tx_pos, rx_pos):
        """
        Trace Knife Edges
        :param tx_pos: Transmitting Position
        :param rx_pos: Receiving Position
        :return: Knife Edges
        """
        return []

