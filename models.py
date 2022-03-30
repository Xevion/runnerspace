import datetime
import json
from typing import List

import humanize
from flask_login import UserMixin
from sqlalchemy import func

from database import db

# Amount of time before a user is considered 'offline'
MAXIMUM_ONLINE_DELTA = datetime.timedelta(minutes=3)


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
    posts = db.relationship("Post", backref='author')
    comments = db.relationship("Comment", backref='author')
    posts_liked = db.relationship("PostLike", backref=db.backref('user', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')
    comments_liked = db.relationship("CommentLike", backref=db.backref('user', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')

    def get_last_seen_text(self) -> str:
        delta: datetime.timedelta = datetime.datetime.utcnow() - self.last_seen
        if delta > MAXIMUM_ONLINE_DELTA:
            return f'Last seen {humanize.naturaldelta(delta)} ago'
        return 'Online now!'

    def is_online(self) -> bool:
        """Returns true if the user has used the website in the time delta specified."""
        delta: datetime.timedelta = datetime.datetime.utcnow() - self.last_seen
        return delta < MAXIMUM_ONLINE_DELTA

    def is_offline(self) -> bool:
        """Returns true if the user has not used the website in the time delta specified."""
        return not self.is_online()

    def get_registration_delta(self) -> str:
        """Returns a string describing how long ago the user registered."""
        delta: datetime.timedelta = datetime.datetime.utcnow() - self.time_registered
        return humanize.naturaldelta(delta)

    def get_post_count(self) -> int:
        """Returns the number of posts this user has made."""
        return Post.query.filter_by(user_id=self.id).count()

    def get_comment_count(self) -> int:
        """Returns the number of comments this user has made."""
        return Comment.query.filter_by(user_id=self.id).count()

    def get_post_likes(self) -> int:
        """Returns the number of likes this user's posts have accumulated."""
        return sum(PostLike.query.filter_by(post=post).count() for post in self.posts)

    def get_comment_likes(self) -> int:
        """Returns the number of likes this user's comment shave accumulated"""
        return sum(CommentLike.query.filter_by(comment=comment).count() for comment in self.comments)

    def get_all_likes(self) -> int:
        """Returns the number of likes this user's posts and comments have accumulated"""
        return self.get_post_likes() + self.get_comment_likes()

    def display_about(self) -> str:
        return self.about_me or "This user hasn't written a bio yet."


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, server_default=func.now())
    date_updated = db.Column(db.DateTime, nullable=True)
    comments = db.relationship("Comment", backref='post')
    liked_by = db.relationship("PostLike", backref=db.backref('post', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')

    def get_time_ago(self) -> str:
        delta: datetime.timedelta = datetime.datetime.utcnow() - self.date_posted
        return humanize.naturaldelta(delta)


class PostLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, server_default=func.now())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    date_posted = db.Column(db.DateTime, server_default=func.now())
    liked_by = db.relationship("CommentLike", backref=db.backref('comment', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')


class CommentLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, server_default=func.now())
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
