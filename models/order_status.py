from enum import Enum

class OrderStatus(Enum):

    AT_PATIENT = "at_patient"
    AT_PHARMACY = "at_pharmacy"
    AT_DRIVER = "at_driver"
    DELIVERED = "delivered"
