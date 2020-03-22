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
            return False

    def __str__(self):
        return "{}/{}/{}/{}".format(self.driver, self.pharmacy, self.patient,self.med)


# calculate distances based on bird distance calculation provided
# by coordinate
def distance(a, b):
    return a.coordinates.bird_distance(b.coordinates)


# this is horribly inefficient as O(|drivers| x |pharmacies|)
# is potentially hughe and the set can be precomputed!
def generate_possible_driver_pharmacy_set(drivers, pharmacies):
    res = list()
    for driver in drivers:
        for pharmacy in pharmacies:
            dis = distance(driver, pharmacy)
            if  dis < driver.range:
                res.append([driver, pharmacy])
            else:
                print("driver {} does not like the distance to {} of {}".format(driver.name, pharmacy.name, dis))
    return res


class Single_order:
    def __init__(self, patient, medication):
        self.patient = patient
        self.medication = medication


def translate_db_orders_to_single_order(orders):
    ret = list()
    for order in orders:
        for med in order.medications:
            ret.append(Single_order(order.patient, med))
    return ret


def generate_possible_driver_order_set(drivers, orders):
    orders = translate_db_orders_to_single_order(orders)
    res = list()
    for driver in drivers:
        for order in orders:
            if distance(driver, order.patient) < driver.range:
                res.append([driver, order.patient, order.medication])
    return res


def generate_delivery_item_base_set(drivers, pharmacies, orders):
    res = list()
    driver_pharmacy_set = generate_possible_driver_pharmacy_set(drivers, pharmacies)
    print(driver_pharmacy_set)
    driver_order_set = generate_possible_driver_order_set(drivers, orders)
    print(driver_order_set)
    for doelement in driver_order_set:
        for dpelement in driver_pharmacy_set:
            if doelement[2] in dpelement[1].stock:
                res.append(Delivery_item(doelement[0], doelement[1], doelement[2], doelement[3]))
    return res


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
    print(possible_delivery_set)
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
        if closest.__class__.__name__ == 'Pharmacy':
            rem_steps += filter(driver_delivery_set, lambda elem: elem.pharamcy == closest, lambda elem: elem.patient)
    return drive_order
