import os
import logging

def setup_logger(output_dir, logname):
    """
    Set up the logger to write to a file in the output directory with the specified name.
    
    Args:
        output_dir (str): The directory where simulation results are stored
        logname (str): Name for the log file, from config[IO][logName]
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create the log file path within the output directory
    log_file = os.path.join(output_dir, f"{logname}.log")
    
    # Create a new logger instance with a unique name
    logger = logging.getLogger(f"SimulationLogger_{os.path.basename(output_dir)}_{logname}")
    logger.setLevel(logging.INFO)
    
    # Remove any existing handlers to prevent duplicate logging
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Create and configure file handler
    file_handler = logging.FileHandler(log_file, mode='w')
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Create a null handler for console output to suppress terminal printing
    null_handler = logging.NullHandler()
    logger.addHandler(null_handler)
    
    # Prevent propagation to prevent duplicate logging
    logger.propagate = False
    
    return logger