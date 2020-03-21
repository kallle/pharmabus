class Coordinates:
    def __init__(self, latitude, longitude):
        self._latitude = latitude
        self._longitude = longitude

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    def __repr__(self):
        return ('Coordinates(latitude={self._latitude!r}, '
                'longitude={self._longitude!r})'
                ).format(self=self)


def get_default_coordinates():
    return Coordinates(0, 0)
