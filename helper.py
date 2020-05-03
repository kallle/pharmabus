import codecs
import csv

from models.dimensions import Dimensions
from models.medication import Medication
from models.route import Route
from models.stop import Stop


# Reads a uploaded csv file and makes a list from it
def process_uploaded_csv_file(stream):
    data = []
    stream = codecs.iterdecode(stream, 'utf-8')
    for row in csv.reader(stream, dialect=csv.excel):
        if row:
            data.append(row)
    return data


# Parse a stock rows from a csv list
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


# Allowed file types one can upload
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['csv']


# Generates a static route to test the rendering
def make_fake_route(cursor):
    return Route([])
    # driver1 = get_driver_by_id(cursor, 3)
    # apo1 = get_pharmacy_by_id(cursor, 1)
    # apo2 = get_pharmacy_by_id(cursor, 2)
    # pat1 = get_patient_by_id(cursor, 1)
    # pat2 = get_patient_by_id(cursor, 2)
    # pat3 = get_patient_by_id(cursor, 3)
    # med1 = get_med("ACC 200 Brausetabletten", "Hexal", cursor)
    # med2 = get_med("Tamiflu 45 mg", "Roche Pharma", cursor)
    # med3 = get_med("ACC 200 Brausetabletten", "Hexal", cursor)
    # stops1 = []
    # stops1.append(Stop("Start", driver1, None))
    # pickup1 = [Post(med1, 4), Post(med2, 3)]
    # stops1.append(Stop("Einladen", apo1, pickup1))
    # drop1 = [Post(med1, 2), Post(med2, 1)]
    # stops1.append(Stop("Ausliefern", pat1, drop1))
    # pickup2 = [Post(med3, 3)]
    # stops1.append(Stop("Einladen", apo2, pickup2))
    # drop2 = [Post(med3, 3), Post(med2, 1)]
    # stops1.append(Stop("Ausliefern", pat2, drop2))
    # drop3 = [Post(med1, 2), Post(med2, 1)]
    # stops1.append(Stop("Ausliefern", pat3, drop3))
    # return Route(driver1, stops1)
