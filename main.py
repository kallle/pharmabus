import sqlite3
from secrets import compare_digest

import flask
from flask import Flask, render_template, session, request, flash, redirect
from flask import g
from flask.views import MethodView
from flask_simplelogin import SimpleLogin, get_username, login_required, is_logged_in

import settings
from data import dao
from data.dao import insert_order, get_pharmacy_id, \
    process_stock, get_patient_id, get_all_drivers, get_all_pharmacies
from helper import process_uploaded_csv_file, read_stock, allowed_file, make_fake_route
from models.address import Address
from models.coordinates import get_default_coordinates
from models.dimensions import get_default_dimensions
from models.driver import Driver
from models.patient import Patient
from models.pharmacy import Pharmacy
from models.role import Role
from pathsolver.path_step_generator import delivery_set_splitter, delivery_set_reducer, generate_delivery_item_base_set, \
    travelling_sales_man


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
    c = conn.cursor()
    username = user['username']
    password = user['password']
    if username == settings.OVERLORD_NAME and compare_digest(password, settings.OVERLORD_PWD):
        return True
    success = dao.check_login(c, username, password)
    return success


def compare_role(username, role):
    if username == settings.OVERLORD_NAME:
        return Role.OVERLORD
    conn = get_db()
    c = conn.cursor()
    r = dao.get_role(c, username)
    return r == role


def is_overlord(username):
    if username == settings.OVERLORD_NAME:
        return
    else:
        return 'User {:1!l} is not the boss!'.format(username)


def is_patient(username):
    if compare_role(username, Role.PATIENT):
        return
    else:
        return 'User {:1!l} is not a patient!'.format(username)


def is_driver(username):
    if compare_role(username, Role.DRIVER):
        return
    else:
        return 'User {:1!l} is not a driver!'.format(username)


def is_pharmacy(username):
    if compare_role(username, Role.PHARMACY):
        return
    else:
        return 'User {:1!l} is not a pharmacy!'.format(username)


def is_logged_in_as_overlord():
    if not is_logged_in():
        return False
    username = session.get('simple_username')
    return username == settings.OVERLORD_NAME


def is_logged_in_as_pharmacy():
    if not is_logged_in():
        return False
    if is_logged_in_as_overlord():
        return False
    username = session.get('simple_username')
    return compare_role(username, Role.PHARMACY)


def is_logged_in_as_driver():
    if not is_logged_in():
        return False
    if is_logged_in_as_overlord():
        return False
    username = session.get('simple_username')
    return compare_role(username, Role.DRIVER)


def is_logged_in_as_patient():
    if not is_logged_in():
        return False
    if is_logged_in_as_overlord():
        return False
    username = session.get('simple_username')
    return compare_role(username, Role.PATIENT)


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
    return render_template('index.html')


@app.route('/secret')
@login_required(username=['chuck', 'mary'])
def secret():
    return render_template('secret.html')


@app.route('/register_pharmacy', methods=['GET', 'POST'])
def register_pharmacy():
    if flask.request.method == 'POST':
        name = flask.request.values.get('name')
        postal_code = flask.request.values.get('plz')
        street = flask.request.values.get('street')
        number = flask.request.values.get('number')
        addr = Address(postal_code, street, number)
        coor = get_default_coordinates()

        pharmacy = Pharmacy(None, name, addr, coor, None)
        conn = get_db()
        c = conn.cursor()
        pharmacy_id = dao.register_pharmacy(c, pharmacy)
        username = flask.request.values.get('username')
        password = flask.request.values.get('password')
        dao.register_user(c, username, password, pharmacy_id=pharmacy_id)
        conn.commit()
        flash("Registrierung erfolgreich")
        return render_template('index.html')
    else:
        return render_template("register_pharmacy.html")


