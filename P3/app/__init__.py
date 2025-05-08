import os
import secrets

from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
load_dotenv()
from app.models.users import User
from app.routes import init_app
from app.routes.auth import auth_bp
from app.routes.events import events_bp
from app.routes.reviews import reviews_bp
from app.routes.sessions import sessions_bp
from app.routes.members import members_bp
from app.routes.prerequisites import prerequisites_bp
from app.utils.database import close_db, check_db_health
from app.utils.init_db import init_db
from app.utils.logger import setup_logger

log = setup_logger(__name__)

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    secret_key = secrets.token_hex(32)
    app.secret_key = secret_key
    app.config["DATABASE"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "activity.db"))
    log.info(f"Using database at: {app.config['DATABASE']}")

    # Disable template caching during testing
    app.config["TESTING"] = True

    # Initialize database tables
    with app.app_context():
        init_db(app)
        if not check_db_health():
            log.warning("Database health check failed - reinitializing database")
            init_db(app)
            if not check_db_health():
                log.error("Database health check failed after reinitialization")
                raise RuntimeError("Failed to initialize database properly")
        
    app.teardown_appcontext(close_db)
    init_app(app=app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # Set the login view for @login_required

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(sessions_bp, url_prefix="/sessions")
    app.register_blueprint(members_bp, url_prefix="/members")
    app.register_blueprint(prerequisites_bp, url_prefix="/prerequisites")

    return app
