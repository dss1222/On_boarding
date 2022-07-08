import json
import jwt

from functools import wraps
from flask import request, g, jsonify, current_app
from bson.json_util import loads
from marshmallow import ValidationError

from app.utils.ErrorHandler import *
from app.user.userSchema import UserSchema, UserCreateSchema
from app.post.postModel import Post


# 로그인 인증 데코레이터
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not 'Authorization' in request.headers:
            return NotLoginUser()

        try:
            access_token = request.headers.get('Authorization')
            payload = jwt.decode(access_token, current_app.config['SECRET'], current_app.config['ALGORITHM'])

        except jwt.InvalidTokenError:
            return NotInvalidToken()

        g.user_id = loads(payload['user_id'])  # 토큰에 있는 내 정보
        g.username = loads(payload['username'])

        return f(*args, **kwargs)

    return decorated_function


#  유저 validation check
def user_validator(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        try:
            UserSchema().load(json.loads(request.data))

        except ValidationError as err:
            return jsonify(err.messages), 422

        return f(*args, **kwargs)

    return decorated_view


# 회원가입 validation check
def user_create_validator(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        try:
            UserCreateSchema().load(json.loads(request.data))

        except ValidationError as err:
            return jsonify(err.messages), 422

        return f(*args, **kwargs)

    return decorated_view


def post_validator(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        post_id = kwargs['post_id']

        if len(post_id) != 24:
            return WrongId()

        if not Post.objects(id=post_id):
            return NotFoundPost()

        return f(*args, **kwargs)

    return decorated_view


def comment_validator(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        comment_id = kwargs['comment_id']

        if bytes(comment_id) != 12:
            return WrongId()

        if not Post.objects(id=comment_id):
            return NotFoundComment()

        return f(*args, **kwargs)

    return decorated_view
