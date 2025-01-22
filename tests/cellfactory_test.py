import pytest
import numpy as np
from src.Simulation.factory import CellFactory
from src.Simulation.cells import Triangle, Line, Vertex

@pytest.fixture
def empty_factory():
    """Provides a fresh, unregistered CellFactory instance."""
    return CellFactory()

@pytest.fixture
def factory_with_triangle(empty_factory):
    """Provides a CellFactory with Triangle registered."""
    empty_factory.register("triangle", Triangle)
    return empty_factory

@pytest.fixture
def full_factory(empty_factory):
    """Provides a CellFactory with all cell types registered."""
    empty_factory.register("triangle", Triangle)
    empty_factory.register("line", Line)
    empty_factory.register("vertex", Vertex)
    return empty_factory

@pytest.fixture
def triangle_test_data():
    """Provides standard test data for triangle creation."""
    return {
        'id': 1,
        'oil_amount': 1.0,
        'area': 0.5,
        'normal_vectors': [((0, 1), np.array([1.0, 0.0]))],
        'faces': [((0, 1), np.array([1.0, 0.0]))],
        'velocity_field': np.array([1.0, 0.0]),
        'neighbors': [],
        'delta_t': 0.01
    }

class TestCellFactoryRegistration:
    def test_single_registration(self, empty_factory):
        """Test registration of a single cell type."""
        empty_factory.register("triangle", Triangle)
        assert "triangle" in empty_factory._cellTypes
        assert empty_factory._cellTypes["triangle"] == Triangle

    def test_multiple_registrations(self, full_factory):
        """Test registration of multiple cell types."""
        expected_types = {
            "triangle": Triangle,
            "line": Line,
            "vertex": Vertex
        }
        
        for cell_type, class_type in expected_types.items():
            assert cell_type in full_factory._cellTypes
            assert full_factory._cellTypes[cell_type] == class_type

    def test_duplicate_registration(self, factory_with_triangle):
        """Test that duplicate registration doesn't override original."""
        original_class = factory_with_triangle._cellTypes["triangle"]
        factory_with_triangle.register("triangle", Line)
        assert factory_with_triangle._cellTypes["triangle"] == original_class

class TestCellFactoryCreation:
    def test_triangle_creation(self, factory_with_triangle, triangle_test_data):
        """Test creation of a triangle cell with valid parameters."""
        triangle = factory_with_triangle("triangle", **triangle_test_data)
        
        assert isinstance(triangle, Triangle)
        assert triangle.id == triangle_test_data['id']
        assert triangle.oil_amount == triangle_test_data['oil_amount']
        assert np.array_equal(triangle.velocity_field, triangle_test_data['velocity_field'])

    def test_invalid_type_creation(self, factory_with_triangle):
        """Test that creating with invalid type raises KeyError."""
        with pytest.raises(KeyError) as exc_info:
            factory_with_triangle("invalid_type", 1)
        assert "invalid_type" in str(exc_info.value)

    @pytest.mark.parametrize("missing_param", [
        "id",
        "oil_amount",
        "area",
        "velocity_field"
    ])
    def test_missing_required_params(self, factory_with_triangle, triangle_test_data, missing_param):
        """Test creation with missing required parameters."""
        invalid_data = triangle_test_data.copy()
        del invalid_data[missing_param]
        
        with pytest.raises(TypeError):
            factory_with_triangle("triangle", **invalid_data)

class TestCellFactoryEdgeCases:
    def test_empty_factory_creation(self, empty_factory):
        """Test attempting to create from empty factory."""
        with pytest.raises(KeyError):
            empty_factory("triangle", 1)

    @pytest.mark.parametrize("invalid_type", [
        None,
        123,
        "",
        "  ",
        "TRIANGLE",  # Case sensitive check
    ])
    def test_invalid_type_variants(self, factory_with_triangle, invalid_type):
        """Test various invalid type inputs."""
        with pytest.raises(KeyError):
            factory_with_triangle(invalid_type, 1)

    def test_registration_with_invalid_class(self, empty_factory):
        """Test registration with invalid class types."""
        invalid_classes = [None, "NotAClass", 123, lambda x: x]
        
        for invalid_class in invalid_classes:
            empty_factory.register("test", invalid_class)
            assert "test" in empty_factory._cellTypes
            assert empty_factory._cellTypes["test"] == invalid_class