import meshio
import numpy as np

from .cells2 import Line, Triangle, Vertex
from .solver2 import CellFactory


class Mesh:
    def __init__(self, mshName) -> None:
        """
        Constructor of mesh class reads in and creates the
        computational mesh and stores points and cells
        :param mshName: name of the .msh file that needs to be stored
        """
        self._msh = meshio.read(mshName)  # Store msh as an instance variable

        cells = self._msh.cells

        self._points = np.array(
            np.vstack(self._msh.points)[:, :2]
        )  # List of all points

        cf = CellFactory()

        cf.register("vertex", Vertex)
        cf.register("line", Line)
        cf.register("triangle", Triangle)

        self._cells = []  # List of all cells

        for cellForType in cells:
            cellType = cellForType.type  # Type of cell (Vertex, Line, Triangle)
            for pts in cellForType.data:
                idx = len(self._cells)
                self._cells.append(cf(cellType, pts, idx, self.coordinates))

    def computeNeighbors(self):
        """
        Calls computeNeighbors function for every cell
        """
        [cell.computeNeighbors(self._cells) for cell in self._cells]

    @property
    def coordinates(self):
        return self._points

    @property
    def cells(self):
        return self._cells
