from flask import Flask

from app.routes.auth import auth_bp
from app.routes.events import events_bp
from app.routes.main import main_bp
from app.routes.members import members_bp
from app.routes.prerequisites import prerequisites_bp
from app.routes.reviews import reviews_bp
from app.routes.sessions import sessions_bp


def init_app(app: Flask):
    """Initialize all blueprints with the app"""
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(sessions_bp)
    app.register_blueprint(prerequisites_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(members_bp)
