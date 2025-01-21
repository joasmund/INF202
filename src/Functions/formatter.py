import numpy as np
from datetime import datetime


def format_simulation_results(simulation_data, cell_indices):
    """
    Format simulation results into a human-readable text format, including cell IDs.
    
    Args:
        simulation_data (dict): Dictionary containing simulation results
        cell_indices (list): List of cell indices corresponding to the oil amounts
        
    Returns:
        str: Formatted text content with cell-specific information
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = [
        "SIMULATION RESULTS REPORT",
        "=" * 50,
        f"Generated: {timestamp}\n",
        
        "CONFIGURATION INFORMATION",
        "-" * 30,
        f"Configuration File: {simulation_data['config_file']}",
        f"Mesh File: {simulation_data['mesh_name']}\n",
        
        "SIMULATION PARAMETERS",
        "-" * 30,
        f"Number of Steps: {simulation_data['simulation_parameters']['nSteps']}",
        f"Start Time: {simulation_data['simulation_parameters']['tStart']}",
        f"End Time: {simulation_data['simulation_parameters']['tEnd']}",
        f"Time Step Size: {simulation_data['simulation_parameters']['delta_t']:.6f}\n",
        
        "PERFORMANCE METRICS",
        "-" * 30,
        f"Total Execution Time: {simulation_data['execution_time']:.2f} seconds\n",
        
        "OIL DISTRIBUTION RESULTS",
        "-" * 30,
        "Final Oil Amounts by Cell:",
        "Cell ID    Oil Amount"  # Header for the data columns
    ]
    
    # Add oil amount data with cell IDs, using proper alignment
    for cell_id, amount in zip(cell_indices, simulation_data['final_oil_amounts']):
        content.append(f"{cell_id:8d}    {amount:8.3f}")
    
    # Calculate and add statistics about oil distribution
    oil_amounts = np.array(simulation_data['final_oil_amounts'])
    content.extend([
        "",  # Empty line for separation
        "OIL DISTRIBUTION STATISTICS",
        "-" * 30,
        f"Maximum Oil Amount: {np.max(oil_amounts):.3f} (Cell {cell_indices[np.argmax(oil_amounts)]})",
        f"Minimum Oil Amount: {np.min(oil_amounts):.3f} (Cell {cell_indices[np.argmin(oil_amounts)]})",
        f"Average Oil Amount: {np.mean(oil_amounts):.3f}",
        f"Standard Deviation: {np.std(oil_amounts):.3f}",
        f"Total Number of Cells: {len(cell_indices)}"
    ])
    
    return "\n".join(content)