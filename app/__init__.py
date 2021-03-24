from flask import Flask

from .extensions import db, api
from .main import main


def create_app(config_object="app.settings"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    api.init_app(app)

    app.register_blueprint(main)

    return app
