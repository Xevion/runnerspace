from flask import Blueprint, flash, redirect, request, url_for
from flask_login import current_user, login_required
from profanity_filter import ProfanityFilter
from forms import RegistrationForm, EditProfileForm, NewPostForm, NewCommentForm
from database import db
from models import User, Post, Comment

blueprint = Blueprint('forms', __name__)
pf = ProfanityFilter()


@blueprint.route('/user/<username>/edit', methods=['POST'])
@login_required
def edit_profile_post(username):
    user = db.session.query(User).filter_by(username=username).first_or_404()

    # Allow admins to edit profiles, but deny other users
    if not current_user.is_admin and current_user.id != user.id:
        return redirect(url_for('main.view_user', username=username))

    form = RegistrationForm(request.form)
    if form.validate():
        user.about_me = form.about_me.data
        user.name = form.name.data
        db.session.commit()

        flash('Successfully updated profile.')
        return redirect(url_for('main.edit_user', username=username))


@blueprint.route('/feed/<post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id: int):
    post = Post.query.get_or_404(post_id)
    form = NewCommentForm(request.form)

    if form.validate():
        if not pf.is_clean(form.text.data):
            flash('Sorry, profanity is not allowed on runnerspace.')
            return redirect(url_for('main.view_post', post_id=post_id))

        comment = Comment(post=post.id, author=current_user.id, text=form.text.data)
        db.session.add(comment)
        db.session.commit()

    return redirect(url_for('main.view_post', post_id=post.id))
