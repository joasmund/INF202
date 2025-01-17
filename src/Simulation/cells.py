from abc import ABC, abstractclassmethod
from collections import defaultdict

import numpy as np


class Cell(ABC):
    def __init__(self, id, area, normal_vectors, faces, velocity_field, current_oil_amount, neighbors, delta_t) -> None:
        super().__init__()
        self._id = id
        self._area = area
        self._normal_vectors = normal_vectors
        self._faces = faces
        self._neighbors = neighbors
        self._velocity_field = velocity_field
        self._current_oil_amount = current_oil_amount
        self._delta_t = delta_t

class Vertex(Cell):
    def __init__(self, id, area, normal_vectors, faces, velocity_field, current_oil_amount, neighbors, delta_t) -> None:
        super().__init__(id, area, normal_vectors, faces, velocity_field, current_oil_amount, neighbors, delta_t)

class Line(Cell):
    def __init__(self, id, area, normal_vectors, faces, velocity_field, current_oil_amount, neighbors, delta_t) -> None:
        super().__init__(id, area, normal_vectors, faces, velocity_field, current_oil_amount, neighbors, delta_t)

class Triangle(Cell):
    def __init__(self, id, area, normal_vectors, faces, velocity_field, current_oil_amount, neighbors, delta_t) -> None:
        super().__init__(id, area, normal_vectors, faces, velocity_field, current_oil_amount, neighbors, delta_t)

    def updated_oil_amount(self):
        up = 0
        for i, ngh in enumerate(self._neighbors):
            for neighbor_face in ngh.neighbors.faces:
                if self._faces[i] == neighbor_face:
                    up = up - (self._delta_t / self._area) * self.flux(ngh.current_oil_amount, ngh.neighbors.normal_vectors[i], ngh.neighbors.velocity_field)

        return self._current_oil_amount + up

            
    def flux(self, ngh, nu, v):
        if np.dot(v, nu) > 0:
            return self._current_oil_amount * np.dot(v, nu)
        else:
            return ngh.current_oil_amount * np.dot(v, nu)

    @property
    def faces(self):
        return self._faces

    @property
    def velocity_field(self):
        return self._velocity_field

    @property
    def current_oil_amount(self):
        return self._current_oil_amount
