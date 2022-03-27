from flask import Blueprint, render_template
from flask_login import login_required, current_user

blueprint = Blueprint('main', __name__)


@blueprint.route('/profile')
@login_required
def profile():
    return render_template('layouts/profile.html', name=current_user.name)


@blueprint.route('/')
def index():  # put application's code here
    return render_template('layouts/index.html', user=user)


@blueprint.route('/about')
def about():
    return render_template('pages/about.html', user=user)


@blueprint.route('/users')
def browse():
    return render_template('pages/browse.html', user=user)


@blueprint.route('/feed')
def feed():
    return render_template('pages/feed.html', user=user)


@blueprint.route('/messages')
def messages():
    return render_template('pages/messages.html', user=user)


@blueprint.route('/search')
def search():
    return render_template('pages/search.html', user=user)


@blueprint.route('/user/<username>')
def user(username: str):
    return render_template('pages/user.html', user=user)


@blueprint.route('/blogs')
def blogs():
    return render_template('pages/blogs.html', user=user)


@blueprint.route('/groups')
def groups():
    return render_template('pages/groups.html', user=user)


@blueprint.route('/login', methods=['GET'])
def login():
    return render_template('pages/login.html', user=user)


@blueprint.route('/signup', methods=['GET'])
def signup():
    return render_template('pages/signup.html', user=user)
