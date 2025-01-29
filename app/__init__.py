from flask import Flask

from app.routes import init_app as init_routes


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    init_routes(app)
    return app
