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
        self._inital_oil = self.initial_oil()
        self._current_oil = self.initial_oil

    def area(self):
        # Stack the arrays vertically
        points_3x3 = np.vstack(self.point_coords)
        # Turn the coordinates into a 2D array
        coords_2d = points_3x3[:, :2]
        # Extract the points
        x1, y1 = coords_2d[0]
        x2, y2 = coords_2d[1]
        x3, y3 = coords_2d[2]

        # Compute the area using the determinant formula
        return 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))

    def midpoint(self):
        """
        Compute the geometric midpoint of the cell.
        :param points: List of all points in the mesh
        :return: Numpy array representing the midpoint
        """
        return np.mean(self.point_coords, axis=0)

    def line_normals(self):
        """
        Calculate the normal vector for each edge of the triangle and append the
        point of origin (midpoint of the edge) for each normal vector.
        :return: List of tuples, each containing a normal vector and its origin point.
        """
        normals_with_origins = []
        coords = self.point_coords  # Cache the point coordinates for efficiency

        for i in range(3):  # Loop over the edges of the triangle
            # Calculate the two points forming the edge
            p1 = np.array(coords[i])
            p2 = np.array(coords[(i + 1) % 3])

            # Compute the midpoint (origin of the normal)
            origin = (p1 + p2) / 2

            # Calculate the edge vector
            edge_vector = p2 - p1

            # Rotate the edge vector by 90 degrees to get the normal (in 2D)
            normal = np.array([-edge_vector[1], edge_vector[0]])

            # Normalize the normal vector
            normal = normal / np.linalg.norm(normal)

            # Append the normal and its origin point as a tuple
            normals_with_origins.append((normal, origin))

        return normals_with_origins

    # def line_normals(self):
    #     """
    #     Calculate the normal vector for each edge of the triangle.
    #     :return: List of normal vectors for each edge of the triangle.
    #     """
    #     return [
    #         (np.array([-self.point_coords[i][1], self.point_coords[(i + 1) % 3][0]]))
    #         / np.linalg.norm(
    #             np.array([-self.point_coords[i][1], self.point_coords[(i + 1) % 3][0]])
    #         )
    #         for i in range(3)
    #     ]

    # def line_normals(self):
    #     """
    #     Calculate the normal vector for each edge of the triangle.
    #     :return: List of normal vectors for each edge of the triangle.
    #     """
    #     normals = []
    #
    #     for i in range(3):  # Loop over the edges of the triangle
    #         p1 = self.point_coords[i]
    #         p2 = self.point_coords[(i + 1) % 3]  # Next point, wrapping around
    #         edge_vector = p2 - p1
    #
    #         if len(edge_vector) == 2:  # 2D case
    #             # Rotate by 90 degrees
    #             normal = np.array([-edge_vector[1], edge_vector[0]])
    #         # elif len(edge_vector) == 3:  # 3D case
    #         #     # Cross product with a vector normal to the triangle's plane
    #         #     p3 = self.point_coords[(i + 2) % 3]
    #         #     triangle_normal = np.cross(p2 - p1, p3 - p1)  # Plane normal
    #         #     normal = np.cross(edge_vector, triangle_normal)
    #         # else:
    #         #     raise ValueError("Unsupported dimensionality")
    #
    #         # Normalize the normal vector
    #         normals.append(normal / np.linalg.norm(normal))
    #
    #     return normals

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
        if np.dot(v, nu):
            return self._idx * np.dot(v, nu)
        else:
            return ngh * np.dot(v, nu)

    def __str__(self) -> str:
        """
        Prints out "Triangle" and then all neighbors
        """

        normals = self.line_normals()
        ordinal_names = ["first", "second", "third"]
        normals_str = "\n".join(
            f"The triangles {ordinal_names[i]} normal vector: {[float(coord) for coord in normals[i][0]]} and the startpoint for this vector: {[float(coord) for coord in normals[i][1]]}"
            for i in range(len(normals))
        )

        return f"""
Triangle with id: {self._idx}
Has neihgbors: {self._neighbors}
Midpoint of triangle is located at {self.midpoint()}.
The triangles normal vectors: {normals_str}.
Area of triangle is {self.area()}
Amount of oil in cell equates to {self._current_oil}
"""
