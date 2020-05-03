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
from models.stock import Stock



# Retrieves the role of the user identified by username
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


# Checks whether the username and password combination identifies a known user
def check_login(cursor, username, password):
    cursor.execute('Select pwd from Users where username = ?', (username,))
    pwhash = cursor.fetchone()
    if not pwhash:
        return False
    return check_password_hash(pwhash[0], password)


# Generic user registration function.
# We just create a login here, the information regarding pharmacy/driver/patient has to be created before
# and passed in as one of the ids
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


# Retrieves the id for a medication, identified by product name and supplier name
def get_medication_by_name_supplier(product_name, supplier, cursor):
    qry = ('SELECT id '
           'FROM meds '
           'WHERE product_name = ? AND '
           '      supplier = ?')
    cursor.execute(qry, (product_name, supplier))
    med_id = cursor.fetchone()
    if not med_id:
        raise Exception("Medication does not exist!")
    else:
        return med_id[0]


# Adds a medication to the database
def insert_medication(pzn, product_name, ingredient, supplier, quantity, x, y, z, cooling_p, recipe_p, cursor):
    qry = ('SELECT id '
           'FROM meds '
           'WHERE pzn = ?')
    cursor.execute(qry, (pzn,))
    med_id = cursor.fetchone()
    if med_id:
        return med_id[0]
    qry = ('INSERT INTO meds('
           'pzn, product_name, ingredient, supplier, quantity, dimension_x, dimension_y, dimension_z, requires_cooling, requires_recipe) '
           'VALUES (?,?,?,?,?,?,?,?,?,?)')
    cursor.execute(qry, (pzn, product_name, ingredient, supplier, quantity, x, y, z, cooling_p, recipe_p))
    return cursor.lastrowid

# Adds a single stock entry for a pharmacy
def insert_stock(pharmacy_id, amount, pzn, product_name, ingredient, supplier, quantity, x, y, z, cooling_p, recipe_p, cursor):
    med_id = insert_medication(pzn, product_name, ingredient, supplier, quantity, x, y, z, cooling_p, recipe_p, cursor)
    qry = ('INSERT INTO pharmacy_stores('
           'pharmacy_id,med_id,amount) '
           'VALUES (?,?,?) '
           'ON CONFLICT(pharmacy_id,med_id) DO UPDATE SET amount = excluded.amount')
    cursor.execute(qry, (pharmacy_id, med_id, amount))


# Clears the current stock of a pharmacy
def clear_stock(cursor, pharmacy_id):
    qry = 'DELETE FROM pharmacy_stores where pharmacy_id = ?'
    cursor.execute(qry, (pharmacy_id,))


# Refreshes the stock of a pharmacy
def process_stock(cursor, pharmacy_id, stock):
    #clear_stock(cursor, pharmacy_id)
    for (med, amount) in stock:
        dim = med.dimensions
        insert_stock(pharmacy_id, amount,
                     med.pzn, med.name, med.ingredients, med.supplier, med.quantity,
                     dim.width, dim.height, dim.depth,
                     med.requires_cooling, med.requires_recipe,
                     cursor)


# Stores an order in the database
def insert_order(cursor, patient_id, meds, recipe_p):
    qry = ('INSERT INTO orders('
           'status, given_by) '
           'VALUES (\'pending\',?)')
    cursor.execute(qry, (patient_id,))
    order_id = cursor.lastrowid
    for med in meds:
        handelsname, hersteller, amount = med
        med_id = get_medication_by_name_supplier(handelsname, hersteller, cursor)
        if med_id == None:
            raise InvalidOrderException("The medication does not exist")
        else:
            insert_order_item(cursor, order_id, med_id, amount, recipe_p)


# Adds a single item belonging to a order consisting of several items
def insert_order_item(cursor, order_id, med_id, amount, recipe_p):
    qry = ('INSERT INTO order_contains('
           'order_id, med_id, amount, recipe_with_customer) '
           'VALUES(?,?,?,?)')
    cursor.execute(qry, (order_id, med_id, amount, 1 if recipe_p else 0))


