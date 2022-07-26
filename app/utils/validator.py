import json
import jwt
import mongoengine.errors
from flask_apispec import marshal_with

from functools import wraps
from flask import request, g, current_app
from bson.json_util import loads
from marshmallow import ValidationError

from app.serializers.userSchema import UserSchema, UserCreateSchema
from app.serializers.postSchema import PostCreateSchema
from app.serializers.boardSchema import BoardCreateSchema
from app.serializers.commentSchema import CommentCreateSchema
from app.utils.enumOrder import OrderEnum
from app.utils.ApiErrorSchema import *
from app.Model import *


# 로그인 인증 데코레이터
def login_required(f):
    @wraps(f)
    @marshal_with(ApiErrorSchema, code=401, description="유효하지 않은 토큰입니다")
    @marshal_with(ApiErrorSchema, code=422, description="유효하지 않은 토큰입니다")
    @marshal_with(ApiErrorSchema, code=403, description="유효하지 않은 토큰입니다")
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

        if not User.objects(id=g.user_id):
            return NotInvalidToken()
        marshal_with(ApiErrorSchema, code=401, description="유효하지 않은 토큰입니다")(f)
        return f(*args, **kwargs)

    return decorated_function


#  유저 validation check
def user_validator(f):
    @wraps(f)
    @marshal_with(ApiErrorSchema, code=422, description="잘못된 요청")
    def decorated_view(*args, **kwargs):
        try:
            user = UserSchema().load(json.loads(request.data))

        except ValidationError as err:
            return defaultError()

        return f(*args, **kwargs)

    return decorated_view


# 회원가입 validation check
def user_create_validator(f):
    @wraps(f)
    @marshal_with(ApiErrorSchema, code=422, description="잘못된 요청")
    def decorated_view(*args, **kwargs):
        try:
            user = UserCreateSchema().load(json.loads(request.data))

        except ValidationError as err:
            return ApiError(message=err.messages), 422

        return f(*args, **kwargs)

    return decorated_view


def create_post_validator(f):
    @wraps(f)
    @marshal_with(ApiErrorSchema, code=422, description="잘못된 요청")
    def decorated_view(*args, **kwargs):
        try:
            PostCreateSchema().load(json.loads(request.data))
        except ValidationError as err:
            return ApiError(message=err.messages), 422

        return f(*args, **kwargs)

    return decorated_view


def post_validator(f):
    @wraps(f)
    @marshal_with(ApiErrorSchema, code=404, description="없는 게시물")
    def decorated_view(*args, **kwargs):
        post_id = kwargs['post_id']
        if len(post_id) != 24:
            return WrongId()

        if not Post.objects(id=post_id, is_deleted=False):
            return NotFoundPost()

        return f(*args, **kwargs)

    return decorated_view


def post_user_validator(f):
    @wraps(f)
    @marshal_with(ApiErrorSchema, code=404, description="없는 게시물")
    @marshal_with(ApiErrorSchema, code=403, description="작성자가 아님")
    def decorated_function(*args, **kwargs):
        post = Post.objects(id=kwargs["post_id"])
        if (not post) or post.get().is_deleted:
            return NotFoundPost()
        try:
            post.get().user.id != g.user_id
        except mongoengine.errors.DoesNotExist:
            return NotCreatedUser()
        return f(*args, **kwargs)

    return decorated_function


def post_list_validator(f):
    @wraps(f)
    @marshal_with(ApiErrorSchema, code=422, description="잘못된 요청")
    def decorated_view(*args, **kwargs):
        params = request.args.to_dict()

        if "page" not in params or "size" not in params or "orderby" not in params or int(params["page"]) < 1:
            return defaultError()

        try:
            result = OrderEnum[str(params["orderby"])].value
        except KeyError:
            return defaultError()

        return f(*args, **kwargs)

    return decorated_view


def create_comment_validator(f):
    @wraps(f)
    @marshal_with(ApiErrorSchema, code=422, description="잘못된 요청")
    def decorated_view(*args, **kwargs):
        try:
            CommentCreateSchema().load(json.loads(request.data))
        except ValidationError as err:
            return ApiError(message=err.messages), 422

        return f(*args, **kwargs)

    return decorated_view


def comment_validator(f):
    @wraps(f)
    @marshal_with(ApiErrorSchema, code=404, description="없는 게시물")
    @marshal_with(ApiErrorSchema, code=422, description="잘못된 요청")
    def decorated_view(*args, **kwargs):
        comment_id = kwargs['comment_id']

        if len(comment_id) != 24:
            return WrongId()

        if not Comment.objects(id=comment_id, is_deleted=False):
            return NotFoundComment()

        return f(*args, **kwargs)

    return decorated_view


def board_crate_validator(f):
    @wraps(f)
    @marshal_with(ApiErrorSchema, code=422, description="잘못된 요청")
    def decorated_view(*args, **kwargs):
        try:
            BoardCreateSchema().load(json.loads(request.data))
        except ValidationError as err:
            return err

        return f(*args, **kwargs)

    return decorated_view


def board_validator(f):
    @wraps(f)
    @marshal_with(ApiErrorSchema, code=404, description="없는 게시판")
    @marshal_with(ApiErrorSchema, code=422, description="잘못된 요청")
    def decorated_view(*args, **kwargs):
        board_id = kwargs['board_id']

        if len(board_id) != 24:
            return WrongId()

        if not Board.objects(id=board_id):
            return NotFoundBoard()

        return f(*args, **kwargs)

    return decorated_view
