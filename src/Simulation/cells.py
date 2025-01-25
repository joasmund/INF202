from abc import ABC
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

    @property
    def oil_amount(self):
        return self._oil_amount

    @property
    def id(self):
        return self._id


class Line(Cell):
    def __init__(self, id, oil_amount, area, normal_vectors_with_faces, faces, velocity_field, neighbors, delta_t) -> None:
        super().__init__(id, oil_amount, area, normal_vectors_with_faces, faces, velocity_field, neighbors, delta_t)

    @property
    def oil_amount(self):
        return self._oil_amount

    @property
    def velocity_field(self):
        return self._velocity_field

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
    
    def update_oil_amount(self, all_cells):
        """
        Update the oil amount in the current cell based on fluxes from neighbors.
        
        Parameters:
        - all_cells: A list of all `Cell` objects (e.g., passed from the `Mesh` class).
        """
        # Initialize total flux for the current cell
        total_flux = 0

        for ngh in self._neighbors:
            # Fetch the actual neighbor Cell object using its index
            neighbor_cell = all_cells[ngh["neighbor_index"]]
            neighbor_oil_amount = neighbor_cell.oil_amount  # Use the neighbor's oil amount
            neighbor_velocity_field = neighbor_cell.velocity_field

            for face, normal in self._normal_vectors_with_faces.items():
                # Normalize the face representation
                face_normalized = tuple(sorted(map(int, face)))

                # Normalize the neighbor's face
                neighbor_face_flattened = [int(vertex) for pair in ngh["neighbor_faces"] for vertex in pair]
                neighbor_face_normalized = tuple(sorted(neighbor_face_flattened))

                if face_normalized == neighbor_face_normalized:
                    # Average velocity across the interface
                    v_avg = 0.5 * (self._velocity_field + neighbor_velocity_field)

                    # Compute flux across the interface
                    flux_contribution = self.flux(
                        self._oil_amount,
                        neighbor_oil_amount,
                        normal,
                        v_avg
                    )

                    # Accumulate the flux contribution
                    total_flux += flux_contribution

        # Update the oil amount for the current cell
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
            f"Faces: {self._normal_vectors_with_faces}"
            f", Velocity: {self._velocity_field}, Neighbors: {self._neighbors}"
        )
