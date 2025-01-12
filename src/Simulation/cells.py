from abc import ABC, abstractmethod

import numpy as np


class Cell(ABC):
    def __init__(self, pts, idx, points) -> None:
        self._pointIds = pts  # Index (in the points list in the mesh) of points in cell
        self._idx = idx  # Cell id
        self._neighbors = []  # List of neighbors
        self._points = points

    def computeNeighbors(self, cells):
        """
        This function computes cell neighbors for current instance
        """
        for cell in cells:
            matches = set(self._pointIds) & set(cell._pointIds)
            if len(matches) == 2:
                self._neighbors.append(cell._idx)
        pass

    @property
    def point_coords(self):
        """
        Returns the coordinates of the points in the cell
        """
        return [self._points[point] for point in self._pointIds]

    @abstractmethod
    def __str__(self) -> str:
        return ""


class Vertex(Cell):
    def __init__(self, pts, idx, points) -> None:
        super().__init__(pts, idx, points)

    def __str__(self) -> str:
        """
        Prints out "Vertex"
        """
        return f"Vertex with id {self._idx}"


class Line(Cell):
    def __init__(self, pts, idx, points) -> None:
        super().__init__(pts, idx, points)

    def __str__(self) -> str:
        """
        Prints out "Line" and then all neighbors
        """
        return f"Line with id {self._idx}: {self._neighbors}"


class Triangle(Cell):
    def __init__(self, pts, idx, points) -> None:
        super().__init__(pts, idx, points)

    def area(self):

        points_3x3 = np.vstack(self.point_coords)  # Stack the arrays vertically
        # Turn the coordinates into a 2D array
        coords_2d = points_3x3[:, :2]
        # Extract the points
        x1, y1 = coords_2d[0]
        x2, y2 = coords_2d[1]
        x3, y3 = coords_2d[2]

        # Compute the area using the determinant formula
        area = 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
        return area

    def midpoint(self):
        """
        Compute the geometric midpoint of the cell.
        :param points: List of all points in the mesh
        :return: Numpy array representing the midpoint
        """
        return np.mean(self.point_coords, axis=0)

    def line_normals(self):
        """
        Calculate the normal vector for each edge of the triangle.
        :return: List of normal vectors for each edge of the triangle.
        """
        normals = []

        for i in range(3):  # Loop over the edges of the triangle
            p1 = self.point_coords[i]
            p2 = self.point_coords[(i + 1) % 3]  # Next point, wrapping around
            edge_vector = p2 - p1

            if len(edge_vector) == 2:  # 2D case
                # Rotate by 90 degrees
                normal = np.array([-edge_vector[1], edge_vector[0]])
            elif len(edge_vector) == 3:  # 3D case
                # Cross product with a vector normal to the triangle's plane
                p3 = self.point_coords[(i + 2) % 3]
                triangle_normal = np.cross(p2 - p1, p3 - p1)  # Plane normal
                normal = np.cross(edge_vector, triangle_normal)
            else:
                raise ValueError("Unsupported dimensionality")

            # Normalize the normal vector
            normals.append(normal / np.linalg.norm(normal))

        return normals

    def __str__(self) -> str:
        """
        Prints out "Triangle" and then all neighbors
        """
        normals = self.line_normals()
        normals_str = ", ".join(
            f"Normal {i + 1}: {normals[i]}" for i in range(len(normals))
        )

        return f"Triangle with id {self._idx}: {self._neighbors} Midpoint of triangle is located at {self.midpoint()}. {normals_str} {self.area()}"
