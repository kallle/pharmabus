from control.app import app
from flask_simplelogin import SimpleLogin, get_username, login_required, is_logged_in
from control.login_checks import is_logged_in_as_pharmacy, is_logged_in_as_driver, is_logged_in_as_patient, is_logged_in_as_overlord
from control.login_checks import is_pharmacy, is_driver, is_patient, is_overlord, check_my_users, is_logged_in_at_all
import flask
from flask import Flask, render_template, session, request, flash, redirect, send_file
from models.DatabaseEntityDoesNotExist import DatabaseEntityDoesNotExist
from data.daoUser import getDoctor, getPatient, getPharmacy
from data.daoOrder import getOrder, insertOrder, addPrescriptionToOrder, updateOrder, deleteOrder, updateOrderStatus
from data.database_handler import get_db
from models.prescription_status import PrescriptionStatus
from control.login_checks import is_doctor, is_patient, is_pharmacy
from models.order_status import OrderStatus
from werkzeug.utils import secure_filename
import tempfile
import os


ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'png', 'jpeg'}

class OrderForm:

    def __init__(self, order_id=None, doctor_id=None, pharmacy_id=None, patient_id=None):
        try:
            self.order_id = int(order_id)
        except:
            self.order_id = None
        try:
            self.doctor_id = int(doctor_id )
        except:
            self.doctor_id = None
        try:
            self.pharmacy_id = int(pharmacy_id)
        except:
            self.pharmacy_id = None
        try:
            self.patient_id = int(patient_id)
        except:
            self.patient_id = None

    def complete(self):
        return (self.order_id is not None and
                self.doctor_id is not None and
                self.pharmacy_id is not None and
                self.patient_id is not None)

    def __str__(self):
        return "P:{}//A:{}//D:{}//O:{}".format(self.patient_id,
                                               self.pharmacy_id,
                                               self.doctor_id,
                                               self.order_id)



def create_new_order(formStatus):
    conn = get_db()
    cursor = conn.cursor()
    try:
        print(session.get('simple_user_id'))
        print(formStatus.patient_id == session.get('simple_user_id'))
        # if the corresponding patient is not the current user
        if formStatus.patient_id != session.get('simple_user_id'):
            raise Exception("given patient does not match current patient")
        patient = getPatient(cursor, formStatus.patient_id)
    except DatabaseEntityDoesNotExist:
        raise Exception("given patient does not exist")
    doctor = getDoctor(cursor, formStatus.doctor_id)
    pharmacy = getPharmacy(cursor, formStatus.pharmacy_id)
    order = insertOrder(cursor, patient, doctor, pharmacy)
    conn.commit()
    return order


def update_pharmacy(formStatus):
    print('updating pharmacy with {}'.format(formStatus))
    conn = get_db()
    cursor = conn.cursor()
    order = getOrder(cursor, formStatus.order_id)
    patient = getPatient(cursor, session.get('simple_user_id'))
    if order.patient.id != patient.id:
        raise Exception("only the owning patient may change the order")
    if order.status != OrderStatus.AT_PATIENT:
        raise Exception("only if the ownership is at the patient may the pharmacy be changed")
    order = updateOrder(cursor, order, pharmacy_id = formStatus.pharmacy_id)
    conn.commit()
    return order


def update_doctor(formStatus):
    print('updating doctor with {}'.format(formStatus))
    conn = get_db()
    cursor = conn.cursor()
    order = getOrder(cursor, formStatus.order_id)
    patient = getPatient(cursor, session.get('simple_user_id'))
    if order.patient.id != patient.id:
        raise Exception("only the owning patient may change the order")
    if order.status != OrderStatus.AT_PATIENT:
        raise Exception("only if the ownership is at the patient may the doctor be changed")
    order = updateOrder(cursor, order, doctor_id = formStatus.order_id)
    conn.commit()
    return order


