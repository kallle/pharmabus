import codecs
import csv

from models.dimensions import Dimensions
from models.medication import Medication


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
        med = Medication(pzn, name, dimensions, requires_cooling, quantity, ingredients, requires_recipe)
        amount = row[9]
        stock.append((med, amount))
    return stock

class InvalidOrderException(Exception):
    pass