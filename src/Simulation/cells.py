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
        self._oil_change = 0


class Vertex(Cell):
    def __init__(self, id, oil_amount, area, normal_vectors_with_faces, faces, velocity_field, neighbors, delta_t) -> None:
        super().__init__(id, oil_amount, area, normal_vectors_with_faces, faces, velocity_field, neighbors, delta_t)

    @property
    def id(self):
        return self._id


class Line(Cell):
    def __init__(self, id, oil_amount, area, normal_vectors_with_faces, faces, velocity_field, neighbors, delta_t) -> None:
        super().__init__(id, oil_amount, area, normal_vectors_with_faces, faces, velocity_field, neighbors, delta_t)

    @property
    def id(self):
        return self._id


class Triangle(Cell):
    def __init__(self, id, oil_amount, area, normal_vectors_with_faces, faces, velocity_field, neighbors, delta_t) -> None:
        super().__init__(id, oil_amount, area, normal_vectors_with_faces, faces, velocity_field, neighbors, delta_t)

    @property
    def id(self):
        return self._id

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
    def oil_amount(self, value):
        self._oil_amount = value

    @property
    def oil_change(self):
        return self._oil_change

    @oil_change.setter
    def oil_change(self, value):
        self._oil_change = value
    
    
    def update_oil_amount(self):
        up = 0  # Accumulate oil change from neighbors
        for ngh in self._neighbors:
            # Find the matching face and normal vector for the neighbor
            for _, (face, normal) in enumerate(self._normal_vectors_with_faces):
                print (ngh['neighbor_faces'][0][0])
                print(face[0])
                if face[0] == ngh['neighbor_faces'][0][0] and face[1] == ngh['neighbor_faces'][0][1]:
                    # Calculate the scaled normal (νk)
                    # nu = normal * np.linalg.norm(face)
                    nu = normal * np.linalg.norm(face)
                    print(nu, 'nu')
                    # Average velocity across the interface
                    v_avg = 0.5 * (self._velocity_field + ngh['neighbor_velocity_field'])

                    # Flux calculation
                    up = up -(self._delta_t / self._area) * self.flux(
                        self._oil_amount,
                        ngh['neighbor_oil_amount'],
                        nu,
                        v_avg,
                    )
                    print(up, 'up')
                    print(ngh['neighbor_oil_amount'], 'neighbor_oil_amount')
        # Update oil amount for this cell
        self.oil_change += up

    def flux(self, u_i, u_ngh, nu, v):
        """
        Compute flux across the interface.
        u_i: Oil amount in the current cell.
        u_ngh: Oil amount in the neighbor cell.
        nu: Scaled normal vector.
        v: Average velocity vector.
        """
        if np.dot(v, nu) > 0:
            return u_i * np.dot(v, nu)
        else:
            return u_ngh * np.dot(v, nu)

    def __str__(self) -> str:
        return (
            f"ID: {self._id}, Oil: {self._oil_amount}, Area: {self._area}, "
            f"Faces: {self._faces}, Velocity: {self._velocity_field}, Neighbors: {self._neighbors}"
        )
