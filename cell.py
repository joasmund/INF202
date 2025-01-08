import numpy as np 

class Cell: 
    def __init__(self, points):
        self.point = np.array(points)
        self.midpoint = self.midpoint_calc()
        self.triangle = self.triangle_calc()
        self.norm = self.norm_calc()

    def triangle_calc(self):
        x1, y1 = self.point[0]
        x2, y2 = self.point[1]
        x3, y3 = self.point[2]
        return 0.5 * abs((x1 - x3) * (y2 - y1) - (x1 - x2) * (y3 - y1))

    def midpoint_calc(self):
        return np.mean(self.point, axis=0)
    
    def  norm_calc(self):
        edge = np.roll(self.point, -1, axis = 0) - self.point
        lenght = np.linalg.norm(edge, axis=1)
        norm = np.column_stack([-edge[:,1], edge[:,0]]) / lenght[:, None]

        scaled = norm * lenght[:, None]
        return norm_calc, scaled




points = [(0, 0), (1, 0), (0, 1)]
cell = Cell(points)
norm_calc, scaled = cell.norm_calc()

print("Midtpunkt:", cell.midpoint)  
print("Areal:", cell.triangle)   
print("Normale vektorer og skalerte vektorer:")
for i, normal in enumerate(cell.norm[0], start=1): 
    print(f"n{i}: {normal}")