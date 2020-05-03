class Order:
    def __init__(self, id, title, status, prescription, patient, doctor, pharmacy):
        self._id = id
        self._title = title
        self._status = status
        self._prescription = prescription
        self._patient = patient
        self._doctor = doctor
        self._pharmacy = pharmacy

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def status(self):
        return self._status

    @property
    def prescription(self):
        return self._prescription

    @property
    def patient(self):
        return self._patient

    @property
    def doctor(self):
        return self._doctor

    @property
    def pharmacy(self):
        return self._pharmacy

    def __repr__(self):
        return ('Order(id={self._id!r}, '
                'patient={self._patient!r}, '
                'medications={self._medications!r}, '
                ).format(self=self)

