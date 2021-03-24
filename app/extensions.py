from flask_mongoengine import MongoEngine
from flask_restful import Api

db = MongoEngine()
api = Api()