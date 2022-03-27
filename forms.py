from flask import Blueprint, flash, redirect, request, url_for
from flask_login import current_user, login_required

from .create_app import db
from .models import User, Post, Comment

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


@blueprint.route('/feed/new', methods=['POST'])
@login_required
def new_post():
    post_text = request.form.get('text')

    if len(post_text) < 15:
        flash('Must have at least 15 characters of text.')
        return redirect(url_for('forms.new_post'))
    elif len(post_text) > 1000:
        flash('Cannot have more than 1000 characters of text.')
        return redirect(url_for('forms.new_post'))

    post = Post(author=current_user.id, text=post_text)
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('main.view_post', post_id=post.id))
