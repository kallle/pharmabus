import sqlite3
from secrets import compare_digest

import flask
from flask import Flask, render_template, session, request, flash, redirect
from flask import g
from flask_simplelogin import SimpleLogin, get_username, login_required, is_logged_in

import settings
from data.dao import getRegisteredUserById, getOverlord, getPatient, getDoctor, getPharmacy, getDriver,\
    registerPatient, registerDoctor, registerPharmacy, registerDriver
from data.dao import getAllDrivers, getAllPharmacies, getAllOrders
from data.dao import checkLogin, getRole
from data.dao import insertOrder, addPrescriptionToOrder
from helper import make_fake_route
from models.address import Address
from models.coordinates import get_default_coordinates, Coordinates
from models.dimensions import get_default_dimensions
from models.driver import Driver
from models.patient import Patient
from models.pharmacy import Pharmacy
from models.doctor import Doctor
from models.role import Role


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


def is_logged_in_as_overlord():
    conn = get_db()
    cursor = conn.cursor()
    if not is_logged_in():
        return False
    user_id = session.get('simple_user_id')
    return getRole(cursor, user_id)  == Role.OVERLORD


def is_logged_in_as_pharmacy():
    conn = get_db()
    cursor = conn.cursor()
    if not is_logged_in():
        return False
    user_id = session.get('simple_user_id')
    return getRole(cursor, user_id)  == Role.PHARMACY


def is_logged_in_as_driver():
    conn = get_db()
    cursor = conn.cursor()
    if not is_logged_in():
        return False
    user_id = session.get('simple_user_id')
    return getRole(cursor, user_id)  == Role.DRIVER


def is_logged_in_as_patient():
    conn = get_db()
    cursor = conn.cursor()
    if not is_logged_in():
        return False
    user_id = session.get('simple_user_id')
    print(user_id)
    return getRole(cursor, user_id)  == Role.PATIENT


def is_logged_in_as_doctor():
    conn = get_db()
    cursor = conn.cursor()
    if not is_logged_in():
        return False
    user_id = session.get('simple_user_id')
    return getRole(cursor, user_id)  == Role.DOCTOR


app = Flask(__name__)
app.config.from_object('settings')
messages = {
    'login_success': 'Login erfolgreich!',
    'login_failure': 'Ungültiges Passwort oder Account existiert nicht!',
    'is_logged_in': 'Eingeloggt',
    'logout': 'Ausgeloggt!',
    'login_required': 'Login Vorausgesetzt',
    'access_denied': 'Zugriff verweigert',
    'auth_error': 'Authentifizierungsfehler： {0}'
}
SimpleLogin(app, messages=messages, login_checker=check_my_users)


@app.route('/')
def index():
    user_id = session.get('simple_user_id')
    if is_logged_in_as_patient():
        conn = get_db()
        cursor = conn.cursor()
        orders = getAllOrdersFiltertForUser(cursor, Role.PATIENT, user_id)
        return render_template('orders.html', orders=orders)
    elif is_logged_in_as_doctor():
        conn = get_db()
        cursor = conn.cursor()
        orders = getAllOrdersFiltertForUser(cursor, Role.DOCTOR, user_id)
        return render_template('orders.html', orders=orders)
    elif is_logged_in_as_doctor():
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


def not_empty(item):
    return item != ''

@app.route('/submit_order', methods=['GET', 'POST'])
@login_required(must=[is_logged_in_as_patient])
def submit_order():
    if flask.request.method == 'POST':
        handelsname = flask.request.form.getlist('handelsname')
        hersteller = flask.request.form.getlist('hersteller')
        amount = flask.request.form.getlist('amount')
        handelsname = filter(not_empty, handelsname)
        hersteller = filter(not_empty, hersteller)
        amount = filter(not_empty, amount)
        order = list(zip(handelsname, hersteller, amount))
        recipe_p = flask.request.values.get('rezept')
        conn = get_db()
        c = conn.cursor()
        patient_id = get_patient_id(c, get_username())
        insert_order(c, patient_id, order, recipe_p)
        conn.commit()
        flash('Bestellung erfolgreich übermittelt')
        return render_template('index.html')
    else:
        return render_template("submit_order.html")


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


app.add_template_global(is_logged_in_as_pharmacy)
app.add_template_global(is_logged_in_as_driver)
app.add_template_global(is_logged_in_as_patient)
app.add_template_global(is_logged_in_as_overlord)
app.teardown_appcontext(close_db)
if __name__ == '__main__':
    app.run(port=5000, use_reloader=True, debug=True)
