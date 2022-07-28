from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, marshal_with, doc

from app.serializers.userSchema import UserCreateSchema, UserSchema, UserUpdateSchema
from app.utils.validator import user_create_validator, user_validator, login_required, marshal_empty
from app.utils.ApiErrorSchema import *
from app.serializers.postSchema import *
from app.serializers.commentSchema import CommentListSchema
from app.service.userService import UserService


class UserView(FlaskView):
    decorators = (doc(tags=['User']),)

    # 회원가입
    @route('/signup', methods=['POST'])
    @doc(description='User 회원가입', summary='User 회원가입')
    @use_kwargs(UserCreateSchema())
    @marshal_with(SuccessSchema, code=200, description="성공")
    @marshal_with(ApiErrorSchema, code=409, description="이미 존재하는 사용자")
    @user_create_validator
    def post(self, user=None):
        return UserService.user_signup(user)

    # 로그인
    @route('/login', methods=['POST'])
    @doc(description='User 로그인', summary='User 로그인')
    @use_kwargs(UserSchema())
    @marshal_with(AuthTokenSchema, code=200, description="토큰 발급")
    @marshal_with(ApiErrorSchema, code=401, description="로그인 실패")
    @user_validator
    def login(self, user=None):
        return UserService.user_login(user)

    # 회원정보수정
    @route('/update', methods=['PATCH'])
    @doc(description='User 정보 수정', summary='Username 수정')
    @use_kwargs(UserUpdateSchema())
    @marshal_with(SuccessSchema, code=200, description="성공")
    @marshal_with(ApiErrorSchema, code=409, description="이미 존재하는 사용자")
    @marshal_with(ApiErrorSchema, code=422, description="입력값이 잘못됨")
    @login_required
    def update_user(self, username=None):
        return UserService.user_update(username)

    # 내가 쓴글 조회
    @route('/mypage/posts', methods=['GET'])
    @doc(description='내가 쓴글 조회', summary='내가 쓴글 조회')
    @marshal_with(PostListSchema(many=True), code=200, description="내가 쓴글 조회")
    @login_required
    def get_myposts(self):
        return UserService.user_get_myposts()

    # 내가 작성한 코멘트 조회
    @route('/mypage/comments', methods=['GET'])
    @doc(description='내가 쓴 댓글 조회', summary='내가 쓴 댓글 조회')
    @marshal_with(CommentListSchema(many=True), code=200, description="내가 쓴글 조회")
    @login_required
    def get_mycomments(self):
        return UserService.user_get_mycomments()

    # 내가 좋아요한 글 조회
    @route('/mypage/posts/likes', methods=['GET'])
    @doc(description='내가 좋아요 한 글 조회', summary='내가 좋아요 한 글 조회')
    @marshal_with(PostListSchema(many=True), code=200, description="내가 좋아요 한 글 조회")
    @login_required
    def get_myposts_likes(self):
        return UserService.user_get_mylikes()
