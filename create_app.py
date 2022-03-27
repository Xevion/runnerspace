from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy
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

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import blueprint as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .routes import blueprint as routes_blueprint
    app.register_blueprint(routes_blueprint)

    # CLI commands setup
    @app.shell_context_processor
    def shell_context():
        """Provides specific Flask components to the shell."""
        return {'app': app, 'db': db}

    return app
