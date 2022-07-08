import datetime
import enum
import bcrypt

from flask_mongoengine import Document
from mongoengine import StringField, DateTimeField, ReferenceField, ListField, BooleanField


class Board(Document):
    name = StringField(required=True)