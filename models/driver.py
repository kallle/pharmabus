class Driver:
    def __init__(self, id, pwd, surname, familyname, plz, street, streetno, longitude, latitude, max_range, current_route):
        super().__init__(id, pwd, surname, familyname, plz, street, streetno, longitude, latitude)
        self._max_range = max_range
        self._current_route = current_route

    @property
    def max_range(self):
        return self._max_range

    def __repr__(self):
        return ('Driver(id={self._id!r}, '
                'name={self._name!r}, '
                'range={self._max_range!r}, '
                'address={self._address!r}, '
                'coordinates={self._coordinates!r})'
                ).format(self=self)


    def with_id(self, id):
        raise Exception("Depricated?")
        return Driver(id, self._name, self._range, self._address, self._coordinates, self._cooler_dimensions, self._storage_dimensions)


