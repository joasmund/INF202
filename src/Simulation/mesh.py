import meshio
import numpy as np


class Mesh:
    def __init__(self, meshName) -> None:
        self._mesh = meshio.read(meshName)

        self._points = np.array(np.vstack(self._mesh.points[:, :2]))
        cells = self._mesh.cells

        for cell in cells:
            for points in cell

