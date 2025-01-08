import streamlit as st
import pandas as pd
import numpy as np
import meshio 
import matplotlib.pyplot as plt



# Load the .msh file
mesh = meshio.read("bay.msh")

st.title('Simulate oil spill')


umax = 1
umin = -1

for i in range (0,20):

    u1 = np.sin(i/10 * np.pi)
    u2 = np.cos(i/10 * np.pi)

    u = np.array([u1, u2, u1, u2])
    
    triangle1 = np.array([[0, 0], [0, 1], [1, 1]])
    triangle2 = np.array([[0, 0], [1, 1], [1, 0]])
    triangle3 = np.array([[-1, 0], [0, 0], [0, 1]])
    triangle4 = np.array([[0, 0], [1, 0], [1, -1]])

    # Plot the mesh by adding all triangles with their value
    plt.figure()

    # Create the colormap
    sm = plt.cm.ScalarMappable(cmap='viridis')
    sm.set_array([umin, umax])
 


    # Add colorbar using a separate axis
    cbar_ax = plt.gca().inset_axes([1, 0, 0.05, 1])  # adjust position and size as needed
    plt.colorbar(sm, cax=cbar_ax, label='label3')

    plt.gca().add_patch(plt.Polygon(triangle1, color=plt.cm.viridis((u[0] - umin)/(umax - umin)), alpha=0.9))
    plt.gca().add_patch(plt.Polygon(triangle2, color=plt.cm.viridis((u[1] - umin)/(umax - umin)), alpha=0.9))

    # Add labels to axes
    plt.xlabel('label1')
    plt.ylabel('label2')

    plt.xlim(0, 1)  # set the x-axis limits
    plt.ylim(0, 1)  # set the y-axis limits
    plt.gca().set_aspect('equal')

    # Show plot
    plt.savefig(f"tmp/img_{i}.png")

    plt.close()

if st.button ('Show image'):
    result = st.image('tmp/img_0.png')
    