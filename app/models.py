from mongoengine import Document, StringField

class Users(Document):
    username = StringField(required=True, max_length=32)
    password = StringField(required=True)
    name = StringField(required=True, max_length=32)
    zodiac = StringField(required=True)
