import matplotlib.pyplot as plt
import numpy as np


def flux(a, b, nu, v):
    if np.dot(v, nu) > 0:
        return a * np.dot(v, nu)
    else:
        return b * np.dot(v, nu)


def oil():
    return 0


def plotter(x, y):
    plt.plot(x, y)
    plt.show()
