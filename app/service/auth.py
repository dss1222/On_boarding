import datetime
import jwt

from bson.json_util import dumps
from flask import current_app
from marshmallow import fields, Schema
from mongoengine import Document, StringField


class AuthAllTokenSchema(Schema):
    access_token = fields.Str(required=True)
    refresh_token = fields.Str(required=True)


class AuthTokenSchema(Schema):
    access_token = fields.Str(required=True)


class AuthToken(Document):
    access_token = StringField(required=True)
    refresh_token = StringField(required=True)

    @classmethod
    def create(cls, user):
        access_token = AuthToken.create_token(user, 3600, "access")
        refresh_token = AuthToken.create_token(user, 3600*24*15, "refresh")
        return cls(access_token=access_token, refresh_token=refresh_token)

    @classmethod
    def create_access_token(cls, user):
        access_token = AuthToken.create_token(user, 60, "access")
        return cls(access_token=access_token)

    @classmethod
    def create_token(cls, user, exp, typ):
        return jwt.encode({"user_id": dumps(user.id), "username": dumps(user.username),
                           "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=exp), "type": typ},
                          current_app.config['SECRET'], current_app.config['ALGORITHM'])
