from flask import Flask
import os
import certifi

from .extensions import db, api, login_manager, cors
from .main import main


def create_app():
    app = Flask(__name__)
    app.testing = True
    app.config['MONGODB_SETTINGS'] = {
        'db': 'animescope',
        'host': os.environ.get("MONGO_ANIMESCOPE"),
        'tlsCAFile': certifi.where()
    }

    print("1#################################1")
    print(os.environ.get("MONGO_ANIMESCOPE"))
    print("1#################################1")

    db.init_app(app)
    api.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app)

    app.register_blueprint(main)

    return app
