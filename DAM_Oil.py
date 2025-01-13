import numpy as np 

def g(a, b, v, nu):
    
    dot = np.dot(v, nu)
    if dot > 0.0:
        return a * dot
    else:
        return b * dot
    
def flux(dt, A_i, u_i, u_ngh, v_i, v_ngh, nu_i):
    v_edge = 0.5 * (v_i + v_ngh)

    val = g(u_i, u_ngh, v_edge, nu_i)
    return - (dt / A_i) * val 

def update_cell(dt, A_i, u_i, neighbors, velocities, normals):

    u_new = u_i

    for(u_ngh, v_ngh, nu_i) in neighbors: 
        f_ = flux_i_ngh(dt, A_i, u_i, u_ngh, velocities, v_ngh, nu_i)
        u_new += f_


        