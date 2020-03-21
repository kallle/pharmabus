# TODO: Add medication storage
class Pharmacy:
    def __init__(self, id, name, address, coordinates):
        self._id = id
        self._name = name
        self._address = address
        self._coordinates = coordinates

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def coordinates(self):
        return self._coordinates

    def __repr__(self):
        return ('Pharmacy(id={self._id!r}, '
                'name={self._name!r}, '
                'address={self._address!r}, '
                'coordinates={self._coordinates!r})'
                ).format(self=self)

