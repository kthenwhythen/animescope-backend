from flask import Flask, request
from flask_restful import Resource, Api
# from pymongo import MongoClient
from mongoengine import connect, ValidationError
import certifi
from werkzeug.security import generate_password_hash, check_password_hash
import os

from models import Users


app = Flask(__name__)
api = Api(app)
# app.config["MONGO_URI"] = "mongodb+srv://null-architect:fanattetrisa@cluster0.dokwo.mongodb.net/animescope?retryWrites=true&w=majority"
# client = MongoClient("mongodb+srv://null-architect:fanattetrisa@cluster0.dokwo.mongodb.net/animescope?retryWrites=true&w=majority", tlsCAFile=certifi.where())
# db = client.animescope
connect(host=os.getenv("MONGODB_ANIMESCOPE"), tlsCAFile=certifi.where())


class UserApi(Resource):
    def get(self, username):
        # user = db.users.find_one({"username": username.lower()})
        # if user:
        #     return {"id": str(user["_id"]), "username": username}
        # return "user not exist"
        user = Users.objects(username=username).first()
        return {"username": user.username, "zodiac": user.zodiac}

    def put(self, username):
        # if not (db.users.find_one({"username": username.lower()})):
        #     password = generate_password_hash(request.form["password"], method="pbkdf2:sha256", salt_length=8)
        #     db.users.insert_one({"username": username.lower(), "password": password, "name": request.form["name"], "zodiac": request.form["zodiac"]})
        #     return "user added"
        # return "user exist"
        try:
            new_user = Users(username=username)
            new_user.password = '123321'
            new_user.name = 'asakura'
            new_user.save()
        except ValidationError as error:
            return error.message

api.add_resource(UserApi, "/user/<string:username>")


# @app.route("/")
# def hello():
#     hello = {"numbers": [1, 2, 3, 4, 5], "name": "hello"}
#     return jsonify({"output": hello})
