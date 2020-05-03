from coordinates import Coordinates
from address import Address

class User:

    def __init__(self, id, email, surname, familyname, plz, street, streetno, tel, longitude, latitude):
        self._id = id
        self._email = email
        self._tel = tel
        self._surname = surname
        self._familyname = familyname
        self._address = Address(plz, street, streetno);
        self._plz = plz
        self._street = street
        self._streetno = streetno
        self._coordinates = Coordinates(latitude, longitude)

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @property
    def pwd(self):
        return self._pwd

    @property
    def tel(self):
        return self._tel

    @property
    def surname(self):
        return self._surname

    @property
    def familyname(self):
        return self._familyname

    @property
    def address(self):
        return self._address

    @property
    def coordinates(self):
        return self._coordinates

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def geq(self, other):
        return self.coordinates.geq(other.coordinates)
