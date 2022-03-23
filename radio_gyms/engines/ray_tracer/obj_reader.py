import numpy as np
from typing import Sequence
from .triangle import Triangle


def ObjToTriangles(file_path: str) -> Sequence[Triangle]:
    faces: Sequence[int] = []
    vertices: Sequence[float] = []
    triangles: Sequence[Triangle] = []

    with open(file_path, "r") as file:
        for line in file:
            components = line.strip(" \n").split(" ")
            if components[0] == "f":
                indices = list(
                    map(lambda c: int(c.split('/')[0]) - 1, components[1:]))
                for i in range(0, len(indices) - 2):
                    faces.append(indices[i: i + 3])
            elif components[0] == "v":
                vertex = list(map(lambda c: float(c), components[1:]))
                vertices.append(vertex)

    for face in faces:
        a = np.array(vertices[face[0]])
        b = np.array(vertices[face[1]])
        c = np.array(vertices[face[2]])
        triangle = Triangle(a, b, c)
        triangles.append(triangle)
    return triangles
