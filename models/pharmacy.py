from models.coordinates import Coordinates
from models.user import User

class Pharmacy(User):

    def __init__(self, id, email, surname, familyname, plz, street, streetno, tel, longitude, latitude, name):
        super().__init__(id, email, surname, familyname, plz, street, streetno, tel, longitude, latitude)
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

