from flask import Blueprint, flash, redirect, request, url_for, render_template
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

    if current_user.is_admin or user.id == current_user.id:
        if form.validate():
            user.about_me = form.about_me.data
            db.session.commit()

    return redirect(url_for('main.view_user', username=user.username))


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()

        # check if the user actually exists, and compare password given
        if not user or not check_password_hash(user.password, form.password.data):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))

    return render_template('pages/auth/login.html', form=form)


@blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    # validate and add user to db
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()  # Check if the username is already in use
        if user:  # redirect back to sign-up page
            flash('This username is already in use.')
            return redirect(url_for('auth.signup'))

        # Create new user with form data
        new_user = User(username=form.username.data, name=form.name.data,
                        password=generate_password_hash(form.password.data, method='sha256'))
        # Add new user to db
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('pages/auth/signup.html', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
