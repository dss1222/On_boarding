import bcrypt

from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, marshal_with, doc
from flask import g

from app.serializers.user import UserCreateFormSchema, UserDetailSchema, UserUpdateFormSchema
from app.service.validator import login_required, token_refresh_validator
from app.utils.ApiErrorSchema import SuccessSchema, ApiError, ApiErrorSchema, NotCreateUsername
from app.service.auth import AuthToken, AuthTokenSchema, AuthAllTokenSchema

from app.models.user import User


class UserView(FlaskView):
    decorators = (doc(tags=['User']),)

    # 회원가입
    @route('/signup', methods=['POST'])
    @doc(description='유저 회원가입', summary='유저 회원가입')
    @use_kwargs(UserCreateFormSchema())
    @marshal_with(SuccessSchema, code=201, description="성공")
    @marshal_with(ApiErrorSchema, code=409, description="이미 존재하는 사용자")
    def signup(self, username, password):
        if User.objects(username=username):
            return NotCreateUsername()
        else:
            hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            user = User(username=username, password=hash_password, provider='default')
            user.save()
            return "", 201

    # 로그인
    @route('/login', methods=['POST'])
    @doc(description='유저 로그인', summary='유저 로그인')
    @use_kwargs(UserDetailSchema())
    @marshal_with(AuthAllTokenSchema, code=200, description="토큰 발급")
    @marshal_with(ApiErrorSchema, code=401, description="로그인 실패")
    def login(self, username, password):
        if not User.objects(username=username):
            return ApiError(message="아이디가 잘못 됐습니다"), 401
        else:
            user = User.objects().get(username=username)

        if user.provider == 'default':
            if not user.check_password(password):
                return ApiError(message="비밀번호가 잘못 됐습니다"), 401
        return AuthToken.create(user=user)

    @route('/check', methods=['GET'])
    @doc(description='유저 상태 확인', summary='유저 상태 확인')
    @marshal_with(UserDetailSchema, code=200, description='유저 상태 확인 성공')
    @login_required
    def check(self):
        user = User.objects().get(id=g.user_id)
        return user

    # 회원정보수정
    @route('/update', methods=['PATCH'])
    @doc(description='유저 정보 수정', summary='유저 정 수정')
    @use_kwargs(UserUpdateFormSchema())
    @marshal_with(SuccessSchema, code=201, description="성공")
    @marshal_with(ApiErrorSchema, code=409, description="이미 존재하는 사용자")
    @login_required
    def update(self, username=None):
        if not User.objects(username=username):
            user = User.objects().get(id=g.user_id)
            user.update(username=username)
            return "", 201
        else:
            return NotCreateUsername()

    @route('/refresh', methods=['GET'])
    @doc(description='토큰 재발급', summary='토큰 재발급')
    @marshal_with(AuthTokenSchema, code=200, description="토큰 발급")
    @token_refresh_validator
    def refresh(self):
        user = User.objects().get(id=g.user_id)
        return AuthToken.create_access_token(user=user)
