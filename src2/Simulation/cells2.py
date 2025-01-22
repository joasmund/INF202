from abc import ABC, abstractmethod
import numpy as np


class Cell(ABC):
    def __init__(
        self,
        pts,
        idx,
        points,
    ) -> None:
        self._pointIds = pts  # Index (in the points list in the mesh) of points in cell
        self._idx = idx  # Cell id
        self._neighbors = []  # List of neighbors
        self._points = points

    def computeNeighbors(self, cells):
        """
        This function computes cell neighbors for current instance.
        Optimized for performance by using point-to-cell mapping.
        """
        # Create a mapping of points to the cells they belong to
        point_to_cells = {}
        for cell in cells:
            for point_id in cell._pointIds:
                if point_id not in point_to_cells:
                    point_to_cells[point_id] = []
                point_to_cells[point_id].append(cell)

        # Use the point-to-cells mapping to find neighbors efficiently
        candidate_neighbors = set()
        for point_id in self._pointIds:
            if point_id in point_to_cells:
                candidate_neighbors.update(point_to_cells[point_id])

        # Filter candidate neighbors to include only valid neighbors
        for cell in candidate_neighbors:
            if cell._idx != self._idx:  # Exclude self
                matches = set(self._pointIds) & set(cell._pointIds)
                if len(matches) == 2:
                    self._neighbors.append(cell._idx)

    # @computeNeighbors.setter
    # def neighbors(self, neighboring_cells: list[int]) -> None:
    #     """
    #     Stores the neighbors found in find_neighbors() from the mesh class in this cell
    #     """
    #     self._neighbors = neighboring_cells

    @property
    def point_coords(self):
        """
        Returns the coordinates of the points in the cell
        """
        return [self._points[point] for point in self._pointIds]

    # @abstractmethod
    # def __str__(self) -> str:
    #     return ""


class Vertex(Cell):
    def __init__(
        self,
        pts,
        idx,
        points,
    ) -> None:
        super().__init__(
            pts,
            idx,
            points,
        )

    # def __str__(self) -> str:
    #     """
    #     Prints out "Vertex"
    #     """
    #     return f"Vertex with id {self._idx}"


class Line(Cell):
    def __init__(
        self,
        pts,
        idx,
        points,
    ) -> None:
        super().__init__(
            pts,
            idx,
            points,
        )

    # def __str__(self) -> str:
    #     """
    #     Prints out "Line" and then all neighbors
    #     """
    #     return f"Line with id {self._idx}: {self._neighbors}"


class Triangle(Cell):
    def __init__(
        self,
        pts,
        idx,
        points,
    ) -> None:
        super().__init__(
            pts,
            idx,
            points,
        )

    def area(self):
        coords_2d = self.point_coords

        # Extract the points
        x1, y1 = coords_2d[0]
        x2, y2 = coords_2d[1]
        x3, y3 = coords_2d[2]

        # Compute the area using the determinant formula
        return 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))

    def center(self):
        """
        Compute the geometric midpoint of the cell.
        :param points: List of all points in the mesh
        :return: Numpy array representing the midpoint
        """
        return np.mean(self.point_coords, axis=0)

    def midpoints(self): #Deprecated
        points = self.point_coords
        return (points + np.roll(points, shift=-1, axis=0)) / 2

    def line_normals(self):
        """
        Calculate the normal vector for each edge of the triangle.
        :return: List of normal vectors for each edge of the triangle.
        """
        return [
            (np.array([-self.point_coords[i][1], self.point_coords[(i + 1) % 3][0]]))
            / np.linalg.norm(
                np.array([-self.point_coords[i][1], self.point_coords[(i + 1) % 3][0]])
            )
            for i in range(3)
        ]

    def initial_oil(self):
        """
        Extract triangular elements from the mesh
        """
        # Access the stored msh object
        x_star = np.array([0.35, 0.45])

        # Compute the Gaussian function for each point in the mesh
        data = np.exp(-np.linalg.norm(self._points - x_star, axis=1) ** 2 / 0.01)

        # Compute and return the average of the data at the triangle's vertices
        return np.mean(data[self._pointIds])

    def flux(self, ngh, nu, v):
        res = np.dot(v, nu)
        if res > 0:
            return self._idx * np.dot(v, nu)
        else:
            return ngh * np.dot(v, nu)

    def __str__(self) -> str:
        """
        Prints out "Triangle" and then all neighbors
        """

        normals = self.line_normals()
        normals_str = "\n                              ".join(
            f"Normal {i + 1}: {normals[i]}" for i in range(len(normals))
        )

        return f"""
Triangle with id: {self._idx}
Has neihgbors: {self._neighbors}
Midpoint of triangle is located at {self.center()}.
The triangles normal vectors: {normals_str}.
The startpoint of each normal vector is located at {self.midpoints()}
Area of triangle is {self.area()}
Amount of oil in cell equates to {self.initial_oil()}
"""
