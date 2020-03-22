import pprint
import sqlite3

import flask
from flask import Flask, jsonify, render_template, session, request, flash, redirect
from flask.views import MethodView
from flask_simplelogin import SimpleLogin, get_username, login_required, is_logged_in

import settings
from data import dao
from data.dao import get_medication_by_name_supplier, insert_order, get_pharmacy_id, \
    process_stock, get_patient_id
from helper import process_uploaded_csv_file, read_stock, InvalidOrderException
from models.address import Address
from models.coordinates import get_default_coordinates
from models.dimensions import get_default_dimensions
from models.driver import Driver
from models.patient import Patient
from models.pharmacy import Pharmacy
from models.role import Role
from flask import current_app, g
from secrets import compare_digest


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
    if username == 'DreadPirateRoberts' and compare_digest(password, 'secret'):
        return True
    success = dao.check_login(c, username, password)
    return success


def compare_role(username, role):
    if username == 'DreadPirateRoberts':
        return Role.OVERLORD
    conn = get_db()
    c = conn.cursor()
    r = dao.get_role(c, username)
    return r == role


def is_overlord(username):
    return username == 'DreadPirateRoberts'


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
    return username == 'DreadPirateRoberts'


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

SimpleLogin(app, login_checker=check_my_users)


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
        return render_template('index.html')
    else:
        return render_template("register_driver.html")

@app.route('/submit_order', methods=['GET', 'POST'])
@login_required(must=[is_patient])
def submit_order():
    if flask.request.method == 'POST':
        handelsname = flask.request.values.get('handelsname')
        hersteller = flask.request.values.get('hersteller')
        amount = flask.request.values.get('amount')
        recipe_p = flask.request.values.get('rezept')
        conn = get_db()
        c = conn.cursor()
        error, userp = is_patient(get_username())
        if not userp:
            raise error
        patient_id = get_patient_id(c, get_username())
        med_id = get_medication_by_name_supplier(handelsname, hersteller)
        if patient_id == None or med_id == None:
            raise InvalidOrderException("You are either not a patient or the medication does not exist")
        insert_order(patient_id, med_id, amount, recipe_p, c)
        conn.commit()
        return render_template('index.html')
    else:
        return render_template("submit_order.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['csv']


@app.route('/upload_stock', methods=['GET', 'POST'])
@login_required(must=[is_pharmacy])
def upload_stock():
    if flask.request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            data = process_uploaded_csv_file(file.stream)
            stock = read_stock(data)
            conn = get_db()
            c = conn.cursor()
            pharmacy_id = get_pharmacy_id(c, get_username())
            process_stock(c, pharmacy_id, stock)
            conn.commit()
            pprint.pprint(stock)
        return render_template('index.html')
    else:
        return render_template("upload_stock.html")


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
