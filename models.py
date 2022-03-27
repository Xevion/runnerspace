from flask_login import UserMixin
from sqlalchemy import func

from .create_app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    about_me = db.Column(db.String(5000), nullable=True)
    time_registered = db.Column(db.DateTime, nullable=False, server_default=func.now())
    last_seen = db.Column(db.DateTime, nullable=False, server_default=func.now())
    last_ip = db.Column(db.String(64), nullable=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer)
    text = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, server_default=func.now())
    date_updated = db.Column(db.DateTime, nullable=True)
    likes = db.Column(db.Text, default='[]')
