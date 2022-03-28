from flask import Blueprint, flash, redirect, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from models import User
from app import db

blueprint = Blueprint('auth', __name__)


@blueprint.route('/user/<username>', methods=['POST'])
def bio_post():
    bio = request.form.get('bio')
    setattr(current_user, 'bio', bio)
    setattr(current_user, 'has_bio', True)


@blueprint.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = bool(request.form.get('remember'))

    user = User.query.filter_by(username=username).first()

    # check if the user actually exists, and compare password given
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('main.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.index'))


@blueprint.route('/signup', methods=['POST'])
def signup_post():
    # validate and add user to db
    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()  # Check if the email exists
    if user:  # redirect back to sign-up page
        flash('Email address already exists')
        return redirect(url_for('main.signup'))

    # Create new user with form data
    new_user = User(username=username, name=name, password=generate_password_hash(password, method='sha256'))

    # Add new user to db
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('main.login'))


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
