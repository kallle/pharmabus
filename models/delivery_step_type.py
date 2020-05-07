from enum import enum

class DeliveryStepType(enum):

    PICK_UP_PRESCRIPTION = 0
    PICK_UP_MED = 1
    DROP_OFF_MED = 2
