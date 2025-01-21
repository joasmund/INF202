import os


def get_search_directory(args):
    """
    Determine the directory to search for configuration files.
    Returns the specified folder path or the current directory as default.
    """
    return os.path.abspath(args.folder)  # Convert to absolute path for clarity

def setup_output_directory(config_file):
    """
    Create and return the output directory paths for a given configuration.
    Now includes a structured directory for all simulation outputs.
    """
    # Extract base name of the config file without extension
    base_name = os.path.splitext(os.path.basename(config_file))[0]
    
    # Create main results directory
    results_dir = os.path.join(os.getcwd(), "results", base_name)
    plots_dir = os.path.join(results_dir, "plots")
    
    # Create all necessary directories
    os.makedirs(plots_dir, exist_ok=True)
    
    return results_dir, plots_dir