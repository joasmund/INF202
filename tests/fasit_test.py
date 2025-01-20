import os
import pytest
import toml
from unittest.mock import patch, MagicMock
import argparse
from fasit import parseInput, directory_search, file_search, get_search_directory, create_subfolder_from_file

def test_directory_search(tmp_path):
    # Create temporary directories for testing
    dir1 = tmp_path / "dir1"
    dir2 = tmp_path / "dir2"
    dir1.mkdir()
    dir2.mkdir()

    # Test the function
    result = directory_search(tmp_path)
    assert "dir1" in result
    assert "dir2" in result
    assert len(result) == 2

def test_file_search(tmp_path):
    # Create temporary files for testing
    file1 = tmp_path / "file1.toml"
    file2 = tmp_path / "file2.txt"
    file1.touch()
    file2.touch()

    # Test the function
    result = file_search(tmp_path)
    assert "file1.toml" in result
    assert "file2.txt" in result
    assert len(result) == 2

def test_get_search_directory_with_folder():
    args = MagicMock()
    args.folder = "test_folder"

    result = get_search_directory(args)
    assert result == "test_folder"

def test_get_search_directory_default():
    args = MagicMock()
    args.folder = None

    result = get_search_directory(args)
    assert result == "./"

def test_create_subfolder_from_file(tmp_path):
    # Create a dummy file
    file_path = tmp_path / "test_file.toml"
    file_path.touch()

    # Test the function
    with patch("os.makedirs") as mock_makedirs:
        create_subfolder_from_file(file_path)
        subfolder_path = os.path.join(os.getcwd(), "results", "test_file")
        mock_makedirs.assert_called_once_with(subfolder_path, exist_ok=True)

def test_parseInput():
    #test_args = ["script.py", "-c", "custom_config.toml", "-f", "test_folder", "--find_all"]
    with patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(
        config_file="custom_config.toml",
        folder="test_folder",
        find_all=True
    )):
        args = parseInput()
        assert args.config_file == "custom_config.toml"
        assert args.folder == "test_folder"
        assert args.find_all is True

@pytest.fixture
def sample_toml(tmp_path):
    file_path = tmp_path / "config.toml"
    with open(file_path, "w") as f:
        toml.dump({"key": "value"}, f)
    return file_path

def test_main_with_find_all(sample_toml, tmp_path):
    with patch("script.parseInput", return_value=argparse.Namespace(
        config_file="input.toml",
        folder=str(tmp_path),
        find_all=True
    )):
        with patch("script.file_search", return_value=[sample_toml.name]):
            with patch("script.create_subfolder_from_file") as mock_create_subfolder:
                data = toml.load(sample_toml)
                assert "key" in data

                create_subfolder_from_file(sample_toml)
                mock_create_subfolder.assert_called_once_with(sample_toml)
