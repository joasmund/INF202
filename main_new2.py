import time
import meshio
import toml

# import matplotlib.pyplot as plt
# import numpy as np
# from matplotlib.tri import Triangulation

from src.Simulation.mesh import Mesh


# Load configuration from toml file
config = toml.load("input.toml")
mshName = config["geometry"]["meshName"]

startTime = time.time()

# Create the mesh and compute neighbors
mesh = meshio.read(mshName)
mesh = Mesh(mesh)
mesh.main_function()

print(mesh.main_function())

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

endTime = time.time()
print(f"Execution time: {endTime - startTime} seconds")
