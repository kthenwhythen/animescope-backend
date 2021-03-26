from flask_mongoengine import MongoEngine
from flask_restful import Api
from flask_login import LoginManager
from flask_cors import CORS


db = MongoEngine()
api = Api()
login_manager = LoginManager()
cors = CORS()