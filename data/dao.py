from werkzeug.security import check_password_hash, generate_password_hash

from models.address import Address
from models.coordinates import Coordinates
from models.dimensions import Dimensions
from models.driver import Driver
from models.medication import Medication
from models.order import Order
from models.patient import Patient
from models.pharmacy import Pharmacy
from models.role import Role, InvalidRoleException
from models.order_status import OrderStatus
from models.stock import Stock


class DatabaseEntityDoesNotExist():

    def __init__(self, entity_type, reference_id):
        self._entity_type = entity_type
        self._reference_id = reference_id

    @property
    def entity_type(self):
        return self._entity_type

    @property
    def reference_id(self):
        return self._reference_id


def getUserId(cursor, email):
    query = """SELECT id
               FROM users
               WHERE email = ?"""
    cursor.execute(query, (email,))
    ret = cursor.fetchone()
    if ret is None:
        raise DatabaseEntityDoesNotExist("User", email)
    else:
        return ret[0]


def getOverlord(cursor, row_id):
    query = """SELECT id,
                      email,
                      surname,
                      familyname,
                      plz,
                      street,
                      streetno,
                      tel,
                      longitude,
                      latitude
                FROM Overlords AS O JOIN Users AS U ON O.user_id = U.id
                WHERE id = ?"""
    cursor.execute(query,(row_id,))
    overlord = cursor.fetchone()
    if overlord is None:
        raise DatabaseEntityDoesNotExist("Overlord", row_id)
    else:
        return Overlord(overlord[0],
                        overlord[1],
                        overlord[2],
                        overlord[3],
                        overlord[4],
                        overlord[5],
                        overlord[6],
                        overlord[7],
                        overlord[8],
                        overlord[9])


def getPatient(cursor, row_id):
    query = """SELECT id,
                      email,
                      surname,
                      familyname,
                      plz,
                      street,
                      streetno,
                      tel,
                      longitude,
                      latitude
                FROM Patients AS P JOIN Users AS U ON P.user_id = U.id
                WHERE id = ?"""
    cursor.execute(query,(row_id,))
    patient = cursor.fetchone()
    if patient is None:
        raise DatabaseEntityDoesNotExist("Patient", row_id)
    else:
        return Patient(patient[0],
                       patient[1],
                       patient[2],
                       patient[3],
                       patient[4],
                       patient[5],
                       patient[6],
                       patient[7],
                       patient[8],
                       patient[9])


def getDoctor(cursor, row_id):
    query = """SELECT id,
                      email,
                      surname,
                      familyname,
                      plz,
                      street,
                      streetno,
                      tel,
                      longitude,
                      latitude
                FROM Doctors AS D JOIN Users AS U ON D.user_id = U.id
                WHERE id = ?"""
    cursor.execute(query,(row_id,))
    doctor = cursor.fetchone()
    if patient is None:
        raise DatabaseEntityDoesNotExist("Doctor", row_id)
    else:
        return Doctor(doctor[0],
                      doctor[1],
                      doctor[2],
                      doctor[3],
                      doctor[4],
                      doctor[5],
                      doctor[6],
                      doctor[7],
                      doctor[8],
                      doctor[9])


def getPharmacy(cursor, row_id):
    query = """SELECT id,
                      email,
                      surname,
                      familyname,
                      plz,
                      street,
                      streetno,
                      tel,
                      longitude,
                      latitude,
                      name
                FROM Pharmacies AS P JOIN Users AS U ON P.user_id = U.id
                WHERE id = ?"""
    cursor.execute(query,(row_id,))
    pharmacy = cursor.fetchone()
    if pharmacy is None:
        raise DatabaseEntityDoesNotExist("Pharmacy", row_id)
    else:
        return Pharmacy(pharmacy[0],
                        pharmacy[1],
                        pharmacy[2],
                        pharmacy[3],
                        pharmacy[4],
                        pharmacy[5],
                        pharmacy[6],
                        pharmacy[7],
                        pharmacy[8],
                        pharmacy[9],
                        pharmacy[10])


def getRoute(cursor, routeId):
    return Route([])


def getDriver(cursor, row_id):
    query = """SELECT id,
                      email,
                      surname,
                      familyname,
                      plz,
                      street,
                      streetno,
                      tel,
                      longitude,
                      latitude,
                      max_range,
                      current_route
                FROM Drivers AS D JOIN Users AS U ON D.user_id = U.id
                WHERE id = ?"""
    cursor.execute(query,(row_id,))
    driver = cursor.fetchone()
    if driver is None:
        raise DatabaseEntityDoesNotExist("Driver", row_id)
    else:
        return Driver(driver[0],
                      driver[1],
                      driver[2],
                      driver[3],
                      driver[4],
                      driver[5],
                      driver[6],
                      driver[7],
                      driver[8],
                      driver[9],
                      driver[10],
                      getRoute(cursor, driver[11]) if driver[11] is not None else None)


