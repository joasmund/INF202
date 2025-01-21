import os


def find_toml_files(directory):
    """
    Search for TOML configuration files in the specified directory.
    Returns a sorted list of TOML files to ensure consistent processing order.
    """
    try:
        with os.scandir(directory) as entries:
            toml_files = [entry.name for entry in entries 
                         if entry.is_file() and entry.name.endswith('.toml')]
            return sorted(toml_files)  # Sort files for consistent ordering
    except OSError as e:
        print(f"Error accessing directory {directory}: {e}")
        return []