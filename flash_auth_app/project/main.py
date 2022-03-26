from flask import Blueprint
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # return render_template('index.html')
    return 'Index'  # placeholder

@main.route('/profile')
def profile():
    # return render_template('profile.html')
    return 'Profile'  # placeholder