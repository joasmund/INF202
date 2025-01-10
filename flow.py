import meshio
import numpy as np
import tomlkit as toml
import math
from structure_start import Cell, Triangle, Mesh #Fikses etter at struktur er fikset


with open ("config.toml" , "r") as f:
    data = toml.load(f)
print(data)



up = 0
u_i = 1              #Solution of triangle i at the time t(n) 
u_ngh = 1             #Solution of neighbor triangle ngh at the time t(n)





#extract parameters from the config file
starttime = data["settings"]["tStart"]
print(starttime)
endtime = data["settings"]["tEnd"]
print(endtime)
steps = data["settings"]["nSteps"]
print(steps)

# Get the start position from the configuration
startposition = data["geometry"]["xStar"]
print(startposition)
meshName = data["geometry"]["meshName"]
print(meshName)

#turn the floats into integers #Dette blir feil
starttime = int(starttime)
endtime = int(endtime)
steps = int(steps)


for mesh in range (starttime, endtime, steps): #Kjører fra starttid til sluttid med steglengde steps #

    for cell in mesh:
        cell_neighbors = cell.neighbors
        for ngh in cell_neighbors:
            up += ngh
            pass
            
print("up: ", up)



#Finner gjennomsnittet av hastigheten i cellen og nabocellen
v_i = 1
v_k = 1 

k = 0.5 * (v_i + v_k)



print("Startposition: ", startposition)

data = meshio.read(meshName)
points = data.points
cells = data.cells

area = Triangle(cell)

cell_neighbors = x
#Scaled outer normal in cell i at the interface to cell ngh
my = 0


#Average of velocity in cell i and cell ngh
v = 0


def flux_function(u_i, u_ngh, my, v):
    if dot_product > 0: #Positive projection on each other. The oil is partly flowing in the direction of the normal vecto
        return u_i * np.dot(my, v)
    else:
        return u_ngh * np.dot(my, v)
    

#Flux
up = up - ((endtime - starttime)/(area * flux_function() )) #IKKe riktig syntaks, men tanken er der


for cell in cells:
    cell_neighbors = cell.neighbors
    for ngh in cell_neighbors:
        up += ngh
        pass


dot_product = np.dot(my, v)



for mesh in range (starttime, endtime, steps): #Kjører fra starttid til sluttid med steglengde steps #

    for cell in mesh:
        cell_neighbors = cell.neighbors
        for ngh in cell_neighbors:
            up += ngh
            pass