import sqlite3
from secrets import compare_digest

import flask
from flask import Flask, render_template, session, request, flash, redirect
from flask import g
from flask_simplelogin import SimpleLogin, get_username, login_required, is_logged_in

import settings
from data.dao import DatabaseEntityDoesNotExist
from data.dao import getRegisteredUserById, getOverlord, getPatient, getDoctor, getPharmacy, getDriver,\
    registerPatient, registerDoctor, registerPharmacy, registerDriver, getUserId
from data.dao import getAllDrivers, getAllPharmacies, getAllOrders, getAllOrdersFiltertForUser
from data.dao import checkLogin, getRole
from data.dao import insertOrder, addPrescriptionToOrder, deleteOrder, getOrder
from helper import make_fake_route
from models.address import Address
from models.coordinates import get_default_coordinates, Coordinates
from models.dimensions import get_default_dimensions
from models.driver import Driver
from models.patient import Patient
from models.pharmacy import Pharmacy
from models.doctor import Doctor
from models.role import Role
from models.prescription_status import PrescriptionStatus
from models.order_status import OrderStatus


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            settings.DATABASE_URL,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def check_my_users(user):
    conn = get_db()
    cursor = conn.cursor()
    email = user['username']
    password = user['password']
    print('test')
    success, id = checkLogin(cursor, email, password)
    if success:
        session['simple_user_id'] = id
        return True
    else:
        return False


def is_overlord(username):
    conn = get_db()
    cursor = conn.cursor()
    if not is_logged_in():
        return False
    user_id = getUserId(cursor, username)
    return getRole(cursor, user_id)  == Role.OVERLORD


def is_logged_in_as_overlord(username):
    if is_overlord(username):
        return
    else:
        return "User {} is not an overlord".format(username)


def is_pharmacy(username):
    conn = get_db()
    cursor = conn.cursor()
    if not is_logged_in():
        return False
    try:
        user_id = getUserid(cursor, username)
        return getRole(cursor, user_id)  == Role.PHARMACY
    except DatabaseEntityDoesNotExist:
        return False


def is_logged_in_as_pharmacy(username):
    if is_pharmacy(username):
        return
    else:
        return "User {} is not a Pharmacy".format(username)


def is_driver(username): #valid change
    conn = get_db()
    cursor = conn.cursor()
    if not is_logged_in():
        return False
    try:
        user_id = getUserId(cursor, username)
        return getRole(cursor, user_id)  == Role.DRIVER
    except DatabaseEntityDoesNotExist:
        return False


def is_logged_in_as_driver(username):
    if is_driver(username):
        return
    else:
        return "User {} is not a driver".format(username)


def is_patient(username):
    print(username)
    conn = get_db()
    cursor = conn.cursor()
    if not is_logged_in():
        return False
    try:
        user_id = getUserId(cursor, username)
        return getRole(cursor, user_id) == Role.PATIENT
    except DatabaseEntityDoesNotExist as e:
        print(e)
        return False


def is_logged_in_as_patient(username):
    if is_patient(username):
        return
    else:
        return "User {} is not a patient".format(username)


def is_doctor(username):
    conn = get_db()
    cursor = conn.cursor()
    if not is_logged_in():
        return False
    try:
        user_id = getUserId(cursor, username)
        return getRole(cursor, user_id) == Role.DOCTOR
    except DatabaseEntityDoesNotExist:
        return False


def is_logged_in_as_doctor(username):
    if is_doctor(username):
        return
    else:
        return "User {} is not a doctor".format(username)


def is_logged_in_at_all(username):
    if is_logged_in():
        return
    else:
        return False


app = Flask(__name__)
app.config.from_object('settings')
messages = {
    'login_success': 'Login erfolgreich!',
    'login_failure': 'Ungültiges Passwort oder Account existiert nicht!',
    'is_logged_in': 'Eingeloggt',
    'logout': 'Ausgeloggt!',
    'login_required': 'Login Vorausgesetzt',
    'access_denied': 'Zugriff verweigert',
    'auth_error': 'Authentifizierungsfehler {0}'
}
SimpleLogin(app, messages=messages, login_checker=check_my_users)


