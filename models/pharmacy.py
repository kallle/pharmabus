# TODO: Add medication storage
class Pharmacy:
    def __init__(self, id, name, address, coordinates, stock):
        self._id = id
        self._name = name
        self._address = address
        self._coordinates = coordinates
        self._stock = stock

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

    @property
    def stock(self):
        return self._stock

    def reduce_stock(self, med, delta):
        self._stock[med] -= delta
        amount = self._stock[med]
        if amount == 0:
            del self._stock[med]
        return amount

    def set_stock(self, stock):
        self._stock = stock

    def __repr__(self):
        return ('Pharmacy(id={self._id!r}, '
                'name={self._name!r}, '
                'address={self._address!r}, '
                'coordinates={self._coordinates!r})'
                ).format(self=self)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def geq(self, other):
        return self.coordinates.geq(other.coordinates)

