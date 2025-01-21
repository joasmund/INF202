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
    parser.add_argument('-f', '--folder', default=None,  # Changed default to None
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
    """Create and return the output directory path for a given configuration."""
    # Extract base name of the config file without extension
    base_name = os.path.splitext(os.path.basename(config_file))[0]
    
    # Create main results directory
    results_dir = os.path.join(os.getcwd(), "results", base_name)
    plots_dir = os.path.join(results_dir, "plots")
    
    # Create directories if they don't exist
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
    """Run the oil distribution simulation with the specified configuration."""
    # Load configuration
    config = toml.load(config_path)
    mshName = config["geometry"]["meshName"]
    
    # Simulation parameters
    nSteps = config["settings"]["nSteps"]  # Number of steps
    tStart = config["settings"]["tStart"]  # Start time
    tEnd = config["settings"]["tEnd"]   # End time
    writeFrequency = config["IO"]["writeFrequency"]  # Write frequency
    
    start_time = time.time()
    
    # Create the mesh and compute neighbors
    mesh = meshio.read(mshName)
    mesh = Mesh(mesh)
    final_cell_data, cell_type_mapping = mesh.main_function()
    
    # Initialize data structures
    triangles = []
    in_oil_amount = []
    points = mesh._mesh.points
    triangle_cell_indices = []
    
    # Process mesh data
    for cell_type, cell_data in mesh._mesh.cells_dict.items():
        for local_index, cell in enumerate(cell_data):
            if len(cell) == 3:  # Only consider triangles
                triangles.append(cell)
                triangle_cell_indices.append(cell_type_mapping[(cell_type, local_index)])
                in_oil_amount.append(final_cell_data[cell_type_mapping[(cell_type, local_index)]]['oil_amount'])
    
    # Convert to numpy arrays
    triangles = np.array(triangles)
    points = np.array(points)
    in_oil_amount = np.array(in_oil_amount)
    
    # Calculate time step
    delta_t = (tEnd - tStart) / nSteps
    
    # Run simulation steps
    for step in range(nSteps):
        current_time = tStart + step * delta_t
        updated_oil_amounts = []
        
        # Update oil amounts
        for cell in mesh._cells:
            if isinstance(cell, Triangle):
                cell.oil_amount = cell.update_oil_amount()
        
        # Collect updated amounts
        for cell_index in triangle_cell_indices:
            updated_oil_amounts.append(mesh._cells[cell_index - 1].oil_amount)
        
        updated_oil_amounts = np.array(updated_oil_amounts)
        
        # Generate plots at intervals
        if step % writeFrequency == 0:
        #for step in range(0, nSteps, writeFrequency):
            print(f"Config: {config_path}, Step {step}, Time: {current_time}")
            
            # Create visualization
            triangulation = Triangulation(points[:, 0], points[:, 1], triangles)
            plt.figure(figsize=(8, 6))
            plt.tripcolor(triangulation, facecolors=updated_oil_amounts, 
                         cmap="viridis", shading="flat")
            plt.colorbar(label="Oil Amount")
            plt.title(f"Oil Distribution at Step {step}")
            plt.xlabel("X")
            plt.ylabel("Y")
            
            # Save plot in configuration-specific directory
            plot_filename = os.path.join(output_dir, "plots", f"step_{step:04d}.png")
            plt.savefig(plot_filename)
            plt.close()
    
    end_time = time.time()
    print(f"Simulation complete for {config_path}")
    print(f"Execution time: {end_time - start_time} seconds")
    
    # Save final simulation data
    simulation_data = {
        'config_file': config_path,
        'execution_time': end_time - start_time,
        'final_oil_amounts': updated_oil_amounts.tolist(),
        'mesh_name': mshName,
        'simulation_parameters': {
            'nSteps': nSteps,
            'tStart': tStart,
            'tEnd': tEnd,
            'delta_t': delta_t
        }
    }
    
    # Save simulation results
    results_file = os.path.join(output_dir, "simulation_results.toml")
    with open(results_file, 'w') as f:
        toml.dump(simulation_data, f)

    # Create  video file
    plots_dir = os.path.join(output_dir, "plots")
    print("Creating video file... ")
    create_simulation_video(plots_dir, output_dir)

def main():
    """
    Main function to handle configuration and run simulations with improved argument handling.
    Provides clear feedback about which files will be processed and why.
    """
    # Parse command line arguments
    args = parse_arguments()
    
    # Convert folder path to absolute path for clarity in messages
    search_dir = get_search_directory(args)
    
    # Determine which configuration files to process based on argument hierarchy
    if args.config_file != 'input.toml':  # User explicitly specified a config file
        config_files = [args.config_file]
        print(f"\nProcessing specific configuration file: {args.config_file}")
    elif args.find_all or args.folder != './':
        config_files = find_toml_files(search_dir)
        if args.find_all:
            print(f"\nSearching for all TOML files in current directory")
        else:
            print(f"\nSearching for all TOML files in: {search_dir}")
    else:
        config_files = ['input.toml']
        print("\nUsing default configuration file: input.toml")
    
    # Provide feedback about found configuration files
    if not config_files:
        print("No configuration files found!")
        return
    
    print(f"Found {len(config_files)} configuration file(s):")
    for cfg in config_files:
        print(f"  - {cfg}")
    
    # Process each configuration file
    for config_file in config_files:
        config_path = os.path.join(search_dir, config_file)
        if not os.path.exists(config_path):
            print(f"\nConfiguration file not found: {config_path}")
            continue
            
        # Setup output directory for this configuration
        results_dir, plots_dir = setup_output_directory(config_file)
        print(f"\nProcessing configuration: {config_file}")
        print(f"Results will be saved to: {results_dir}")
        
        # Run simulation with this configuration
        try:
            run_simulation(config_path, results_dir)
        except Exception as e:
            print(f"Error processing {config_file}: {str(e)}")
            print("Continuing with next configuration file...")

if __name__ == "__main__":
    main()