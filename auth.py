from flask import Blueprint, flash, redirect, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from forms import LoginForm, RegistrationForm, EditProfileForm
from models import User
from database import db

blueprint = Blueprint('auth', __name__)


@blueprint.route('/user/<username>', methods=['POST'])
def edit_profile_post(username: str):
    form = EditProfileForm(request.form)
    user = User.query.filter_by(username=username).first_or_404()

    if current_user.is_admin or user.id == current_user.id
        if form.validate():
            user.about_me = form.about_me.data
            db.session.commit()

    return redirect(url_for('main.view_user', username=user.username))


@blueprint.route('/login', methods=['POST'])
def login_post():
    form = LoginForm(request.form)
    user = User.query.filter_by(username=form.data.username).first()

    # check if the user actually exists, and compare password given
    if not user or not check_password_hash(user.password, form.password.data):
        flash('Please check your login details and try again.')
        return redirect(url_for('main.login'))

    login_user(user, remember=form.remember.data)
    return redirect(url_for('main.index'))


@blueprint.route('/signup', methods=['POST'])
def signup_post():
    # validate and add user to db
    form = RegistrationForm(request.form)

    user = User.query.filter_by(username=form.username.data).first()  # Check if the username is already in use
    if user:  # redirect back to sign-up page
        flash('This username is already in use.')
        return redirect(url_for('main.signup'))

    # Create new user with form data
    new_user = User(username=form.username.data, name=form.name.data, password=generate_password_hash(form.password.data, method='sha256'))

    # Add new user to db
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('main.login'))


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
