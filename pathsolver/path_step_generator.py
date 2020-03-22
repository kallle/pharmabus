import models.driver


class Delivery_item:

    def __init__(self, driver, pharmacy, patient, med, amount):
        self.driver = driver
        self.pharmacy = pharmacy
        self.patient = patient
        self.med = med
        self.amount = amount

    def geq(self, delivery_item):
        if self.driver.geq(delivery_item.driver):
            return True
        elif self.pharmacy.geq(delivery_item.pharmacy):
            return True
        elif self.patient.geq(delivery_item.patient):
            return True
        elif self.med.geq(delivery_item.med):
            return True
        elif self.amount >= delivery_item.amount:
            return True
        else:
            return False

    def __str__(self):
        return "{}/{}/{}/{}".format(self.driver.name, self.pharmacy.name, self.patient.name,self.med.name)


# calculate distances based on bird distance calculation provided
# by coordinate
def distance(a, b):
    return a.coordinates.bird_distance(b.coordinates)


class Driver_pharmacy_element:

    def __init__(self, driver, pharmacy):
        self.driver = driver
        self.pharmacy = pharmacy

# this is horribly inefficient as O(|drivers| x |pharmacies|)
# is potentially hughe and the set can be precomputed!
def generate_possible_driver_pharmacy_set(drivers, pharmacies):
    res = list()
    for driver in drivers:
        for pharmacy in pharmacies:
            dis = distance(driver, pharmacy)
            if  dis < driver.range:
                res.append(Driver_pharmacy_element(driver, pharmacy))
            else:
                print("driver {} does not like the distance to {} of {}".format(driver.name, pharmacy.name, dis))
    return res


class Single_order:
    def __init__(self, patient, medication, amount):
        self.patient = patient
        self.medication = medication
        self.amount = amount


def translate_db_orders_to_single_order(orders):
    ret = list()
    for order in orders:
        for med in order.medications:
            ret.append(Single_order(order.patient, med[0], med[1]))
    return ret


class Driver_order_element:

    def __init__(self, driver, patient, medication, amount):
        self.driver = driver
        self.patient = patient
        self.medication = medication
        self.amount = amount


def generate_possible_driver_order_set(drivers, orders):
    orders = translate_db_orders_to_single_order(orders)
    res = list()
    for driver in drivers:
        for order in orders:
            if distance(driver, order.patient) < driver.range:
                res.append(Driver_order_element(driver, order.patient, order.medication, order.amount))
    return res


def generate_delivery_item_base_set(drivers, pharmacies, orders):
    res = list()
    driver_pharmacy_set = generate_possible_driver_pharmacy_set(drivers, pharmacies)
    print("I have a {} size driver pharmacy set".format(len(driver_pharmacy_set)))
    driver_order_set = generate_possible_driver_order_set(drivers, orders)
    print("I have a {} size driver order set".format(len(driver_order_set)))
    for doelement in driver_order_set:
        for dpelement in driver_pharmacy_set:
            if doelement.medication in dpelement.pharmacy.stock.stock.keys():
                res.append(Delivery_item(doelement.driver, dpelement.pharmacy, doelement.patient, doelement.medication, doelement.amount))
            else:
                print("{} has {} not in stock".format(dpelement.pharmacy.name, doelement.medication.name))
                print("stock is {}".format(dpelement.pharmacy.stock.stock.keys()))
    return res


def sort(list, geq):
    n = len(list)
    for x in range(n):
        for y in range(0,n-x-1):
            if geq(list[y], list[y+1]):
                list[y], list[y+1] = list[y+1], list[y]


def remove(lst, probe):
    deleted = list()
    pop_list = list()
    removed = True
    while removed == True:
        removed = False
        for i in range(len(lst)):
            if probe(lst[i]):
                deleted.append(lst[i])
                lst.pop(i)
                removed = True
                break


    for i in range(len(lst)):
        if probe(lst[i]):
            pop_list.append(i)
    for elem in pop_list:
        deleted.append(lst.pop(elem))
    return deleted


def filter(lst, probe, key=lambda a: a):
    ret = list()
    for elem in lst:
        if probe(elem):
            ret.append(key(elem))
    return ret


def print_delivery_set(delivery_set):
    for elem in delivery_set:
        print(elem)


def delivery_set_reducer(possible_delivery_set):
    assert len(possible_delivery_set) > 0
    sort(possible_delivery_set, lambda a,b : a.geq(b))
    assert len(possible_delivery_set) > 0
    print_delivery_set(possible_delivery_set)
    drives = list()
    while len(possible_delivery_set) > 0:
        current = possible_delivery_set[0]
        drives.append(current)
        remove(possible_delivery_set, lambda b : current.patient == b.patient and current.med == b.med)
        remaining = current.pharmacy.reduce_stock(current.med, 1)
        if remaining == 0:
            print("pharmacy {} is empty of {}".format(current.pharmacy.name, current.med.name))
            remove(possible_delivery_set, lambda a,b : a.pharmacy == b.pharmacy)
    return drives


# we are assuming a sorted and reduced set
# after calling delivery_set_reducer
def delivery_set_splitter(possible_delivery_set):
    assert len(possible_delivery_set) > 0
    driver_sets = dict()
    for drive in possible_delivery_set:
        if drive.driver in driver_sets.keys():
            driver_sets[drive.driver].append(drive)
        else:
            driver_sets[drive.driver] = list([drive])
    return [value for value in driver_sets.values()]


def generate_pharmacy_count_table(driver_delivery_set):
    pharmacy_count = dict()
    for elem in driver_delivery_set:
        if elem.pharmacy in pharmacy_count:
            pharmacy_count[elem.pharmacy] += 1
        else:
            pharmacy_count[elem.pharmacy] = 1
    return pharmacy_count


def find_closest_next_step(start_step, possible_next_steps):
    closest_element = possible_next_steps[0]
    closest_distance = start_step.coordinates.distance(possible_next_steps[0].coordinates)
    for step in possible_next_steps[1:]:
        if start_step.coordinates.distance(step.coordinates) < closest_distance:
            closest_distance = start_step.coordinates.distance(step.coordinates)
            closest_element = step
    return closest_element


def travelling_sales_man(driver_delivery_set):
    drive_order = list()
    pharmacy_count = generate_pharmacy_count_table(driver_delivery_set)
    sort(driver_delivery_set, lambda a,b : pharmacy_count[a.pharmacy] >= pharmacy_count[b.pharmacy])
    start_pharmacy = driver_delivery_set[0].pharmacy
    drive_order.append(start_pharmacy)
    rem_steps = filter(driver_delivery_set, lambda elem: elem.pharmacy == start_pharmacy, lambda elem: elem.patient)
    rem_pharmacies = list(dict.fromkeys(filter(driver_delivery_set, lambda elem: elem.pharmacy != start_pharmacy, lambda elem: elem.pharmacy)))
    rem_steps += rem_pharmacies
    while len(rem_steps) > 0:
        closest = find_closest_next_step(drive_order[-1], rem_steps)
        drive_order.append(closest)
        remove(rem_steps, lambda elem: elem == closest)
        if closest.__class__.__name__ == 'Pharmacy':
            rem_steps += filter(driver_delivery_set, lambda elem: elem.pharamcy == closest, lambda elem: elem.patient)
    return drive_order
