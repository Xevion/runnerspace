import random
from datetime import datetime

import click
import pytz
from faker import Faker
from flask import Flask, render_template, request
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
# init SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret key goes here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User, Post, Comment

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import blueprint as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .routes import blueprint as routes_blueprint
    app.register_blueprint(routes_blueprint)

    from .forms import blueprint as forms_blueprint
    app.register_blueprint(forms_blueprint)

    @app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        return render_template('errors/404.html'), 404

    @app.before_request
    def update_last_seen():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.now(tz=pytz.UTC)  # datetime.utcnow doesn't actually attach a timezone
            current_user.last_ip = str(request.remote_addr)
            db.session.add(current_user)
            db.session.commit()

    @app.context_processor
    def inject():
        return dict(now=datetime.utcnow)

    # CLI commands setup
    @app.shell_context_processor
    def shell_context():
        """Provides specific Flask components to the shell."""
        return {'app': app, 'db': db}

    @app.cli.command("fake")
    @click.argument("count")
    def create_fake_users(count: int):
        fake = Faker()
        count = int(count)
        users = {}
        for _ in range(count):
            profile: dict = fake.simple_profile()
            users[profile['username']] = profile

        for profile in users.values():
            new_user = User(username=profile['username'],
                            name=profile['name'],
                            password=generate_password_hash('password', method='sha256'),
                            about_me=fake.paragraph(nb_sentences=5))
            db.session.add(new_user)

        print(f'Committing {len(users)} users into DB.')
        db.session.commit()

        all_users: List[User] = User.query.all()

        post_count: int = 0
        for author in random.choices(all_users, k=count // 2):
            new_post = Post(author=author.id, text=fake.paragraph(nb_sentences=2))
            db.session.add(new_post)
            post_count += 1

        print(f'Committing {post_count} posts into the DB.')
        db.session.commit()

        comment_count: int = 0
        for post in Post.query.all():
            for _ in range(random.randint(3, len(all_users) // 4)):
                new_comment = Comment(text=fake.paragraph(nb_sentences=1), author=random.choice(all_users).id, post=post.id)
                db.session.add(new_comment)
                comment_count += 1

        print(f'Committing {comment_count} comments into the DB.')
        db.session.commit()

    @app.cli.command("create_all")
    def db_create_all() -> None:
        db.create_all(app=app)

    return app
