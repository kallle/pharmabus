from enum import Enum

class PrescriptionStatus(Enum):

    PRESENT_AT_DOCTOR = "PRESENT_AT_DOCTOR"
    PRESENT_AT_PATIENT = "PRESENT_AT_PATIENT"

    def toString(enumValue):
        if enumValue == PrescriptionStatus.PRESENT_AT_DOCTOR:
            return "PRESENT_AT_DOCTOR"
        elif enumValue == PrescriptionStatus.PRESENT_AT_PATIENT:
            return "PRESENT_AT_PATIENT"
        else:
            raise Exception("unsupporeted prescription status value {}".format(enumValue))

    def fromString(enum):
        if enum == "PRESENT_AT_DOCTOR":
            return PrescriptionStatus.PRESENT_AT_DOCTOR
        elif enum == "PRESENT_AT_PATIENT":
            return PrescriptionStatus.PRESENT_AT_PATIENT
        else:
            raise Exception("unsopported string for prescription status {}".format(enum))


class InvalidPrescriptionStatus(Exception):

    def __init__(self, reason):
        self._reason = reason
