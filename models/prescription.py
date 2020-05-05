class Prescription:

    def __init__(self, id, status, scan):
        self._id = id
        self._status = status
        self._scan = scan

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self,value):
        raise Exception("this is a read only object")

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self,value):
        raise Exception("this is a read only object")

    @property
    def scan(self):
        return self._scan

    @scan.setter
    def scan(self,value):
        raise Exception("this is a read only object")
