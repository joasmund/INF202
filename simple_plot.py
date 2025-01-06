import matplotlib.pyplot as plt
import meshio
import numpy as np
from matplotlib.tri import Triangulation

# Load the .msh file
mesh = meshio.read("bay.msh")

# Extract points and triangles (cells) from the mesh
points = mesh.points[:, :2]  # Assuming the mesh is 2D (X, Y)
cells = mesh.cells_dict.get("triangle")  # Triangular elements

# Define the source point (x_star)
x_star = np.array([0.35, 0.45])

# Compute the Gaussian function for each point in the mesh
data = np.exp(-np.linalg.norm(points - x_star, axis=1) ** 2 / 0.01)

# For each triangle, calculate an average data value (or any other aggregation)
triangle_data = []
for triangle in cells:
    # Get the indices of the vertices of the triangle
    indices = triangle
    # Compute the average of the data at the triangle's vertices
    avg_value = np.mean(data[indices])
    triangle_data.append(avg_value)

triangle_data = np.array(triangle_data)

# Create a Triangulation object
triangulation = Triangulation(points[:, 0], points[:, 1], cells)

# Plot the data on the triangular mesh
plt.figure(figsize=(5, 5))
plt.tripcolor(triangulation, facecolors=triangle_data, cmap="viridis", shading="flat")
plt.colorbar(label="Amount of oil")

# Plot the triangle edges with transparency
for triangle in cells:
    # Get the vertices of the triangle
    pts = points[triangle]
    # Loop through the edges and plot each one
    for i in range(3):
        x_values = [pts[i][0], pts[(i + 1) % 3][0]]
        y_values = [pts[i][1], pts[(i + 1) % 3][1]]
        plt.plot(x_values, y_values, color="grey", lw=0.1, alpha=0.3)

# Labels and title
plt.xlabel("X")
plt.ylabel("Y")
plt.title("")
plt.show()
