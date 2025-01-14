from abc import ABC, abstractclassmethod

import numpy as np


class Cell(ABC):
    def __init__(self, id, pt_id, pts_coords) -> None:
        super().__init__()

    def neighbors(self):
        pass

    def midpoint(self):
        pass

    def area(self):
        pass

    def normal_vectors(self):
        pass

    def flux(self):
        pass

    def oil_amount(self):
        pass


class Vertex(Cell):
    def __init__(self, id, pt_id, pts_coords) -> None:
        super().__init__(id, pt_id, pts_coords)


class Line(Cell):
    def __init__(self, id, pt_id, pts_coords) -> None:
        super().__init__(id, pt_id, pts_coords)


class Triangle(Cell):
    def __init__(self, id, pt_id, pts_coords) -> None:
        super().__init__(id, pt_id, pts_coords)
