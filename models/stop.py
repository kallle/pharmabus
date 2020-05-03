class Stop:
    def __init__(self, kind, related_order):
        self._kind = kind
        self._related_order = related_order

    @property
    def kind(self):
        return self._kind

    @property
    def related_order(self):
        return self._meds

    def __eq__(self, other):
        if self.related_order != other.related_order:
            return False
        else:
            return self.kind == other.kind
