from marshmallow import fields, Schema


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
