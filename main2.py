import time

import matplotlib.pyplot as plt
import numpy as np
import toml
from matplotlib.tri import Triangulation

from src2.Simulation.cells2 import Triangle
from src2.Simulation.mesh2 import Mesh

if __name__ == "__main__":

    # Load configuration from toml file
    config = toml.load("input.toml")
    mshName = config["geometry"]["meshName"]

    startTime = time.time()

    # Create the mesh and compute neighbors
    mesh = Mesh(mshName)
    mesh.computeNeighbors()

    # # Extract oil values and prepare for plotting
    # points = mesh.coordinates
    # triangles = []
    # oil_values = []
    #
    # for cell in mesh.cells:
    #     if isinstance(cell, Triangle):
    #         triangles.append(cell._pointIds)  # Store triangle vertex indices
    #         oil_values.append(cell.initial_oil())  # Compute oil value for the cell
    #
    # triangles = np.array(triangles)
    # oil_values = np.array(oil_values)
    #
    # # Plot the data
    # triangulation = Triangulation(points[:, 0], points[:, 1], triangles)
    #
    # plt.figure(figsize=(5, 5))
    # plt.tripcolor(triangulation, facecolors=oil_values, cmap="viridis", shading="flat")
    # plt.colorbar(label="Amount of oil")
    #
    # # Plot triangle edges with transparency
    # for triangle in triangles:
    #     pts = points[triangle]
    #     for i in range(3):
    #         x_values = [pts[i][0], pts[(i + 1) % 3][0]]
    #         y_values = [pts[i][1], pts[(i + 1) % 3][1]]
    #         plt.plot(x_values, y_values, color="grey", lw=0.1, alpha=0.3)
    #
    #
    # # Labels and title
    # plt.xlabel("X")
    # plt.ylabel("Y")
    # plt.title("Oil Distribution on Triangular Mesh")
    # plt.show()

    for cell in mesh.cells:
        print(cell)

    endTime = time.time()
    print(f"Execution time: {endTime - startTime} seconds")

    """

3710: {3562, 3443, 3511}, 
3711: {3642, 349, 470}, 
3712: {520, 3662, 3638}, 
3713: {3524, 3605, 3679}, 
3714: {3664, 3715, 470}, 
3715: {322, 3714, 3495}, 
3716: {3624, 3698, 3660}, 
3717: {3634, 3659, 292}, 
3718: {3576, 3689, 3603}, 
3719: {3490, 3645, 3647}, 
3720: {3708, 3577, 3628}}
    """
