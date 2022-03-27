from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, login_required, logout_user
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
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists, and compare password given
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    # validate and add user to db
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()  # Check if the email exists
    if user:  # redirect back to sign-up page
        flash('Email address already exists')
        return(redirect(url_for('auth.signup')))

    # Create new user with form data
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # Add new user to db
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
