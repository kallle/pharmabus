from control.app import app
from data.database_handler import get_db
from flask import session, render_template
from models.DatabaseEntityDoesNotExist import DatabaseEntityDoesNotExist
from data.daoUser import getUserId
from data.daoOrder import getAllOrdersFiltertForUser
from control.login_checks import is_patient, is_doctor, is_pharmacy
from models.role import Role

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    username = session.get('simple_username')
    if username is not None:
        try:
            user_id = getUserId(cursor, username)
        except DatabaseEntityDoesNotExist:
            return render_template('index.html')
    if username is not None and is_patient(username):
        conn = get_db()
        cursor = conn.cursor()
        orders = getAllOrdersFiltertForUser(cursor, Role.PATIENT, user_id)
        return render_template('orders.html', orders=orders)
    elif username is not None and  is_doctor(username):
        conn = get_db()
        cursor = conn.cursor()
        orders = getAllOrdersFiltertForUser(cursor, Role.DOCTOR, user_id)
        return render_template('orders.html', orders=orders)
    elif username is not None and is_pharmacy(username):
        conn = get_db()
        cursor = conn.cursor()
        orders = getAllOrdersFiltertForUser(cursor, Role.PHARMACY, user_id)
        return render_template('orders.html', orders=orders)
    else:
        return render_template('index.html')
