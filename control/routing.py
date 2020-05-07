from control.app import app
import flask
from flask_simplelogin import login_required
from data.database_handler import get_db
from data.dao import getAllDrivers, getAllPharmacies, getAllOrdersByStatus
from models.order_status import OrderStatus
from data.routeHandling import insertNewRoute


@app.route('/routing/calculate_route', method=['POST','GET'])
@login_required(must=[is_logged_in_as_overlord])
def calculateRoute():
    performRouteCalculationAndAssignment()
    flash('success')
    return flask.render_template('index.html')


def performRouteCalculationAndAssignment():
    conn = get_db()
    cursor = conn.cursor()
    drivers = getAllActiveDrivers(cursor)
    orders = getAllOrdersByStatus(cursor, OrderStatus.AT_PHARMACY_CONFIRMED)
    driverPharmacyTuples = generatePossibleDriverPharmacySet(drivers, pharmacies)
    driveOrderTuples = generatePossibleDriveOrderSet(drivers, orders)
    intersec = calculateDriverSetsIntersection(driverPharmacyTuples, driverOrderTuples)
    driverSets = delierySetSplitter(intersec)
    driverSets.sort(key=len)
    for driverSet in driverSets:
        route = Route(travellingSalesMan(driverSet[0].driver, driverSet))
        insertNewRoute(cursor, route)
