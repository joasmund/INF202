from abc import ABC
import numpy as np


class Cell(ABC):
    def __init__(self, id, oil_amount, area, normal_vectors_with_faces, faces, velocity_field, neighbors, delta_t, cell_in_bay = False) -> None:
        super().__init__()
        self._id = id
        self._oil_amount = oil_amount
        self._area = area
        self._normal_vectors_with_faces = normal_vectors_with_faces
        self._faces = faces
        self._neighbors = neighbors
        self._velocity_field = velocity_field
        self._delta_t = delta_t
        self._cell_in_bay = cell_in_bay  # Add new attribute



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
    
    def update_oil_amount(self):
        total_flux = 0  # Initialize the total flux for the current cell

        for face, normal in self._normal_vectors_with_faces:
            for ngh in self._neighbors:
            # Find the matching face and normal vector for the neighbor
                # Normalize and sort both face representations
                face_normalized = sorted(map(int, face))  # Convert face to sorted list of integers

                # print(self._id, face, normal)
                # Flatten ngh['neighbor_faces'] if it contains tuples
                neighbor_face_flattened = [int(vertex) for pair in ngh['neighbor_faces'] for vertex in pair]
                neighbor_face_normalized = sorted(neighbor_face_flattened)  # Normalize neighbor faces
                
                if face_normalized == neighbor_face_normalized:  # Match the shared face
                    # Average velocity across the interface
                    v_avg = 0.5 * (self._velocity_field + ngh['neighbor_velocity_field'])

                    # print(f"{self._id}, Ui face: {face_normalized}, Neihgbor face: {neighbor_face_normalized}")
                    # print(f"{self._id}, Ui velocity: {self._velocity_field}, Niehgbor velocity: {ngh['neighbor_velocity_field']}")
                    # print(f"{self._id}, Average velocity: {v_avg}, Normal vector: {normal}")

                    # Compute flux across the interface
                    flux_contribution = self.flux(
                        self._oil_amount, 
                        ngh['neighbor_oil_amount'], 
                        normal, 
                        v_avg
                    )

                    # Accumulate the flux contribution
                    total_flux += flux_contribution

        # Update the oil amount using the property setter
        return self._oil_amount - (self._delta_t / self._area) * total_flux

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
