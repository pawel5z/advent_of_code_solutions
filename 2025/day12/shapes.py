class Shape:
    def __init__(self, shape_lines: list[str]):
        self._coords: set[tuple[int]] = set()
        for y, line in enumerate(shape_lines):
            for x, char in enumerate(line):
                if char == "#":
                    self.coords.add((x, y))

    @property
    def coords(self):
        return self._coords

    @property
    def space(self):
        return len(self._coords)
