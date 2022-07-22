import json
import jwt
import bcrypt

from functools import wraps
from flask import request, g, current_app
from bson.json_util import loads
from marshmallow import ValidationError

from app.utils.ErrorHandler import *
from app.user.userSchema import UserSchema, UserCreateSchema
from app.post.postSchema import PostCreateSchema
from app.post.postModel import Post
from app.board.boardSchema import BoardCreateSchema
from app.board.boardModel import Board
from app.comment.commentModel import Comment
from app.comment.commentSchema import CommentCreateSchema
from app.user.userModel import User
from app.utils.enumOrder import OrderEnum
from app.utils.error.ApiErrorSchema import *


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
            user = UserSchema().load(json.loads(request.data))

        except ValidationError as err:
            return jsonify(err.messages), 422

        return f(*args, **kwargs)

    return decorated_view


# 회원가입 validation check
def user_create_validator(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        try:
            user = UserCreateSchema().load(json.loads(request.data))

        except ValidationError as err:
            return ApiError(message="잘못된 요청입니다"), 422

        return f(*args, **kwargs)

    return decorated_view


def create_post_validator(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        try:
            PostCreateSchema().load(json.loads(request.data))
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

        if not Post.objects(id=post_id, is_deleted=False):
            return NotFoundPost()

        return f(*args, **kwargs)

    return decorated_view


def post_list_validator(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        params = request.args.to_dict()

        if "page" not in params or "size" not in params or "orderby" not in params or int(params["page"]) < 1:
            return NotApiError()

        try:
            result = OrderEnum[str(params["orderby"])].value
        except KeyError:
            return NotApiError()

        return f(*args, **kwargs)

    return decorated_view


def create_comment_validator(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        try:
            CommentCreateSchema().load(json.loads(request.data))
        except ValidationError as err:
            return jsonify(err.messages), 422

        return f(*args, **kwargs)

    return decorated_view


def comment_validator(f):
    @wraps(f)
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
    def decorated_view(*args, **kwargs):
        try:
            BoardCreateSchema().load(json.loads(request.data))
        except ValidationError as err:
            return ErrorResponseDto(CreatedError())

        return f(*args, **kwargs)

    return decorated_view


def board_validator(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        board_id = kwargs['board_id']

        if len(board_id) != 24:
            return WrongId()

        if not Board.objects(id=board_id):
            return NotFoundComment()

        return f(*args, **kwargs)

    return decorated_view
