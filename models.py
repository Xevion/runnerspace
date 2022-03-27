import datetime
import json
from typing import List

import humanize
from flask_login import UserMixin
from sqlalchemy import func

from .create_app import db

MAXIMUM_ONLINE_DELTA = datetime.timedelta(minutes=1)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    about_me = db.Column(db.String(5000), nullable=True)
    time_registered = db.Column(db.DateTime, nullable=False, server_default=func.now())
    last_seen = db.Column(db.DateTime, nullable=False, server_default=func.now())
    last_ip = db.Column(db.String(64), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    posts = db.relationship("Post")
    comments = db.relationship("Comment")

    def get_last_seen(self) -> str:
        delta: datetime.timedelta = datetime.datetime.utcnow() - self.last_seen
        if delta > MAXIMUM_ONLINE_DELTA:
            return f'Last seen {humanize.naturaldelta(delta)} ago'
        return 'Online now!'

    def get_registration_delta(self) -> str:
        delta: datetime.timedelta = datetime.datetime.utcnow() - self.time_registered
        return humanize.naturaldelta(delta)

    def get_post_count(self) -> int:
        return len(self.posts)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, server_default=func.now())
    date_updated = db.Column(db.DateTime, nullable=True)
    likes = db.Column(db.Text, default='[]')
    comments = db.relationship("Comment")

    def get_likes(self) -> List[int]:
        """Return the IDs of the Users who have liked this post."""
        return json.loads(self.likes)

    def set_likes(self, likes: List[int]) -> None:
        """Set the likes c"""
        self.likes = list(dict.fromkeys(json.dumps(likes)))
        self.save()

    def add_like(self, user_id: int) -> None:
        likes: List[int] = self.get_likes()
        if user_id not in likes:
            likes.append(user_id)
            self.set_likes(likes)

    def get_time_ago(self) -> str:
        delta: datetime.timedelta = datetime.datetime.utcnow() - self.date_posted
        return humanize.naturaldelta(delta)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    date_posted = db.Column(db.DateTime, server_default=func.now())
