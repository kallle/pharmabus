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


def sort(list, geq):
    n = len(list)
    for x in range(n):
        for y in range(0,n-x-1):
            if geq(list[y], list[y+1]):
                list[y], list[y+1] = list[y+1], list[y]


def remove(list, probe):
    deleted = list()
    pop_list = list()
    for i in range(len(list)):
        if probe(list[i]):
            pop_list.append(i)
    for elem in pop_list:
        deleted.append(list.pop(elem))
    return deleted


def filter(list, probe, key=lambda a: a):
    ret = list()
    for elem in list:
        if probe(elem):
            ret.append(key(elem))
    return ret


def delivery_set_reducer(possible_delivery_set):
    sort(possible_delivery_set, lambda a,b : a.geq(b))
    drives = list()
    while len(possible_delivery_set) > 0:
        current = possible_delivery_set[0]
        drives.append(current)
        remove(possible_delivery_set, lambda b : current.patient == b.patient and current.med == b.med)
        remaining = current.pharmacy.reduce_stock(current.med, 1)
        if remaining == 0:
            remove(possible_delivery_set, lambda a,b : a.pharmacy == b.pharmacy)
    return drives


# we are assuming a sorted and reduced set
# after calling delivery_set_reducer
def delivery_set_splitter(possible_delivery_set):
    driver_sets = list()
    driver_sets.append(list([possible_delivery_set[0]]))
    possible_delivery_set = possible_delivery_set[1:]
    for drive in possible_delivery_set:
        if drive.driver == driver_sets[-1][-1]:
            driver_sets[-1].append(driver)
        else:
            driver_sets.append(list([driver]))


def generate_pharmacy_count_table(driver_delivery_set):
    pharmacy_count = dict()
    for elem in driver_delivery_set:
        if elem.pharmacy in pharmacy_count:
            pharmacy_count[elem.pharmacy] += 1
        else:
            pharmacy_count[elem.pharmacy] = 1
    return pharmacy_count


def find_closest_next_step(start_step, possible_next_steps):
    closest = possible_next_steps[0]
    for step in possible_next_steps[1:]:
        if start_step.distance(step) < closest:
            closest = step
    return closest


def distance(a, b):
    return a.coordinates().bird_distance(b.coordinates())


def travelling_sales_man(driver_delivery_set):
    drive_order = list()
    pharmacy_count = generate_pharmacy_count_table(driver_delivery_set)
    sort(driver_delivery_set, lambda a,b : pharmacy_count[a.pharmacy] >= pharmacy_count[b.pharmacy])
    start_pharmacy = driver_delivery_set[0].pharmacy
    drive_order.append(start_pharmacy)
    rem_steps = filter(driver_delivery_set, lambda elem: elem.pharamcy == start_pharmacy, lambda elem: elem.patient)
    rem_pharmacies = list(dict.fromkeys(filter(driver_delivery_set, lambda elem: elem.pharmacy != start_pharmacy, lambda elem: elem.pharmacy)))
    rem_steps += rem_pharmacies
    while len(rem_steps) > 0:
        closest = find_closest_next_step(drive_order[-1], rem_steps)
        drive_order.append(closest)
        remove(rem_steps, lambda elem: elem == closest)
        if closest.__class__.__name__ = 'Pharmacy':
            rem_steps += filter(driver_delivery_set, lambda elem: elem.pharamcy == closest, lambda elem: elem.patient)
