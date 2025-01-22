import pytest
import os
import logging
from src.Functions.logger import setup_logger  # Replace with actual module

@pytest.fixture
def temp_output_dir(tmp_path):
    """Fixture to provide a temporary output directory."""
    output_dir = tmp_path / "simulation_results"
    output_dir.mkdir()
    return str(output_dir)

@pytest.fixture
def cleanup_loggers():
    """Fixture to clean up logger configurations after each test."""
    yield
    # Clean up any loggers created during the test
    root_logger = logging.getLogger()
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        if logger.name.startswith("SimulationLogger"):
            logger.handlers.clear()
    root_logger.handlers.clear()

def test_basic_logger_setup(temp_output_dir, cleanup_loggers):
    """Test basic logger creation and configuration."""
    logname = "test_simulation"
    logger = setup_logger(temp_output_dir, logname)
    
    # Check logger name
    expected_name = f"SimulationLogger_{os.path.basename(temp_output_dir)}_{logname}"
    assert logger.name == expected_name
    
    # Check log level
    assert logger.level == logging.INFO
    
    # Check handlers
    assert len(logger.handlers) == 2
    assert isinstance(logger.handlers[0], logging.FileHandler)
    assert isinstance(logger.handlers[1], logging.NullHandler)
    
    # Check log file creation
    log_file = os.path.join(temp_output_dir, f"{logname}.log")
    assert os.path.exists(log_file)

def test_logger_file_handler_configuration(temp_output_dir, cleanup_loggers):
    """Test specific configuration of the file handler."""
    logger = setup_logger(temp_output_dir, "test_config")
    file_handler = next(h for h in logger.handlers if isinstance(h, logging.FileHandler))
    
    # Check formatter
    formatter = file_handler.formatter
    assert formatter._fmt == "%(asctime)s - %(levelname)s - %(message)s"
    
    # Check file handler mode (should be 'w' for write)
    assert file_handler.mode == 'w'

def test_logger_writing_capability(temp_output_dir, cleanup_loggers):
    """Test that logger can write to the log file."""
    logname = "write_test"
    logger = setup_logger(temp_output_dir, logname)
    
    test_message = "Test log message"
    logger.info(test_message)
    
    log_file = os.path.join(temp_output_dir, f"{logname}.log")
    with open(log_file, 'r') as f:
        content = f.read()
        assert test_message in content

def test_multiple_logger_instances(temp_output_dir, cleanup_loggers):
    """Test creation of multiple logger instances."""
    logger1 = setup_logger(temp_output_dir, "test1")
    logger2 = setup_logger(temp_output_dir, "test2")
    
    assert logger1.name != logger2.name
    assert os.path.exists(os.path.join(temp_output_dir, "test1.log"))
    assert os.path.exists(os.path.join(temp_output_dir, "test2.log"))

def test_logger_no_console_output(temp_output_dir, cleanup_loggers, capsys):
    """Test that logger doesn't write to console."""
    logger = setup_logger(temp_output_dir, "console_test")
    test_message = "This should not appear in console"
    logger.info(test_message)
    
    captured = capsys.readouterr()
    assert test_message not in captured.out
    assert test_message not in captured.err

def test_logger_propagation(temp_output_dir, cleanup_loggers):
    """Test that logger doesn't propagate messages to parent loggers."""
    logger = setup_logger(temp_output_dir, "propagation_test")
    assert not logger.propagate

def test_duplicate_logger_handling(temp_output_dir, cleanup_loggers):
    """Test handling of duplicate logger creation."""
    logname = "duplicate_test"
    logger1 = setup_logger(temp_output_dir, logname)
    logger2 = setup_logger(temp_output_dir, logname)
    
    # Should have same name but be different instances
    assert logger1.name == logger2.name
    assert len(logger2.handlers) == 2  # Should have cleared previous handlers

def test_special_characters_in_logname(temp_output_dir, cleanup_loggers):
    """Test logger creation with special characters in logname."""
    logname = "test-log_123"
    logger = setup_logger(temp_output_dir, logname)
    log_file = os.path.join(temp_output_dir, f"{logname}.log")
    assert os.path.exists(log_file)

@pytest.mark.parametrize("logname", [
    "simple",
    "test-123",
    "log_with_underscore",
    "Test.Log",
    "UPPERCASE_LOG"
])
def test_various_lognames(temp_output_dir, cleanup_loggers, logname):
    """Test logger creation with various logname formats."""
    logger = setup_logger(temp_output_dir, logname)
    log_file = os.path.join(temp_output_dir, f"{logname}.log")
    assert os.path.exists(log_file)
    
    test_message = f"Test message for {logname}"
    logger.info(test_message)
    
    with open(log_file, 'r') as f:
        content = f.read()
        assert test_message in content

def test_logger_levels(temp_output_dir, cleanup_loggers):
    """Test different logging levels."""
    logger = setup_logger(temp_output_dir, "level_test")
    log_file = os.path.join(temp_output_dir, "level_test.log")
    
    # Test all levels
    logger.debug("Debug message")  # Should not appear
    logger.info("Info message")    # Should appear
    logger.warning("Warning message")  # Should appear
    logger.error("Error message")      # Should appear
    
    with open(log_file, 'r') as f:
        content = f.read()
        assert "Debug message" not in content  # DEBUG is below INFO
        assert "Info message" in content
        assert "Warning message" in content
        assert "Error message" in content