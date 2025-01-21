import os
from src.Functions.simulator import run_simulation
from src.Functions.parser import parse_arguments
from src.Functions.directories import get_search_directory, setup_output_directory
from src.Functions.finder import find_toml_files



def main():
    """Main function with organized logging support."""
    args = parse_arguments()
    search_dir = get_search_directory(args)
    
    # Determine which configuration files to process
    if args.config_file != 'input.toml':
        config_files = [args.config_file]
        print(f"Processing specific configuration file: {args.config_file}")
    elif args.find_all or args.folder != './':
        config_files = find_toml_files(search_dir)
        print(f"Found {len(config_files)} configuration files in {search_dir}")
    else:
        config_files = ['input.toml']
        print("Using default configuration file: input.toml")
    
    if not config_files:
        print("No configuration files found!")
        return
    
    # Process each configuration file
    for config_file in config_files:
        config_path = os.path.join(search_dir, config_file)
        if not os.path.exists(config_path):
            print(f"Configuration file not found: {config_path}")
            continue
        
        try:
            # Setup output directory for this configuration
            results_dir, plots_dir = setup_output_directory(config_file)
            
            # Run simulation with this configuration
            run_simulation(config_path, results_dir)
            print(f"Simulation completed for {config_file}")
        except Exception as e:
            print(f"Error processing {config_file}: {str(e)}")
            print("Continuing with next configuration file...")

if __name__ == "__main__":
    main()