from marshmallow import fields, Schema
from mongoengine import Document, StringField


class ApiErrorSchema(Schema):
    statusCode = fields.Integer(data_key="code", required=True)
    message = fields.String(required=True)


class ApiError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code


class SuccessSchema(Schema):
    statusCode = fields.Integer(data_key="code", required=True)
    message = fields.String(required=True)


class SuccessDto:
    def __init__(self):
        self.statusCode = 200
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
    return ApiError(message="이미 존재하는 아이디입니다", status_code=409), 409


def NotPassword():
    return ApiError(message="잘못된 비밀번호 입니다", status_code=401), 401


def NotUser():
    return ApiError(message="존재하지 않는 아이디입니다", status_code=401), 401


def NotFoundBoard():
    return ApiError(message="해당 게시판이 존재하지 않습니다", status_code=404), 404


def NotFoundPost():
    return ApiError(message="해당 게시글이 존재하지 않습니다", status_code=404), 404


def NotFoundComment():
    return ApiError(message="해당 댓글이 존재하지 않습니다", status_code=404), 404


def WrongId():
    return ApiError(message="잘못된 id형식입니다", status_code=404), 404


def NotCreatedUser():
    return ApiError(message="게시글 작성자가 아닙니다", status_code=403), 403


def NotLoginUser():
    return ApiError(message="로그인이 필요합니다", status_code=403), 403


def NotInvalidToken():
    return ApiError(message="유효하지 않은 토큰입니다", status_code=403), 403


def defaultError():
    return ApiError(message="유효하지 않은 요청입니다", status_code=422), 422
