from flask import Blueprint, flash, redirect, request, url_for
from flask_login import current_user, login_required

from .create_app import db
from .models import User

blueprint = Blueprint('forms', __name__)


@blueprint.route('/user/<username>/edit', methods=['POST'])
@login_required
def edit_profile_post(username):
    user = db.session.query(User).filter_by(username=username).first_or_404()

    # Ignore non
    if current_user.id != user.id:
        return redirect(url_for('main.user', username=username))

    user.about_me = request.form.get('about-me', user.about_me)
    user.name = request.form.get('name', user.name)
    db.session.commit()

    flash('Successfully updated profile.')
    return redirect(url_for('main.edit_user', username=username))
