import jwt
import mongoengine.errors
from flask_apispec import marshal_with

from functools import wraps
from flask import request, g, current_app
from bson.json_util import loads

from app.utils.ApiErrorSchema import *
from app.models.Model import *


# 로그인 인증 데코레이터
def login_required(f):
    @wraps(f)
    @marshal_with(ApiErrorSchema, code=403, description="유효하지 않은 토큰입니다")
    def decorated_function(*args, **kwargs):

        if not 'Authorization' in request.headers:
            return ApiError(message="로그인이 필요합니다"), 403
        try:
            access_token = request.headers.get('Authorization')
            payload = jwt.decode(access_token, current_app.config['SECRET'], current_app.config['ALGORITHM'])

        except jwt.InvalidTokenError:
            return ApiError(message="유효하지 않은 토큰입니다"), 403

        g.user_id = loads(payload['user_id'])  # 토큰에 있는 내 정보

        # if not User.objects(id=g.user_id):
        #     return ApiError(message="유효하지 않은 토큰입니다"), 403

        g.username = loads(payload['username'])

        return f(*args, **kwargs)

    marshal_with(ApiErrorSchema, code=403, description="유효하지 않은 토큰입니다")(f)
    return decorated_function


def post_validator(f):
    @wraps(f)
    @marshal_with(ApiErrorSchema, code=404, description="없는 게시물")
    def decorated_view(*args, **kwargs):
        post_id = kwargs['post_id']
        if len(post_id) != 24:
            return WrongId()

        if not Post.objects(id=post_id, is_deleted=False):
            return ApiError(message="없는 게시글 입니다"), 404

        return f(*args, **kwargs)

    marshal_with(ApiErrorSchema, code=404, description="없는 게시물")(f)
    return decorated_view


def post_user_validator(f):
    @wraps(f)
    @marshal_with(ApiErrorSchema, code=404, description="없는 게시물")
    @marshal_with(ApiErrorSchema, code=403, description="작성자가 아님")
    def decorated_function(*args, **kwargs):
        post = Post.objects(id=kwargs["post_id"])
        if (not post) or post.get().is_deleted:
            return ApiError(message="없는 게시글 입니다"), 404
        try:
            post.get().user.id != g.user_id
        except mongoengine.errors.DoesNotExist:
            return NotCreatedUser()
        return f(*args, **kwargs)

    marshal_with(ApiErrorSchema, code=404, description="없는 게시물")(f)
    marshal_with(ApiErrorSchema, code=403, description="작성자가 아님")(f)
    return decorated_function


def comment_validator(f):
    @wraps(f)
    @marshal_with(ApiErrorSchema, code=404, description="없는 댓글")
    @marshal_with(ApiErrorSchema, code=422, description="잘못된 요청")
    def decorated_view(*args, **kwargs):
        comment_id = kwargs['comment_id']

        if len(comment_id) != 24:
            return WrongId()

        if not Comment.objects(id=comment_id, is_deleted=False):
            return ApiError(message="없는 댓글입니다"), 404

        return f(*args, **kwargs)

    marshal_with(ApiErrorSchema, code=404, description="없는 게시물")(f)
    marshal_with(ApiErrorSchema, code=422, description="잘못된 요청")(f)
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
            return ApiError(message="없는 게시판 입니다"), 404

        return f(*args, **kwargs)

    marshal_with(ApiErrorSchema, code=404, description="없는 게시판")(f)
    marshal_with(ApiErrorSchema, code=422, description="잘못된 요청")(f)
    return decorated_view
