from flask import Blueprint, redirect
from flask_restful import Resource, abort, reqparse
from flask_login import logout_user, login_required
from mongoengine import ValidationError, NotUniqueError
from werkzeug.security import generate_password_hash

from .extensions import api, login_manager
from .models import Users, Predictions


main = Blueprint("main", __name__)


def abort_if_user_doesnt_exist(username):
    if not Users.objects(username=username).first():
        abort(404, message=f"User with username:'{username}' doesn't exist")


def abort_if_prediction_doesnt_exist(prediction_id):
    if not Predictions.objects(id=prediction_id).first():
        abort(404, message=f"Prediction with id:'{prediction_id}' doesn't exist")


parser = reqparse.RequestParser()
parser.add_argument("username")
parser.add_argument("password")
parser.add_argument("name")
parser.add_argument("zodiac")
parser.add_argument("img")
parser.add_argument("text")
parser.add_argument("source")

# @login_manager.user_loader
# def load_user(username):
#     return Users.objects(username=username).first()


# @app.route("/signin", methods=["GET", "POST"])
# def signin():
#     # form
#     return "Signed in"


# @app.route("/signout")
# @login_required
# def signout():
#     logout_user()
#     return "Signed out"


# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     # form
#     return "Signed up"


# @login_required
class UserResource(Resource):
    def get(self, username):
        abort_if_user_doesnt_exist(username)
        user = Users.objects(username=username).first()
        return {"id": str(user.id), 
                "username": user.username, 
                "name": user.name, 
                "zodiac": user.zodiac,
                "predictions": user.predictions}

    def put(self, username):
        abort_if_user_doesnt_exist(username)
        args = parser.parse_args()
        user = Users.objects(username=username).first()
        user.name = args["name"]
        user.zodiac = args["zodiac"]

        try:
            user.save()
        except ValidationError as error:
            return error.message
            
        return f"User: '{username}' was changed"

    def delete(self, username):
        abort_if_user_doesnt_exist(username)
        Users.objects(username=username).first().delete()
        return f"User: '{username}' was deleted"


class UsersResource(Resource):
    def get(self):
        users = [{"id": str(user.id), 
                  "username": user.username, 
                  "name": user.name,
                  "zodiac": user.zodiac, 
                  "predictions": user.predictions} for user in Users.objects()]
        return users

    def post(self):
        args = parser.parse_args()
        new_user = Users()
        new_user.username = args["username"].lower()

        password = args["password"]
        if password:
            new_user.password = generate_password_hash(args["password"], method="pbkdf2:sha256", salt_length=8)
        else:
            abort(404, message=f"Password can't be null")

        new_user.name = args["name"]
        new_user.zodiac = args["zodiac"]

        try:
            new_user.save()
        except ValidationError as error:
            return error.message
        except NotUniqueError as error:
            return "username not unique"

        return f"User: '{new_user.username}' was created"


# @login_required
class PredictionResource(Resource):
    def get(self, prediction_id):
        abort_if_prediction_doesnt_exist(prediction_id)
        prediction = Predictions.objects.get(id=prediction_id)
        return {"id": str(prediction.id), 
                "img": prediction.img, 
                "text": prediction.text, 
                "source": prediction.source}

    def put(self, prediction_id):
        abort_if_prediction_doesnt_exist(prediction_id)
        args = parser.parse_args()
        prediction = Predictions.objects.get(id=prediction_id)
        prediction.img = args["img"]
        prediction.text = args["text"]
        prediction.source = args["source"]

        try:
            prediction.save()
        except ValidationError as error:
            return error.message
        
        return f"Prediction: '{prediction_id}' was changed"

    def delete(self, prediction_id):
        abort_if_prediction_doesnt_exist(prediction_id)
        Predictions.objects.get(id=prediction_id).delete()
        return f"Prediction: '{prediction_id}' was deleted"


class PredictionsResource(Resource):
    def get(self):
        predictions = [{"id": str(prediction.id), 
                        "img": prediction.img, 
                        "text": prediction.text,
                        "source": prediction.source} for prediction in Predictions.objects()]
        return predictions

    def post(self):
        args = parser.parse_args()
        new_prediction = Predictions()
        new_prediction.img = args["img"]
        new_prediction.text = args["text"]
        new_prediction.source = args["source"]

        try:
            new_prediction.save()
        except ValidationError as error:
            return error.message, 400
        
        return "fine", 201


api.add_resource(UserResource, "/user/<string:username>")
api.add_resource(UsersResource, "/users")
api.add_resource(PredictionResource, "/prediction/<string:prediction_id>")
api.add_resource(PredictionsResource, "/predictions")
