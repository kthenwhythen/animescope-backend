from flask import Blueprint
from flask_restful import Resource

from .extensions import api
from .models import Users


main = Blueprint("main", __name__)


class UserApi(Resource):
    def get(self, username):
        user = Users.objects(username=username).first()
        return {"username": user.username, "zodiac": user.zodiac}

    def put(self, username):
        try:
            new_user = Users(username=username)
            new_user.password = '123321'
            new_user.name = 'asakura'
            new_user.save()
        except ValidationError as error:
            return error.message


api.add_resource(UserApi, "/user/<string:username>")
