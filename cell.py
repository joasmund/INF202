import numpy as np 

class Cell: 
    def __init__(self, points, neighbors=None):
        self.point = np.array(points)
        self.neighbors = neighbors if neighbors is not None else []
        self.midpoint = self.midpoint()
        self.triangle = self.triangle_calc()

    def triangle_calc(self):
        x1, y1 = self.point[0]
        x2, y2 = self.point[1]
        x3, y3 = self.point[2]
        return 0.5 * abs((x1 - x3) * (y2 - y1) - (x1 - x2) * (y3 - y1))

    def midpoint(self):
        return np.mean(self.point, axis=0)



"""
For testing 

points = [(0, 0), (1, 0), (0, 1)]
cell = Cell(points)

print("Midtpunkt:", cell.midpoint)  
print("Areal:", cell.triangle)   
- Mangler normalvektor.
"""