import os
import secrets

from flask import Flask

from app.routes import init_app
from app.utils.database import close_db
from app.utils.init_db import init_db


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    secret_key = secrets.token_hex(32)
    app.secret_key = secret_key
    app.config["DATABASE"] = os.path.join(app.root_path, "northwind.db")
    
    # Disable template caching during testing
    app.config["TESTING"] = True
    
    # Initialize database tables
    web_employee_id = init_db(app)
    app.config["WEB_EMPLOYEE_ID"] = web_employee_id
    
    app.teardown_appcontext(close_db)
    init_app(app=app)
    return app
