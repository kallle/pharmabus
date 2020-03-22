from enum import Enum

class Role(Enum):
    PATIENT = 1
    PHARMACY = 2
    DRIVER = 3
    OVERLORD = 4


class InvalidRoleException(Exception):
    pass
