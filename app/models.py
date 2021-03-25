from mongoengine import Document, StringField, DictField, URLField


class Users(Document):
    username = StringField(required=True, max_length=32, unique=True)
    password = StringField(required=True)
    name = StringField(required=True, max_length=32)
    zodiac = StringField(required=True)
    predictions = DictField()


class Predictions(Document):
    img = URLField(required=True)
    text = StringField(required=True)
    source = URLField(required=True)
