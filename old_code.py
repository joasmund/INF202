from abc import ABC, abstractmethod

import meshio

"""
Flow: 

1. Mesh class: Read the mesh file and extract points and cells data.
2. Point class: Create `Point` objects for each point in the mesh.
3. Cell class: Create `Triangle` or `Line` objects for each cell, depending on its type.
4. Cell class: For each cell, find neighboring cells by checking shared points.
5. Cell class: Determine if a cell is a boundary cell.
6. Print information about specific cells using their indexes. 
7. Test the implementation with cells having indexes 4, 189, 222.

"""


# Creating a Point class with x and y coordinates
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    # String representation of the Point object
    def __str__(self):
        return f"X-coordinate: ({self.x}, Y-coordinate: {self.y})"


# Creating an abstract Cell class with index, points, and a list to store the neighbors
class Cell(ABC):
    def __init__(self, index: int, points: list):
        self.index = index
        self._points = points
        self._neighbors = []

    @abstractmethod
    def border_check(self):
        pass

    # Abstract method to check if a cell is a neighbor of another cell
    @abstractmethod
    def neighbor_check(self, cell):
        pass

    def neighbor_add(self, neighbor):
        self._neighbors.append(neighbor)

    def __str__(self):
        # Check if the cell is a boundary cell.
        # Print the cell index, boundary status, and the indexes of its neighbors.
        neighbor_ids = [neighbor.index for neighbor in self._neighbors]
        if self.border_check():
            boundary_check = "boundary"
        else:
            boundary_check = "NOT boundary"
        return f"Cell number: {self.index} is {boundary_check}. And the cell is neighbor to the follwing cells: {neighbor_ids}"


# Creating a Line class inheriting from Cell
class Line(Cell):
    def neighbor_check(self, cell):
        shared_points = set(self._points).intersection(set(cell._points))
        if len(shared_points) == 1 and len(cell._points) == 2:
            return True
        elif len(shared_points) == 2 and len(cell._points) == 3:
            return True
        else:
            return False

    def border_check(self):
        return True


# Creating a Triangle class inheriting from Cell
class Triangle(Cell):
    def neighbor_check(self, cell):
        shared_points = set(self._points).intersection(set(cell._points))
        if len(shared_points) == 2:
            return True
        return False

    def border_check(self):
        for neighbor in self._neighbors:
            if type(neighbor) == Line:
                return True
        return False


# Creating a Mesh class to read the mesh file and extract points and cells data
class Mesh:
    def __init__(self, meshFile):
        self._points = []
        self._cells = []
        self.read_mesh(meshFile)
        self.find_neighbors()

    # Reading the mesh file and storing the points and cells
    def read_mesh(self, meshFile):
        msh = meshio.read(meshFile)
        points = msh.points
        cells = msh.cells

        for coordinates in points:
            x, y = coordinates[0], coordinates[1]
            self._points.append(Point(x, y))

        cell_nr = 0
        for cell in cells:
            cell_type = cell.type
            for cell_coordinates in cell.data:
                checking_cell = CellFactory.create_cell(
                    cell_type, cell_nr, cell_coordinates.tolist()
                )
                self._cells.append(checking_cell)
                cell_nr += 1

    # Finding the neighbors of each cell
    def find_neighbors(self):
        for i, first_cell in enumerate(self._cells):
            for j, second_cell in enumerate(self._cells):
                if i != j and first_cell.neighbor_check(second_cell):
                    first_cell.neighbor_add(second_cell)

    # Printing the cell information for given indexes
    def print_cell_info(self, indexes: list):
        for i in indexes:
            if 0 <= i < len(self._cells):
                print(self._cells[i])
            else:
                print(f"Cell {i} is out of bounds")


# Creating a CellFactory class to create a cell object based on the cell type
class CellFactory:
    def create_cell(cell_type, index: int, points: list):
        if cell_type == "triangle":
            return Triangle(index, points)
        elif cell_type == "line":
            return Line(index, points)


# Running the implementation with cells having indexes 4, 189, 222
mesh = Mesh("bay.msh")
mesh.print_cell_info([2345, 189, 222])
