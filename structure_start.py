import time
from abc import ABC, abstractmethod

import meshio
import numpy as np
import toml

# Load configuration from toml file
config = toml.load("config.toml")

mshName = config["geometry"]["meshName"]
mshName2 = config["geometry"]["meshName2"]

startTime = time.time()


class Mesh:
    def __init__(self, mshName) -> None:
        """
        Constructor of mesh class reads in and creates the
        computational mesh and stores points and cells
        :param mshName: name of the .msh file that needs to be stored
        """
        msh = meshio.read(mshName)

        cells = msh.cells

        self._points = msh.points  # List of all cells

        cf = CellFactory()

        cf.register("vertex", Vertex)
        cf.register("line", Line)
        cf.register("triangle", Triangle)

        self._cells = []  # List of all points

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


class CellFactory:
    def __init__(self) -> None:
        self._cellTypes = {}

    def register(self, key: str, name):
        self._cellTypes[key] = name

    def __call__(self, key, pts, idx) -> None:
        return self._cellTypes[key](pts, idx)


class Cell(ABC):
    def __init__(self, pts, idx) -> None:
        self._pointIds = pts  # Index (in the points list in the mesh) of points in cell
        self._idx = idx  # Cell id
        self._neighbors = []  # List of neighbors

    def computeNeighbors(self, cells):
        """
        This function computes cell neighbors for current instance
        """
        for cell in cells:
            matches = set(self._pointIds) & set(cell._pointIds)
            if len(matches) == 2:
                self._neighbors.append(cell._idx)
        pass

    @abstractmethod
    def __str__(self) -> str:
        return ""


class Vertex(Cell):
    def __init__(self, pts, idx) -> None:
        super().__init__(pts, idx)

    def __str__(self) -> str:
        """
        Prints out "Vertex"
        """
        return f"Vertex with id {self._idx}"


class Line(Cell):
    def __init__(self, pts, idx) -> None:
        super().__init__(pts, idx)

    def __str__(self) -> str:
        """
        Prints out "Line" and then all neighbors
        """
        return f"Line with id {self._idx}: {self._neighbors}"


class Triangle(Cell):
    def __init__(self, pts, idx) -> None:
        super().__init__(pts, idx)

    def __str__(self) -> str:
        """
        Prints out "Triangle" and then all neighbors
        """
        return f"Triangle with id {self._idx}: {self._neighbors}"


m = Mesh(mshName)
m.computeNeighbors()
cell = m._cells[3]
points = m._points
pts = cell._pointIds
print(points[pts])
print(cell)

endTime = time.time()

print(f"Execution time: {endTime - startTime} seconds")
