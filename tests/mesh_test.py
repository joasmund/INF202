import pytest
import numpy as np
from src.Simulation.mesh import Mesh

class MockMesh:
    def __init__(self):
        self.points = np.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [1.0, 1.0, 0.0]
        ])
        self.cells_dict = {
            "triangle": [[0, 1, 2], [1, 2, 3]],
            "line": [[0, 1], [1, 2]],
            "vertex": [[0], [1]]
        }

@pytest.fixture
def mesh_instance():
    mock_mesh = MockMesh()
    return Mesh(mock_mesh, delta_t=0.01, x_star=np.array([0.5, 0.5]))

def test_mesh_initialization(mesh_instance):
    assert mesh_instance.mesh is not None
    assert mesh_instance.cells == []

def test_mesh_area_calculation(mesh_instance):
    # Test triangle area calculation
    cell = [0, 1, 2]  # Triangle vertices
    areas = {}
    mesh_instance.area(cell, 1, areas)
    
    # Area should be 0.5 for this triangle
    assert abs(areas[1] - 0.5) < 1e-10

def test_mesh_velocity_field(mesh_instance):
    midpoint = np.array([0.5, 0.5])
    velocity = mesh_instance.velocity_field(midpoint)
    
    # Test velocity field calculation
    expected_velocity = np.array([0.4, -0.5])  # Based on the formula
    assert np.allclose(velocity, expected_velocity)

def test_mesh_initial_oil(mesh_instance):
    cell_points = {1: [0, 1, 2]}
    point_coordinates = {
        0: [0.0, 0.0],
        1: [1.0, 0.0],
        2: [0.0, 1.0]
    }
    
    oil_values = mesh_instance.initial_oil(cell_points, point_coordinates)
    assert 1 in oil_values
    assert 0 <= oil_values[1] <= 1  # Oil values should be between 0 and 1

def test_mesh_normal_vectors(mesh_instance):
    point_coordinates = {
        0: [0.0, 0.0],
        1: [1.0, 0.0]
    }
    face = (0, 1)
    triangle_midpoint = np.array([0.5, 0.5])
    
    result = mesh_instance.normal_vectors_with_faces(face, point_coordinates, triangle_midpoint)
    assert result is not None
    assert len(result) == 2
    assert isinstance(result[1], np.ndarray)  # Normal vector should be numpy array

def test_mesh_find_neighbors(mesh_instance):
    face_to_cells = {
        (0, 1): [1, 2],  # Face shared between cells 1 and 2
        (1, 2): [1, 3],  # Face shared between cells 1 and 3
        (2, 3): [2, 3]   # Face shared between cells 2 and 3
    }
    
    neighbors = mesh_instance.find_neighbors(face_to_cells)
    
    assert 2 in neighbors[1]  # Cell 1 should be neighbor with cell 2
    assert 3 in neighbors[1]  # Cell 1 should be neighbor with cell 3
    assert 3 in neighbors[2]  # Cell 2 should be neighbor with cell 3

def test_mesh_midpoint_calculation(mesh_instance):
    # Test vertex midpoint
    vertex = [0]
    point_coordinates = {0: [0.0, 0.0]}
    midpoint = mesh_instance.midpoint(vertex, point_coordinates)
    assert np.array_equal(midpoint, np.array([0.0, 0.0]))
    
    # Test line midpoint
    line = [0, 1]
    point_coordinates = {0: [0.0, 0.0], 1: [1.0, 0.0]}
    midpoint = mesh_instance.midpoint(line, point_coordinates)
    assert np.array_equal(midpoint, np.array([0.5, 0.0]))
    
    # Test triangle midpoint
    triangle = [0, 1, 2]
    point_coordinates = {0: [0.0, 0.0], 1: [1.0, 0.0], 2: [0.0, 1.0]}
    midpoint = mesh_instance.midpoint(triangle, point_coordinates)
    expected_midpoint = np.array([1/3, 1/3])
    assert np.allclose(midpoint, expected_midpoint)

def test_mesh_invalid_cell_type(mesh_instance):
    # Test with invalid cell (4 points)
    invalid_cell = [0, 1, 2, 3]
    point_coordinates = {
        0: [0.0, 0.0],
        1: [1.0, 0.0],
        2: [0.0, 1.0],
        3: [1.0, 1.0]
    }
    
    with pytest.raises(ValueError):
        mesh_instance.midpoint(invalid_cell, point_coordinates)