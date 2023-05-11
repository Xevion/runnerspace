from flask import Blueprint, redirect, render_template, url_for, request, jsonify
from flask_login import current_user, login_required

from runnerspace.models import User, Post, Comment, PostLike, CommentLike
from runnerspace.forms import NewPostForm, NewCommentForm, EditProfileForm
from runnerspace.database import db

blueprint = Blueprint('main', __name__)


@blueprint.route('/')
def index():  # put application's code here
    users = User.query.order_by(User.time_registered.desc()).limit(10).all()
    stats = {
        'total_users': User.query.count(),
        'total_comments': Comment.query.count(),
        'total_posts': Post.query.count()
    }
    return render_template('layouts/index.html', new_users=users, stats=stats)


@blueprint.route('/users')
def browse():
    users = User.query.all()
    return render_template('pages/browse.html', users=users)


@blueprint.route('/feed', methods=['GET', 'POST'])
def feed():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    form = NewPostForm(request.form)

    if request.method == 'POST' and form.validate():
        post = Post(author=current_user, text=form.text.data)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('main.view_post', post_id=post.id))

    return render_template('pages/feed.html', posts=posts, form=form)


@blueprint.route('/post/<post_id>')
def view_post(post_id: int):
    post = Post.query.get_or_404(post_id)
    return render_template('pages/post.html', form=NewCommentForm(), post=post)


@blueprint.route('/post/<post_id>/like', methods=['POST'])
@login_required
def like_post(post_id: int):
    # Check that the relevant post exists
    post = db.session.query(Post).get_or_404(post_id)

    # Acquire the relevant PostLike in question
    post_like = db.session.query(PostLike).filter_by(post=post, user=current_user).first()
    if post_like is None:
        post_like = PostLike(post=post, user=current_user)
        db.session.add(post_like)
    else:
        db.session.delete(post_like)
        post_like = None

    db.session.commit()

    # post_like is only NOT None if the user had not liked it before, but has liked it now after db.commit().
    return jsonify({'liked': post_like is not None, 'status_text': post.get_like_text()})


@blueprint.route('/search')
def search():
    return render_template('pages/search.html')


@blueprint.route('/user/<username>/')
def view_user(username: str):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('pages/user.html', user=user)


@blueprint.route('/user/<username>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(username: str):
    user = db.session.query(User).filter_by(username=username).first_or_404()
    form = EditProfileForm(request.form)

    # Check that a form was submitted
    if form.validate_on_submit():
        # Check that the user submitting the form is allowed to do this
        if current_user.is_admin or current_user == user:
            user.about_me = form.about_me.data
            user.name = form.name.data

            db.session.commit()
            return redirect(url_for('main.view_user', username=username))
        return render_template('pages/user_edit.html', form=form)

    form.process(obj=user)
    return render_template('pages/user_edit.html', form=form)
