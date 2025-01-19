import time
import meshio
import toml
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.tri import Triangulation
from src.Simulation.mesh import Mesh

# Load configuration from toml file
config = toml.load("input.toml")
mshName = config["geometry"]["meshName"]

startTime = time.time()

# Create the mesh and compute neighbors
mesh = meshio.read(mshName)
mesh = Mesh(mesh)
final_cell_data, cell_type_mapping = mesh.main_function()

# Extract oil values and prepare for plotting
oil_values = []
triangles = []
points = mesh._mesh.points  # Get the points from the mesh

# Assuming that the mesh is composed of triangular cells:
for cell_type, cell_data in mesh._mesh.cells_dict.items():
    for local_index, cell in enumerate(cell_data):
        if len(cell) == 3:  # Only consider triangles
            triangles.append(cell)  # Store triangle vertex indices
            oil_values.append(final_cell_data[cell_type_mapping[(cell_type, local_index)]]['oil_amount'])

# Convert to numpy arrays for efficient processing
triangles = np.array(triangles)
oil_values = np.array(oil_values)

# Create a Triangulation object
triangulation = Triangulation(np.array(points)[:, 0], np.array(points)[:, 1], triangles)

# Plot the data on the triangular mesh
plt.figure(figsize=(5, 5))
plt.tripcolor(triangulation, facecolors=oil_values, cmap="viridis", shading="flat")
plt.colorbar(label="Amount of oil")

# Plot the triangle edges with transparency
for triangle in triangles:
    # Get the vertices of the triangle
    pts = np.array([points[pt] for pt in triangle])
    # Loop through the edges and plot each one
    for i in range(3):
        x_values = [pts[i][0], pts[(i + 1) % 3][0]]
        y_values = [pts[i][1], pts[(i + 1) % 3][1]]
        plt.plot(x_values, y_values, color="grey", lw=0.1, alpha=0.3)

# Labels and title
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Oil Distribution in Triangular Mesh")
endTime = time.time()
print(f"Execution time: {endTime - startTime} seconds")
plt.show()


