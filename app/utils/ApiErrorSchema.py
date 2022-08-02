import datetime
import jwt

from bson.json_util import dumps
from flask import current_app
from marshmallow import fields, Schema
from mongoengine import Document, StringField


class ApiErrorSchema(Schema):
    message = fields.String(required=True)


class ApiError(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message


class SuccessSchema(Schema):
    message = fields.String(required=True)


class SuccessDto:
    def __init__(self):
        self.message = "성공"


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
        access_token = AuthToken.create_token(user, 60, "access")
        refresh_token = AuthToken.create_token(user, 3600, "refresh")
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


def NotCreateUsername():
    return ApiError(message="이미 존재하는 아이디입니다"), 409


def NotPassword():
    return ApiError(message="잘못된 비밀번호 입니다"), 401


def NotUser():
    return ApiError(message="존재하지 않는 아이디입니다"), 401


def WrongId():
    return ApiError(message="잘못된 id형식입니다"), 404


def NotCreatedUser():
    return ApiError(message="게시글 작성자가 아닙니다"), 403


def defaultError():
    return ApiError(message="유효하지 않은 요청입니다"), 422
