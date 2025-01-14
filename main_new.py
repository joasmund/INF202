import time
from collections import defaultdict

import meshio
import numpy as np


def find_neighbors(mesh):
    # Print cell types and their counts
    # print("\nCell types in mesh:")
    # for cell_type, cell_data in mesh.cells_dict.items():
    #     print(f"{cell_type}: {len(cell_data)} elements")
    # print("\n")

    face_to_cells = defaultdict(list)
    cell_faces = {}  # Dictionary to store faces for each cell

    # Create a global cell index mapping
    global_index = 1
    cell_type_mapping = {}  # Maps (cell_type, local_index) to global_index

    # First pass: create global indices
    for cell_type, cell_data in mesh.cells_dict.items():
        for local_index in range(len(cell_data)):
            cell_type_mapping[(cell_type, local_index)] = global_index
            global_index += 1

    # Process all cell types
    for cell_type, cell_data in mesh.cells_dict.items():
        for local_index, cell in enumerate(cell_data):
            global_cell_index = cell_type_mapping[(cell_type, local_index)]
            num_nodes = len(cell)

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
            cell_faces[global_cell_index] = (cell_type, faces)

            for face in faces:
                face_to_cells[face].append(global_cell_index)

    # # Print faces for each cell
    # print("Faces for each cell:")
    # for cell_index in sorted(cell_faces.keys()):
    #     cell_type, faces = cell_faces[cell_index]
    #     print(f"Cell {cell_index} ({cell_type}) faces: {faces}")
    # print("\n")

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

    # # Sort and print neighbors
    # print("\nNeighbors for each cell:")
    # for cell_index in sorted(cell_faces.keys()):
    #     cell_type = cell_faces[cell_index][0]
    #     neighbors_list = sorted(cell_neighbors[cell_index])
    #     print(f"Cell {cell_index} ({cell_type}) has neighbors: {neighbors_list}")

    return cell_neighbors


# Load the mesh file
mesh = meshio.read("bay.msh")

# Measure the time taken to find neighbors
start_time = time.time()

# Find neighbors
neighbors = find_neighbors(mesh)

end_time = time.time()

# Print the time taken
print(f"\nExecution Time: {end_time - start_time} seconds")
