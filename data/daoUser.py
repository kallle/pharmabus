from models.DatabaseEntityDoesNotExist import DatabaseEntityDoesNotExist
from werkzeug.security import check_password_hash, generate_password_hash
from models.role import Role, InvalidRoleException
from models.address import Address
from models.driver import Driver
from models.order import Order
from models.patient import Patient
from models.pharmacy import Pharmacy
from models.doctor import Doctor


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
    if doctor is None:
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
        return False, -1
    return check_password_hash(pwhash[0], password), pwhash[1]


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



def getAllActiveDrivers(cursor):
    query = """SELECT user_id
               FROM drivers
               WHERE current_route IS NULL"""
    cursor.execute(query)
    drivers = list()
    for driver in cursor.fetchall():
        drivers.append(getDriver(cursor, driver[0]))
    return drivers
