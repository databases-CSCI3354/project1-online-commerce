from flask import Blueprint

from app.routes.auth import auth_bp
from app.routes.main import main_bp
from app.routes.status import status_bp


def init_app(app: Blueprint):
    """Initialize all blueprints with the app"""
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(status_bp, url_prefix="/status")
