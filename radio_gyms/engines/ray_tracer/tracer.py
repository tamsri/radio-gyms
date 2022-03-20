from typing import Tuple, List, Dict
from numpy.typing import NDArray

import numpy as np

from ...utils import ObjToTriangles, VecNorm, VecDistance
from ...utils.constants import EPSILON
from .bvh import BVH


class Tracer:

    def __init__(self, object_file_path):
        """
        Initialize Map for Ray Tracer
        :param object_file_path:
        """
        triangles = ObjToTriangles(object_file_path)
        self.map = BVH(triangles)

    def trace_outdoor(self, tx_pos: NDArray, rx_pos: NDArray):
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
            result["roof_edges"] = self.trace_roof_edges(tx_pos, rx_pos)

        result['reflections'] = self.trace_reflections(tx_pos, rx_pos)
        return result

    @staticmethod
    def make_ray(tx_pos: NDArray, rx_pos: NDArray) -> Tuple[NDArray, NDArray]:
        ray_org: NDArray = tx_pos
        ray_dir: NDArray = VecNorm(rx_pos - tx_pos)
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

    @staticmethod
    def get_mirror_point(pos: NDArray, triangle: 'Triangle') -> NDArray:
        normal = triangle.normal
        t = (np.dot(normal, triangle.pointB) - np.dot(pos, normal)) / np.dot(normal, normal)
        return pos + normal * 2 * t

    def trace_reflections(self, tx_pos, rx_pos) -> Dict:
        """
        Trace Reflection Points
        :param tx_pos: Transmitting Position
        :param rx_pos: Receiving Position
        :return: reflection points
        """
        reflections = {'single': self.trace_single_reflect(tx_pos, rx_pos),
                       'double': self.trace_double_reflect(tx_pos, rx_pos)}
        return reflections

    def trace_single_reflect(self, tx_pos, rx_pos) -> List[NDArray]:
        single_reflections = []
        for triangle in self.map.root.triangles:
            mirror_point = Tracer.get_mirror_point(tx_pos, triangle)
            dir_mirror_to_rx = VecNorm(rx_pos - mirror_point)
            ray = (mirror_point, dir_mirror_to_rx)
            mirror_to_rx_dist = triangle.is_intersect(ray)
            if mirror_to_rx_dist < 0:
                continue
            point_on_triangle = mirror_point + dir_mirror_to_rx * (mirror_to_rx_dist + EPSILON)
            if self.direct_path(tx_pos, point_on_triangle) and self.direct_path(rx_pos, point_on_triangle):
                single_reflections.append(point_on_triangle)
        return single_reflections

    def trace_double_reflect(self, tx_pos, rx_pos):
        double_reflections = []
        tx_mirror_points = []
        rx_mirror_points = []
        triangle_n = len(self.map.root.triangles)
        for triangle in self.map.root.triangles:
            tx_mirror_point = Tracer.get_mirror_point(tx_pos, triangle)
            rx_mirror_point = Tracer.get_mirror_point(rx_pos, triangle)
            tx_mirror_points.append(tx_mirror_point)
            rx_mirror_points.append(rx_mirror_point)

        for tx_mirror_i in range(triangle_n):
            tx_mirror_point = tx_mirror_points[tx_mirror_i]
            tx_triangle = self.map.root.triangles[tx_mirror_i]
            for rx_mirror_i in range(tx_mirror_i + 1, triangle_n):
                rx_mirror_point = rx_mirror_points[rx_mirror_i]
                rx_triangle = self.map.root.triangles[rx_mirror_i]

                tx_mirror_to_rx_mirror_dir = VecNorm(rx_mirror_point - tx_mirror_point)
                rx_mirror_to_tx_mirror_dir = -tx_mirror_to_rx_mirror_dir

                tx_mirror_ray = (tx_mirror_point, tx_mirror_to_rx_mirror_dir)
                rx_mirror_ray = (rx_mirror_point, rx_mirror_to_tx_mirror_dir)

                tx_mirror_to_rx_mirror_dist = tx_triangle.is_intersect(tx_mirror_ray)
                rx_mirror_to_tx_mirror_dist = rx_triangle.is_intersect(rx_mirror_ray)
                if tx_mirror_to_rx_mirror_dist < 0 or rx_mirror_to_tx_mirror_dist < 0:
                    continue
                tx_point_on_triangle = tx_mirror_point + tx_mirror_to_rx_mirror_dir * (
                            tx_mirror_to_rx_mirror_dist + EPSILON)
                rx_point_on_triangle = rx_mirror_point + rx_mirror_to_tx_mirror_dir * (
                            rx_mirror_to_tx_mirror_dist + EPSILON)

                if self.direct_path(tx_pos, tx_point_on_triangle) and \
                        self.direct_path(tx_point_on_triangle, rx_point_on_triangle) and \
                        self.direct_path(rx_point_on_triangle, rx_pos):
                    double_reflections.append([tx_point_on_triangle, rx_point_on_triangle])
        return double_reflections

    def trace_roof_edges(self, tx_pos, rx_pos):
        """
        Trace Knife Edges
        :param tx_pos: Transmitting Position
        :param rx_pos: Receiving Position
        :return: Knife Edges
        """
        return []
