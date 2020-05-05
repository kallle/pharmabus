from enum import Enum

class OrderStatus(Enum):

    AT_PATIENT = "at_patient"
    AT_PHARMACY = "at_pharmacy"
    AT_DRIVER = "at_driver"
    AT_DOCTOR = "at_doctor"
    DELIVERED = "delivered"

    def toString(enum_value):
        if enum_value == OrderStatus.AT_PATIENT:
            return "at_patient"
        elif enum_value == OrderStatus.AT_DOCTOR:
            return "at_doctor"
        elif enum_value == OrderStatus.AT_PHARMACY:
            return "at_pharamcy"
        elif enum_value == OrderStatus.AT_DRIVER:
            return "at_driver"
        elif enum_value == OrderStatus.DELIVERED:
            return "delivered"
        else:
            raise Exception("unsuppored order status enum value {}".format(enum_value))

    def fromString(enum):
        if enum == "at_patient":
            return OrderStatus.AT_PATIENT
        elif enum == "at_doctor":
            return OrderStatus.AT_DOCTOR
        elif enum == "at_pharmacy":
            return OrderStatus.AT_PHARMACY
        elif enum == "at_driver":
            return OrderStatus.AT_DRIVER
        elif enum == "delivered":
            return OrderStatus.DELIVERED
        else:
            raise Exception("unsupported string for order status {}".format(enum))
