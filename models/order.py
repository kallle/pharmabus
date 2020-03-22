class Order:
    def __init__(self, id, patient, medications, status):
        self._id = id
        self._patient = patient
        self._medications = medications
        self._status = status

    @property
    def id(self):
        return self._id

    @property
    def status(self):
        return self._status

    @property
    def patient(self):
        return self._patient

    @property
    def medications(self):
        return self._medications

    def __repr__(self):
        return ('Order(id={self._id!r}, '
                'patient={self._patient!r}, '
                'medications={self._medications!r}, '
                ).format(self=self)

