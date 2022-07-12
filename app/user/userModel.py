import datetime
import bcrypt

from flask_mongoengine import Document
from mongoengine import StringField, DateTimeField


class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now())

    def check_password(self, password):
        if not bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8')):
            return False
        else:
            return True

    def update_token(self, token):
        self.update(token=token)