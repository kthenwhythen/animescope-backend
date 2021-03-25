from flask import Blueprint
from flask_restful import Resource, abort, reqparse
from flask_login import logout_user, login_required
from mongoengine import ValidationError, NotUniqueError

from .extensions import api, login_manager
from .models import Users, Predictions


main = Blueprint("main", __name__)


def abort_if_user_doesnt_exist(username):
    if not Users.objects(username=username):
        abort(404, message=f"User with username:'{username}' doesn't exist")


def abort_if_prediction_doesnt_exist(id):
    if not Predictions.objects(id=id):
        abort(404, message=f"Prediction with id:'{id}' doesn't exist")


parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('name')
parser.add_argument('zodiac')

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
        user.name = args['name']
        user.zodiac = args['zodiac']
        user.save()
        return f"User: '{username}' was changed"

    def delete(self, username):
        abort_if_user_doesnt_exist(username)
        Users.objects(username=username).first().delete()
        return f"User: '{username}' was deleted", 204


class UsersResource(Resource):
    def get(self):
        users = [{"id": str(user.id), 
                  "username": user.username, 
                  "name": user.name,
                  "zodiac": user.zodiac, 
                  "predictions": user.predictions} for user in Users.objects()]
        return users

    def post(self):
        try:
            args = parser.parse_args()
            new_user = Users()
            new_user.username = args['username']
            new_user.password = args['password']
            new_user.name = args['name']
            new_user.zodiac = args['zodiac']
            new_user.save()
        except ValidationError as error:
            return error.message
        except NotUniqueError as error:
            return "Not unique username"
        return f"User: '{new_user.username}' was created"


# @login_required
class PredictionResource(Resource):
    def get(self, id):
        abort_if_prediction_doesnt_exist(id)
        user = Users.objects(username=username).first()
        return {"id": str(user.id), 
                "username": user.username, 
                "name": user.name, 
                "zodiac": user.zodiac,
                "predictions": user.predictions}

    def put(self, id):
        abort_if_prediction_doesnt_exist(id)
        args = parser.parse_args()
        user = Users.objects(username=username).first()
        user.name = args['name']
        user.zodiac = args['zodiac']
        user.save()
        return f"User: '{username}' was changed"

    def delete(self, id):
        abort_if_prediction_doesnt_exist(id)
        Users.objects(username=username).first().delete()
        return f"User: '{username}' was deleted", 204


class PredictionsResource(Resource):
    def get(self):
        predictions = [{"id": str(prediction.id), 
                        "img": prediction.img, 
                        "text": prediction.text,
                        "source": prediction.source} for prediction in Predictions.objects()]
        return predictions

    def post(self):
        try:
            args = parser.parse_args()
            new_prediction = Predictions()
            new_prediction.img = args['img']
            new_prediction.text = args['text']
            new_prediction.source = args['source']
            new_prediction.save()
        except ValidationError as error:
            return error.message
        return f"Prediction was created"


api.add_resource(UserResource, "/user/<string:username>")
api.add_resource(UsersResource, "/users")
api.add_resource(PredictionResource, "/prediction/<string:prediction_id>")
api.add_resource(PredictionsResource, "/predictions")
