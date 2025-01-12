import time

import toml

from src.Simulation.mesh import Mesh

if __name__ == "__main__":

    # Load configuration from toml file
    config = toml.load("config.toml")

    mshName = config["geometry"]["meshName"]
    mshName2 = config["geometry"]["meshName2"]

    startTime = time.time()

    m = Mesh(mshName)
    # m.computeNeighbors()

    cells = []
    for i in range(10000):
        try:
            cells.append(m._cells[i])
        except:
            break

    for cell in cells:
        print(cell)

    endTime = time.time()
    print(f"Execution time: {endTime - startTime} seconds")
