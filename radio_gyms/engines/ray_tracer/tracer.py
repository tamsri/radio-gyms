from typing import Tuple
from numpy.typing import NDArray

from ...utils import ObjToTriangles, VecNorm, VecDistance
from .bvh import BVH

class Tracer:

    def __init__(self, object_file_path):
        """
        Initialize Map for Ray Tracer
        :param object_file_path:
        """
        triangles = ObjToTriangles(object_file_path)
        self.map = BVH(triangles)

    def trace_outdoor(self, tx_pos: NDArray, rx_pos:NDArray):
        """
        Trace the possible ray paths from tx_pos to rx_pos in outdoor scenario (open sky)
        :param tx_pos: Transmitting Position
        :param rx_pos: Receiving Position
        :return: Outdoor Tracing Result
        """
        result = {
            "direct": True,
            "reflections": [],
            "roofEdges": []
        }

        if self.direct_path(tx_pos, rx_pos):
            result["direct"] = True
        else:
            result["direct"] = False
            result["roofEdges"] = self.trace_roof_edges(tx_pos, rx_pos)

        result['reflections'] = self.trace_reflections(tx_pos, rx_pos)
        return result

    @staticmethod
    def make_ray(tx_pos: NDArray, rx_pos: NDArray) -> Tuple[NDArray, NDArray]:
        ray_org:NDArray = tx_pos
        ray_dir:NDArray = VecNorm(rx_pos - tx_pos)
        ray = (ray_org, ray_dir)
        return ray

    def direct_path(self, tx_pos: NDArray, rx_pos: NDArray):
        """
        Check Direct Path
        :param tx_pos: Transmitting Position
        :param rx_pos: Receiving Position
        :return: true if tx_pos and rx_pos are in line-of-sight.
        """
        ray = Tracer.make_ray(tx_pos, rx_pos)
        point_distance = VecDistance(tx_pos, rx_pos)
        nearest_hit = self.map.is_intersect(ray)
        if nearest_hit < 0:
            return True
        return nearest_hit > point_distance

    def trace_reflections(self, tx_pos, rx_pos, max_bounce=3):
        """
        Trace Reflection Points
        :param tx_pos: Transmitting Position
        :param rx_pos: Receiving Position
        :return: reflection points
        """

        return []

    def trace_roof_edges(self, tx_pos, rx_pos):
        """
        Trace Knife Edges
        :param tx_pos: Transmitting Position
        :param rx_pos: Receiving Position
        :return: Knife Edges
        """
        return []

