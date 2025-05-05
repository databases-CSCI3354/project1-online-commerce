import os
import secrets

from flask import Flask
from flask_login import LoginManager

from app.models.users import User
from app.routes import init_app
from app.routes.auth import auth_bp
from app.routes.events import events_bp
from app.routes.reviews import reviews_bp
from app.utils.database import close_db
from app.utils.init_db import init_db


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    secret_key = secrets.token_hex(32)
    app.secret_key = secret_key
    app.config["DATABASE"] = os.path.join(app.root_path, "activity.db")

    # Disable template caching during testing
    app.config["TESTING"] = True

    # Initialize database tables
    init_db(app)
    app.teardown_appcontext(close_db)
    init_app(app=app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(reviews_bp)

    return app
