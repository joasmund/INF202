class CellFactory:
    def __init__(self) -> None:
        self._cellTypes = {}

    def register(self, key: str, name: object):
        if key not in self._cellTypes:
            self._cellTypes[key] = name

    def __call__(self, key: str, id: int, current_oil_amount: float=0.0, area: float=0.0, normal_vectors_with_faces: tuple=tuple(), velocity_field: float=0.0, neighbors: list=[], delta_t=0.01):
        return self._cellTypes[key](id, current_oil_amount, area, normal_vectors_with_faces, velocity_field, delta_t)
