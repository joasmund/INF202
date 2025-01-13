import numpy as np 

x_min, x_max = 0.0, 0.45
y_min, y_max = 0.0, 0.20

num_points = 100
x_values = np.linspace(x_min, x_max, num_points)
y_values = np.linspace(y_min, y_max, num_points)

x, y = np.meshgrid(x_values, y_values)

x_start, y_start = 0.35, 0.45


def formula_unit(x,y):

    return np.exp(-((x-x_start)**2 + (y+y_start)**2)/0.01)


result = formula_unit(x, y)

print("Result dimensjon:", result.shape)
print("Example:", result[0, 0])

    

