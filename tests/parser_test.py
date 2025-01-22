import pytest
from src.Functions.parser import parse_arguments  # Replace 'your_module' with actual module name

@pytest.fixture
def mock_sys_argv(monkeypatch):
    """Fixture to simulate command line arguments."""
    def _mock_argv(args):
        monkeypatch.setattr('sys.argv', ['script.py'] + args)
    return _mock_argv

def test_default_arguments(mock_sys_argv):
    """Test parser with no arguments provided."""
    mock_sys_argv([])
    args = parse_arguments()
    assert args.config_file == 'input.toml'
    assert args.folder == './'
    assert not args.find_all
    assert not args.folder_provided

def test_specific_config_file(mock_sys_argv):
    """Test parser with specific config file argument."""
    mock_sys_argv(['--config_file', 'custom.toml'])
    args = parse_arguments()
    assert args.config_file == 'custom.toml'
    assert args.folder == './'
    assert not args.find_all
    assert not args.folder_provided

def test_folder_argument(mock_sys_argv):
    """Test parser with folder argument."""
    mock_sys_argv(['--folder', 'test_folder'])
    args = parse_arguments()
    assert args.folder == 'test_folder'
    assert args.config_file == 'input.toml'
    assert not args.find_all
    assert args.folder_provided

def test_find_all_flag(mock_sys_argv):
    """Test parser with find_all flag."""
    mock_sys_argv(['--find_all'])
    args = parse_arguments()
    assert args.find_all
    assert args.folder == './'
    assert args.config_file == 'input.toml'
    assert not args.folder_provided

def test_folder_current_directory(mock_sys_argv):
    """Test parser with current directory as folder."""
    mock_sys_argv(['--folder', './'])
    args = parse_arguments()
    assert args.folder == './'
    assert args.config_file == 'input.toml'
    assert not args.find_all
    assert args.folder_provided

def test_combined_arguments(mock_sys_argv):
    """Test parser with multiple arguments (folder and config file)."""
    mock_sys_argv(['--folder', 'configs', '--config_file', 'special.toml'])
    args = parse_arguments()
    assert args.folder == 'configs'
    assert args.config_file == 'special.toml'
    assert not args.find_all
    assert args.folder_provided

def test_combined_with_find_all(mock_sys_argv):
    """Test parser with folder, config file, and find_all flag."""
    mock_sys_argv(['--folder', 'configs', '--config_file', 'special.toml', '--find_all'])
    args = parse_arguments()
    assert args.folder == 'configs'
    assert args.config_file == 'special.toml'
    assert args.find_all
    assert args.folder_provided

def test_short_arguments(mock_sys_argv):
    """Test parser with short form arguments."""
    mock_sys_argv(['-f', 'configs', '-c', 'special.toml'])
    args = parse_arguments()
    assert args.folder == 'configs'
    assert args.config_file == 'special.toml'
    assert not args.find_all
    assert args.folder_provided

def test_various_folder_paths(mock_sys_argv, folder_path, expected):
    """Test parser with various folder path formats."""
    mock_sys_argv(['--folder', folder_path])
    args = parse_arguments()
    assert args.folder == expected
    assert args.folder_provided

