from enum import Enum

class PrescriptionStatus(Enum):

    PRESENT_AT_DOCTOR = "PRESENT_AT_DOCTOR"
    PRESENT_AT_PATIENT = "PRESENT_AT_PATIENT"


class InvalidPrescriptionStatus(Exception):

    def __init__(self, reason):
        self._reason = reason
