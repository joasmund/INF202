import pytest
import numpy as np
from src.Simulation.cells import Triangle, Line, Vertex

def test_triangle_initialization():
    # Test data
    id = 1
    oil_amount = 1.0
    area = 0.5
    normal_vectors = [((0, 1), np.array([1.0, 0.0]))]
    faces = [((0, 1), np.array([1.0, 0.0]))]
    velocity_field = np.array([1.0, 0.0])
    neighbors = [{'neighbor_index': 2, 'neighbor_faces': [(0, 1)], 
                 'neighbor_velocity_field': np.array([1.0, 0.0]), 
                 'neighbor_oil_amount': 0.5}]
    delta_t = 0.01

    # Create triangle cell
    triangle = Triangle(id, oil_amount, area, normal_vectors, faces, 
                       velocity_field, neighbors, delta_t)

    # Test properties
    assert triangle.id == id
    assert triangle.oil_amount == oil_amount
    assert triangle.faces == faces
    assert np.array_equal(triangle.velocity_field, velocity_field)

def test_triangle_oil_update():
    # Test data
    triangle = Triangle(
        id=1,
        oil_amount=1.0,
        area=0.5,
        normal_vectors_with_faces=[((0, 1), np.array([1.0, 0.0]))],
        faces=[((0, 1), np.array([1.0, 0.0]))],
        velocity_field=np.array([1.0, 0.0]),
        neighbors=[{
            'neighbor_index': 2,
            'neighbor_faces': [(0, 1)],
            'neighbor_velocity_field': np.array([1.0, 0.0]),
            'neighbor_oil_amount': 0.5
        }],
        delta_t=0.01
    )

    # Test oil amount update
    new_oil_amount = triangle.update_oil_amount()
    assert isinstance(new_oil_amount, float)
    assert new_oil_amount != triangle.oil_amount  # Should change due to flux

def test_triangle_flux():
    triangle = Triangle(
        id=1,
        oil_amount=1.0,
        area=0.5,
        normal_vectors_with_faces=[],
        faces=[],
        velocity_field=np.array([1.0, 0.0]),
        neighbors=[],
        delta_t=0.01
    )

    # Test positive flux
    flux_pos = triangle.flux(
        u_i=1.0,
        u_ngh=0.5,
        nu=np.array([1.0, 0.0]),
        v=np.array([1.0, 0.0])
    )
    assert flux_pos == 1.0  # Should use u_i when v·n > 0

    # Test negative flux
    flux_neg = triangle.flux(
        u_i=1.0,
        u_ngh=0.5,
        nu=np.array([-1.0, 0.0]),
        v=np.array([1.0, 0.0])
    )
    assert flux_neg == -0.5  # Should use u_ngh when v·n < 0

def test_line_initialization():
    line = Line(
        id=1,
        oil_amount=1.0,
        area=0.1,
        normal_vectors_with_faces=[],
        faces=[],
        velocity_field=np.array([0.0, 0.0]),
        neighbors=[],
        delta_t=0.01
    )
    assert line.id == 1

def test_vertex_initialization():
    vertex = Vertex(
        id=1,
        oil_amount=1.0,
        area=0.0,
        normal_vectors_with_faces=[],
        faces=[],
        velocity_field=np.array([0.0, 0.0]),
        neighbors=[],
        delta_t=0.01
    )
    assert vertex.id == 1