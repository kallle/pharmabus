from werkzeug.security import check_password_hash, generate_password_hash

from models.role import Role, InvalidRoleException


def get_role(cursor, username):
    cursor.execute('Select driver_id, pharmacy_id, patient_id from Users where username = ?', (username,))
    driver_id, pharmacy_id, patient_id = cursor.fetchone()
    if driver_id:
        return Role.DRIVER
    if patient_id:
        return Role.PATIENT
    if pharmacy_id:
        return Role.PHARMACY
    raise InvalidRoleException('User {:1!l} has an invalid role!'.format(username))


def check_login(cursor, username, password):
    cursor.execute('Select pwd from Users where username = ?', (username,))
    pwhash = cursor.fetchone()
    if not pwhash:
        return False
    return check_password_hash(pwhash[0], password)


def register_user(cursor, username, password, driver_id=None, patient_id=None, pharmacy_id=None):
    salted = generate_password_hash(password)
    cursor.execute('INSERT INTO Users(username, pwd, driver_id, patient_id, pharmacy_id) Values (?,?,?,?,?)', (username, salted, driver_id, patient_id, pharmacy_id))
    return cursor.lastrowid


def register_driver(cursor, driver):
    coors = driver.coordinates
    addr = driver.address
    cooler = driver.cooler_dimensions
    storage = driver.storage_dimensions
    qry = (
        'INSERT INTO drivers('
        'name, range, addr_plz, addr_street, addr_street_nr, koo_lat, koo_long, '
        'cooler_dim_x, cooler_dim_y, cooler_dim_z, storage_dim_x, storage_dim_y, storage_dim_z) '
        'Values (?,?,?,?,?,?,?,?,?,?,?,?,?)'
    )
    cursor.execute(qry, (driver.name, driver.range, addr.postal_code, addr.street, addr.number,
                         coors.latitude, coors.longitude,
                         cooler.width, cooler.height, cooler.depth,
                         storage.width, storage.height, storage.depth))
    driver_id = cursor.lastrowid
    return driver_id


def register_patient(cursor, patient):
    coors = patient.coordinates
    addr = patient.address
    qry = (
        'INSERT INTO patients('
        'name, addr_plz, addr_street, addr_street_nr, koo_lat, koo_long) '
        'Values (?,?,?,?,?,?)'
    )
    cursor.execute(qry, (patient.name, addr.postal_code, addr.street, addr.number,
                         coors.latitude, coors.longitude))
    patient_id = cursor.lastrowid
    return patient_id


def register_pharmacy(cursor, pharmacy):
    coors = pharmacy.coordinates
    addr = pharmacy.address
    qry = (
        'INSERT INTO pharmacies('
        'name, addr_plz, addr_street, addr_street_nr, koo_lat, koo_long) '
        'Values (?,?,?,?,?,?)'
    )
    cursor.execute(qry, (pharmacy.name, addr.postal_code, addr.street, addr.number,
                         coors.latitude, coors.longitude))
    pharmacy_id = cursor.lastrowid
    return pharmacy_id