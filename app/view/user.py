from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, marshal_with, doc

from app.serializers.user import UserCreateFormSchema, UserDetailSchema, UserUpdateFormSchema
from app.service.validator import login_required, token_refresh_validator
from app.utils.ApiErrorSchema import *
from app.service.auth import *
from app.service.user import UserService


class UserView(FlaskView):
    decorators = (doc(tags=['User']),)

    # 회원가입
    @route('/signup', methods=['POST'])
    @doc(description='유저 회원가입', summary='유저 회원가입')
    @use_kwargs(UserCreateFormSchema())
    @marshal_with(SuccessSchema, code=201, description="성공")
    @marshal_with(ApiErrorSchema, code=409, description="이미 존재하는 사용자")
    def signup(self, username, password):
        result = UserService.signup(username, password) #
        if result == 201:
            return "", 201
        elif result == 409:
            return NotCreateUsername()

    # 로그인
    @route('/login', methods=['POST'])
    @doc(description='유저 로그인', summary='유저 로그인')
    @use_kwargs(UserDetailSchema())
    @marshal_with(AuthAllTokenSchema, code=200, description="토큰 발급")
    @marshal_with(ApiErrorSchema, code=401, description="로그인 실패")
    def login(self, username, password):
        result = UserService.login(username, password)
        if result == 401:
            return ApiError(message="아이디 혹은 비밀번호가 잘못 됐습니다"), 401
        return result

    @route('/check', methods=['GET'])
    @doc(description='유저 상태 확인', summary='유저 상태 확인')
    @marshal_with(UserDetailSchema, code=200, description='유저 상태 확인 성공')
    @login_required
    def check(self):
        return UserService.check()

    # 회원정보수정
    @route('/update', methods=['PATCH'])
    @doc(description='유저 정보 수정', summary='유저 정 수정')
    @use_kwargs(UserUpdateFormSchema())
    @marshal_with(SuccessSchema, code=201, description="성공")
    @marshal_with(ApiErrorSchema, code=409, description="이미 존재하는 사용자")
    @login_required
    def update(self, username=None):
        result = UserService.user_update(username)
        if result == 201:
            return "", 201
        elif result == 409:
            return NotCreateUsername()

    @route('/refresh', methods=['GET'])
    @doc(description='토큰 재발급', summary='토큰 재발급')
    @marshal_with(AuthTokenSchema, code=200, description="토큰 발급")
    @token_refresh_validator
    def refresh(self):
        result = UserService.refresh()
        return result
