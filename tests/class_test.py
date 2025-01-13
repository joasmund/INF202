import pytest
import sys
import os
import numpy as np


from src.Simulation.cells import Cell, Vertex, Line, Triangle


@pytest.fixture
def _cell_factory(cell_type, pts, idx):
    def __init__(self) -> None:
        self._cellTypes = {}

    def register(self, key: str, name):
        self._cellTypes[key] = name

    def __call__(self, key, pts, idx, points):
        return self._cellTypes[key](pts, idx, points)




def test_compute_neighbors():
    c = cell_factory
    



class TestPositiveLength:
    def test_positive_length(self):
        c = Cell([1, 2], 1)
        assert c.cell_size() == 1


def test_line():
    l = Line([1, 2], 1)
    assert l.__str__() == "Line with id 1: []"


def test_midpoint():
    c = Triangle((1,1),(2,2), (3,3))
    assert c.midpoint() == 1.5


def test_computeNeighbors():
    l = Line([1, 2], 1)
    l.computeNeighbors([Line([2, 3], 2)])
    assert l._neighbors == [2]


def test_vertex():
    v = Vertex([1], 1)
    assert v.__str__() == "Vertex with id 1: []"


def test_id_positive():
    """
    Test that the ID is positive
    """
    l = Line([1, 2], 1)
    assert l._idx >= 0, f"Line ID is {l._idx}"


def test_cell_id_positive(cells):
    c = Cell([1, 2], 1)
    assert c._idx >= 0, f"Cell ID is {c._idx}"


def test_cell_id(cells):
    for cell in cells:
        assert cell._idx >= 0, f"Cell ID is {cell._idx}"


def test_cell_id_negative():
    c = Cell([1, 2], -1)
    assert c._idx <= 0, f"Cell ID is {c._idx}"


def test_vertex_id_positive():
    v = Vertex([1], 1)
    assert v._idx >= 0, f"Vertex ID is {v._idx}"
