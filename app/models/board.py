from flask_mongoengine import Document
from mongoengine import StringField


class Board(Document):
    name = StringField(required=True)










