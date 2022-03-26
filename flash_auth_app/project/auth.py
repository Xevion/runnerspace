from flask import Blueprint
from . import db

auth = Blueprint('auth', __name__)

'''
FIXME this will have to be revisited later with added funcitonality,
as right now `login`, `signup`, and `logout` only return text

There will also be routes for handling POST requests from login and signup
'''

@auth.route('/login')
def login():
    return 'Login'

@auth.route('/signup')
def signup():
    return 'Signup'

@auth.route('/logout')
def logout():
    return 'Logout'