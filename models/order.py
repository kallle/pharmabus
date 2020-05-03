class Order:
    def __init__(self, id, status, prescription, patient, doctor, pharmacy):
        self._id = id
        self._status = status
        self._prescription = prescription
        self._patient = patient
        self._doctor = doctor
        self._pharmacy = pharmacy

    @property
    def id(self):
        return self._id

    @property
    def id(self,value):
        raise Exception("this is a read only object")

    @property
    def title(self):
        return self._title

    @property
    def title(self,value):
        raise Exception("this is a read only object")

    @property
    def status(self):
        return self._status

    @property
    def status(self,value):
        raise Exception("this is a read only object")

    @property
    def prescription(self):
        return self._prescription

    @property
    def prescription(self,value):
        raise Exception("this is a read only object")

    @property
    def patient(self):
        return self._patient

    @property
    def patient(self,value):
        raise Exception("this is a read only object")

    @property
    def doctor(self):
        return self._doctor

    @property
    def doctor(self,value):
        raise Exception("this is a read only object")

    @property
    def pharmacy(self):
        return self._pharmacy

    @property
    def pharmacy(self,value):
        raise Exception("this is a read only object")

    def __repr__(self):
        return ('Order(id={self._id!r}, '
                'patient={self._patient!r}, '
                'medications={self._medications!r}, '
                ).format(self=self)

