from flask_mongoengine import MongoEngine
from flask_restful import Api
from flask_login import LoginManager


db = MongoEngine()
api = Api()
login_manager = LoginManager()