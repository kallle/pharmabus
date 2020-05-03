from enum import Enum

class Role(Enum):
    NONE = "Pleb"
    DOCTOR = "Doctor"
    PATIENT = "Patient"
    PHARMACY = "Pharmacy"
    DRIVER = "Driver"
    OVERLORD = "Overlord"


class InvalidRoleException(Exception):
    pass
