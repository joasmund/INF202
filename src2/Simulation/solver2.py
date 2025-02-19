class CellFactory:
    def __init__(self) -> None:
        self._cellTypes = {}

    def register(self, key: str, name: object):
        if key not in self._cellTypes:
            self._cellTypes[key] = name

    def __call__(self, key: str, pts: float, idx: int, points):
        return self._cellTypes[key](pts, idx, points)
