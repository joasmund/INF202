from abc import ABC
from collections import defaultdict

import numpy as np


class Cell(ABC):
    def __init__(self, id, oil_amount, area, normal_vectors_with_faces, faces, velocity_field, neighbors, delta_t) -> None:
        super().__init__()
        self._id = id
        self._oil_amount = oil_amount
        self._area = area
        self._normal_vectors_with_faces = normal_vectors_with_faces
        self._faces = faces
        self._neighbors = neighbors
        self._velocity_field = velocity_field
        self._delta_t = delta_t

class Vertex(Cell):
    def __init__(self, id, oil_amount, area, normal_vectors_with_faces, faces, velocity_field, neighbors, delta_t) -> None:
        super().__init__(id, oil_amount, area, normal_vectors_with_faces, faces, velocity_field, neighbors, delta_t)

class Line(Cell):
    def __init__(self, id, oil_amount, area, normal_vectors_with_faces, faces, velocity_field, neighbors, delta_t) -> None:
        super().__init__(id, oil_amount, area, normal_vectors_with_faces, faces, velocity_field, neighbors, delta_t)

class Triangle(Cell):
    def __init__(self, id, oil_amount, area, normal_vectors_with_faces, faces, velocity_field, neighbors, delta_t) -> None:
        super().__init__(id, oil_amount, area, normal_vectors_with_faces, faces, velocity_field, neighbors, delta_t)

    @property
    def oil_amount(self):
        return self._oil_amount

    @property
    def faces(self):
        return self._faces

    @property
    def velocity_field(self):
        return self._velocity_field

    @oil_amount.setter
    def oil_amount(self):
        self.update_oil_amount()

    def update_oil_amount(self):
        up = 0
        for i, ngh in enumerate(self._neighbors):
            for neighbor_face in ngh.faces:
                if self._normal_vectors_with_faces[1][i] == neighbor_face:
                    up -= (self._delta_t / self._area) * self.flux(
                        ngh.oil_amount, 
                        self._normal_vectors_with_faces[0][i], 
                        ngh.velocity_field
                    )
        self._oil_amount += up

    def flux(self, ngh, nu, v):
        if np.dot(v, nu) > 0:
            return self._oil_amount * np.dot(v, nu)
        else:
            return ngh.current_oil_amount * np.dot(v, nu)

    def __str__(self) -> str:
        return f"""
        Triangle with cell id: {self._id}
        The oil amount in the cell is equal to {self._oil_amount}
        Has area: {self._area}
        It has the normal vectors and faces: {self._normal_vectors_with_faces}
        The velocity field at the midpoint of the triangle = {self._velocity_field}
        The triangle is neighbor with the following cells {self._neighbors}
        """
