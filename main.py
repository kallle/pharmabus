import sqlite3

import flask
from flask import Flask, jsonify, render_template
from flask.views import MethodView
from flask_simplelogin import SimpleLogin, get_username, login_required

import settings
from data import dao
from models.address import Address
from models.coordinates import get_default_coordinates
from models.dimensions import get_default_dimensions
from models.driver import Driver
from models.patient import Patient
from models.pharmacy import Pharmacy
from models.role import Role
from flask import current_app, g


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
    success = dao.check_login(c, username, password)
    return success

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

        pharmacy = Pharmacy(None, name, addr, coor)
        conn = get_db()
        c = conn.cursor()
        pharmacy_id = dao.register_driver(c, pharmacy)
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
        patient_id = dao.register_driver(c, patient)
        username = flask.request.values.get('username')
        password = flask.request.values.get('password')
        dao.register_user(c, username, password, patient_id=patient_id)
        conn.commit()
        return render_template('index.html')
    else:
        return render_template("register_driver.html")


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


def compare_role(username, role):
    conn = sqlite3.connect(settings.DATABASE_URL)
    c = conn.cursor()
    r = dao.get_role(c, username)
    return r == role


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



@app.route('/complex')
@login_required(must=[is_driver])
def complexview():
    return render_template('secret.html')


class ProtectedView(MethodView):
    decorators = [login_required]

    def get(self):
        return "You are logged in as <b>{0}</b>".format(get_username())


app.add_url_rule('/protected', view_func=ProtectedView.as_view('protected'))
app.teardown_appcontext(close_db)
if __name__ == '__main__':
    app.run(port=5000, use_reloader=True, debug=True)