# this is an internal function and should never be used outside of this file!
def registerUser(cursor, email, pwd, surname, familyname, plz, street, streetno, tel, longitude, latitude):
    salted = generate_password_hash(pwd)
    query = """INSERT INTO Users(email,
                                 pwd,
                                 surname,
                                 familyname,
                                 plz,
                                 street,
                                 streetno,
                                 tel,
                                 longitude,
                                 latitude)
               VALUES (?,?,?,?,?,?,?,?,?,?)"""
    cursor.execute(query,(email, salted, surname, familyname, plz, street, streetno, tel, longitude, latitude))
    return cursor.lastrowid


def registerPatient(cursor, email, pwd, surname, familyname, plz, street, streetno, tel, longitude, latitude):
    row_id = registerUser(cursor, email, pwd, surname, familyname, plz, street, streetno, tel, longitude, latitude)
    query = """INSERT INTO Patients (user_id)
               VALUES (?)"""
    cursor.execute(query, (row_id,))
    return getPatient(cursor, row_id)


def registerDoctor(cursor, email, pwd, surname, familyname, plz, street, streetno, tel, longitude, latitude):
    row_id = registerUser(cursor, email, pwd, surname, familyname, plz, street, streetno, tel, longitude, latitude)
    query = """INSERT INTO Doctors (user_id)
               VALUES (?)"""
    cursor.execute(query, (row_id,))
    return getDoctor(cursor, row_id)


def registerPharmacy(cursor, email, pwd, surname, familyname, plz, street, streetno, tel, longitude, latitude, name):
    row_id = registerUser(cursor, email, pwd, surname, familyname, plz, street, streetno, tel, longitude, latitude)
    query = """INSERT INTO Pharmacies(user_id,
                                      name)
               VALUES (?,?)"""
    cursor.execute(query, (row_id, name))
    return getPharmacy(cursor, row_id)


def registerDriver(cursor, email, pwd, surname, familyname, plz, street, streetno, tel, longitude, latitude, max_range):
    row_id = registerUser(cursor, email, pwd, surname, familyname, plz, street, streetno, tel, longitude, latitude)
    query = """INSERT INTO Drivers(user_id,
                                   max_range)
               VALUES (?,?)"""
    cursor.execute(query, (row_id, max_range))
    return getDriver(cursor, row_id)


def translateRoleToString(role, plural=True):
    assert role in [Role.PATIENT, Role.PHARMACY, Role.DOCTOR, Role.OVERLORD, Role.DRIVER]
    if role == Role.PHARMACY:
        if plural:
            role = "Pharmacies"
        else:
            role = "Pharmacy"
    elif role == Role.DOCTOR:
        role = "Doctor"
        if plural:
            role += "s"
    elif role == Role.PATIENT:
        role = "Patient"
        if plural:
            role += "s"
    elif role == Role.DRIVER:
        role = "Driver"
        if plural:
            role += "s"
    elif role == Role.OVERLORD:
        role = "Overlord"
        if plural:
            role += "s"
    else:
        raise Exception("WTF")
    return role

def checkIfRole(cursor, role, id):
    role = translateRoleToString(role, plural=True)
    query = "SELECT True FROM {} WHERE user_id = ?".format(role)
    cursor.execute(query, (id,))
    res = cursor.fetchone()
    ret = False if res == None else True
    return ret


def getRegisteredUserById(cursor, id):
    role = getRole(cursor, id)
    if role == Role.PATIENT:
        return getPatient(cursor, id)
    elif role == Role.PHARMACY:
        return getPharmacy(cursor, id)
    elif role == Role.DOCTOR:
        return getDoctor(cursor, id)
    elif role == Role.DRIVER:
        return getDriver(cursor, id)
    elif role == Role.OVERLORD:
        return getOverlord(cursor, id)
    else:
        raise Exception("WTF?")


def getRole(cursor, id):
    if id is None:
        return Role.NONE
    elif checkIfRole(cursor, Role.PATIENT, id):
        return Role.PATIENT
    elif checkIfRole(cursor, Role.DOCTOR, id):
        return Role.DOCTOR
    elif checkIfRole(cursor, Role.PHARMACY, id):
        return Role.PHARMACY
    elif checkIfRole(cursor, Role.DRIVER, id):
        return Role.DRIVER
    elif checkIfRole(cursor, Role.OVERLORD, id):
        return Role.OVERLORD
    else:
        raise InvalidRoleException('User {} has an invalid role!'.format(id))


