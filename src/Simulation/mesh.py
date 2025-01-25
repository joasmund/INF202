from collections import defaultdict
import numpy as np
from numpy.linalg import norm

from src.Simulation.cells import Line, Triangle, Vertex
from src.Simulation.factory import CellFactory

class Mesh:
    def __init__(self, mesh, x_star, delta_t) -> None:
        self._mesh = mesh
        self._cells = []
        self._x_star = x_star
        self._delta_t = delta_t

    @property
    def cells(self):
        return self._cells

    def main_function(self):
        global_index = 0
        
        # Maps (cell_type, local_index) to global_index
        cell_type_mapping = {}
        face_to_cells = defaultdict(list)

        # Consolidated dictionary to store all cell data
        final_cell_data = {}

        # Store the point coordinates
        point_coordinates = {i: point[:2].tolist() for i, point in enumerate(self._mesh.points)}

        for cell_type, cell_data in self._mesh.cells_dict.items():
            for local_index, cell in enumerate(cell_data):
                # Create global index mapping
                cell_type_mapping[(cell_type, local_index)] = global_index
                global_cell_index = global_index
                global_index += 1

                # Initialize data for the current cell
                final_cell_data[global_cell_index] = {
                    "points": cell,
                    "faces": [],
                    "area": 0,
                    "midpoint": None,
                    "velocity_field": None,
                    "normal_vectors_with_faces": {},
                    "neighbors": [],
                }

                # Calculate cell faces
                faces = self.find_faces(len(cell), cell)
                final_cell_data[global_cell_index]["faces"] = faces

                # Map faces to cells
                for face in faces:
                    face_to_cells[face].append(global_cell_index)

                # Calculate cell area
                final_cell_data[global_cell_index]["area"] = self.area(cell, point_coordinates)

                # Calculate midpoint
                final_cell_data[global_cell_index]["midpoint"] = self.midpoint(cell, point_coordinates)

                # Calculate velocity field
                final_cell_data[global_cell_index]["velocity_field"] = self.velocity_field(
                    final_cell_data[global_cell_index]["midpoint"]
                )

        # Assign normal vectors to faces
        for global_cell_index, cell_data in final_cell_data.items():
            midpoint = cell_data["midpoint"]
            for face in cell_data["faces"]:
                normal_vector = self.normal_vectors_with_faces(face, point_coordinates, midpoint)
                cell_data["normal_vectors_with_faces"][face] = normal_vector

        # Calculate oil values
        oil_values = self.initial_oil(final_cell_data, self._x_star)
        for global_cell_index, oil_value in oil_values.items():
            final_cell_data[global_cell_index]["oil_amount"] = oil_value

        # Calculate neighbors
        cell_neighbors = self.find_neighbors(face_to_cells)
        for global_cell_index, neighbors in cell_neighbors.items():
            for neighbor in neighbors:
                shared_faces = [
                    face
                    for face in final_cell_data[global_cell_index]["faces"]
                    if face in final_cell_data[neighbor]["faces"]
                ]
                neighbor_data = {
                    "neighbor_index": neighbor,
                    "neighbor_faces": shared_faces,
                    "neighbor_velocity_field": final_cell_data[neighbor]["velocity_field"],
                }
                final_cell_data[global_cell_index]["neighbors"].append(neighbor_data)

        # Register cells
        self.register_cell(self._cells, final_cell_data, cell_type_mapping)
        return final_cell_data, cell_type_mapping

    def initial_oil(self, final_cell_data, x_star):
        oil_values = {}
        for global_cell_index, cell_data in final_cell_data.items():
            midpoint = cell_data["midpoint"]
            distance = norm(midpoint - x_star)
            oil_values[global_cell_index] = np.exp(-distance**2 / 0.01)
        return oil_values

    def midpoint(self, cell, point_coordinates):
        points = np.array([point_coordinates[node] for node in cell])
        return np.mean(points, axis=0)

    def velocity_field(self, midpoint):
        return np.array([midpoint[1] - 0.2 * midpoint[0], -midpoint[0]])

    def area(self, cell, point_coordinates):
        if len(cell) == 3:
            p1, p2, p3 = [point_coordinates[node] for node in cell]
            x1, y1 = p1
            x2, y2 = p2
            x3, y3 = p3
            return 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
        return 0

    def normal_vectors_with_faces(self, face, point_coordinates, triangle_midpoint):
        if len(face) != 2:
            return None
        
        point1 = np.array(point_coordinates[face[0]])
        point2 = np.array(point_coordinates[face[1]])
        direction = point2 - point1
        normal = np.array([-direction[1], direction[0]])
        
        face_midpoint = (point1 + point2) / 2
        vector_to_face_midpoint = face_midpoint - triangle_midpoint
        
        if np.dot(normal, vector_to_face_midpoint) < 0:
            normal = -normal

        return normal

    def find_faces(self, num_nodes, cell):
        if num_nodes == 1:
            return [tuple(sorted(cell))]
        elif num_nodes == 2:
            return [tuple(sorted(cell))]
        elif num_nodes == 3:
            return [
                tuple(sorted([cell[0], cell[1]])),
                tuple(sorted([cell[1], cell[2]])),
                tuple(sorted([cell[0], cell[2]])),
            ]
        else:
            return [tuple(sorted([cell[i], cell[j]])) for i in range(num_nodes) for j in range(i + 1, num_nodes)]

    def find_neighbors(self, face_to_cells):
        cell_neighbors = defaultdict(set)
        for _, cells in face_to_cells.items():
            if len(cells) == 2:
                cell_neighbors[cells[0]].add(cells[1])
                cell_neighbors[cells[1]].add(cells[0])
        return cell_neighbors

    def register_cell(self, cells, final_cell_data, cell_type_mapping):
        cf = CellFactory()
        cf.register("vertex", Vertex)
        cf.register("line", Line)
        cf.register("triangle", Triangle)
        for cell_type, cell_data in self._mesh.cells_dict.items():
            for local_index, _ in enumerate(cell_data):
                global_cell_index = cell_type_mapping[(cell_type, local_index)]
                cell_info = final_cell_data[global_cell_index]
                cell_object = cf(
                    key=cell_type,
                    id=global_cell_index,
                    oil_amount=cell_info["oil_amount"],
                    area=cell_info["area"],
                    normal_vectors_with_faces=cell_info["normal_vectors_with_faces"],
                    faces=cell_info["faces"],
                    velocity_field=cell_info["velocity_field"],
                    neighbors=cell_info["neighbors"],
                    delta_t=self._delta_t,
                )
                cells.append(cell_object)
