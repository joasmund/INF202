import matplotlib.pyplot as plt
import numpy as np
from matplotlib.tri import Triangulation

from src.Simulation.cells import Triangle


def plot_triangles_with_oil(cells, points):
    # Extract triangle points and oil values
    triangles = [cell._pointIds for cell in cells if isinstance(cell, Triangle)]
    oil_values = [cell._oil for cell in cells if isinstance(cell, Triangle)]

    # Convert to numpy arrays for efficient processing
    triangles = np.array(triangles)
    oil_values = np.array(oil_values)

    # Create a Triangulation object
    triangulation = Triangulation(
        np.array(points)[:, 0], np.array(points)[:, 1], triangles
    )

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
    plt.show()


# Example Usage
# Assuming `cells` is a list of Cell objects and `points` is a list of point coordinates
# plot_triangles_with_oil(cells, points)