@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    username = session.get('simple_username')
    user_id = getUserId(cursor, username)
    if is_patient(username):
        conn = get_db()
        cursor = conn.cursor()
        orders = getAllOrdersFiltertForUser(cursor, Role.PATIENT, user_id)
        return render_template('orders.html', orders=orders)
    elif is_doctor(username):
        conn = get_db()
        cursor = conn.cursor()
        orders = getAllOrdersFiltertForUser(cursor, Role.DOCTOR, user_id)
        return render_template('orders.html', orders=orders)
    elif is_pharmacy(username):
        conn = get_db()
        cursor = conn.cursor()
        orders = getAllOrdersFiltertForUser(cursor, Role.PHARMACY, user_id)
        return render_template('orders.html', orders=orders)
    else:
        return render_template('index.html')


@app.route('/register_pharmacy', methods=['GET', 'POST'])
def register_pharmacy():
    if flask.request.method == 'POST':
        email = flask.request.values.get('email')
        pwd = flask.request.values.get('password')
        surname = flask.request.values.get('vorname_besitzer')
        familyname = flask.request.values.get('nachname_besitzer')
        plz = flask.request.values.get('postleitzahl')
        street = flask.request.values.get('street')
        streetno = flask.request.values.get('number')
        tel = flask.request.values.get('telefonnummer')
        longitude = flask.request.values.get('longitude')
        latitude = flask.request.values.get('latitude')
        name  = flask.request.values.get('name')
        conn = get_db()
        cursor = conn.cursor()
        registerPharmacy(cursor, email, pwd, surname, familyname, plz, street, streetno, tel, longitude, latitude, name)
        conn.commit()
        flash("Registrierung erfolgreich")
        return render_template('index.html')
    else:
        return render_template("register_pharmacy.html")


@app.route('/register_patient', methods=['GET', 'POST'])
def register_patient():
    if flask.request.method == 'POST':
        email = flask.request.values.get('email')
        pwd = flask.request.values.get('password')
        surname = flask.request.values.get('vorname_besitzer')
        familyname = flask.request.values.get('nachname_besitzer')
        plz = flask.request.values.get('postleitzahl')
        street = flask.request.values.get('street')
        streetno = flask.request.values.get('number')
        tel = flask.request.values.get('telefonnummer')
        longitude = flask.request.values.get('longitude')
        latitude = flask.request.values.get('latitude')
        conn = get_db()
        cursor = conn.cursor()
        partient = registerPatient(cursor, email, pwd, surname, familyname, plz, street, streetno, tel, longitude, latitude)
        session['simple_user_id'] = driver.id
        conn.commit()
        flash("Registrierung erfolgreich")
        return render_template('index.html')
    else:
        return render_template("register_patient.html")


@app.route('/register_driver', methods=['GET', 'POST'])
def register_driver():
    if flask.request.method == 'POST':
        email = flask.request.values.get('email')
        pwd = flask.request.values.get('password')
        surname = flask.request.values.get('vorname_besitzer')
        familyname = flask.request.values.get('nachname_besitzer')
        plz = flask.request.values.get('postleitzahl')
        street = flask.request.values.get('street')
        streetno = flask.request.values.get('number')
        tel = flask.request.values.get('telefonnummer')
        longitude = flask.request.values.get('longitude')
        latitude = flask.request.values.get('latitude')
        max_range = flask.request.values.get('max_range')
        conn = get_db()
        cursor = conn.cursor()
        driver = registerDriver(cursor, email, pwd, surname, familyname, plz, street, streetno, tel, longitude, latitude, max_range)
        session['simple_user_id'] = driver.id
        conn.commit()
        flash("Registrierung erfolgreich")
        return render_template('index.html')
    else:
        return render_template("register_driver.html")


@app.route('/register_doctor', methods=['GET', 'POST'])
def register_doctor():
    if flask.request.method == 'POST':
        email = flask.request.values.get('email')
        pwd = flask.request.values.get('password')
        surname = flask.request.values.get('vorname_besitzer')
        familyname = flask.request.values.get('nachname_besitzer')
        plz = flask.request.values.get('postleitzahl')
        street = flask.request.values.get('street')
        streetno = flask.request.values.get('number')
        tel = flask.request.values.get('telefonnummer')
        longitude = flask.request.values.get('longitude')
        latitude = flask.request.values.get('latitude')
        conn = get_db()
        cursor = conn.cursor()
        doctor = registerDoctor(cursor, email, pwd, surname, familyname, plz, street, streetno, tel, longitude, latitude)
        session['simple_user_id'] = doctor.id
        conn.commit()
        flash("Registrierung erfolgreich")
        return render_template('index.html')
    else:
        return render_template("register_driver.html")


