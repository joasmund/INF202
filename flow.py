import meshio
import numpy as np
import toml


up = 0

starttime = toml.load("config.toml")["simulation"]["tStart"]
endtime = toml.load("config.toml")["simulation"]["tEnd"]
steps = toml.load("config.toml")["simulation"]["nSteps"]

# Load configuration from toml file
config = toml.load("config.toml")

# Get the star position from the configuration
x_star = config["geometry"]["xStar"]
meshName = config["geometry"]["meshName"]


data = meshio.read(meshName)
points = data.points
cells = data.cells


# Load configuration from toml file
config = toml.load("config.toml")

#Scaled outer normal in cell i at the interface to cell ngh
my = 0


#Average of velocity in cell i and cell ngh
v = 0

#Flux
up = up - (toml.)


for cell in cells:
    cell_neighbors = cell.neighbors
    for ngh in cell_neighbors:
        up += ngh
        pass


dot_product = np.dot(my, v)


def flux_function():
    if dot_product > 0: #Positive projection on each other. The oil is partly flowing in the direction of the normal vecto
        return u(i) * np.dot(my, v)
    else:
        return u(ngh) * np.dot(my, v)