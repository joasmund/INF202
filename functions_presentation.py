def updateSolution(nu, v):
    up = 0

    for i in range(100):
        nu = "scaled outer normal in cell i at the interface to cell ngh"
        v = "average of velocity in cell i and cell ngh"
        up = "up - ∆t / Ai * FLUX(u[i], u[ngh], ν, v )"

    uNew[i] = u[i] - up

    return uNew[i]


def dot(v, nu):
    return v * nu


def flux(a, b, nu, v):
    if dot(v, nu) > 0:
        return a * dot(v, nu)
    else:
        return b * dot(v, nu)