@app.route('/order_choose_doctor', methods=['GET', 'POST'])
@login_required(must=[is_logged_in_as_patient])
def order_choose_doctor():
    conn = get_db()
    cursor = conn.cursor()
    if flask.request.method == 'POST':
        doctor_id = flask.request.form.get('doctor')
        try:
            doctor = getDoctor(cursor, doctor_id)
        except DatabaseEntityDoesNotExist:
            flash('Dieser Doktor existiert nicht')
            return render_template('order_choose_doctor.html')
        return render_template('order_choose_pharmacy.html', doctor_id=doctor_id)
    else:
        return render_template("order_choose_doctor.html")


@app.route('/order_choose_pharmacy', methods=['GET', 'POST'])
@login_required(must=[is_logged_in_as_patient])
def order_choose_pharmacy():
    if flask.request.method == 'POST':
        doctor_id = flask.request.form.get('doctor_id')
        try:
            pharmacy_id = flask.request.form.get('pharmacy')
        except DatabaseEntityDoesNotExist:
            flash('Diese Apotheke existiert nicht')
            return render_template('order_choose_pharmacy.html', doctor_id=doctor_id)
        return render_template('order_upload_prescription.html', doctor_id=doctor_id, pharmacy_id=pharmacy_id)
    else:
        return render_template("order_choose_doctor.html")


@app.route('/order_upload_prescription', methods=['GET', 'POST'])
@login_required(must=[is_logged_in_as_patient])
def order_upload_prescription():
    if flask.request.method == "POST":
        doctor_id = flask.request.form.get('doctor_id')
        pharmacy_id = flask.request.form.get('pharmacy_id')
        prescription_location = flask.request.form.get('prescription_location')
        status = PrescriptionStatus.PRESENT_AT_DOCTOR if flask.request.form.get('prescription_location') == "doctor" else PrescriptionStatus.PRESENT_AT_PATIENT
        scan = flask.request.form.get('scan')
        conn = get_db()
        cursor = conn.cursor()
        try:
            doctor = getDoctor(cursor, doctor_id)
            pharmacy = getPharmacy(cursor, pharmacy_id)
            patient = getPatient(cursor, session.get('simple_user_id'))
        except DatabaseEntityDoesNotExist:
            flash('Ups, da ist wohl etwas schief gelaufen. Probiere es doch bitte noch einmal')
            return render_template('order_choose_doctor')
        order = insertOrder(cursor, patient, doctor, pharmacy)
        order = addPrescriptionToOrder(cursor, order, status, scan)
        conn.commit()
        flash('Bestellung erfolgreich eingetragen')
        return render_template('index.html')
    else:
        return render_template('order_choose_doctor.html')


@app.route('/modify_order', methods=['GET','POST'])
@login_required(must=[is_logged_in_at_all])
def modify_order():
    conn = get_db()
    cursor = conn.cursor()
    if flask.request.method == "GET":
        order_id = flask.request.args.get('order_id')
    else:
        order_id = flask.request.form.get("order_id")
    if not order_id:
        raise Exception("Order Id expected for cancellation")
    try:
        order = getOrder(cursor, order_id)
    except DatabaseEntityDoesNotExist:
        flash('Uups da ist wohl etwas schief gelaufen. Probiere es doch bitte noch einmal')
        return render_template('index.html')
    if not order_status_corresponds_to_user_role(order.status):
        flash('Tut uns leid, aber diese Bestellung kann von dir aktuell nicht geändert werden')
        return render_template('index.html')
    if flask.request.method == "POST":
        username = session.get('simple_username')
        if is_user(username):
            pharmacy_id = flask.request.form.get('pharmacy')
            doctor_id = flask.request.form.get('doctor')
            location = flask.request.form.get('prescription_location')
            scan = flask.request.form.get('scan')
            try:
                pharmacy = getPharmacy(cursor, pharmacy_id)
                doctor = getDoctor(cursor, doctor_id)
                status = PrescriptionStatus.PRESENT_AT_DOCTOR if flask.request.form.get('prescription_location') == "doctor" else PrescriptionStatus.PRESENT_AT_PATIENT
            except DatabaseEntityDoesNotExist:
                flash('Uups da ist wohl etwas schief gelaufen. Probiere es doch bitte noch einmal')
                return render_template("modify_order.html", order=order)
        elif is_doctor(username):
            pass
        elif is_pharmacy(username):
            pass
        flash('Änderung erfolgreich übernommen')
        return render_template("index.html")
    if flask.request.method == "GET":
        return render_template("modify_order.html", order=order)


