import meshio
import numpy as np
from math import e

msh = meshio.read("bay.msh")

points = msh.points
cells = msh.cells

x = 0
delta_x = 0.1
t = 0.01

def oil_distribution():
    return e ** (-((abs(x-delta_x))**2 / t))

def flow_rate():
    return np.array[[y-0.2*x][-x]]