# Checks that the user is a pharmacy and returns their pharmacy id.
def get_pharmacy_id(cursor, username):
    cursor.execute('Select pharmacy_id from Users where username = ?', (username,))
    (pharmacy_id,) = cursor.fetchone()
    if pharmacy_id:
        return pharmacy_id
    else:
        raise InvalidRoleException('{:1!l} is missing his pharmacy id'.format(username))


# Checks that the user is a patient and returns their patient id.
def get_patient_id(cursor, username):
    cursor.execute('Select patient_id from Users where username = ?', (username,))
    (patient_id,) = cursor.fetchone()
    if patient_id:
        return patient_id
    else:
        raise InvalidRoleException('{:1!l} is missing his patient id'.format(username))


# Checks that the user is a driver and returns their driver id.
def get_driver_id(cursor, username):
    cursor.execute('Select driver_id from Users where username = ?', (username,))
    (driver_id,) = cursor.fetchone()
    if driver_id:
        return driver_id
    else:
        raise InvalidRoleException('{:1!l} is missing his driver id'.format(username))


# Retrieves all drivers known to the system
def get_all_drivers(cursor):
    qry = ('SELECT id, name, range, addr_plz, addr_street, addr_street_nr, koo_lat, koo_long, '
           'cooler_dim_x, cooler_dim_y, cooler_dim_z, storage_dim_x, storage_dim_y, storage_dim_z '
           'FROM drivers')
    drivers = []
    cursor.execute(qry)
    for d in cursor.fetchall():
        (id, name, range, addr_plz, addr_street, addr_street_nr, koo_lat, koo_long,
         cooler_dim_x, cooler_dim_y, cooler_dim_z, storage_dim_x, storage_dim_y, storage_dim_z) = d
        cooler_dim = Dimensions(cooler_dim_x, cooler_dim_y, cooler_dim_z)
        storage_dim = Dimensions(storage_dim_x, storage_dim_y, storage_dim_z)
        addr = Address(addr_plz, addr_street, addr_street_nr)
        coors = Coordinates(koo_lat, koo_long)
        drivers.append(Driver(id, name, range, addr, coors, cooler_dim, storage_dim))
    return drivers


# Retrieves the stock of a single pharmacy, identified by pharmacy_id
def get_stock_for_pharmacy(cursor, pharmacy_id):
    qry = ('SELECT med_id, amount '
           'FROM pharmacy_stores '
           'WHERE pharmacy_id = ?')
    stock = []
    cursor.execute(qry, (pharmacy_id,))
    for s in cursor.fetchall():
        (med_id, amount) = s
        med = get_medication_by_id(cursor, med_id)
        stock.append((med, amount))
    return Stock(stock)


# Retrieves all pharmacies known to the system with their current stock
def get_all_pharmacies(cursor):
    qry = ('SELECT id, name, addr_plz, addr_street, addr_street_nr, koo_lat, koo_long '
           'FROM pharmacies')
    pharmacies = []
    cursor.execute(qry)
    for p in cursor.fetchall():
        (id, name, addr_plz, addr_street, addr_street_nr, koo_lat, koo_long) = p
        addr = Address(addr_plz, addr_street, addr_street_nr)
        coors = Coordinates(koo_lat, koo_long)
        stock = get_stock_for_pharmacy(cursor, id)
        pharmacies.append(Pharmacy(id, name, addr, coors, stock))
    return pharmacies


# Retrieves all medication belonging to a order identified by order_id
def get_meds_for_order(cursor, order_id):
    qry = ('SELECT med_id, amount '
           'FROM order_contains '
           'where order_id = ?')
    medications = []
    cursor.execute(qry, (order_id,))
    for p in cursor.fetchall():
        (med_id, amount) = p
        med = get_medication_by_id(cursor, med_id)
        medications.append((med, amount))
    return medications


# Retrieves all orders known to the system
# Can be filtered for specific patients by passing in an id as for_patient
def get_all_orders(cursor, for_patient=None):
    qry = ('SELECT id, given_by, status from orders')
    orders = []
    cursor.execute(qry)
    for o in cursor.fetchall():
        (order_id, pat_id, status) = o
        patient = get_patient_by_id(cursor, pat_id)
        medications = get_meds_for_order(cursor, order_id)
        order = Order(order_id, patient, medications, status)
        if for_patient and pat_id != for_patient:
            pass
        else:
            orders.append(order)
    return orders


