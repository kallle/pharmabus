from models.route import Route
from models.delivery_step import DeliveryStep
from models.delivery_step_type import DeliveryStepType
from data.dao import getDriver

def updateDriverRoute(cursor, driver, route_id):
    driver = getDriver(cursor, driver.id)
    if driver.route is not None:
        raise Exception('driver {} is not available'.format(driver))
    query = """UPDATE drivers
               SET current_route = ?
               WHERE user_id = ?"""
    cusor.execute(query, (route_id, driver.id,))
    return getDriver(cursor, driver.id)


def insertRouteStop(cursor, stop_nr, route_id, stop):
    query = """INSERT INTO Stops (step_no, belongs_to, part_of, stop_type)
               VALUES(?,?,?,?)"""
    cursor.execute(query, (stop_nr,
                           stop.order.id,
                           route_id,
                           DeliveryStepType.toString(stop.action)))


def insertNewRoute(cursor, route):
    query = """INSERT INTO Routes ()
               VALUES ()
               RETURNING id"""
    id = cursor.lastrowid
    counter = 0
    for stop in route.stops:
        insertRouteStop(cursor, counter, id, stop)
        counter += 1
    return route
