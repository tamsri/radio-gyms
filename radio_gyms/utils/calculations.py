import numpy as np
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
    for i in range(3):
        if vector[i] == 0:
            vector[i] = EPSILON
    return 1 / vector
