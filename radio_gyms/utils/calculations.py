import numpy as np
from typing import List
from numpy.typing import NDArray
from .constants import EPSILON


def normalize(vector: NDArray) -> NDArray:
    norm = np.linalg.norm(vector)
    if norm != 0:
        vector = vector / norm
    return vector


def point_distance(point_a: NDArray, point_b: NDArray) -> float:
    return np.sqrt(np.sum((point_a - point_b) ** 2))


def vector_angle(a_dir: NDArray, b_dir: NDArray) -> float:
    a_norm = normalize(a_dir)
    b_norm = normalize(b_dir)
    dot_product = np.dot(a_norm, b_norm)
    return np.arccos(dot_product)


def position_between_xz(min_x, max_x, min_z, max_z, pos) -> bool:
    return min_x <= pos[0] <= max_x and min_z <= pos[2] <= max_z


def vector_inverse(vector: NDArray) -> NDArray:
    inv_vec = np.copy(vector).astype('float64')
    for i in range(len(vector)):
        if inv_vec[i] == 0:
            inv_vec[i] = EPSILON
    return 1.0 / inv_vec


def plane_y_distance(pos_a: NDArray, pos_b: NDArray):
    a_on_plane, b_on_plane = np.copy(pos_a), np.copy(pos_b)
    a_on_plane[1], b_on_plane[1] = 0.0, 0.0
    return point_distance(a_on_plane, b_on_plane)


def sort_nearest_points_from_on_plane_y(ref_pos: NDArray, points: List[NDArray]) -> List[NDArray]:
    sorted_points = sorted(points, key=lambda point: plane_y_distance(point, ref_pos))
    return sorted_points


def calculate_reflection_angle(tx_pos, ref_pos, rx_pos):
    ref_tx_dir = normalize(tx_pos-ref_pos)
    ref_rx_dir = normalize(rx_pos-ref_pos)
    return vector_angle(ref_tx_dir, ref_rx_dir)/2
