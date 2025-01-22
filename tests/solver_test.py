import numpy as np
import pytest

from src.Simulation.factory import CellFactory 
from src.Simulation.cells import Cell, Vertex, Line, Triangle

@pytest.fixture
def cell_factory():
    factory = CellFactory()
    factory.register("Vertex", Vertex)
    factory.register("Line", Line)
    factory.register("Triangle", Triangle)
    return factory

@pytest.mark.parametrize(
    "cell_type, pts, idx", [("Vertex", [1], 1), 
                            ("Line", [1, 2], 1), 
                            ("Triangle", [1, 2, 3], 1)])
def test_register(cell_factory, cell_type, pts, idx):
    assert cell_factory._cellTypes == {"Vertex": Vertex, "Line": Line, "Triangle": Triangle}


