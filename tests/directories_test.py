import pytest
import os
from types import SimpleNamespace
from src.Functions.directories import get_search_directory, setup_output_directory  # Replace with actual module

@pytest.fixture
def mock_args():
    """Fixture to create mock command line arguments."""
    def _create_args(folder='./'): 
        return SimpleNamespace(folder=folder)
    return _create_args

@pytest.fixture
def temp_working_dir(tmp_path):
    """Fixture to create and change to a temporary working directory."""
    original_dir = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(original_dir)

class TestGetSearchDirectory:
    def test_default_directory(self, mock_args):
        """Test with default directory (./)"""
        args = mock_args()
        result = get_search_directory(args)
        assert os.path.isabs(result)
        assert result == os.path.abspath('./')

    def test_specific_directory(self, mock_args):
        """Test with a specific directory path"""
        test_path = 'test_configs'
        args = mock_args(test_path)
        result = get_search_directory(args)
        assert os.path.isabs(result)
        assert result == os.path.abspath(test_path)

    def test_nested_directory(self, mock_args):
        """Test with a nested directory path"""
        test_path = 'configs/nested/folder'
        args = mock_args(test_path)
        result = get_search_directory(args)
        assert os.path.isabs(result)
        assert result == os.path.abspath(test_path)

    def test_parent_directory(self, mock_args):
        """Test with parent directory path"""
        test_path = '../parent'
        args = mock_args(test_path)
        result = get_search_directory(args)
        assert os.path.isabs(result)
        assert result == os.path.abspath(test_path)

    @pytest.mark.parametrize("test_path", [
        './',
        'test_dir',
        'deeply/nested/config/folder',
        '../parent_dir',
        './relative/path'
    ])
    def test_various_paths(self, mock_args, test_path):
        """Test with various path formats"""
        args = mock_args(test_path)
        result = get_search_directory(args)
        assert os.path.isabs(result)
        assert result == os.path.abspath(test_path)

class TestSetupOutputDirectory:
    def test_basic_setup(self, temp_working_dir):
        """Test basic directory setup with simple config file"""
        config_file = 'test_config.toml'
        results_dir, plots_dir = setup_output_directory(config_file)
        
        # Check paths are correct
        expected_results = os.path.join(temp_working_dir, 'results', 'test_config')
        expected_plots = os.path.join(expected_results, 'plots')
        assert results_dir == expected_results
        assert plots_dir == expected_plots
        
        # Check directories were created
        assert os.path.exists(results_dir)
        assert os.path.exists(plots_dir)
        assert os.path.isdir(results_dir)
        assert os.path.isdir(plots_dir)

    def test_nested_config_path(self, temp_working_dir):
        """Test with config file in nested directory"""
        config_file = 'nested/folder/config.toml'
        results_dir, plots_dir = setup_output_directory(config_file)
        
        expected_results = os.path.join(temp_working_dir, 'results', 'config')
        expected_plots = os.path.join(expected_results, 'plots')
        assert results_dir == expected_results
        assert plots_dir == expected_plots
        assert os.path.exists(results_dir)
        assert os.path.exists(plots_dir)

    def test_existing_directories(self, temp_working_dir):
        """Test handling of existing directories"""
        config_file = 'test_config.toml'
        
        # Create directories first
        os.makedirs(os.path.join(temp_working_dir, 'results', 'test_config', 'plots'), exist_ok=True)
        
        # Should not raise an error
        results_dir, plots_dir = setup_output_directory(config_file)
        assert os.path.exists(results_dir)
        assert os.path.exists(plots_dir)

    def test_special_characters(self, temp_working_dir):
        """Test with config file name containing special characters"""
        config_file = 'test-config_123.toml'
        results_dir, plots_dir = setup_output_directory(config_file)
        
        expected_results = os.path.join(temp_working_dir, 'results', 'test-config_123')
        expected_plots = os.path.join(expected_results, 'plots')
        assert results_dir == expected_results
        assert plots_dir == expected_plots
        assert os.path.exists(results_dir)
        assert os.path.exists(plots_dir)

    @pytest.mark.parametrize("config_file,expected_base", [
        ('simple.toml', 'simple'),
        ('path/to/config.toml', 'config'),
        ('test-123_config.toml', 'test-123_config'),
        ('./relative/path/conf.toml', 'conf'),
        ('../parent/conf.toml', 'conf')
    ])
    def test_various_config_paths(self, temp_working_dir, config_file, expected_base):
        """Test with various config file paths"""
        results_dir, plots_dir = setup_output_directory(config_file)
        
        expected_results = os.path.join(temp_working_dir, 'results', expected_base)
        expected_plots = os.path.join(expected_results, 'plots')
        assert results_dir == expected_results
        assert plots_dir == expected_plots
        assert os.path.exists(results_dir)
        assert os.path.exists(plots_dir)