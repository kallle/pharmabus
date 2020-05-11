from models.order_status import OrderStatus
from moels.order import Order
import os
from models.DatabaseEntityDoesNotExist import DatabaseEntityDoesNotExist
from models.prescription_status import PrescriptionStatus
from models.prescription import Prescription

def getOrder(cursor, row_id):
    query = """SELECT id,
                      status,
                      prescription,
                      patient,
                      doctor,
                      pharmacy
               FROM Orders
               WHERE id = ?"""
    cursor.execute(query,(row_id,))
    ret = cursor.fetchone()
    if ret is None:
        raise DatabaseEntityDoesNotExist("Order", row_id)
    id, status, prescription, patient, doctor, pharmacy = ret
    return Order(id,
                 OrderStatus.fromString(status),
                 getPrescription(cursor, prescription) if prescription else None,
                 getPatient(cursor, patient),
                 getDoctor(cursor, doctor),
                 getPharmacy(cursor, pharmacy))


def insertOrder(cursor, patient, doctor, pharmacy, prescription=None):
    query = """INSERT INTO Orders(status, patient, doctor, pharmacy)
               VALUES (?,?,?,?)"""
    cursor.execute(query,(OrderStatus.toString(OrderStatus.AT_PATIENT), patient.id, doctor.id, pharmacy.id))
    rowId = cursor.lastrowid
    return getOrder(cursor, rowId)


def deleteOrder(cursor, order):
    if order.prescription is not None:
        deletePrescription(cursor, order.prescription)
    print('deleting order {}'.format(order))
    query = """DELETE FROM Orders
               WHERE id = ?"""
    cursor.execute(query,(order.id,))


def updateOrder(cursor, order, pharmacy_id=None, doctor_id=None):
    query = """UPDATE Orders
               SET pharmacy = ?,
                   doctor = ?
               WHERE id = ?"""
    cursor.execute(query,(order.pharmacy.id if pharmacy_id is None else pharmacy_id,
                          order.doctor.id if doctor_id is None else doctor_id,
                          order.id))
    return order


# this function must never be used outside of this file
def getPrescription(cursor, rowId):
    query = """SELECT id,
                      status,
                      scan
               FROM Prescriptions
               WHERE id = ?"""
    cursor.execute(query,(rowId,))
    prescription = cursor.fetchone()
    if prescription is None:
        DatabaseEntityDoesNotExist("Prescription", rowId)
    else:
        return Prescription(prescription[0],
                            PrescriptionStatus.fromString(prescription[1]),
                            prescription[2])


# this function must never be used outside of this file
def insertPrescription(cursor, status, scan):
    query = """INSERT INTO Prescriptions(status, scan)
               VALUES(?,?)"""
    cursor.execute(query, (PrescriptionStatus.toString(status), scan))
    rowId = cursor.lastrowid
    return getPrescription(cursor, rowId)


def deletePrescription(cursor, prescription):
    if prescription.scan is not None:
        prescription_file = os.path.join(app.instance_path, app.config['UPLOAD_FOLDER'], order.prescription.scan)
        if os.path.exists(prescription_file):
            os.remove(prescription_file)
    query = """DELETE FROM Prescriptions
               WHERE id = ?"""
    print('pres: {}'.format(prescription))
    cursor.execute(query, (prescription.id,))


class OrderAlreadyHasPrescription(Exception):
    pass


def updateOrderStatus(cursor, order, order_status):
    query = """UPDATE Orders
               SET status = ?
               WHERE id = ?"""
    cursor.execute(query,(OrderStatus.toString(order_status), order.id))
    order._status = order_status
    return order


def addPrescriptionToOrder(cursor, order, status, scan=None, supersede=False):
    assert status in [PrescriptionStatus.PRESENT_AT_DOCTOR, PrescriptionStatus.PRESENT_AT_PATIENT]
    print(order)
    prescription = order.prescription
    if (prescription is not None):
        if not supersede:
            raise OrderAlreadyHasPrescription()
        else:
            deletePrescription(cursor, prescription)
    prescription = insertPrescription(cursor, status, scan)
    query = """UPDATE Orders
               SET prescription = ?
               WHERE id = ?"""
    if scan: # if we have the scan the order is now the pharmacies job
        order = updateOrderStatus(cursor, order, OrderStatus.AT_PHARMACY)
    elif status == PrescriptionStatus.PRESENT_AT_DOCTOR:
        # if the prescription is at the doctor it is the doctors job to upload
        order = updateOrderStatus(cursor, order, OrderStatus.AT_DOCTOR)
    else: # if the prescription is at the patient it is the patients job to upload
        order = updateOrderStatus(cursor, order, OrderStatus.AT_PATIENT)
    cursor.execute(query,(prescription.id, order.id))
    order._prescription = prescription
    return order


def getAllOrders(cursor):
    query = "SELECT id FROM orders"
    cursor.execute(query)
    orders = list()
    for order_id in cursor.fetchall():
        orders.append(getOrder(cursor, order_id[0]))
    return orders


def getAllOrdersFiltertForUser(cursor, userRole, userId):
    query = """SELECT id
               FROM orders
               WHERE {} = ?""".format(translateRoleToString(userRole, plural=False))
    cursor.execute(query, (userId,))
    orders = list()
    for order_id in cursor.fetchall():
        orders.append(getOrder(cursor, order_id[0]))
    return orders


def getAllOrdersByStatus(cursor, status):
    query = """SELECT id
               FROM orders
               WHERE status = ?"""
    cursor.execute(query, (OrderStatus.toString(status),))
    orders = list()
    for order_id in cursor.fetchall():
        orders.append(getOrder(cursor, order_id[0]))
    return orders
