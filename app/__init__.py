import os
import secrets

from flask import Flask

from app.routes import init_app
from app.utils.database import close_db


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    secret_key = secrets.token_hex(32)
    app.secret_key = secret_key
    app.config["DATABASE"] = os.path.join(app.root_path, "northwind.db")
    app.teardown_appcontext(close_db)
    init_app(app=app)
    return app
