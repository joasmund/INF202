import meshio
import numpy as np
import toml

from .cells import Line, Triangle, Vertex
from .solver import CellFactory

x_star = config[]

class Mesh:
    def __init__(self, mshName) -> None:
        """
        Constructor of mesh class reads in and creates the
        computational mesh and stores points and cells
        :param mshName: name of the .msh file that needs to be stored
        """
        msh = meshio.read(mshName)

        cells = msh.cells

        self._points = np.array(
            np.vstack(msh.points)[:, :2], dtype=np.float64
        )  # List of all points

        # self._points = np.vstack(msh.points)[:, :2]

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
        """
        Turn the arrays into a single numpy array
        and remove the z-axis
        """
        return self._points
