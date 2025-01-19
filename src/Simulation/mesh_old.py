from collections import defaultdict

import numpy as np
from numpy.linalg import norm

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
        areas = defaultdict(list)
        face_with_normal_vector = {}
        midpoints = {}  # Store the midpoints of each cell
        velocity_fields = {}

        # Store the point coordinates
        for i, point in enumerate(self._mesh.points):
            point_coordinates[i] = point[:2].tolist()  # Store coordinates of each point

        for cell_type, cell_data in self._mesh.cells_dict.items():
            for local_index, cell in enumerate(cell_data):
                # Create global index mapping
                cell_type_mapping[(cell_type, local_index)] = global_index
                global_cell_index = global_index
                global_index += 1

                # Perform additional processing
                num_nodes = len(cell)

                cell_points[global_cell_index] = cell  # Points are the nodes of the cell

                self.find_faces(num_nodes, cell, global_cell_index, cell_faces, face_to_cells)

                self.area(cell, global_cell_index, areas)

                # Calculate normal vectors for the faces of the current cell
                for face in cell_faces[global_cell_index]:
                    normal_vector = self.normal_vectors_with_faces(face, point_coordinates)
                    face_with_normal_vector[face] = normal_vector


                midpoints[global_cell_index] = self.midpoint(cell, point_coordinates)

                # Now, use the midpoint of the current cell for the velocity field
                velocity_fields[global_cell_index] = self.velocity_field(midpoints[global_cell_index])

        # Call initial_oil inside main_function to compute oil values
        oil_values = self.initial_oil(cell_points, point_coordinates)

        cell_neighbors = self.find_neighbors(face_to_cells)

        # print(dict(face_with_normal_vector))
        # print(dict(midpoints.items()))
        # print(dict(velocity_fields.items()))
        print("Oil values:", oil_values)  # Print the oil values dictionary

        # for face, cells in cell_faces.items():
        #     print(cells)
        # print(dict(sorted(cell_faces.items())))
        # print(dict(sorted(areas.items())))
        # Print normal vectors
        # print(normal_vectors)


    
    def initial_oil(self, cell_points, point_coordinates):
        # The fixed point x_star where the oil distribution is centered
        x_star = np.array([0.35, 0.45])

        # Dictionary to store the oil value for each cell
        oil_values = {}

        # Iterate over each cell
        for global_cell_index, cell_points in cell_points.items():
            # Calculate the midpoint for the cell
            midpoint = self.midpoint(cell_points, point_coordinates)
            
            # Compute the Euclidean distance between the midpoint and x_star
            distance = norm(midpoint - x_star)
            
            # Apply the Gaussian formula to calculate the oil value
            oil_value = np.exp(-distance**2 / 0.01)
            
            # Store the oil value for the cell
            oil_values[global_cell_index] = oil_value

        return oil_values

    def midpoint(self, cell, point_coordinates):
        """
        Calculate the midpoint of a given cell based on its type.
        
        Parameters:
        - cell: List of point indices representing the cell.
        - point_coordinates: Dictionary of point coordinates indexed by point IDs.
        
        Returns:
        - Midpoint coordinates as a numpy array.
        """
        if len(cell) == 1:  # Vertex (single point)
            # The midpoint of a single vertex is just the point itself
            return np.array(point_coordinates[cell[0]])
        
        elif len(cell) == 2:  # Line (2 points)
            # Midpoint is the average of the two points
            point1 = np.array(point_coordinates[cell[0]])
            point2 = np.array(point_coordinates[cell[1]])
            return (point1 + point2) / 2
        
        elif len(cell) == 3:  # Triangle (3 points)
            # Midpoint (centroid) is the average of the three points
            point1 = np.array(point_coordinates[cell[0]])
            point2 = np.array(point_coordinates[cell[1]])
            point3 = np.array(point_coordinates[cell[2]])
            return (point1 + point2 + point3) / 3
        
        else:
            raise ValueError("Unsupported cell type: only vertex, line, and triangle are supported.")

    def velocity_field(self, midpoint):
        """
        Vector function v(x, y) = [y - 0.2*x, -x]
        
        Parameters:
        - x: x-coordinate (scalar)
        - y: y-coordinate (scalar)
        
        Returns:
        - A numpy array representing the vector v(x, y)
        """
        return np.array([midpoint[1] - 0.2 * midpoint[0], -midpoint[0]])

    def area(self, cell, global_cell_index, areas):
        if len(cell) == 3:  # Triangle
            p1, p2, p3 = cell
            x1, y1 = self._mesh.points[p1][:2]
            x2, y2 = self._mesh.points[p2][:2]
            x3, y3 = self._mesh.points[p3][:2]

            # Calculate the area of the triangle
            area = 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))

            # Store only the area value at the specified index
            areas[global_cell_index] = area
        else:
            pass  # Do nothing for non-triangle cells

    
    def normal_vectors_with_faces(self, face, point_coordinates):
        """
        Calculate the normal vector for a given face using the point coordinates of that face.
        
        :param face: A tuple containing two point indices representing a face.
        :param point_coordinates: A dictionary of point coordinates indexed by point IDs.
        
        :return: Normal vector for the given face.
        """
    # Ensure that face contains exactly two points
        if len(face) != 2:
            normal = None
        else:
    
            # Retrieve the coordinates for the two points of the face
            point1 = np.array(point_coordinates[face[0]])  # First point
            point2 = np.array(point_coordinates[face[1]])  # Second point
            
            # Calculate the direction vector (difference between the two points)
            direction = point2 - point1
            
            # Compute the normal (2D case: perpendicular vector)
            normal = np.array([-direction[1], direction[0]])  # Perpendicular to the direction vector
            
            # Normalize the normal vector
            normal = normal / np.linalg.norm(normal)
            
        return normal

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
        cell_faces[global_cell_index] = (faces)

        for face in faces:
            face_to_cells[face].append(global_cell_index)

    def find_neighbors(self, face_to_cells):
        cell_neighbors = defaultdict(set)
        for face, cells in face_to_cells.items():
            if len(cells) == 2:  # Only process manifold edges/faces
                cell_neighbors[cells[0]].add(cells[1])
                cell_neighbors[cells[1]].add(cells[0])

        return cell_neighbors

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
