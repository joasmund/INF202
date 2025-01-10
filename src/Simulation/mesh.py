import meshio

from .cells import Line, Triangle, Vertex
from .solver import CellFactory


class Mesh:
    def __init__(self, mshName) -> None:
        """
        Constructor of mesh class reads in and creates the
        computational mesh and stores points and cells
        :param mshName: name of the .msh file that needs to be stored
        """
        msh = meshio.read(mshName)

        cells = msh.cells

        self._points = msh.points  # List of all points

        cf = CellFactory()

        cf.register("vertex", Vertex)
        cf.register("line", Line)
        cf.register("triangle", Triangle)

        self._cells = []  # List of all cells

        for cellForType in cells:
            cellType = cellForType.type  # Type of cell (Vertex, Line, Triangle)
            for pts in cellForType.data:
                idx = len(self._cells)
                self._cells.append(cf(cellType, pts, idx))

    def computeNeighbors(self):
        """
        Calls computeNeighbors function for every cell
        """
        for cell in self._cells:
            cell.computeNeighbors(self._cells)
