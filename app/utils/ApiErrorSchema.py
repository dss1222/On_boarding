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


class AuthTokenSchema(Schema):
    token = fields.Str(required=True)


class AuthToken(Document):
    token = StringField(required=True)

    @classmethod
    def create(cls, token_):
        authtoken = cls(token=token_)
        return authtoken


def NotCreateUsername():
    return ApiError(message="이미 존재하는 아이디입니다"), 409


def NotPassword():
    return ApiError(message="잘못된 비밀번호 입니다"), 401


def NotUser():
    return ApiError(message="존재하지 않는 아이디입니다"), 401


def NotFoundBoard():
    return ApiError(message="해당 게시판이 존재하지 않습니다"), 404


def NotFoundPost():
    return ApiError(message="해당 게시글이 존재하지 않습니다"), 404


def NotFoundComment():
    return ApiError(message="해당 댓글이 존재하지 않습니다"), 404


def WrongId():
    return ApiError(message="잘못된 id형식입니다"), 404


def NotCreatedUser():
    return ApiError(message="게시글 작성자가 아닙니다"), 403


def defaultError():
    return ApiError(message="유효하지 않은 요청입니다"), 422
