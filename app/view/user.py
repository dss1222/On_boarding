from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, marshal_with, doc

from app.serializers.user import UserCreateSchema, UserSchema, UserUpdateSchema
from app.service.validator import login_required
from app.utils.ApiErrorSchema import *
from app.serializers.post import *
from app.serializers.comment import CommentListSchema
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

    # 내가 쓴글 조회
    @route('/mypage/posts', methods=['GET'])
    @doc(description='내가 쓴글 조회', summary='내가 쓴글 조회')
    @marshal_with(PostListSchema(many=True), code=200, description="내가 쓴글 조회")
    @login_required
    def get_myposts(self):
        return UserService.get_myposts()

    # 내가 작성한 코멘트 조회
    @route('/mypage/comments', methods=['GET'])
    @doc(description='내가 쓴 댓글 조회', summary='내가 쓴 댓글 조회')
    @marshal_with(CommentListSchema(many=True), code=200, description="내가 쓴글 조회")
    @login_required
    def get_mycomments(self):
        return UserService.get_mycomments()

    # 내가 좋아요한 글 조회
    @route('/mypage/posts/likes', methods=['GET'])
    @doc(description='내가 좋아요 한 글 조회', summary='내가 좋아요 한 글 조회')
    @marshal_with(PostListSchema(many=True), code=200, description="내가 좋아요 한 글 조회")
    @login_required
    def get_myposts_likes(self):
        return UserService.get_mylikes()
