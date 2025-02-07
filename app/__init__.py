import os

from flask import Flask

from app.routes import init_app
from app.utils.database import close_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config["DATABASE"] = os.path.join(app.root_path, "northwind.db")
    app.teardown_appcontext(close_db)
    init_app(app=app)
    return app
