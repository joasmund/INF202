import pytest
import numpy as np
from src.Simulation.cells import Triangle, Line, Vertex

# Fixtures for common test data
@pytest.fixture
def basic_cell_data():
    return {
        'id': 1,
        'oil_amount': 1.0,
        'area': 0.5,
        'velocity_field': np.array([1.0, 0.0]),
        'delta_t': 0.01,
        'normal_vectors_with_faces': [],
        'faces': [],
        'neighbors': []
    }

@pytest.fixture
def triangle_with_neighbors(basic_cell_data):
    data = basic_cell_data.copy()
    data.update({
        'normal_vectors_with_faces': [((0, 1), np.array([1.0, 0.0]))],
        'faces': [((0, 1), np.array([1.0, 0.0]))],
        'neighbors': [{
            'neighbor_index': 2,
            'neighbor_faces': [(0, 1)],
            'neighbor_velocity_field': np.array([1.0, 0.0]),
            'neighbor_oil_amount': 0.5
        }]
    })
    return Triangle(**data)

@pytest.fixture
def simple_triangle(basic_cell_data):
    return Triangle(**basic_cell_data)

# Triangle tests
class TestTriangle:
    def test_initialization(self, triangle_with_neighbors):
        """Test triangle initialization with all properties."""
        assert triangle_with_neighbors.id == 1
        assert triangle_with_neighbors.oil_amount == 1.0
        assert triangle_with_neighbors.faces == [((0, 1), np.array([1.0, 0.0]))]
        assert np.array_equal(triangle_with_neighbors.velocity_field, np.array([1.0, 0.0]))

    def test_oil_update(self, triangle_with_neighbors):
        """Test oil amount update calculation."""
        new_oil_amount = triangle_with_neighbors.update_oil_amount()
        assert isinstance(new_oil_amount, float)
        assert new_oil_amount != triangle_with_neighbors.oil_amount

    @pytest.mark.parametrize("u_i, u_ngh, nu, v, expected", [
        (1.0, 0.5, np.array([1.0, 0.0]), np.array([1.0, 0.0]), 1.0),  # Positive flux
        (1.0, 0.5, np.array([-1.0, 0.0]), np.array([1.0, 0.0]), -0.5),  # Negative flux
        (1.0, 0.5, np.array([0.0, 1.0]), np.array([0.0, 0.0]), 0.0),  # Zero velocity
    ])
    def test_flux_calculations(self, simple_triangle, u_i, u_ngh, nu, v, expected):
        """Test various flux calculations with parameterized inputs."""
        flux = simple_triangle.flux(u_i, u_ngh, nu, v)
        assert np.isclose(flux, expected)

# Line tests
class TestLine:
    def test_initialization(self, basic_cell_data):
        """Test line initialization."""
        line = Line(**basic_cell_data)
        assert line.id == basic_cell_data['id']
        assert isinstance(line.id, int)

# Vertex tests
class TestVertex:
    def test_initialization(self, basic_cell_data):
        """Test vertex initialization."""
        vertex = Vertex(**basic_cell_data)
        assert vertex.id == basic_cell_data['id']
        assert isinstance(vertex.id, int)

# Edge cases and error handling
class TestEdgeCases:
    def test_triangle_zero_area(self, basic_cell_data):
        """Test triangle behavior with zero area."""
        data = basic_cell_data.copy()
        data['area'] = 0.0
        triangle = Triangle(**data)
        # Verify no division by zero in oil update
        new_amount = triangle.update_oil_amount()
        assert isinstance(new_amount, float)

    def test_triangle_negative_oil(self, basic_cell_data):
        """Test triangle behavior with negative oil amount."""
        data = basic_cell_data.copy()
        data['oil_amount'] = -1.0
        triangle = Triangle(**data)
        assert triangle.oil_amount == -1.0

    @pytest.mark.parametrize("invalid_velocity", [
        None,
        [1.0, 0.0],  # Should be numpy array
        np.array([1.0, 0.0, 0.0])  # Wrong dimensions
    ])
    def test_invalid_velocity_field(self, basic_cell_data, invalid_velocity):
        """Test handling of invalid velocity field formats."""
        data = basic_cell_data.copy()
        data['velocity_field'] = invalid_velocity
        if invalid_velocity is None:
            with pytest.raises(TypeError):
                Triangle(**data)
        elif isinstance(invalid_velocity, list):
            with pytest.raises(AttributeError):
                Triangle(**data)
        else:
            with pytest.raises(ValueError):
                triangle = Triangle(**data)
                _ = triangle.update_oil_amount()