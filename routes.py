from flask import Blueprint, render_template
from flask_login import login_required

from .models import User

blueprint = Blueprint('main', __name__)


@blueprint.route('/')
def index():  # put application's code here
    return render_template('layouts/index.html')


@blueprint.route('/about')
def about():
    return render_template('pages/about.html')


@blueprint.route('/users')
def browse():
    users = User.query.all()
    return render_template('pages/browse.html', users=users)


@blueprint.route('/feed')
def feed():
    return render_template('pages/feed.html')


@blueprint.route('/messages')
def messages():
    return render_template('pages/messages.html')


@blueprint.route('/search')
def search():
    return render_template('pages/search.html')


@blueprint.route('/user/<username>/')
def user(username: str):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('pages/user.html', user=user)


@blueprint.route('/user/<username>/edit')
@login_required
def edit_user(username: str):
    return render_template('pages/user_edit.html')


@blueprint.route('/blogs')
def blogs():
    return render_template('pages/blogs.html')


@blueprint.route('/groups')
def groups():
    return render_template('pages/groups.html')


@blueprint.route('/login', methods=['GET'])
def login():
    return render_template('pages/auth/login.html')


@blueprint.route('/signup', methods=['GET'])
def signup():
    return render_template('pages/auth/signup.html')
