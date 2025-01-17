import meshio

mesh = meshio.read("bay.msh")

# Iterate over the items in the cells_dict
for key, value in mesh.cells_dict.items():
    print(f"The amount of {key}: {len(value)}")