# TODO: we need a stronger file check!
def allowed_file_name(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def update_prescription(formStatus, pstatus, scan):
    print('{}//{}//{}'.format(formStatus, pstatus, scan))
    assert formStatus.complete()
    if scan and allowed_file_name(scan.filename):
        filename = secure_filename('prescription-{}.{}'.format(formStatus.order_id,
                                                               scan.filename.split('.')[-1].lower()))
        instance_path = app.instance_path
        print(instance_path)
        path = os.path.join(instance_path, app.config['UPLOAD_FOLDER'], filename)
        print(path)
        scan.save(path)
    else:
        filename = None
    conn = get_db()
    cursor = conn.cursor()
    if is_patient(session.get('simple_username')):
        order = getOrder(cursor, formStatus.order_id)
        patient = getPatient(cursor, session.get('simple_user_id'))
        if order.patient.id != patient.id:
            raise Exception('probable hacking attempt, order patient mismatch logged in patient')
        order = addPrescriptionToOrder(cursor, order, pstatus, scan=filename, supersede=True)
        conn.commit()
        return order
    elif is_doctor(session.get('simple_username')):
        order = getOrder(cursor, formStatus.order_id)
        doctor = getDoctor(cursor, session.get('simple_user_id'))
        if order.doctor.id != doctor.id:
            raise Exception('probable hacking attempt, doctor patient mismatch logged in doctor')
        order = addPrescriptionToOrder(cursor, order, pstatus, scan=filename, supersede=True)
        conn.commit()
        return order
    else:
        raise Exception("only the patient or doctor may change a prescription")


@app.route('/order/create_order', methods=['GET'])
@login_required(must=[is_logged_in_as_patient])
def create_order():
    if flask.request.method == 'GET':
        formStatus = OrderForm()
        formStatus.patient_id = session.get('simple_user_id')
        return render_template('/order/choose_doctor.html', formStatus=formStatus)
    else:
        render_template('index.html')


@app.route('/order/modify_order', methods=['GET','POST'])
@login_required(must=[is_logged_in_at_all])
def modify_order():
    conn = get_db()
    cursor = conn.cursor()
    try:
        order = getOrder(cursor, int(flask.request.args.get('order_id')))
        print(order)
    except:
        raise Exception('to be modified order does not exist')
    if flask.request.method == 'GET':
        if is_pharmacy(session.get('simple_username')):
            pharmacy = getPharmacy(cursor, session.get('simple_user_id'))
            if order.pharmacy.id != pharmacy.id:
                raise Exception('wrong pharmacy to change order')
            return render_template('/order/modify_order.html', actor='pharmacy', order=order, pstatus=PrescriptionStatus, ostatus=OrderStatus)
        elif is_doctor(session.get('simple_username')):
            doctor = getDoctor(cursor, session.get('simple_user_id'))
            if order.doctor.id != doctor.id:
                raise Exception('wrong doctor to change order')
            return render_template('/order/modify_order.html', actor='doctor', order=order, pstatus=PrescriptionStatus, ostatus=OrderStatus)
        elif is_patient(session.get('simple_username')):
            patient = getPatient(cursor, session.get('simple_user_id'))
            if order.patient.id != patient.id:
                raise Exception('wrong patient to change order')
            return render_template('/order/modify_order.html', actor='patient', order=order, pstatus=PrescriptionStatus, ostatus=OrderStatus)
        else:
            raise Exception('who is trying to modify an existing order here?')
    elif flask.request.method == 'POST':
        pass
    else:
        raise Exception('wtf')


@app.route('/order/choose_doctor', methods=['GET','POST'])
@login_required(must=[is_logged_in_as_patient])
def choose_doctor():
    if flask.request.method == 'GET':
        formStatus = OrderForm(flask.request.args.get('order_id'),
                               flask.request.args.get('doctor_id'),
                               flask.request.args.get('pharmacy_id'),
                               flask.request.args.get('patient_id'))
        print('choosing new doctor')
        print(formStatus)
        return render_template('/order/choose_doctor.html', formStatus=formStatus)
    elif flask.request.method == 'POST':
        formStatus = OrderForm(flask.request.form.get('order_id'),
                               flask.request.form.get('doctor_id'),
                               flask.request.form.get('pharmacy_id'),
                               flask.request.form.get('patient_id'))
        print(formStatus)
        conn = get_db()
        cursor = conn.cursor()
        if formStatus.doctor_id is not None:
            try:
                doctor = getDoctor(cursor, formStatus.doctor_id)
            except DatabaseEntityDoesNotExist:
                flash('Bitte waehle einen existierenden Arzt')
                return render_template('/order/choose_doctor.html', formStatus=formStatus)
        else:
            flash('Bitte wahle einen Arzt aus')
            return render_template('/order/choose_doctor.html', formStatus=formStatus)
        # if we reached this point the doctor exists and we have to decide what the
        # next step is
        if formStatus.complete():
            # if the form is already complete, this is an update (further sanity checks performed there)
            print('form complete')
            order = update_doctor(formStatus)
            return render_template('/order/modify_order.html', order=order, actor='patient', pstatus=PrescriptionStatus, ostatus=OrderStatus)
        else:
            # if the form is incomplete, this is a new order creation (further sanity checks performed there)
            print('form incomplete')
            return render_template('/order/choose_pharmacy.html', formStatus=formStatus)
    else:
        return render_template('index.html')


@app.route('/order/choose_pharmacy', methods=['GET', 'POST'])
@login_required(must=[is_logged_in_as_patient])
def choose_pharmacy():
    # this function should only be reached via POST
    if flask.request.method == 'GET':
        formStatus = OrderForm(flask.request.args.get('order_id'),
                               flask.request.args.get('doctor_id'),
                               flask.request.args.get('pharmacy_id'),
                               flask.request.args.get('patient_id'))
        print('choosing new pharmacy')
        print(formStatus)
        return render_template('/order/choose_pharmacy.html', formStatus=formStatus)
    elif flask.request.method == 'POST':
        formStatus = OrderForm(flask.request.form.get('order_id'),
                               flask.request.form.get('doctor_id'),
                               flask.request.form.get('pharmacy_id'),
                               flask.request.form.get('patient_id'))
        print(formStatus)
        conn = get_db()
        cursor = conn.cursor()
        if formStatus.pharmacy_id is not None:
            try:
                pharmacy = getPharmacy(cursor, formStatus.pharmacy_id)
            except:
                flash('Bitte wahle eine existierende Apotheke')
                return render_template('order/choose_pharmacy.html', formStatus=formStatus)
        else:
            return render_template('order/choose_pharmacy.html', formStatus=formStatus)
        # if we reached this point the pharmacy exists and we have to decide what the
        # next step is
        if formStatus.complete():
            # if the form is already complete, this is an update (further sanity checks performed there)
            order = update_pharmacy(formStatus)
            return render_template('order/modify_order.html', order=order, actor='patient', pstatus=PrescriptionStatus, ostatus=OrderStatus)
        else:
            # if the form is incomplete, this is a new order creation (further sanity checks performed there)
            order = create_new_order(formStatus)
            return render_template('order/change_prescription.html', order=order)
    else:
        return render_template('index.html')


@app.route('/order/change_prescription', methods=['GET', 'POST'])
@login_required(must=[is_logged_in_at_all]) # doctor and patient can change the prescription
def upload_prescription():
    # this function should only be reached via POST
    if flask.request.method == "GET":
        formStatus = OrderForm(flask.request.args.get('order_id'),
                               flask.request.args.get('doctor_id'),
                               flask.request.args.get('pharmacy_id'),
                               flask.request.args.get('patient_id'))
        conn = get_db()
        cursor = conn.cursor()
        order = getOrder(cursor, formStatus.order_id)
        if is_patient(session.get('simple_username')):
            patient = getPatient(cursor, formStatus.patient_id)
            if order.patient.id != patient.id:
                raise Exception('invalid patient to change that order')
        elif is_doctor(session.get('simple_username')):
            doctor = getDoctor(cursor, formStatus.doctor_id)
            if order.doctor.id != doctor.id:
                raise Exception('invalid doctor to change that oder')
        else:
            raise Exception('invalid user role to change a prescription')
        return render_template('/order/change_prescription.html', order=order)
    if flask.request.method == "POST":
        formStatus = OrderForm(flask.request.form.get('order_id'),
                               flask.request.form.get('doctor_id'),
                               flask.request.form.get('pharmacy_id'),
                               flask.request.form.get('patient_id'))
        if not formStatus.complete():
            flash('Uups something went wrong.')
            return render_template('index.html')
        plocation = flask.request.form.get('prescription_location')
        status = PrescriptionStatus.PRESENT_AT_DOCTOR if plocation == "doctor" else PrescriptionStatus.PRESENT_AT_PATIENT
        # print('request {}'.format(flask.request.form))
        # print('files {}'.format(flask.request.files))
        if 'prescription' not in flask.request.files:
            order = update_prescription(formStatus, status, None)
        else:
            if flask.request.files['prescription'].filename == '':
                order = update_prescription(formStatus, status, None)
            else:
                order = update_prescription(formStatus, status, flask.request.files['prescription'])
        if is_patient(session.get('simple_username')):
            actor = 'patient'
        elif is_doctor(session.get('simple_username')):
            actor = 'doctor'
        else:
            raise Exception('wtf')
        return render_template('order/modify_order.html', order=order, actor=actor, pstatus=PrescriptionStatus, ostatus=OrderStatus)
    else:
        return render_template('index.html')


#TODO: need to also delete uploaded prescriptions
@app.route('/order/cancel_order', methods=['GET'])
@login_required(must=[is_logged_in_as_patient])
def cancel_order():
    conn = get_db()
    cursor = conn.cursor()
    order_id = flask.request.args.get('order_id')
    if order_id is None:
        raise Exception("Order Id expected for cancellation")
    order = getOrder(cursor, order_id)
    patient = getPatient(cursor, session.get('simple_user_id'))
    if patient.id != order.patient.id:
        raise Exception("Only the order owning patient can cancel")
    else:
        if order.status in [OrderStatus.AT_PATIENT, OrderStatus.AT_DRIVER]:
            deleteOrder(cursor, order)
            conn.commit()
    flash('Bestellung erfolgreich gecancelt')
    return render_template('index.html')


@app.route('/order/download_prescription', methods=['POST'])
@login_required(must=[is_logged_in_at_all])
def download_prescription():
    if flask.request.method == 'POST':
        formStatus = OrderForm(flask.request.form.get('order_id'),
                               flask.request.form.get('doctor_id'),
                               flask.request.form.get('pharmacy_id'),
                               flask.request.form.get('patient_id'))
        conn = get_db()
        cursor = conn.cursor()
        order = getOrder(cursor, formStatus.order_id)
        if is_patient(session.get('simple_username')):
            patient = getPatient(cursor, formStatus.patient_id)
            if order.patient.id != patient.id:
                raise Exception('download denied')
        elif is_doctor(session.get('simple_username')):
            doctor = getDoctor(cursor, formStatus.doctor_id)
            if order.doctor.id != doctor.id:
                raise Exception('download denied')
        elif is_pharmacy(session.get('simple_username')):
            pharmacy = getPharmacy(cursor, formStatus.pharmacy_id)
            if order.pharmacy.id != pharmacy.id:
                raise Exception('download denied')
        else:
            raise Exception('wtf')
        prescription_file = os.path.join(app.instance_path, app.config['UPLOAD_FOLDER'], order.prescription.scan)
        return send_file(prescription_file, as_attachment=True)
    else:
        raise Exception('wtf')


@app.route('/order/order_confirmation_pharmacy', methods=['POST'])
@login_required(must=[is_logged_in_as_pharmacy])
def confirmation_pharmacy():
    if flask.request.method == 'POST':
        formStatus = OrderForm(flask.request.form.get('order_id'),
                               flask.request.form.get('doctor_id'),
                               flask.request.form.get('pharmacy_id'),
                               flask.request.form.get('patient_id'))
        conn = get_db()
        cursor = conn.cursor()
        order = getOrder(cursor, formStatus.order_id)
        pharmacy = getPharmacy(cursor, session.get('simple_user_id'))
        if not order.pharmacy.id == pharmacy.id:
            raise Exception('no you may not change a foreign order asshat')
        updateOrderStatus(cursor, order, OrderStatus.AT_PHARMACY_CONFIRMED)
        conn.commit()
        flash('you confirmed the order, please wait for the driver to pick up the order')
        return render_template('index.html')
    else:
        raise Exception('wtf')
