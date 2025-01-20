import numpy as np 

class Cell: 
    def __init__(self, points):
        self.point = np.array(points)
        self.midpoint = self.midpoint_calc()
        self.triangle = self.triangle_calc()
        self.norm = self.unit_normal_vector(self.point[0], self.point[1])
    
    # Calculate the triangle
    def triangle_calc(self):
        x1, y1 = self.point[0]
        x2, y2 = self.point[1]
        x3, y3 = self.point[2]
        return 0.5 * abs((x1 - x3) * (y2 - y1) - (x1 - x2) * (y3 - y1))
    
    # Calculate the midpoint 
    def midpoint_calc(self):
        return np.mean(self.point, axis=0)
    
    # Finding the normal
    def unit_normal_vector(self, point1, point2):
        vector = point2 - point1
        normal_vector = np.array([-vector[1], vector[0]])
        return normal_vector / np.linalg.norm(normal_vector)
    
    # Checking the direction 
    def check_vector_direction(self, m, pov, es, ee): # midpoint, point on vector, edge start and edge end.
        vector = np.array(pov) - np.array(m)
        normal = Cell.unit_normal_vector(es, ee)
        edge_length = np.linalg.norm(np.array(ee)-np.array(es))
        
        scaled_normal = normal * edge_length
        
        # Dot product for direction 
        dot_product = np.dot(vector, scaled_normal)
        if dot_product > 0:
            direction = m * dot_product, "Same as normal vector"
        elif dot_product < 0:
            direction = pov * dot_product, "Opposit of normal vector"
        else:
            direction = "Orthogona"
        return dot_product, direction
    
# Using fixed coordinates try the function
points = [(0, 0), (1, 0), (0, 1)]

cell = Cell(points)


print("Midtpunkt:", cell.midpoint)  
print("Areal:", cell.triangle)   
print("Normale vektorer", cell.norm)

