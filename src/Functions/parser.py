import argparse


def parse_arguments():
    """
    Parse command line arguments for configuration handling with improved logic.
    
    The argument hierarchy is:
    1. Specific config file (-c): Highest priority, processes only this file
    2. Folder (-f) or find_all flag: Processes all TOML files in the specified location
    3. Default: Looks for input.toml in current directory
    """
    parser = argparse.ArgumentParser(description='Oil distribution simulation with multiple configuration support.')
    parser.add_argument('--find_all', action='store_true',
                       help='Search for and run all config files in the current directory')
    parser.add_argument('-f', '--folder', default=None,
                       help='Process all TOML files in the specified folder')
    parser.add_argument('-c', '--config_file', default='input.toml',
                       help='Process a specific config file')
    args = parser.parse_args()
    
    # If folder argument was provided, store the path, otherwise use default './'
    if args.folder is not None:
        args.folder_provided = True
        args.folder = args.folder if args.folder != './' else './'
    else:
        args.folder_provided = False
        args.folder = './'
    
    return args