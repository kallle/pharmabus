# TODO: keep list of synonyms in here?
class Medication:
    def __init__(self, pzn, name, dimensions, requires_cooling, quantity, ingredients):
        self._pzn = pzn
        self._name = name
        self._dimensions = dimensions
        self._requires_cooling = requires_cooling
        self._quantity = quantity
        self._ingredients = ingredients

    @property
    def pzn(self):
        return self._pzn

    @property
    def name(self):
        return self._name

    @property
    def dimensions(self):
        return self._dimensions

    @property
    def requires_cooling(self):
        return self._requires_cooling

    @property
    def quantity(self):
        return self._quantity

    @property
    def ingredients(self):
        return self._ingredients

    def __repr__(self):
        return ('Medication(pzn={self._pzn!r}, '
                'name={self._name!r}, '
                'dimensions={self._dimensions!r}, '
                'requires_cooling={self._requires_cooling!r}, '
                'quantity={self._quantity!r}, '
                'ingredients={self._ingredients!r}, '
                ).format(self=self)

    def __eq__(self, other):
        return self.pzn() == other.pzn()

    def geq(self, other):
        return self.pzn() >= other.pzn()
