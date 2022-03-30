from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import current_user, login_required

from models import User, Post, Comment
from forms import NewPostForm, NewCommentForm, EditProfileForm
from database import db

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


@blueprint.route('/about')
def about():
    return render_template('pages/about.html')


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


@blueprint.route('/feed/<post_id>')
def view_post(post_id: int):
    post = Post.query.get_or_404(post_id)
    return render_template('pages/post.html', form=NewCommentForm(), post=post)


# @blueprint.route('/messages')
# def messages():
#     return render_template('pages/messages.html')


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


@blueprint.route('/terms_of_service')
def tos():
    return render_template('static/tos.html')


@blueprint.route('/privacy')
def privacy():
    return render_template('static/privacy.html')


@blueprint.route('/license')
def license():
    return render_template('static/license.html')
# @blueprint.route('/blogs')
# def blogs():
#     return render_template('pages/blogs.html')
#
#
# @blueprint.route('/groups')
# def groups():
#     return render_template('pages/groups.html')