@app.route('/cancel_order', methods=['GET'])
@login_required(must=[is_logged_in_as_patient])
def cancel_order():
    conn = get_db()
    cursor = conn.cursor()
    order_id = flask.request.args.get('order_id')
    if not order_id:
        raise Exception("Order Id expected for cancellation")
    order = getOrder(cursor, order_id)
    patient = getPatient(cursor, session.get('simple_user_id'))
    if patient.id != order.patient.id:
        raise Exception("Only the order owning patient can cancel")
    else:
        deleteOrder(cursor, order)
        conn.commit()
    flash('Bestellung erfolgreich gecancelt')
    return render_template('index.html')


def start_calculation():
    print("MAGIC IS HAPPENING NOW")
    conn = get_db()
    c = conn.cursor()
    drivers = get_all_drivers(c)
    print("I have {} drivers".format(len(drivers)))
    pharmacies = get_all_pharmacies(c)
    print("I have {} pharmacies".format(len(pharmacies)))
    orders = get_all_orders(c)
    print("I have {} orders".format(len(orders)))
    if len(orders) == 0:
        flash("Keine mögliche Lösung")
        return list()
    base_set = generate_delivery_item_base_set(drivers, pharmacies, orders)
    if len(base_set) == 0:
        flash("Keine mögliche Lösung")
        return list()
    reduced_set = delivery_set_reducer(base_set)
    driver_based_delivery_sets = delivery_set_splitter(reduced_set)
    routes = list()
    for delivery_set in driver_based_delivery_sets:
        routes.append(travelling_sales_man(delivery_set))
    return routes

# test
@app.route('/calculate_routes', methods=['GET', 'POST'])
@login_required(must=[is_logged_in_as_overlord])
def calculate_routes():
    if flask.request.method == 'POST':
        conn = get_db()
        c = conn.cursor()
        routes = start_calculation()
        #route = make_fake_route(c)
        #routes = [route, route]
        return render_template('calculated_routes.html', routes=routes)
    else:
        return render_template("calculate_routes.html")


def template_translate_order_status(status):
    if status == OrderStatus.AT_PATIENT:
        return "Patient muss tätig werden"
    elif status == OrderStatus.AT_DOCTOR:
        return "Arzt muss das Rezept hochladen"
    elif status == OrderStatus.AT_PHARMACY:
        return "Apotheke muss die Bestellung bearbeiten"
    elif status == OrderStatus.AT_DRIVER:
        return "Fahrer hat das Medikament abgeholt"
    elif status == OrderStatus.DELIVERED:
        return "Bestellung wurde zugestellt"
    else:
        raise Exception("unsuppored order status enum value {}".format(status))


def order_status_corresponds_to_user_role(status):
    username = session.get('simple_username')
    if status == OrderStatus.AT_PATIENT:
        print('is patient {}'.format(is_patient(username)))
        return is_patient(username)
    elif status == OrderStatus.AT_DOCTOR:
        return is_doctor(username)
    elif status == OrderStatus.AT_PHARMACY:
        return is_pharmacy(username)
    elif status == OrderStatus.AT_DRIVER:
        return is_driver(username)
    elif status == OrderStatus.DELIVERED:
        return is_patient(username)
    else:
        raise Exception("unsuppored order status enum value {}".format(status))

app.add_template_global(is_logged_in_as_pharmacy)
app.add_template_global(is_logged_in_as_driver)
app.add_template_global(is_logged_in_as_patient)
app.add_template_global(is_logged_in_as_overlord)
app.add_template_global(is_pharmacy)
app.add_template_global(is_driver)
app.add_template_global(is_patient)
app.add_template_global(is_overlord)
app.add_template_global(template_translate_order_status)
app.add_template_global(order_status_corresponds_to_user_role)

app.teardown_appcontext(close_db)
if __name__ == '__main__':
    app.run(port=5000, use_reloader=True, debug=True)
