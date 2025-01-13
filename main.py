import time

import toml

from src.Simulation.mesh import Mesh

if __name__ == "__main__":

    # Load configuration from toml file
    config = toml.load("config.toml")

    mshName = config["geometry"]["meshName"]
    # x_star = config["geometry"]["x_star"]

    startTime = time.time()

    m = Mesh(mshName)
    m.computeNeighbors()

    for cell in m.cells:
        print(cell)

    endTime = time.time()
    print(f"Execution time: {endTime - startTime} seconds")
