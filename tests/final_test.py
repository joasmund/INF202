import pytest
import numpy as np
from src.Simulation.cells import Vertex, Line, Triangle  

@pytest.fixture
def sample_points():
    return [
        np.array([0, 0, 0]),
        np.array([1, 0, 0]),
        np.array([0, 1, 0]),
        np.array([1, 1, 0]),
    ]


@pytest.fixture
def sample_cells(sample_points):
    triangle1 = Triangle([0, 1, 2], 0, sample_points)
    triangle2 = Triangle([1, 2, 3], 1, sample_points)
    return [triangle1, triangle2]


def test_vertex_creation(sample_points):
    vertex = Vertex([0], 0, sample_points)
    assert vertex._pointIds == [0]
    assert vertex._idx == 0
    assert str(vertex) == "Vertex with id 0"


def test_line_creation(sample_points):
    line = Line([0, 1], 1, sample_points)
    assert line._pointIds == [0, 1]
    assert line._idx == 1
    assert str(line) == "Line with id 1: []"


def test_triangle_area(sample_points):
    triangle = Triangle([0, 1, 2], 0, sample_points)
    assert triangle.area() == 0.5  


def test_triangle_midpoint(sample_points):
    triangle = Triangle([0, 1, 2], 0, sample_points)
    midpoint = triangle.midpoint()
    assert np.allclose(midpoint, np.array([1 / 3, 1 / 3, 0]))


def test_triangle_line_normals(sample_points):
    triangle = Triangle([0, 1, 2], 0, sample_points)
    normals = triangle.line_normals()
    assert len(normals) == 3
    for normal in normals:
        assert np.isclose(np.linalg.norm(normal), 1)  


def test_neighbors_computation(sample_cells):
    triangle1, triangle2 = sample_cells
    triangle1.computeNeighbors(sample_cells)
    triangle2.computeNeighbors(sample_cells)

    assert triangle1._neighbors == [1]
    assert triangle2._neighbors == [0]


def test_triangle_str(sample_points):
    triangle = Triangle([0, 1, 2], 0, sample_points)
    triangle.computeNeighbors([triangle])
    output = str(triangle)
    assert "Triangle with id 0" in output
    assert "Midpoint of triangle is located at" in output
    assert "0.5" in output
