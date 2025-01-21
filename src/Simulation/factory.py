class CellFactory:
    def __init__(self) -> None:
        self._cellTypes = {}

    def register(self, key: str, name: object):
        if key not in self._cellTypes:
            self._cellTypes[key] = name

    def __call__(self, key: str, id: int, oil_amount: float = 0.0, area: float = 0.0, 
                normal_vectors_with_faces: tuple = tuple(), faces: list = [], 
                velocity_field: float = 0.0, neighbors: list = [], delta_t=0.01, cell_in_bay=False):
        return self._cellTypes[key](id, oil_amount, area, normal_vectors_with_faces, faces, velocity_field, neighbors, delta_t, cell_in_bay)
