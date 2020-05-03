class Route:
    def __init__(self, points):
        # has to be list with first stop first
        self._points = points

    @property
    def points(self):
        return self._points
