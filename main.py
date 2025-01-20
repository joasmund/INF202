
import time
import meshio
import toml
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.tri import Triangulation
from src.Simulation.cells import Triangle
from src.Simulation.mesh import Mesh

# Load configuration from toml file
config = toml.load("input.toml")
mshName = config["geometry"]["meshName"]

nSteps = 500  # Number of steps
tStart = 0.0  # Start time
tEnd = 0.5    # End time

if __name__ == "__main__":
    start_time = time.time()

    # Create the mesh and compute neighbors
    mesh = meshio.read(mshName)
    mesh = Mesh(mesh)
    final_cell_data, cell_type_mapping = mesh.main_function()

    # Initialize lists for storing the triangles and oil amounts
    triangles = []
    in_oil_amount = []
    points = mesh._mesh.points  # Get the points from the mesh

    # Store triangle cell data and initial oil amounts in a single pass
    for cell_type, cell_data in mesh._mesh.cells_dict.items():
        for local_index, cell in enumerate(cell_data):
            if len(cell) == 3:  # Only consider triangles
                triangles.append(cell)  # Store triangle vertex indices
                in_oil_amount.append(final_cell_data[cell_type_mapping[(cell_type, local_index)]]['oil_amount'])

    # Convert lists to numpy arrays for efficiency
    triangles = np.array(triangles)
    points = np.array(points)
    in_oil_amount = np.array(in_oil_amount)

    # Calculate delta_t for each time step
    delta_t = (tEnd - tStart) / nSteps

    # Perform computations over nSteps (update oil amounts directly)
    for step in range(nSteps):
        current_time = tStart + step * delta_t
        # Update oil amounts in all triangular cells in one loop
        for cell in mesh._cells:
            if isinstance(cell, Triangle):
                cell.update_oil_amount()

    # Collect the final oil amounts directly (single pass)
    final_oil_amount = np.array([cell.oil_amount for cell in mesh._cells if isinstance(cell, Triangle)])

    # Create a Triangulation object
    triangulation = Triangulation(points[:, 0], points[:, 1], triangles)

    # Plot initial oil distribution and final oil distribution
    plt.figure(figsize=(10, 5))

    # Plot initial oil distribution
    plt.subplot(1, 2, 1)
    plt.tripcolor(triangulation, facecolors=in_oil_amount, cmap="viridis", shading="flat")
    plt.colorbar(label="Initial Amount of Oil")
    plt.title("Initial Oil Distribution")
    plt.xlabel("X")
    plt.ylabel("Y")

    # Plot final oil distribution
    plt.subplot(1, 2, 2)
    plt.tripcolor(triangulation, facecolors=final_oil_amount, cmap="viridis", shading="flat")
    plt.colorbar(label="Final Amount of Oil")
    plt.title("Final Oil Distribution After Updates")
    plt.xlabel("X")
    plt.ylabel("Y")

    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")

    # Display plots
    plt.tight_layout()
    plt.show()
