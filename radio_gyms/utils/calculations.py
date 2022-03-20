import numpy as np
from numpy.typing import NDArray


def normalize(vector: NDArray) -> NDArray:
    norm = np.linalg.norm(vector)
    if norm != 0:
        vector = vector / norm
    return vector

def point_distance(pointA: NDArray, pointB: NDArray)->float:
    return np.sqrt(np.sum((pointA - pointB) ** 2))