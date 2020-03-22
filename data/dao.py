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


def get_medication_by_name_supplier(product_name, supplier, cursor):
    qry = ('SELECT id '
           'FROM meds '
           'WHERE product_name = ? AND '
           '      supplier = ?')
    cursor.execute(qry, (product_name, supplier))
    med_id = cursor.fetchone()
    return med_id


def get_patient_id_by_username(username, cursor):
    qry = ('SELECT patient_id '
           'FROM Users '
           'WHERE username = ?')
    cursor.execute(qry, (username))
    driver_id = cursor.fetchone()
    return driver_id


def insert_medication(pzn, product_name, ingredient, supplier, quantity, x, y, z, cooling_p, recipe_p, cursor):
    qry = ('SELECT id
            FROM meds
            WHERE pzn = ?')
    cursor.execute(qry, (pzn))
    med_id = cursor.fetchone()
    if med_id:
        return med_id
    qry = ('INSERT INTO meds('
           'pzn, product_name, ingredient, supplier, quantity, dimension_x, dimension_y, dimension_z, requires_cooling, requires_recipe) '
           'VALUES (?,?,?,?,?,?,?,?,?,?)')
    cursor.execute(qry, (product_name, ingredient, supplier, quantity, x, y, z, cooling_p, recipe_p))
    return cursor.lastrowid


def insert_stock(pharmacy_id, amount, pzn, product_name, ingredient, supplier, quantity, x, y, z, cooling_p, recipe_p, cursor):
    med_id = insert_medication(pzn, product_name, ingredient, supplier, quantity, x, y, z, cooling_p, recipe_p, cursor)
    qry = ('INSERT INTO pharmacy_stores('
           'pharmacy_id,med_id,amount) '
           'VALUES (?,?,?) '
           'ON DUPLICATE KEY UPDATE')
    cursor.execute(qry, (pharmacy_id, med_id, amount))


def insert_order(patient_id, med_id, amount, recipe_p, cursor):
    qry = ('INSERT INTO orders('
           'status, given_by) '
           'VALUES (\'pending\',?)')
    cursor.execute(qry, (patient))
    order_id = cursor.lastrowid
    qry = ('INSERT INTO order_contains('
           'order_id, med_id, amount, recipe_with_customer) '
           'VALUES(?,?,?,?)')
    cursor.execute(qry, (order_id, med_id, amount, 1 if recipe_p else 0))


def get_pharmacy_id(cursor, username):
    cursor.execute('Select pharmacy_id from Users where username = ?', (username,))
    (pharmacy_id,) = cursor.fetchone()
    if pharmacy_id:
        return pharmacy_id
    else:
        raise InvalidRoleException('{:1!l} is missing his pharmacy id'.format(username))


def get_patient_id(cursor, username):
    cursor.execute('Select patient_id from Users where username = ?', (username,))
    (patient_id,) = cursor.fetchone()
    if patient_id:
        return patient_id
    else:
        raise InvalidRoleException('{:1!l} is missing his patient id'.format(username))


def get_driver_id(cursor, username):
    cursor.execute('Select driver_id from Users where username = ?', (username,))
    (driver_id,) = cursor.fetchone()
    if driver_id:
        return driver_id
    else:
        raise InvalidRoleException('{:1!l} is missing his driver id'.format(username))
