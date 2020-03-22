class Stop:
    def __init__(self, kind, where, meds):
        self._kind = kind
        self._meds = meds
        self._where = where

    @property
    def kind(self):
        return self._kind

    @property
    def meds(self):
        return self._meds

    @property
    def where(self):
        return self._where
