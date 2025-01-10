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
    m.computeNeighbors()
    cell = m._cells[299]
    points = m._points
    pts = cell._pointIds
    print(points[pts])
    print(cell)

    endTime = time.time()

    print(f"Execution time: {endTime - startTime} seconds")
