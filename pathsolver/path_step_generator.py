from models.route import Route
from models.delivery_step import DeliveryStep


# calculate distances based on bird distance calculation provided
# by coordinate
def distance(a, b):
    return a.coordinates.bird_distance(b.coordinates)


class DriverPharmacyElement:

    def __init__(self, driver, pharmacy):
        self.driver = driver
        self.pharmacy = pharmacy

# this is horribly inefficient as O(|drivers| x |pharmacies|)
# is potentially hughe and the set can be precomputed!
def generatePossibleDriverPharmacySet(drivers, pharmacies):
    res = list()
    for driver in drivers:
        for pharmacy in pharmacies:
            dis = distance(driver, pharmacy)
            if  dis < driver.range:
                res.append(DriverPharmacyElement(driver, pharmacy))
            else:
                print("driver {} does not like the distance to {} of {}".format(driver.name, pharmacy.name, dis))
    return res


class DriverOrderElement:

    def __init__(self, driver, order):
        self.driver = driver
        self.order = order
        self.requiresPrescriptionPickup = (order.prescription.status == PrescriptionStatus.AT_DOCTOR)


def generatePossibleDriverOrderSet(drivers, orders):
    res = list()
    for driver in drivers:
        for order in orders:
            if order.prescription.status == PrescriptionStatus.AT_PATIENT:
                if distance(driver, order.patient) < driver.range:
                    res.append(DriverOrderElement(driver, order))
            elif order.prescription.status == PrescriptionStatus.AT_DOCTOR:
                if distance(driver, order.patient) < driver.range and distance (driver, order.doctor) < driver.range:
                    res.append(DriverOrderElement(driver, order))
    return res


def remove(lst, probe, rem=list(), deleted=list()):
    if len(lst) == 0:
        return builder
    elif probe(lst[0]):
        deleted.append(lst[0])
        rem, deleted = remove(lst[1:], probe, rem, deleted)
        return rem, deleted
    else:
        rem.append(lst[0])
        rem, deleted = remove(lst[1:], probe, rem, deleted)
        return rem, deleted


class DeliveryActions(enum):

    PICK_UP_PRESCRIPTION = 0
    PICK_UP_MED = 1
    DROP_OFF_MED = 2


class PossibleDeliveryStep(DeliveryStep):

    def __init__(self, driver, destination, action, order, prerequisites=list()):
        super().__init__(driver, destination, action, order)
        self.prerequisites = prerequisites
        self.isDependedOnBy = None
        self.isScheduled = False

    def geq(self, other):
        return distance(self.driver, self.destination) >= distance(other.driver, other.destination)

    def deleteDependency(self, dependency):
        rem, deleted = remove(self.prerequisites, lambda a: a = dependency)
        self.prerequisites = rem

    def hasUnresolvedDependencies(self):
        return len(self.prerequisistes) == 0

    def __repr__(self):
        return 'Driver {} -> Destination {} (Order {})'.format(self.driver.id,
                                                               self.destination.id,
                                                               self.order.id)


def calculateDriverSetsIntersection(driverPharmacySet, driverOrderSet):
    ret = list()
    for driverPharmacy in driverPharmacySet:
        for driverOrder in driverOrderSet:
            if driverPharmacy.driver == driverOrder.driver:
                dependency = list()
                pharmacyPickup = PossibleDeliveryStep(driverOrder.driver,
                                                      driverOrder.order.pharmacy,
                                                      DeliveryAction.PICK_UP_MED
                                                      driverOrder.order)
                ret.append(pharmacyPickup)
                dependency.append(pharmacyPickup)
                doctorPickup = None
                if driverOrder.requiresPrescriptionPickup:
                    doctorPickup = PossibleDeliveryStep(driverOrder.driver,
                                                        driverOrder.order.doctor,
                                                        DeliveryAction.PICK_UP_PRESCRIPTION,
                                                        driverOrder.order)
                    ret.append(doctorPickup)
                    dependency.append(doctorPickup)
                patientDropOff = PossibleDeliveryStep(driverOrder.driver,
                                                      driverOrder.order.patient,
                                                      DeliveryAction.DROP_OFF_MED,
                                                      driverOrder.order,
                                                      prerequisites=dependency)
                pharmacyPickup.isDependedOnBy = patientDropOff
                if doctorPickup is not None:
                    doctorPickup.isDependedOnBy = patientDropOff
    return ret


def sort(list, geq):
    n = len(list)
    for x in range(n):
        for y in range(0,n-x-1):
            if geq(list[y], list[y+1]):
                list[y], list[y+1] = list[y+1], list[y]


def filter(lst, probe, key=lambda a: a):
    ret = list()
    for elem in lst:
        if probe(elem):
            ret.append(key(elem))
    return ret


def printDeliverySet(delivery_set):
    for elem in delivery_set:
        print(elem)


# O(n)
def deliverySetSplitter(possibleDeliverySet):
    assert len(possible_delivery_set) > 0
    driverSets = dict()
    for drive in possibleDeliverySet:
        if drive.driver in driverSets.keys():
            driverSets[drive.driver].append(drive)
        else:
            driverSets[drive.driver] = list([drive])
    return [value for value in driver_sets.values()]


# O(n)
def generatePharmacyCountTable(driverDeliverySet):
    pharmacyCount = dict()
    for elem in driverDeliverySet:
        if elem.pharmacy in pharmacyCount:
            pharmacy_count[elem.order.pharmacy] += 1
        else:
            pharmacy_count[elem.order.pharmacy] = 1
    return pharmacy_count


# O(n)
def findClosestNextStep(location, possibleNextSteps):
    closestElement = possibleNextSteps[0]
    closestDistance = distance(location, closestElement.destination)
    for step in possibleNextSteps[1:]:
        curDistance = distance(location, step.destination)
        if cur < closestDistance:
            closestDistance = curDistance
            closest_element = step
    return closestElement


def travellingSalesMan(driver, driverDeliverySet):
    theDrive = list()
    driverDeliverySet = remove(driverDeliverSet, lambda a : not a.isScheduled)
    possibleSteps, dependingSteps = remove(driverDeliverySet, lambda a : a.hasUnresolvedDependency())
    current = findClosestNextStep(driver, possibleSteps)
    theDrive.append(current)
    possibleSteps.remove(current)
    while len(possibleSteps) > 0:
        depending = current.isDependedOnBy
        if depending is not None:
            depending.deleteDependency(current)
            if not depending.hasUnresolvedDependencies():
                possibleSteps.append(depending)
        current = findClosestNextStep(current.destination, possibleSteps)
        current.isScheduled=True
        possibleSteps.remove(current)
        theDrive.append(current)
    return theDrive
