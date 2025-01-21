import os
import time
import meshio
import toml
import argparse
import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.tri import Triangulation
from src.Simulation.cells import Triangle
from src.Simulation.mesh import Mesh
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

def create_simulation_video(plots_dir, output_dir):
    """
    Creates a video from the simulation plot images.
    
    Args:
        plots_dir: Directory containing the plot images
        output_dir: Directory where the video will be saved
    """
    # Get all PNG files in the plots directory and sort them numerically
    image_files = [f for f in os.listdir(plots_dir) if f.endswith('.png')]
    image_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
    
    if not image_files:
        print("No image files found for video creation")
        return
    
    # Get the full path of the first image
    first_image_path = os.path.join(plots_dir, image_files[0])
    
    # Read the first image to determine dimensions
    frame = cv2.imread(first_image_path)
    if frame is None:
        print(f"Error reading image: {first_image_path}")
        return
        
    height, width, layers = frame.shape
    
    # Create the output video file
    video_path = os.path.join(output_dir, "simulation.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # Using 10 frames per second for a smooth visualization
    video = cv2.VideoWriter(video_path, fourcc, 10, (width, height))
    
    # Write each image to the video
    try:
        for image_file in image_files:
            image_path = os.path.join(plots_dir, image_file)
            frame = cv2.imread(image_path)
            if frame is not None:
                video.write(frame)
            else:
                print(f"Error reading image: {image_path}")
    finally:
        # Ensure proper cleanup of resources
        video.release()
    
    print(f"Video created successfully: {video_path}")

def run_simulation(config_path, output_dir):
    """Run the oil distribution simulation with the specified configuration and logging."""
    # First, create a temporary logger to use while loading the configuration
    temp_logger = setup_logger(output_dir, "temp")
    
    # Load configuration with defaults using the temporary logger
    config = load_config_with_defaults(config_path, temp_logger)
    
    # Now create the proper logger with the name from the configuration
    logger = setup_logger(output_dir, config["IO"]["logName"])
    logger.info(f"Starting simulation with config: {config_path}")
    
    # Continue with the rest of the simulation using the proper logger
    try:
        mshName = config["geometry"]["meshName"]
        logger.info(f"Using mesh file: {mshName}")
    except Exception as e:
        logger.error(f"Configuration loading failed: {str(e)}")
        raise
    
    # Simulation parameters
    nSteps = config["settings"]["nSteps"]
    tStart = config["settings"]["tStart"]
    tEnd = config["settings"]["tEnd"]
    writeFrequency = config["IO"]["writeFrequency"]
    
    start_time = time.time()
    logger.info(f"Simulation parameters: nSteps={nSteps}, tStart={tStart}, tEnd={tEnd}")
    
    # Create the mesh and compute neighbors
    try:
        logger.info(f"Loading mesh from {mshName}")
        mesh = meshio.read(mshName)
        mesh = Mesh(mesh)
        final_cell_data, cell_type_mapping = mesh.main_function()
        logger.info("Mesh processing completed successfully")
    except Exception as e:
        logger.error(f"Mesh processing failed: {str(e)}")
        raise
    
    # Initialize data structures
    logger.info("Initializing simulation data structures")
    triangles = []
    in_oil_amount = []
    points = mesh._mesh.points
    triangle_cell_indices = []
    
    # Process mesh data
    try:
        for cell_type, cell_data in mesh._mesh.cells_dict.items():
            for local_index, cell in enumerate(cell_data):
                if len(cell) == 3:  # Only consider triangles
                    triangles.append(cell)
                    triangle_cell_indices.append(cell_type_mapping[(cell_type, local_index)])
                    in_oil_amount.append(final_cell_data[cell_type_mapping[(cell_type, local_index)]]['oil_amount'])
        
        logger.info(f"Processed {len(triangles)} triangular cells")
    except Exception as e:
        logger.error(f"Error processing mesh cells: {str(e)}")
        raise
    
    # Convert to numpy arrays
    triangles = np.array(triangles)
    points = np.array(points)
    in_oil_amount = np.array(in_oil_amount)
    
    # Calculate time step
    delta_t = (tEnd - tStart) / nSteps
    logger.info(f"Time step size: {delta_t}")
    
    # Run simulation steps
    logger.info("Starting simulation time steps")
    for step in range(nSteps):
        current_time = tStart + step * delta_t
        updated_oil_amounts = []
        
        try:
            # Update oil amounts
            for cell in mesh._cells:
                if isinstance(cell, Triangle):
                    cell.oil_amount = cell.update_oil_amount()
            
            # Collect updated amounts
            for cell_index in triangle_cell_indices:
                updated_oil_amounts.append(mesh._cells[cell_index - 1].oil_amount)
            
            updated_oil_amounts = np.array(updated_oil_amounts)
            
            if step % writeFrequency == 0:
                logger.info(f"Step {step}/{nSteps} completed (t={current_time:.3f})")
                
                # Create visualization
                try:
                    triangulation = Triangulation(points[:, 0], points[:, 1], triangles)
                    plt.figure(figsize=(8, 6))
                    plt.tripcolor(triangulation, facecolors=updated_oil_amounts, 
                                cmap="viridis", shading="flat")
                    plt.colorbar(label="Oil Amount")
                    plt.title(f"Oil Distribution at Step {step}")
                    plt.xlabel("X")
                    plt.ylabel("Y")
                    
                    # Save plot
                    plot_filename = os.path.join(output_dir, "plots", f"step_{step:04d}.png")
                    plt.savefig(plot_filename)
                    plt.close()
                    logger.info(f"Plot saved: {plot_filename}")
                except Exception as e:
                    logger.error(f"Error creating visualization at step {step}: {str(e)}")
                    
        except Exception as e:
            logger.error(f"Error during simulation step {step}: {str(e)}")
            raise
    
    end_time = time.time()
    execution_time = end_time - start_time
    logger.info(f"Simulation completed. Total execution time: {execution_time:.2f} seconds")
    
    # Save final simulation data
    try:
        simulation_data = {
            'config_file': config_path,
            'execution_time': execution_time,
            'final_oil_amounts': updated_oil_amounts.tolist(),
            'mesh_name': mshName,
            'simulation_parameters': {
                'nSteps': nSteps,
                'tStart': tStart,
                'tEnd': tEnd,
                'delta_t': delta_t
            }
        }
        
        results_file = os.path.join(output_dir, "simulation_results.toml")
        with open(results_file, 'w') as f:
            toml.dump(simulation_data, f)
        logger.info(f"Simulation results saved to: {results_file}")
    except Exception as e:
        logger.error(f"Error saving simulation results: {str(e)}")
        raise
    
    # Create video file
    try:
        plots_dir = os.path.join(output_dir, "plots")
        logger.info("Creating simulation video...")
        create_simulation_video(plots_dir, output_dir)
        logger.info("Video creation completed")
    except Exception as e:
        logger.error(f"Error creating simulation video: {str(e)}")
        raise

    return logger  # Return logger for potential use in main function

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