class PatientNotFoundException(Exception):
    pass


class PharmacyNotFoundException(Exception):
    pass


class DriverNotFoundException(Exception):
    pass


class MedicationNotFoundException(Exception):
    pass


# Retrieves all information of a pharmacy, identified by its id
def get_pharmacy_by_id(cursor, pharmacy_id):
    qry = ('SELECT  name, addr_plz, addr_street, addr_street_nr, koo_lat, koo_long '
           'FROM pharmacies '
           'where id = ?')
    cursor.execute(qry, (pharmacy_id,))
    pharmacy = cursor.fetchone()
    if not pharmacy:
        raise PharmacyNotFoundException('Patient with id {:1!r} not found'.format(pharmacy_id))
    (name, addr_plz, addr_street, addr_street_nr, koo_lat, koo_long) = pharmacy
    addr = Address(addr_plz, addr_street, addr_street_nr)
    coors = Coordinates(koo_lat, koo_long)
    return Pharmacy(pharmacy_id, name, addr, coors, None)


# Retrieves all information of a patient, identified by their id
def get_patient_by_id(cursor, patient_id):
    qry = ('SELECT  name, addr_plz, addr_street, addr_street_nr, koo_lat, koo_long '
           'FROM patients '
           'where id = ?')
    cursor.execute(qry, (patient_id,))
    patient = cursor.fetchone()
    if not patient:
        raise PatientNotFoundException('Patient with id {:1!r} not found'.format(patient_id))
    (name, addr_plz, addr_street, addr_street_nr, koo_lat, koo_long) = patient
    addr = Address(addr_plz, addr_street, addr_street_nr)
    coors = Coordinates(koo_lat, koo_long)
    return Patient(patient_id, name, addr, coors)


# Retrieves all information of a driver, identified by their id
def get_driver_by_id(cursor, driver_id):
    qry = ('SELECT name, range, addr_plz, addr_street, addr_street_nr, koo_lat, koo_long, '
           'cooler_dim_x, cooler_dim_y, cooler_dim_z, storage_dim_x, storage_dim_y, storage_dim_z '
           'FROM drivers '
           'where id = ?')
    cursor.execute(qry, (driver_id,))
    driver = cursor.fetchone()
    if not driver:
        raise DriverNotFoundException('Driver with id {:1!r} not found'.format(driver_id))
    (name, range, addr_plz, addr_street, addr_street_nr, koo_lat, koo_long,
     cooler_dim_x, cooler_dim_y, cooler_dim_z, storage_dim_x, storage_dim_y, storage_dim_z) = driver
    cooler_dim = Dimensions(cooler_dim_x, cooler_dim_y, cooler_dim_z)
    storage_dim = Dimensions(storage_dim_x, storage_dim_y, storage_dim_z)
    addr = Address(addr_plz, addr_street, addr_street_nr)
    coors = Coordinates(koo_lat, koo_long)
    return Driver(driver_id, name, range, addr, coors, cooler_dim, storage_dim)


# Retrieves all information of a medication, identified by its id
def get_medication_by_id(cursor, med_id):
    qry = ('SELECT pzn, product_name, ingredient, supplier, quantity, '
           'dimension_x, dimension_y, dimension_z, requires_cooling, requires_recipe '
           'from meds where id = ?')

    cursor.execute(qry, (med_id,))
    med = cursor.fetchone()
    if not med:
        raise MedicationNotFoundException('Medication with id {:1!r} not found'.format(med_id))
    (pzn, name, ingredients, supplier, quantity,
     dimension_x, dimension_y, dimension_z, requires_cooling, requires_recipe) = med
    dimensions = Dimensions(dimension_x, dimension_y, dimension_z)
    return Medication(pzn, name, supplier, dimensions, requires_cooling, quantity, ingredients, requires_recipe)


# Retrieves all information of a patient, identified by its product name and supplier name
def get_med(product_name, supplier, cursor):
    med_id = get_medication_by_name_supplier(product_name, supplier, cursor)
    return get_medication_by_id(cursor, med_id)

