from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, marshal_with, doc

from app.serializers.user import UserCreateSchema, UserSchema, UserUpdateSchema
from app.service.validator import login_required
from app.utils.ApiErrorSchema import *
from app.service.user import UserService


class UserView(FlaskView):
    decorators = (doc(tags=['User']),)

    # 회원가입
    @route('/signup', methods=['POST'])
    @doc(description='User 회원가입', summary='User 회원가입')
    @use_kwargs(UserCreateSchema())
    @marshal_with(SuccessSchema, code=201, description="성공")
    @marshal_with(ApiErrorSchema, code=409, description="이미 존재하는 사용자")
    def signup(self, username, password):
        result = UserService.signup(username, password)
        if result == 201:
            return "", 201
        elif result == 409:
            return NotCreateUsername()

    # 로그인
    @route('/login', methods=['POST'])
    @doc(description='User 로그인', summary='User 로그인')
    @use_kwargs(UserSchema())
    @marshal_with(AuthTokenSchema, code=200, description="토큰 발급")
    @marshal_with(ApiErrorSchema, code=401, description="로그인 실패")
    def login(self, username, password):
        result = UserService.login(username, password)
        if result == 401:
            return ApiError(message="아이디 혹은 비밀번호가 잘못 됐습니다"), 401
        return result

    # 회원정보수정
    @route('/update', methods=['PATCH'])
    @doc(description='User 정보 수정', summary='Username 수정')
    @use_kwargs(UserUpdateSchema())
    @marshal_with(SuccessSchema, code=201, description="성공")
    @marshal_with(ApiErrorSchema, code=409, description="이미 존재하는 사용자")
    @login_required
    def update(self, username=None):
        result = UserService.user_update(username)
        if result == 201:
            return "", 201
        elif result == 409:
            return NotCreateUsername()
