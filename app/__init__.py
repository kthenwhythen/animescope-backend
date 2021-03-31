from flask import Flask
import os

from .extensions import db, api, login_manager, cors
from .main import main


def create_app(config_object="app.settings"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    print("1#################################1")
    print(os.environ.get("MONGO_ANIMESCOPE"))
    print("1#################################1")

    db.init_app(app)
    api.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app)

    app.register_blueprint(main)

    return app
