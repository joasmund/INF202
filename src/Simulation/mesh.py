from collections import defaultdict
import numpy as np
from numpy.linalg import norm

from src.Simulation.cells import Line, Triangle, Vertex
from src.Simulation.factory import CellFactory


class Mesh:
    def __init__(self, mesh, delta_t) -> None:
        self._mesh = mesh
        self._cells = []
        self._delta_t = delta_t

    @property
    def mesh(self):
        return self._mesh

    @property
    def cells(self):
        return self._cells

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

        # To store the resulting dictionary with all the required information
        final_cell_data = {}

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

                # Calculate the midpoint of the current cell
                midpoints[global_cell_index] = self.midpoint(cell, point_coordinates)

                # Calculate normal vectors for the faces of the current cell
                for face in cell_faces[global_cell_index]:
                    normal_vector = self.normal_vectors_with_faces(face, point_coordinates, midpoints[global_cell_index])
                    face_with_normal_vector[face] = normal_vector

                # Now, use the midpoint of the current cell for the velocity field
                velocity_fields[global_cell_index] = self.velocity_field(midpoints[global_cell_index])

        # Calculate oil values
        oil_values = self.initial_oil(cell_points, point_coordinates)

        cell_neighbors = self.find_neighbors(face_to_cells)

        # Create the final dictionary with all the requested info
        for global_cell_index in cell_points.keys():
            # Prepare the data for the current cell
            cell_data = {
                'oil_amount': (oil_values.get(global_cell_index, 0)),
                'area': (areas.get(global_cell_index, 0)),
                'faces': [
                    (face_with_normal_vector.get(face)) 
                    for face in cell_faces.get(global_cell_index, [])
                ],
                'velocity_field': ((velocity_fields.get(global_cell_index, np.array([0, 0])))),
                'neighbors': []
            }

            # Adding details for each neighbor
            for neighbor in cell_neighbors.get(global_cell_index, []):
                # Get the faces shared between the current cell and the neighbor
                shared_faces = [
                    face for face in cell_faces[global_cell_index]
                    if face in cell_faces.get(neighbor, [])
                ]
                
                # Get the neighbor's velocity field (we use the same computation as for the current cell)
                neighbor_velocity_field = velocity_fields.get(neighbor, np.array([0, 0]))
                neighbor_velocity_field_magnitude = (neighbor_velocity_field)

                # Get the neighbor's oil amount
                neighbor_oil_amount = oil_values.get(neighbor, 0)

                # Add the neighbor's data
                neighbor_data = {
                    'neighbor_index': neighbor,
                    'neighbor_faces': shared_faces,
                    'neighbor_velocity_field': (neighbor_velocity_field_magnitude),
                    'neighbor_oil_amount': (neighbor_oil_amount)
                }
                cell_data['neighbors'].append(neighbor_data)

            final_cell_data[global_cell_index] = cell_data

        # Print or return the final cell data
        self.register_cell(self._cells, final_cell_data, cell_type_mapping)

        return final_cell_data, cell_type_mapping

    def initial_oil(self, cell_points, point_coordinates):
        x_star = np.array([0.35, 0.45])
        oil_values = {}

        for global_cell_index, cell_points in cell_points.items():
            midpoint = self.midpoint(cell_points, point_coordinates)
            distance = norm(midpoint - x_star)
            oil_value = np.exp(-distance**2 / 0.01)
            oil_values[global_cell_index] = oil_value

        return oil_values

    def midpoint(self, cell, point_coordinates):
        if len(cell) == 1:  # Vertex
            return np.array(point_coordinates[cell[0]])
        elif len(cell) == 2:  # Line
            point1 = np.array(point_coordinates[cell[0]])
            point2 = np.array(point_coordinates[cell[1]])
            return (point1 + point2) / 2
        elif len(cell) == 3:  # Triangle
            point1 = np.array(point_coordinates[cell[0]])
            point2 = np.array(point_coordinates[cell[1]])
            point3 = np.array(point_coordinates[cell[2]])
            return (point1 + point2 + point3) / 3

    def velocity_field(self, midpoint):
        return np.array([midpoint[1] - 0.2 * midpoint[0], -midpoint[0]])

    def area(self, cell, global_cell_index, areas):
        if len(cell) == 3:  # Triangle
            p1, p2, p3 = cell
            x1, y1 = self._mesh.points[p1][:2]
            x2, y2 = self._mesh.points[p2][:2]
            x3, y3 = self._mesh.points[p3][:2]
            area = 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
            areas[global_cell_index] = area

    
    def normal_vectors_with_faces(self, face, point_coordinates, triangle_midpoint):
        if len(face) != 2:
            return None
        
        # Get points on the face
        point1 = np.array(point_coordinates[face[0]])
        point2 = np.array(point_coordinates[face[1]])

        # Calculate the direction vector
        direction = point2 - point1
        
        # Compute the normal vector
        normal = np.array([-direction[1], direction[0]])

        # Calculate the length of the edge
        edge_length = np.linalg.norm(direction)
         
        # Scale the normal vector by the edge length
        normal *= edge_length
        
        # Calculate the midpoint of the face
        face_midpoint = (point1 + point2) / 2
        
        # Vector from triangle's midpoint to face midpoint
        vector_to_face_midpoint = face_midpoint - triangle_midpoint
        
        # Check if the normal points outward
        if np.dot(normal, vector_to_face_midpoint) < 0:
            normal = -normal  # Flip the normal if it's pointing inward

        return face, normal

    def find_faces(self, num_nodes, cell, global_cell_index, cell_faces, face_to_cells):
        if num_nodes == 1:
            faces = [tuple(sorted(cell))]
        elif num_nodes == 2:
            faces = [tuple(sorted(cell))]
        elif num_nodes == 3:
            faces = [
                tuple(sorted([cell[0], cell[1]])),
                tuple(sorted([cell[1], cell[2]])),
                tuple(sorted([cell[0], cell[2]])),
            ]
        else:
            faces = []
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    faces.append(tuple(([cell[i], cell[j]])))

        cell_faces[global_cell_index] = faces
        for face in faces:
            face_to_cells[face].append(global_cell_index)

    def find_neighbors(self, face_to_cells):
        cell_neighbors = defaultdict(set)
        for face, cells in face_to_cells.items():
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
                
                # Extract parameters for the cell
                oil_amount = cell_info["oil_amount"]
                area = cell_info["area"]
                normal_vectors_with_faces = cell_info["faces"]
                velocity_field = cell_info["velocity_field"]
                neighbors = cell_info["neighbors"]

                # Create the cell using CellFactory
                cell_object = cf(
                    key=cell_type,
                    id=global_cell_index,
                    oil_amount=oil_amount,
                    area=area,
                    normal_vectors_with_faces=normal_vectors_with_faces,
                    faces=normal_vectors_with_faces,
                    velocity_field=velocity_field,
                    neighbors=neighbors,
                    delta_t=self._delta_t,
                )
                
                cells.append(cell_object)
