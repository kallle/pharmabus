from control.app import app
from flask_simplelogin import SimpleLogin, get_username, login_required, is_logged_in
from control.login_checks import is_logged_in_as_pharmacy, is_logged_in_as_driver, is_logged_in_as_patient, is_logged_in_as_overlord
from control.login_checks import is_pharmacy, is_driver, is_patient, is_overlord, check_my_users, is_logged_in_at_all
import flask
from flask import Flask, render_template, session, request, flash, redirect

@app.route('/order_create_order', methods=['GET','POST'])
@login_required(must=[is_logged_in_as_patient])


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
