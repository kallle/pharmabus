from data.database_handler import get_db
from data.dao import checkLogin, DatabaseEntityDoesNotExist, getUserId, getRole
from flask_simplelogin import is_logged_in
from models.role import Role


def check_my_users(user):
    conn = get_db()
    cursor = conn.cursor()
    email = user['username']
    password = user['password']
    print('test')
    try:
        success, id = checkLogin(cursor, email, password)
    except DataBaseEntityDoesNotExist:
        return False
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
