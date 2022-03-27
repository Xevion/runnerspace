from flask_login import UserMixin
from .create_app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    has_bio = db.Column(db.Boolean, default=False)
    bio = db.Column(db.String(5000), nullable=True)

    # day registered, last online, register date, last ip
