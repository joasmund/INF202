
import os
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
tStart = 0.1  # Start time
tEnd = 0.2    # End time

if __name__ == "__main__":
    start_time = time.time()

    # Create the mesh and compute neighbors
    mesh = meshio.read(mshName)
    mesh = Mesh(mesh)
    final_cell_data, cell_type_mapping = mesh.main_function()

    # for cell in mesh._cells:
    #     print(cell)
    # Initialize lists for storing the triangles and oil amounts
    triangles = []
    in_oil_amount = []
    points = mesh._mesh.points  # Get the points from the mesh

    # Store triangle cell data and initial oil amounts in a single pass
    triangle_cell_indices = []  # To map oil amounts to triangles
    for cell_type, cell_data in mesh._mesh.cells_dict.items():
        for local_index, cell in enumerate(cell_data):
            if len(cell) == 3:  # Only consider triangles
                triangles.append(cell)  # Store triangle vertex indices
                triangle_cell_indices.append(cell_type_mapping[(cell_type, local_index)])
                in_oil_amount.append(final_cell_data[cell_type_mapping[(cell_type, local_index)]]['oil_amount'])

    # Convert lists to numpy arrays for efficiency
    triangles = np.array(triangles)
    points = np.array(points)
    in_oil_amount = np.array(in_oil_amount)

    # Create the /plots directory if it doesn't exist
    output_dir = "./plots"
    os.makedirs(output_dir, exist_ok=True)

    # Calculate delta_t for each time step
    delta_t = (tEnd - tStart) / nSteps

    # Perform computations over nSteps (update oil amounts directly)
    for step in range(nSteps):
        current_time = tStart + step * delta_t

        # Create a temporary array to store updated oil amounts for triangles
        updated_oil_amounts = []

        # Update oil amounts for each triangular cell
        for cell in mesh._cells:
            if isinstance(cell, Triangle):
                cell.oil_amount = cell.update_oil_amount()

        # Collect updated oil amounts for triangular cells only
        for cell_index in triangle_cell_indices:
            updated_oil_amounts.append(mesh._cells[cell_index - 1].oil_amount)

        updated_oil_amounts = np.array(updated_oil_amounts)

        # Save a plot every 50 iterations
        if step % 50 == 0:
            print(f"Step {step}, Time: {current_time}")
            print("Oil distribution:", updated_oil_amounts)

            # Create a Triangulation object for plotting
            triangulation = Triangulation(points[:, 0], points[:, 1], triangles)

            # Generate the plot
            plt.figure(figsize=(8, 6))
            plt.tripcolor(triangulation, facecolors=updated_oil_amounts, cmap="viridis", shading="flat")
            plt.colorbar(label="Oil Amount")
            plt.title(f"Oil Distribution at Step {step}")
            plt.xlabel("X")
            plt.ylabel("Y")

            # Save the plot
            plot_filename = os.path.join(output_dir, f"step_{step:04d}.png")
            plt.savefig(plot_filename)
            plt.close()  # Close the figure to save memory

    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")
