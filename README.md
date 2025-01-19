# INF202 - Simulating an Oil Spill

This repository contains the code and resources for the INF202 project of 2025, which focuses on simulating the flow of oil spills using Python. The project includes various scripts for configuration parsing, simulation, and visualization.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Simulation](#simulation)
- [Visualization](#visualization)
- [Contributing](#contributing)
- [License](#license)

## Installation

To get started, clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/INF202.git
cd INF202
pip install -r requirements.txt
```

## Usage

### Running the Simulation

1. **Configuration**: Ensure you have a valid TOML configuration file. You can use the provided 

input.toml

 as a template.
2. **Execute**: Run the main simulation script:

```bash
python main2.py -f path/to/your/config.toml
```

### Visualizing Results

The project includes scripts for visualizing the simulation results. For example, you can use 

test_plot.py

 to plot the oil distribution in a triangular mesh.

```bash
python test_plot.py
```

## Project Structure

```
INF202/
├── src2/
│   ├── Simulation/
│   │   ├── cells2.py
│   │   ├── functions2.py
│   │   ├── mesh2.py
│   └── main2.py
├── random_functions/
│   ├── parser.py
│   ├── toml_read.py
├── inputs/
│   ├── input.toml
│   ├── solution.txt
├── tests/
│   ├── test_plot.py
├── scanner.py
├── requirements.txt
├── README.md
└── Report/
    ├── main.tex
```

## Configuration

The configuration for the simulation is done through TOML files. Below is an example configuration (`input.toml`):

```toml
[settings]
nSteps = 500 # Number of steps
tStart = 0.1 # Start time
tEnd = 0.2   # End time

[geometry]
meshName = "bay.msh"
meshName2 = "simple.msh"
borders = [[0.0, 0.45], [0.0, 0.2]] # Defines where fish are located
xStar = [0.35, 0.45]

[IO]
logName = "log"                    # Name of the log file created
writeFrequency = 10                # Frequency of output video. If not provided, no video is recorded
restartFile = "input/solution.txt" # Restart file must be provided if start time is provided.
```

## Simulation

The main simulation logic is implemented in 

main2.py

, which reads the configuration, sets up the mesh, and runs the simulation.

## Visualization

Visualization scripts like 

test_plot.py

 use `matplotlib` to plot the results of the simulation. For example, `plot_triangles_with_oil` function in 

test_plot.py

 visualizes the oil distribution in a triangular mesh.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
```