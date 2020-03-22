class Stock:
    def __init__(self, med_amount_list):
        self._stock = dict()
        for elem in med_amount_list:
            self._stock[elem[0]] = elem[1]

        @property
        def stock(self):
            return self._stock