# Checks whether the username and password combination identifies a known user
def checkLogin(cursor, email, password):
    cursor.execute("""SELECT pwd, id
                      FROM users
                      WHERE email = ?""", (email,))
    pwhash = cursor.fetchone()
    if not pwhash:
        return False
    return check_password_hash(pwhash[0], password), pwhash[1]


def getOrder(cursor, row_id):
    query = """SELECT id,
                      status,
                      prescription,
                      patient,
                      doctor,
                      pharmacy
               FROM Orders
               WHERE id = ?"""
    cursor.execute(query,(row_id,))
    ret = cursor.fetchone()
    if ret is None:
        raise DatabaseEntityDoesNotExist("Order", row_id)
    id,status,prescription,patient,doctor,pharmacy = ret
    return Order(id,
                 OrderStatus.get(status),
                 getPrescription(cursor, prescription) if prescription else None,
                 patient,
                 doctor,
                 pharmacy)


def insertOrder(cursor, patient, doctor, pharmacy, prescription=None):
    query = """INSERT INTO Orders(status, patient, doctor, pharamcy, prescription)
               VALUES (?)"""
    cursor.execute(query,(OrderStatus.AT_PATIENT,))
    rowId = cursor.lastrowid
    return getOrder(cursor, row_id)


# this function must never be used outside of this file
def getPrescription(cursor, rowId):
    query = """SELECT id,
                      status,
                      scan
               FROM Prescriptions
               WHERE row_id = ?"""
    cursor.execute(query,(rowId,))
    prescription = cursor.fetchone()
    if prescription is None:
        DatabaseEntityDoesNotExist("Prescription", rowId)
    else:
        return Prescription(prescription[0],
                            prescription[1],
                            prescription[2])


# this function must never be used outside of this file
def insertPrescription(cursor, status, scan):
    query = """INSERT INTO Prescriptions(status, scan)
               VALUES(?,?)"""
    cursor.execute(query, (status, scan))
    rowId = cursor.lastrowid
    return getPrescription(cursor, rowId)


# this function must never be used outside of this file
def deletePrescription(cursor, id):
    cursor.execute("""DELETE FROM Prescriptions
                      WHERE id = ?""",(id,))


class OrderAlreadyHasPrescription(Exception):
    pass


# this function must never be used outside of this file
def updateOrderStatus(cursor, order, order_status):
    query = """UPDATE Orders
               SET status = ?
               WHERE id = ?"""
    cursor.execute(query,(order_status, order_id))
    order._status = order_status
    return order


def addPrescriptionToOrder(cursor, order, status, scan=None, supersede=False):
    assert status in [PrescriptionStatus.PRESENT_AT_DOCTOR, PrescriptionStatus.PRESENT_AT_PATIENT]
    if order.prescription is not None and not supersede:
        raise OrderAlreadyHasPrescription()
    else:
        deletePrescription(cusor, order.prescription.id)
    prescription = insertPrescription(cursor, status, scan)
    query = """UPDATE Orders
               SET prescription = ?
               WHERE id = ?"""
    if scan: # if we have the scan the order is now the pharmacies job
        order = updateOrderStatus(cursor, OrderStatus.AT_PHARMACY)
    elif status == PrescriptionStatus.PRESENT_AT_DOCTOR:
        # if the prescription is at the doctor it is the doctors job to upload
        order = updateOrderStatus(cursor, OrderStatus.AT_DOCTOR)
    else: # if the prescription is at the patient it is the patients job to upload
        order = updateOrderStatus(cursor, OrderStatus.AT_PATIENT)
    cursor.execute(query,(prescription.id, oder.id))
    order._prescription = prescription
    return order


# Retrieves all drivers known to the system
def getAllDrivers(cursor):
    query = """SELECT user_id FROM Drivers"""
    cursor.execute(query)
    drivers = list()
    for driver_id in cursor.fetchall():
        drivers.append(getDriver(cursor, driver_id[0]))
    return drivers


def getAllPharmacies(cursor):
    query = "SELECT user_id FROM Pharmacies"
    cursor.execute(query)
    pharmacies = list()
    for pharmacy_id in cursor.fetchall():
        pharmacies.append(getPharmacy(cursor, pharmacy_id[0]))
    return pharmacies


def getAllOrders(cursor):
    query = "SELECT id FROM orders"
    cursor.execute(query)
    orders = list()
    for order_id in cursor.fetchall():
        orders.append(getOrder(cursor, order_id[0]))
    return orders


def getAllOrdersFiltertForUser(cursor, userRole, userId):
    query = """SELECT id
               FROM orders
               WHERE {} = ?""".format(translateRoleToString(userRole, plural=False))
    cursor.execute(query, (userId,))
    orders = list()
    for order_id in cursor.fetchall():
        orders.append(getOrder(cursor, order_id[0]))
    return orders
