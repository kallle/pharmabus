import models.driver


class Delivery_item:

    def __init__(self, driver, pharmacy, patient, med):
        self.driver = driver
        self.pharmacy = pharmacy
        self.patient = patient
        self.med = med

    def geq(self, delivery_item):
        if self.driver.geq(delivery_item.driver):
            return True
        elif self.pharmacy.geq(delivery_item.pharmacy):
            return True
        elif self.patient.geq(delivery_item.patient):
            return True
        elif self.med.geq(delivery_item.med):
            return True
        else:
            False


def path_step_generator(possible_delivery_set):
    sort(possible_delivery_set, compare
