from abc import ABC, abstractmethod

import meshio
import numpy as np
import toml

# Load configuration from toml file
config = toml.load("config.toml")

mshName = config["geometry"]["meshName"]


class Mesh:
    def __init__(self, mshName) -> None:
        """
        Constructor of mesh class reads in and creates the
        computational mesh and stores points and cells
        :param mshName: name of the .msh file that needs to be stored
        """
        msh = meshio.read(mshName)

        self._cells = msh.cells  # List of all cells
        self._points = msh.points  # List of all points
        pass

    def compute_neighbors(self):
        """
        Calls compute_neighbors function for every cell
        """
        pass


class CellFactory:
    def __init__(self) -> None:
        self._cellTypes = {}

    def register(self, key: str, name):
        self._cellTypes[key] = name

    def __call__(self, key) -> None:
        return self._cellTypes[key]()


class Cell(ABC):
    def __init__(self) -> None:
        self._pointIds = 0  # Index (in the points list in the mesh) of points in cell
        self._idx = 0  # Cell id
        self._neighbors = []  # List of neighbors

    def compute_neighbors(self):
        """
        This function computes cell neighbors for current instance
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        return ""


class Vertex(Cell):
    def __init__(self) -> None:
        super().__init__()

    def compute_neighbors(self):
        pass

    def __str__(self) -> str:
        return ""


class Line(Cell):
    def __init__(self) -> None:
        super().__init__()

    def compute_neighbors(self):
        pass

    def __str__(self) -> str:
        return ""


class Triangle(Cell):
    def __init__(self) -> None:
        super().__init__()

    def compute_neighbors(self):
        pass

    def __str__(self) -> str:
        return ""


m = Mesh()
t = Triangle()

cf = CellFactory()
cf.register("line", Line)
cf.register("triangle", Triangle)

lineCell = cf("line")
triangleCell = cf("triangle")

print(lineCell._pointIds)
