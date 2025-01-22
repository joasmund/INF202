import os
import time
import toml
import meshio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
from src.Simulation.mesh import Mesh
from src.Simulation.cells import Triangle
from src.Functions.videomaker import create_simulation_video
from src.Functions.loader import load_config_with_defaults
from src.Functions.logger import setup_logger
from src.Functions.formatter import format_simulation_results


def run_simulation(config_path, output_dir):
    """Run the oil distribution simulation with the specified configuration and logging."""
    try:
        # Load configuration first to get the log name
        with open(config_path, 'r') as f:
            raw_config = toml.load(f)
        log_name = raw_config.get("IO", {}).get("logName", "simulation")
        
        # Create single logger instance that will be used throughout
        logger = setup_logger(output_dir, log_name)
        logger.info(f"Starting simulation with config: {config_path}")
        
        # Load complete configuration with defaults using the established logger
        config = load_config_with_defaults(config_path, logger)
        
        # Continue with the rest of the simulation using the same logger
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
                        cell_id = cell_type_mapping[(cell_type, local_index)]
                        triangle_cell_indices.append(cell_id)
                        in_oil_amount.append(final_cell_data[cell_id]['oil_amount'])
            
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
        for step in range(nSteps + 1):
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
        
        # When saving final simulation data, format it as text instead of TOML
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
            
            # Format and save results as text file with cell indices
            formatted_results = format_simulation_results(simulation_data, triangle_cell_indices)
            results_file = os.path.join(output_dir, "simulation_results.txt")
            
            with open(results_file, 'w') as f:
                f.write(formatted_results)
            
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
        
    except Exception as e:
        logger.error(f"Fatal error in simulation: {str(e)}")
        raise