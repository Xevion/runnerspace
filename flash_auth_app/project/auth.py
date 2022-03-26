from flask import Blueprint, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

'''
FIXME this will have to be revisited later with added funcitonality,
as right now `login`, `signup`, and `logout` only return text

There will also be routes for handling POST requests from login and signup
'''


@auth.route('/login')
def login():
    # return render_template('login.html')
    return 'Login'  # placeholder


@auth.route('/signup')
def signup():
    # return render_template('signup.html')
    return 'Signup'  # placeholder


@auth.route('/signup', methods=['POST'])
def signup_post():
    # validate and add user to db
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()  # Check if the email exists
    if user:  # redirect back to sign-up page
        return(redirect(url_for('auth.signup')))

    # Create new user with form data
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # Add new user to db
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    return 'Logout'  # placeholder
