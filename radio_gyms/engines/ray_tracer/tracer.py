from typing import Tuple, List, Dict
from numpy.typing import NDArray

import numpy as np

from ..ray_tracer.obj_reader import ObjToTriangles
from ...utils import VecNorm, VecDistance, VecAngle, PosBetweenXZ, SortPointsFromPlaneY
from ...utils.constants import EPSILON, MIN_ROOF_EDGE_DISTANCE, ROOF_MIN_ANGLE, ROOF_MAX_SCAN, MAX_FLT
from .bvh import BVH


class Tracer:
    min_bound = None
    max_bound = None
    def __init__(self, object_file_path):
        """
        Initialize Map for Ray Tracer
        :param object_file_path:
        """
        triangles = ObjToTriangles(object_file_path)
        self.map = BVH(triangles)
        self.min_bound = self.map.root.min_bound
        self.max_bound = self.map.root.max_bound

    def trace_outdoor(self, tx_pos: List[float], rx_pos: List[float]):
        """
        Trace the possible ray paths from tx_pos to rx_pos in outdoor scenario (open sky)
        :param tx_pos: Transmitting Position
        :param rx_pos: Receiving Position
        :return: Outdoor Tracing Result
        """
        tx_pos = np.array(tx_pos)
        rx_pos = np.array(rx_pos)
        result = {
            "direct": True,
            "reflections": [],
            "roof_edges": [],
            'tx_pos': tx_pos,
            'rx_pos': rx_pos
        }

        if self.direct_path(tx_pos, rx_pos):
            result["direct"] = True
        else:
            result["direct"] = False
            sorted_edges = SortPointsFromPlaneY(tx_pos, self.trace_roof_edges(tx_pos, rx_pos))
            result["roof_edges"] = sorted_edges

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
        b = np.dot(normal, triangle.pointB)
        c = np.dot(pos, normal)
        d = np.dot(normal, normal)
        if d == 0:
            d = EPSILON
        t = (b - c) / d
        return pos + normal * 2 * t

    def trace_reflections(self, tx_pos: NDArray, rx_pos: NDArray) -> Dict:
        """
        Trace Reflection Points
        :param tx_pos: Transmitting Position
        :param rx_pos: Receiving Position
        :return: reflection points
        """
        reflections = {
            'single': self.trace_single_reflect(tx_pos, rx_pos),
            'double': self.trace_double_reflect(tx_pos, rx_pos)
        }
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
            if self.direct_path(tx_pos, point_on_triangle) and \
                    self.direct_path(rx_pos, point_on_triangle):
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

    def trace_roof_edges(self, tx_pos, rx_pos) -> List:
        """
        Trace Knife Edges
        :param tx_pos: Transmitting Position
        :param rx_pos: Receiving Position
        :return: Knife Edges
        """
        edges = []
        left_pos = tx_pos
        right_pos = rx_pos

        current_scan = 0

        while not self.direct_path(left_pos, right_pos):
            if current_scan > ROOF_MAX_SCAN:
                return edges
            edge_left = self.find_edge(left_pos, right_pos)
            if edge_left is None:
                return []
            edge_right = self.find_edge(right_pos, left_pos)
            if edge_right is None:
                return []

            if self.direct_path(edge_left, edge_right):
                if VecDistance(edge_left, edge_right) < MIN_ROOF_EDGE_DISTANCE:
                    avg_edge = (edge_left + edge_right) / 2
                    edges.append(avg_edge)
                    return edges
                edges.append(edge_left)
                edges.append(edge_right)
                return edges

            edges.append(edge_left)
            edges.append(edge_right)
            left_pos = edge_left
            right_pos = edge_right
        return []

    def find_edge(self, left_pos, right_pos):
        min_x = min(left_pos[0], right_pos[0])
        max_x = max(left_pos[0], right_pos[0])
        min_z = min(left_pos[2], right_pos[2])
        max_z = max(left_pos[2], right_pos[2])

        top_direction = np.array([0, 1, 0])
        upper_ray = (left_pos, top_direction)
        if self.map.is_intersect(upper_ray) > 0:
            return None
        lower_ray = (left_pos, VecNorm(right_pos - left_pos))

        current_scan = 0
        while current_scan < ROOF_MAX_SCAN and \
                VecAngle(upper_ray[1], lower_ray[1]) > ROOF_MIN_ANGLE:
            current_scan += 1

            new_dir = VecNorm((upper_ray[1] + lower_ray[1]) / 2)
            check_ray = (left_pos, new_dir)

            hit_nearest = self.map.is_intersect(check_ray)
            if hit_nearest > 0 and PosBetweenXZ(min_x, max_x, min_z, max_z, left_pos + new_dir * hit_nearest):
                lower_ray = check_ray
            else:
                upper_ray = check_ray

        distance = self.map.is_intersect(lower_ray)
        if distance < 0:
            return None

        left_pos_on_plane = np.array([left_pos[0], 0, left_pos[2]])
        right_pos_on_plane = np.array([right_pos[0], 0, right_pos[2]])
        plane_dir = VecNorm(right_pos_on_plane - left_pos_on_plane)

        theta = VecAngle(plane_dir, lower_ray[1])
        x_angle = VecAngle(lower_ray[1], upper_ray[1])

        height = distance * np.cos(theta) * np.tan(theta + x_angle)
        width = distance * np.cos(theta)
        edge_distance = np.sqrt(height ** 2 + width ** 2)
        edge_pos = upper_ray[0] + upper_ray[1] * edge_distance
        return edge_pos

    def is_outdoor(self, pos):
        sky_pos = np.copy(pos)
        sky_pos[1] = 1000
        return self.direct_path(pos, sky_pos)
