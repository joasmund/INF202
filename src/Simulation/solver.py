class CellFactory:
    def __init__(self) -> None:
        self._cellTypes = {}

    def register(self, key: str, name):
        self._cellTypes[key] = name

    def __call__(self, key, pts, idx) -> None:
        return self._cellTypes[key](pts, idx)
