from flask import Blueprint, flash, redirect, request, url_for, render_template
from flask_login import current_user, login_required
from runnerspace.forms import RegistrationForm, EditProfileForm, NewPostForm, NewCommentForm
from runnerspace.database import db
from runnerspace.models import User, Post, Comment

blueprint = Blueprint('forms', __name__)


@blueprint.route('/user/<username>/edit', methods=['POST'])
@login_required
def edit_profile_post(username):
    user = db.session.query(User).filter_by(username=username).first_or_404()

    # Allow admins to edit profiles, but deny other users
    if not current_user.is_admin and current_user != user:
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

    if form.validate_on_submit():
        comment = Comment(post=post, author=current_user, text=form.text.data)
        db.session.add(comment)
        db.session.commit()

        return redirect(url_for('main.view_post', post_id=post.id))

    return render_template('pages/post.html', form=form, post=post)
