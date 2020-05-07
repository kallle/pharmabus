from enum import Enum

class DeliveryStepType(Enum):

    PICK_UP_PRESCRIPTION = 0
    PICK_UP_MED = 1
    DROP_OFF_MED = 2

    def toString(enum_value):
        if enum_value == DeliveryStepType.PICK_UP_PRESCRIPTION:
            return "PICK_UP_PRESCRIPTION"
        elif enum_value == DeliveryStepType.PICK_UP_MED:
            return "PICK_UP_MED"
        elif enum_value == DeliveryStepType.DROP_OFF_MED:
            return "DROP_OFF_MED"
        else:
            raise Exception("unsopported delivery step action {}".format(enum_value))

    def fromString(enum):
        if enum == "PICK_UP_PRESCRIPTION":
            return DeliveryStepType.PICK_UP_PRESCRIPTION
        elif enum == "PICK_UP_MED":
            return DeliveryStepType.PICK_UP_MED
        elif enum == "DROP_OFF_MED":
            return DeliveryStepType.DROP_OFF_MED
        else:
            raise Exception("unsopported string for order status {}".format(enum))
