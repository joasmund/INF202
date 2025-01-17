import time
from collections import defaultdict

import meshio
import numpy as np


def find_neighbors(mesh):

    # Create a global cell index mapping
    global_index = 1
    cell_type_mapping = {}  # Maps (cell_type, local_index) to global_index

    face_to_cells = defaultdict(list)
    cell_faces = {}  # Dictionary to store faces for each cell
    cell_points = defaultdict(list)  # Maps global cell index to its points (nodes)
    point_coordinates = defaultdict(list)  # Maps point index to the coordinates of that point

    # Store the point coordinates
    for i, point in enumerate(mesh.points):
        point_coordinates[i] = point[:2].tolist()  # Store coordinates of each point

    for cell_type, cell_data in mesh.cells_dict.items():
        for local_index, cell in enumerate(cell_data):
            # Create global index mapping
            cell_type_mapping[(cell_type, local_index)] = global_index
            global_cell_index = global_index
            global_index += 1

            # Perform additional processing
            num_nodes = len(cell)

            cell_points[global_cell_index] = cell  # Points are the nodes of the cell

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

    # Check for non-manifold edges
    # non_manifold_edges = [
    #     (face, cells) for face, cells in face_to_cells.items() if len(cells) > 2
    # ]
    # if non_manifold_edges:
    #     print("Warning: Found non-manifold edges:")
    #     for edge, cells in non_manifold_edges:
    #         print(f"Edge {edge} is shared by cells: {cells}")

    cell_neighbors = defaultdict(set)
    for face, cells in face_to_cells.items():
        if len(cells) == 2:  # Only process manifold edges/faces
            cell_neighbors[cells[0]].add(cells[1])
            cell_neighbors[cells[1]].add(cells[0])

    print(dict(sorted(cell_neighbors.items())))
    # print(dict(sorted(cell_faces.items())))
    # print(dict(sorted(face_to_cells.items())))
    # print(dict(sorted(cell_points.items())))
    # print(dict(sorted(point_coordinates.items())))
    # print(dict((cell_type_mapping)))

    return cell_neighbors


# Load the mesh file bay.msh
mesh = meshio.read("bay.msh")

# Measure the time taken to find neighbors
start_time = time.time()

# Find neighbors
neighbors = find_neighbors(mesh)

end_time = time.time()

# Print the time taken
print(f"\nExecution Time: {end_time - start_time} seconds")
