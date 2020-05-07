import flask
from flask import Flask, render_template, session, request, flash, redirect
from flask import g
from flask_simplelogin import SimpleLogin, get_username, login_required, is_logged_in
from control.login_checks import is_logged_in_as_pharmacy, is_logged_in_as_driver, is_logged_in_as_patient, is_logged_in_as_overlord
from control.login_checks import is_pharmacy, is_driver, is_patient, is_overlord, check_my_users, is_doctor
from models.order_status import OrderStatus
from models.prescription_status import PrescriptionStatus
from data.database_handler import close_db


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


app.add_template_global(is_logged_in_as_pharmacy)
app.add_template_global(is_logged_in_as_driver)
app.add_template_global(is_logged_in_as_patient)
app.add_template_global(is_logged_in_as_overlord)
app.add_template_global(is_pharmacy)
app.add_template_global(is_driver)
app.add_template_global(is_patient)
app.add_template_global(is_overlord)


def template_translate_order_status(status):
    if status == OrderStatus.AT_PATIENT:
        return "Patient muss tätig werden"
    elif status == OrderStatus.AT_DOCTOR:
        return "Arzt muss das Rezept hochladen"
    elif status == OrderStatus.AT_PHARMACY:
        return "Apotheke muss die Bestellung bearbeiten"
    elif status == OrderStatus.AT_PHARMACY_CONFIRMED:
        return "Fahrer muss das Medikament abholen"
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
    elif status == OrderStatus.At_PHARMACY_CONFIRMED:
        return is_pharmacy(username)
    elif status == OrderStatus.AT_DRIVER:
        return is_driver(username)
    elif status == OrderStatus.DELIVERED:
        return is_patient(username)
    else:
        raise Exception("unsuppored order status enum value {}".format(status))


app.add_template_global(template_translate_order_status)
app.add_template_global(order_status_corresponds_to_user_role)
app.teardown_appcontext(close_db)
