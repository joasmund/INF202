

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


if __name__ == "__main__":
    start_time = time.time()

    # Create the mesh and compute neighbors
    mesh = meshio.read(mshName)
    mesh = Mesh(mesh)
    final_cell_data, cell_type_mapping = mesh.main_function()

    for cell in mesh._cells:
        if isinstance(cell, Triangle):
            print(cell.oil_amount)
