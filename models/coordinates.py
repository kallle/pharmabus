from math import sin, cos, sqrt, atan2, radians


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

    # shamelessly stolen from https://stackoverflow.com/a/19412565/919434
    def bird_distance(self, other):
        lat1 = self.latitude
        lon1 = self.longitude
        lat2 = other.latitude
        lon2 = other.longitude
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        assert a >= 0
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        R = 6373.0
        distance = R * c
        return distance


def get_default_coordinates():
    return Coordinates(0, 0)
