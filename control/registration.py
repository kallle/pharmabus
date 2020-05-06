from control.app import app
import flask
from flask import render_template, session, request, flash, redirect
from data.database_handler import get_db
from data.dao import registerPharmacy, registerPatient, registerDoctor, registerDriver


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
