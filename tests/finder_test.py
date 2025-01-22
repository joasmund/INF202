import pytest
import os
from src.Functions.finder import find_toml_files  # Replace with actual module

@pytest.fixture
def temp_dir_with_files(tmp_path):
    """Fixture to create a temporary directory with various test files."""
    # Create test files
    files = [
        "config1.toml",
        "config2.toml",
        "test.txt",
        "data.csv",
        "script.py",
        "config3.TOML",  # Different case, shouldn't be included
        ".toml",         # Hidden file
        "noextension",
        "partial.tom"
    ]
    
    for file in files:
        (tmp_path / file).touch()
    
    return tmp_path

@pytest.fixture
def nested_dir_structure(tmp_path):
    """Fixture to create a nested directory structure with TOML files."""
    # Create main structure
    (tmp_path / "subdir1").mkdir()
    (tmp_path / "subdir2").mkdir()
    
    # Create files in root
    (tmp_path / "root.toml").touch()
    
    # Create files in subdir1
    (tmp_path / "subdir1" / "config1.toml").touch()
    (tmp_path / "subdir1" / "data.txt").touch()
    
    # Create files in subdir2
    (tmp_path / "subdir2" / "config2.toml").touch()
    
    return tmp_path


def test_empty_directory(tmp_path):
    """Test behavior with an empty directory."""
    files = find_toml_files(tmp_path)
    assert files == []

def test_no_toml_files(tmp_path):
    """Test directory with no TOML files."""
    # Create some non-TOML files
    (tmp_path / "test.txt").touch()
    (tmp_path / "data.csv").touch()
    
    files = find_toml_files(tmp_path)
    assert files == []

def test_single_toml_file(tmp_path):
    """Test directory with a single TOML file."""
    (tmp_path / "config.toml").touch()
    files = find_toml_files(tmp_path)
    assert files == ["config.toml"]

def test_nonexistent_directory():
    """Test behavior with a nonexistent directory."""
    files = find_toml_files("/nonexistent/directory")
    assert files == []

def test_non_file_entries(tmp_path):
    """Test handling of non-file entries."""
    # Create a subdirectory with .toml extension
    (tmp_path / "fake.toml").mkdir()
    files = find_toml_files(tmp_path)
    assert files == []

def test_special_characters(tmp_path):
    """Test handling of filenames with special characters."""
    special_files = [
        "test-config.toml",
        "test_config.toml",
        "test.config.toml",
        "test@config.toml",
        "test spaces.toml"
    ]
    
    for file in special_files:
        (tmp_path / file).touch()
    
    files = find_toml_files(tmp_path)
    assert len(files) == len(special_files)
    assert sorted(files) == sorted(special_files)

def test_symlinks(tmp_path):
    """Test handling of symlinked files."""
    # Create a real TOML file
    real_file = tmp_path / "real.toml"
    real_file.touch()
    
    # Create a symlink to it
    symlink = tmp_path / "link.toml"
    symlink.symlink_to(real_file)
    
    files = find_toml_files(tmp_path)
    assert len(files) == 2
    assert sorted(files) == ["link.toml", "real.toml"]

@pytest.mark.parametrize("filename", [
    "normal.toml",
    "UPPERCASE.toml",
    "mixed.TOML",  # Should not be included due to case sensitivity
    ".hidden.toml",
    "no-extension",
    "partial.tom",
    "spaces in name.toml",
    "special-chars@#$.toml"
])
def test_various_filenames(tmp_path, filename):
    """Test various filename patterns."""
    (tmp_path / filename).touch()
    files = find_toml_files(tmp_path)
    expected = [filename] if filename.endswith('.toml') else []
    assert files == expected

def test_permission_handling(tmp_path):
    """Test handling of permission errors."""
    # Create a test file
    (tmp_path / "test.toml").touch()
    
    # Remove read permissions if not on Windows
    if os.name != 'nt':
        os.chmod(tmp_path, 0o000)
        files = find_toml_files(tmp_path)
        assert files == []
        # Restore permissions for cleanup
        os.chmod(tmp_path, 0o755)
    else:
        pytest.skip("Permission test skipped on Windows")