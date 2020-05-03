from models.user import User

class Patient(User):

    def __init__(self, id, email, surname, familyname, plz, street, streetno, tel, longitude, latitude):
        super().__init__(id, email, surname, familyname, plz, street, streetno, tel, longitude, latitude)
