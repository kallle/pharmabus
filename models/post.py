class Post:
    def __init__(self, medication, amount):
        self._medication = medication
        self._amount = amount

    @property
    def medication(self):
        return self._medication

    @property
    def amount(self):
        return self._amount

    def __eq__(self, other):
        return (self.medication == other.medication and
                self.amount == other.amount)
