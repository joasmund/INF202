
import time
from collections import defaultdict
import numpy as np
from .cells import Line, Triangle, Vertex
from .factory import CellFactory


class Mesh:
    def __init__(self, mesh) -> None:
        self._mesh = mesh

    def main_function(self):
        # Create a global cell index mapping
        global_index = 1

        cell_type_mapping = {}  # Maps (cell_type, local_index) to global_index
        face_to_cells = defaultdict(list)
        cell_faces = {}  # Dictionary to store faces for each cell
        cell_points = defaultdict(list)  # Maps global cell index to its points (nodes)
        point_coordinates = defaultdict(list)  # Maps point index to the coordinates of that point
        cell_data = {}

        # Store the point coordinates
        for i, point in enumerate(self._mesh.points):
            point_coordinates[i] = point[:2].tolist()  # Store coordinates of each point

        # Loop through each cell type and local index
        for cell_type, cell_data_in in self._mesh.cells_dict.items():
            for local_index, cell in enumerate(cell_data_in):
                # Create global index mapping
                cell_type_mapping[(cell_type, local_index)] = global_index
                global_cell_index = global_index
                global_index += 1

                num_nodes = len(cell)

                cell_points[global_cell_index] = cell  # Points are the nodes of the cell

                # Find faces for this cell and store them
                faces = self.find_faces(num_nodes, cell, global_cell_index, cell_faces, face_to_cells)

                # Perform all calculations immediately while looping
                area = self.calculate_area(cell)
                midpoint = self.calculate_midpoint(cell)
                normal_vectors = self.calculate_normals(cell, faces)

                # Store the cell data with all calculated values
                cell_data[global_cell_index] = {
                    "cell_id": int(global_cell_index),
                    "points_and_coordinates": [
                        (point_id, point_coordinates[point_id]) for point_id in cell
                    ],
                    "faces_and_normals": [
                        (face, normal) for face, normal in zip(faces, normal_vectors)
                    ],
                    "area_of_cell": float(area),
                    "midpoint_of_cell": (midpoint[0], midpoint[1]),  # Ensure midpoint is a tuple of floats
                    "neighbors": {neighbor: None for neighbor in self.find_neighbors(face_to_cells).get(global_cell_index, [])}
                }

        # Printing cell data dictionary for visualization
        # print(dict(sorted(cell_data.items())))

        for cell_index, data in cell_data.items():
            print(f"Neighbors of cell {cell_index}: {dict(sorted(data['neighbors'].items()))}")

    def find_faces(self, num_nodes, cell, global_cell_index, cell_faces, face_to_cells):
        if num_nodes == 1:  # Vertex
            faces = [tuple(sorted(cell))]
        elif num_nodes == 2:  # Line
            faces = [tuple(sorted(cell))]
        elif num_nodes == 3:  # Triangle
            faces = [
                tuple(sorted([cell[0], cell[1]])),
                tuple(sorted([cell[1], cell[2]])),
                tuple(sorted([cell[0], cell[2]])),
            ]
        else:  # For other cell types, create edges between all vertex pairs
            faces = []
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    faces.append(tuple(sorted([cell[i], cell[j]])))

        # Store faces for this cell
        cell_faces[global_cell_index] = faces

        for face in faces:
            face_to_cells[face].append(global_cell_index)

        return faces

    def find_neighbors(self, face_to_cells):
        cell_neighbors = defaultdict(set)
        for face, cells in face_to_cells.items():
            if len(cells) == 2:  # Only process manifold edges/faces
                cell_neighbors[cells[0]].add(cells[1])
                cell_neighbors[cells[1]].add(cells[0])

        return cell_neighbors

    def calculate_area(self, cell):
        if len(cell) == 3:  # Triangle
            p1, p2, p3 = cell
            x1, y1 = self._mesh.points[p1][:2]
            x2, y2 = self._mesh.points[p2][:2]
            x3, y3 = self._mesh.points[p3][:2]
            return 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
        else:
            return 0.0  # Placeholder for other shapes (should be customized for different cell types)

    def calculate_midpoint(self, cell):
        x_sum = sum(self._mesh.points[point][0] for point in cell)
        y_sum = sum(self._mesh.points[point][1] for point in cell)
        return (x_sum / len(cell), y_sum / len(cell))  # Return a tuple of floats

    # def calculate_normals(self, cell, faces):
    #     normals = []
    #     
    #     # Extract the points of the cell (triangle) for normal calculation
    #     p0, p1, p2 = [self._mesh.points[point_id] for point_id in cell]
    #     
    #     # Compute the edge vectors for the triangle
    #     v1 = np.array(p1) - np.array(p0)  # Vector from p0 to p1
    #     v2 = np.array(p2) - np.array(p0)  # Vector from p0 to p2
    #     
    #     # Compute the cross product of the edge vectors to get the normal
    #     normal = np.cross(v1, v2)
    #     
    #     # Normalize the normal vector
    #     normal_length = np.linalg.norm(normal)
    #     if normal_length > 0:
    #         normal = normal / normal_length
    #     
    #     # Append the normal for each face
    #     for _ in faces:
    #         normals.append(tuple(normal))  # Add the computed normal for each face
    #     
    #     return normals

    def calculate_normals(self, cell, faces):
        # Placeholder normal calculation. In a real application, this should be calculated based on the geometry
        # For simplicity, assume the normal vector is a unit vector for now.
        return [(1.0, 0.0) for _ in faces]  # Return a list of normal tuples]

    def register_cells(self):
        cf = CellFactory()
        cf.register("vertex", Vertex)
        cf.register("line", Line)
        cf.register("triangle", Triangle)

        cells = self._mesh.cells

        self._cells = []  # List of all cells
        for cellForType in cells:
            cellType = cellForType.type  # Type of cell (Vertex, Line, Triangle)
            for pts in cellForType.data:
                self._cells.append(cf(cellType, id, oil_amount, area, normal_vectors_with_faces, faces, velocity_field, neighbors, delta_t))

# Example usage:
# mesh = meshio.read("bay.msh")
# mesh_instance = Mesh(mesh)
# mesh_instance.main_function()
