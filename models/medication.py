# TODO: keep list of synonyms in here?
class Medication:
    def __init__(self, pzn, name, supplier, dimensions, requires_cooling, quantity, ingredients, requires_recipe):
        self._pzn = pzn
        self._name = name
        self._supplier = supplier
        self._dimensions = dimensions
        self._requires_cooling = requires_cooling
        self._quantity = quantity
        self._ingredients = ingredients
        self._requires_recipe = requires_recipe

    @property
    def pzn(self):
        return self._pzn

    @property
    def name(self):
        return self._name

    @property
    def supplier(self):
        return self._supplier

    @property
    def dimensions(self):
        return self._dimensions

    @property
    def requires_cooling(self):
        return self._requires_cooling

    @property
    def requires_recipe(self):
        return self._requires_recipe

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
                'requires_recipe={self._requires_recipe!r}, '
                'quantity={self._quantity!r}, '
                'supplier={self._supplier!r}, '
                'ingredients={self._ingredients!r}, '
                ).format(self=self)

    def __eq__(self, other):
        return self.pzn == other.pzn

    def __hash__(self):
        return hash(self.pzn)

    def geq(self, other):
        return self.pzn >= other.pzn
