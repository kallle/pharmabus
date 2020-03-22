import codecs
import csv

from models.address import Address
from models.coordinates import get_default_coordinates
from models.dimensions import Dimensions, get_default_dimensions
from models.driver import Driver
from models.medication import Medication
from models.pharmacy import Pharmacy
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


class InvalidOrderException(Exception):
    pass

def make_fake_route():
    dim = get_default_dimensions()
    coors = get_default_coordinates()
    driver1 = Driver(None, "Ray Gillette", 50, Address(38100, "Jasperallee", 12), coors, dim, dim)
    apo1 = Pharmacy()
    stops1 = []
    stops1.append(Stop(""))