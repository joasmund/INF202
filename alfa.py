import meshio
import numpy as np

data = meshio.read("bay.msh")
points = data.points
cells = data.cells

print(cells[11])
