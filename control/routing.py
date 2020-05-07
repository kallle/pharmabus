from control.app import app
import flask
from flask_simplelogin import login_required
from data.database_handler import get_db
from data.dao import getAllDrivers, getAllPharmacies, getAllOrdersByStatus, getAllActiveDrivers
from models.order_status import OrderStatus
from data.routeHandling import insertNewRoute
from control.login_checks import is_logged_in_as_overlord
from pathsolver.path_step_generator import generatePossibleDriverPharmacySet, generatePossibleDriverOrderSet, calculateDriverSetsIntersection, deliverySetSplitter, travellingSalesMan
from models.route import Route

@app.route('/routing/calculate_route', methods=['POST','GET'])
@login_required(must=[is_logged_in_as_overlord])
def calculateRoutes():
    performRouteCalculationAndAssignment()
    flask.flash('success')
    return flask.render_template('index.html')


def performRouteCalculationAndAssignment():
    conn = get_db()
    cursor = conn.cursor()
    drivers = getAllActiveDrivers(cursor)
    pharmacies = getAllPharmacies(cursor)
    orders = getAllOrdersByStatus(cursor, OrderStatus.AT_PHARMACY_CONFIRMED)
    driverPharmacyTuples = generatePossibleDriverPharmacySet(drivers, pharmacies)
    driverOrderTuples = generatePossibleDriverOrderSet(drivers, orders)
    intersec = calculateDriverSetsIntersection(driverPharmacyTuples, driverOrderTuples)
    driverSets = deliverySetSplitter(intersec)
    driverSets.sort(key=len)
    for driverSet in driverSets:
        if len(driverSet) > 0:
            route = Route(travellingSalesMan(driverSet[0].driver, driverSet))
            insertNewRoute(cursor, route)
