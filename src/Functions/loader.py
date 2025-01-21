import toml

def load_config_with_defaults(config_path, logger):
    """
    Load the TOML configuration file and set default values for missing parameters.
    
    Args:
        config_path (str): Path to the TOML configuration file
        logger (logging.Logger): Logger instance for recording events
        
    Returns:
        dict: Configuration dictionary with all required parameters
    """
    logger.info(f"Loading configuration from: {config_path}")
    
    try:
        config = toml.load(config_path)
        logger.info("Configuration file loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load configuration file: {str(e)}")
        raise
    
    # Ensure the settings section exists
    if "settings" not in config:
        logger.warning("No 'settings' section found in config, creating with defaults")
        config["settings"] = {}
    
    # Set default value for tStart if not provided
    if "tStart" not in config["settings"]:
        config["settings"]["tStart"] = 0
        logger.info("Using default tStart value: 0")
    
    # Ensure the IO section exists
    if "IO" not in config:
        logger.warning("No 'IO' section found in config, creating with defaults")
        config["IO"] = {}
    
    # Set default value for logName if not provided
    if "logName" not in config["IO"]:
        config["IO"]["logName"] = "logfile"
        logger.info("Using default logName value: 'logfile'")
    
    logger.info("Configuration loaded with all required parameters")
    return config