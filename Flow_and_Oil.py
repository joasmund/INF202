import numpy as np 


class FAO: #Flow and Oil
    def __init__(self, x_center = 0.35, y_center=0.45, spread=0.01):
        self.x_center = x_center
        self.y_center = y_center
        self.spread = spread

    def flow_velocity(self, x, y):
        
        vx = y - 0.2 * x
        vy = -x 
        return np.array([vx, vy])
    
    def IOD(self, x, y): #Initial oil distibution, where t = 0
        
        distance_squared = (x - self.x_center)**2 + (y-self.y_center)**2
        return np.exp(-distance_squared / self.spread)


