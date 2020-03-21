class Address:
    def __init__(self, postal_code, street, number):
        self._postal_code = postal_code
        self._street = street
        self._number = number

    @property
    def postal_code(self):
        return self._postal_code

    @property
    def street(self):
        return self._street

    @property
    def number(self):
        return self._number

    def __repr__(self):
        return ('Address(postal_code={self._postal_code!r}, '
                'street={self._street!r},  number={self._number!r})'
                ).format(self=self)
