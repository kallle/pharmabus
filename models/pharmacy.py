# TODO: Add medication storage
class Pharmacy:


    def __init__(self, id, pwd, name, surname, familyname, plz, street, streetno, longitude, latitude):
        super().__init__(id, pwd, surname, familyname, plz, street, streetno, longitude, latitude)
        self._name = name

    @property
    def name(self):
        return self._name

    def __repr__(self):
        return ('Pharmacy(id={self._id!r}, '
                'name={self._name!r}, '
                'address={self._address!r}, '
                'coordinates={self._coordinates!r})'
                ).format(self=self)

