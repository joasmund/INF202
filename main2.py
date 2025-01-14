import time

import matplotlib.pyplot as plt
import numpy as np
import toml
from matplotlib.tri import Triangulation

from src2.Simulation.cells2 import Triangle
from src2.Simulation.mesh2 import Mesh

if __name__ == "__main__":

    # Load configuration from toml file
    config = toml.load("config.toml")
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
Cell 3503 has neighbors: [96, 124, 3276]
Cell 3504 has neighbors: [132, 3278, 3469]
Cell 3505 has neighbors: [191, 3354, 3374]
Cell 3506 has neighbors: [615, 2591, 3457]
Cell 3507 has neighbors: [3311, 3388, 3509]
Cell 3508 has neighbors: [204, 3450, 3466]
Cell 3509 has neighbors: [2889, 3431, 3507]
Cell 3510 has neighbors: [106, 179, 3444]
Cell 3511 has neighbors: [3196, 3484, 3529]
Cell 3512 has neighbors: [3269, 3292, 3410]
Cell 3513 has neighbors: [24, 3478, 3500]
Cell 3514 has neighbors: [3336, 3362, 3501]
Cell 3515 has neighbors: [3372, 3411, 3489]
Cell 3516 has neighbors: [259, 3130, 3368]
Cell 3517 has neighbors: [3182, 3415, 3470]
Cell 3518 has neighbors: [3321, 3359, 3456]
Cell 3519 has neighbors: [3173, 3301, 3349]
Cell 3520 has neighbors: [246, 568, 3324]
Cell 3521 has neighbors: [99, 3467, 3533]
Cell 3522 has neighbors: [138, 3426, 3481]
Cell 3523 has neighbors: [3256, 3324, 3375]
Cell 3524 has neighbors: [162, 283, 3455]
Cell 3525 has neighbors: [333, 3451, 3475]
Cell 3526 has neighbors: [3337, 3418, 3492]
Cell 3527 has neighbors: [283, 3477, 3528]
Cell 3528 has neighbors: [135, 3308, 3527]
Cell 3529 has neighbors: [3437, 3473, 3511]
Cell 3530 has neighbors: [105, 3447, 3472]
Cell 3531 has neighbors: [3389, 3416, 3502]
Cell 3532 has neighbors: [3303, 3458, 3460]
Cell 3533 has neighbors: [3390, 3441, 3521]
    """
