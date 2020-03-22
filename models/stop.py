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

    def __eq__(self, other):
        if self.where != other.where:
            return False
        elif self.kind != other.kind:
            return False
        elif self.meds != other.meds:
            for elem in self.meds:
                found = False
                for other_elem in other.meds:
                    if elem == other_elem:
                        found = True
                        break
                if not found:
                    return False
        else:
            return True
