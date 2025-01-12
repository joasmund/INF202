import numpy as np


def flux(a, b, nu, v):
    if np.dot(v, nu) > 0:
        return a * np.dot(v, nu)
    else:
        return b * np.dot(v, nu)

def oil()