@app.route('/register_patient', methods=['GET', 'POST'])
def register_patient():
    if flask.request.method == 'POST':
        name = flask.request.values.get('name')
        postal_code = flask.request.values.get('plz')
        street = flask.request.values.get('street')
        number = flask.request.values.get('number')
        addr = Address(postal_code, street, number)
        coor = get_default_coordinates()

        patient = Patient(None, name, addr, coor)
        conn = get_db()
        c = conn.cursor()
        patient_id = dao.register_patient(c, patient)
        username = flask.request.values.get('username')
        password = flask.request.values.get('password')
        dao.register_user(c, username, password, patient_id=patient_id)
        conn.commit()
        flash("Registrierung erfolgreich")
        return render_template('index.html')
    else:
        return render_template("register_patient.html")


@app.route('/register_driver', methods=['GET', 'POST'])
def register_driver():
    if flask.request.method == 'POST':
        name = flask.request.values.get('name')
        range = flask.request.values.get('range')
        postal_code = flask.request.values.get('plz')
        street = flask.request.values.get('street')
        number = flask.request.values.get('number')
        addr = Address(postal_code, street, number)
        coor = get_default_coordinates()
        storage = get_default_dimensions()
        cooled_storage = get_default_dimensions()

        driver = Driver(None, name, range, addr, coor, storage, cooled_storage)
        conn = get_db()
        c = conn.cursor()
        driver_id = dao.register_driver(c, driver)
        username = flask.request.values.get('username')
        password = flask.request.values.get('password')
        dao.register_user(c, username, password, driver_id=driver_id)
        conn.commit()
        flash("Registrierung erfolgreich")
        return render_template('index.html')
    else:
        return render_template("register_driver.html")


def not_empty(item):
    return item != ''

@app.route('/submit_order', methods=['GET', 'POST'])
@login_required(must=[is_patient])
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




@app.route('/upload_stock', methods=['GET', 'POST'])
@login_required(must=[is_pharmacy])
def upload_stock():
    if flask.request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('Keine Datei ausgewählt')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('Keine Datei ausgewählt')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            data = process_uploaded_csv_file(file.stream)
            stock = read_stock(data)
            conn = get_db()
            c = conn.cursor()
            pharmacy_id = get_pharmacy_id(c, get_username())
            process_stock(c, pharmacy_id, stock)
            conn.commit()
            flash('Bestand erfolgreich aktualisiert')
        return render_template('index.html')
    else:
        return render_template("upload_stock.html")


def start_calculation():
    print("MAGIC IS HAPPENING NOW")
    conn = get_db()
    c = conn.cursor()
    drivers = get_all_drivers(c)
    pharmacies = get_all_pharmacies(c)
    orders = get_all_orders(c)
    driver_based_delivery_sets = delivery_set_splitter(delivery_set_reducer(generate_delivery_item_base_set(drivers, pharmacies, orders)))
    for delivery_set in driver_based_delivery_sets:
        print("for driver " + delivery_set[0].driver)
        print(travelling_sales_man(delivery_set))


@app.route('/calculate_routes', methods=['GET', 'POST'])
@login_required(must=[is_overlord])
def calculate_routes():
    if flask.request.method == 'POST':
        conn = get_db()
        c = conn.cursor()
        route = make_fake_route(c)
        routes = [route, route]
        return render_template('calculated_routes.html', routes=routes)
    else:
        return render_template("calculate_routes.html")


@app.route('/complex')
@login_required(must=[is_driver])
def complexview():
    return render_template('secret.html')


class ProtectedView(MethodView):
    decorators = [login_required]

    def get(self):
        return "You are logged in as <b>{0}</b>".format(get_username())


app.add_url_rule('/protected', view_func=ProtectedView.as_view('protected'))
app.add_template_global(is_logged_in_as_pharmacy)
app.add_template_global(is_logged_in_as_driver)
app.add_template_global(is_logged_in_as_patient)
app.add_template_global(is_logged_in_as_overlord)
app.teardown_appcontext(close_db)
if __name__ == '__main__':
    app.run(port=5000, use_reloader=True, debug=True)
