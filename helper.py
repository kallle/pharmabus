import codecs
import csv

from data.dao import get_driver_by_id, get_pharmacy_by_id, get_patient_by_id, get_medication_by_name_supplier, get_med
from models.address import Address
from models.coordinates import get_default_coordinates
from models.dimensions import Dimensions, get_default_dimensions
from models.driver import Driver
from models.medication import Medication
from models.pharmacy import Pharmacy
from models.post import Post
from models.route import Route
from models.stop import Stop


def process_uploaded_csv_file(stream):
    data = []
    stream = codecs.iterdecode(stream, 'utf-8')
    for row in csv.reader(stream, dialect=csv.excel):
        if row:
            data.append(row)
    return data


def read_stock(data):
    stock = []
    for row in data:
        pzn = row[0]
        name = row[1]
        ingredients = row[2]
        quantity = row[3]
        width = row[4]
        height = row[5]
        depth = row[6]
        requires_cooling = row[7]
        requires_recipe = row[8]
        dimensions = Dimensions(width, height, depth)
        supplier = row[9]
        med = Medication(pzn, name, supplier, dimensions, requires_cooling, quantity, ingredients, requires_recipe)

        amount = row[10]
        stock.append((med, amount))
    return stock


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['csv']


def make_fake_route(cursor):
    driver1 = get_driver_by_id(cursor, 3)
    apo1 = get_pharmacy_by_id(cursor, 1)
    apo2 = get_pharmacy_by_id(cursor, 2)
    pat1 = get_patient_by_id(cursor, 1)
    pat2 = get_patient_by_id(cursor, 2)
    pat3 = get_patient_by_id(cursor, 3)
    med1 = get_med("ACC 200 Brausetabletten", "Hexal", cursor)
    med2 = get_med("Tamiflu 45 mg", "Roche Pharma", cursor)
    med3 = get_med("ACC 200 Brausetabletten", "Hexal", cursor)
    stops1 = []
    stops1.append(Stop("Start", driver1, None))
    pickup1 = [Post(med1, 4), Post(med2, 3)]
    stops1.append(Stop("Einladen", apo1, pickup1))
    drop1 = [Post(med1, 2), Post(med2, 1)]
    stops1.append(Stop("Ausliefern", pat1, drop1))
    pickup2 = [Post(med3, 3)]
    stops1.append(Stop("Einladen", apo2, pickup2))
    drop2 = [Post(med3, 3), Post(med2, 1)]
    stops1.append(Stop("Ausliefern", pat2, drop2))
    drop3 = [Post(med1, 2), Post(med2, 1)]
    stops1.append(Stop("Ausliefern", pat3, drop3))
    return Route(driver1, stops1)
