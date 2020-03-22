class Driver:
    def __init__(self, id, name, range, address, coordinates, cooler_dimensions, storage_dimensions):
        self._id = id
        self._name = name
        self._range = range
        self._address = address
        self._coordinates = coordinates
        self._cooler_dimensions = cooler_dimensions
        self._storage_dimensions = storage_dimensions

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def range(self):
        return self._range

    @property
    def address(self):
        return self._address

    @property
    def coordinates(self):
        return self._coordinates

    @property
    def cooler_dimensions(self):
        return self._cooler_dimensions

    @property
    def storage_dimensions(self):
        return self._storage_dimensions

    def __repr__(self):
        return ('Driver(id={self._id!r}, '
                'name={self._name!r}, '
                'range={self._range!r}, '
                'address={self._address!r}, '
                'coordinates={self._coordinates!r})'
                'cooler_dimensions={self._cooler_dimensions!r})'
                'storage_dimensions={self._storage_dimensions!r})'
                ).format(self=self)

    def with_id(self, id):
        return Driver(id, self._name, self._range, self._address, self._coordinates, self._cooler_dimensions, self._storage_dimensions)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def geq(self, other):
        return self.volume() >= other.volume()


