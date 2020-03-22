class Route:
    def __init__(self, driver, points):
        self._driver = driver
        self._points = points

    @property
    def driver(self):
        return self._driver

    @property
    def points(self):
        return self._points