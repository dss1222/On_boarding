import jwt

from flask_classful import FlaskView, route
from flask import request, g, current_app
from bson.json_util import dumps
from flask_apispec import use_kwargs, marshal_with, doc

from app.user.userSchema import UserCreateSchema, UserSchema, UserUpdateSchema
from app.utils.validator import user_create_validator, user_validator, login_required
from app.utils.ApiErrorSchema import *
from app.Model import *
from app.post.postSchema import *
from app.comment.commentSchema import CommentListSchema


class UserView(FlaskView):
    decorators = (doc(tags=['User']),)

    # 회원가입
    @route('/signup', methods=['POST'])
    @doc(description='User 회원가입', summary='User 회원가입')
    @use_kwargs(UserCreateSchema())
    @marshal_with(ApiErrorSchema, code=200, description="성공")
    @marshal_with(ApiErrorSchema, code=409, description="이미 존재하는 사용자")
    @user_create_validator
    def post(self, user=None):
        if User.objects(username=user.username):
            return NotCreateUsername()
        else:
            user.save()
            return SuccessDto(), 200

    # 로그인
    @route('/login', methods=['POST'])
    @doc(description='User 로그인', summary='User 로그인')
    @use_kwargs(UserSchema())
    @marshal_with(AuthTokenSchema, code=200, description="토큰 발급")
    @marshal_with(ApiErrorSchema, code=401, description="로그인 실패")
    @user_validator
    def login(self, user=None):

        if not user:
            return NotUser()

        if not user.check_password(request.json["password"]):
            return NotPassword()

        token = jwt.encode({"user_id": dumps(user.id), "username": dumps(user.username)},
                           current_app.config['SECRET'], current_app.config['ALGORITHM'])
        # print(jwt.decode())
        return AuthToken.create(token_=token)

    # 회원정보수정
    @route('/update', methods=['PATCH'])
    @doc(description='User 정보 수정', summary='Username 수정')
    @use_kwargs(UserUpdateSchema())
    @marshal_with(SuccessSchema, code=200, description="성공")
    @marshal_with(ApiErrorSchema, code=409, description="이미 존재하는 사용자")
    @marshal_with(ApiErrorSchema, code=422, description="입력값이 잘못됨")
    @login_required
    def update_user(self, username=None):
        if not User.objects(username=username):
            user = User.objects(id=g.user_id).get()
            user.update(username=username)
            return SuccessDto(), 200
        else:
            return NotCreateUsername()

    # 내가 쓴글 조회
    @route('/mypage/posts', methods=['GET'])
    @doc(description='내가 쓴글 조회', summary='내가 쓴글 조회')
    @marshal_with(PostListSchema(many=True), code=200, description="내가 쓴글 조회")
    @login_required
    def get_myposts(self):
        posts = Post.objects(user=g.user_id, is_deleted=False)
        return posts, 200

    # 내가 작성한 코멘트 조회
    @route('/mypage/comments', methods=['GET'])
    @doc(description='내가 쓴 댓글 조회', summary='내가 쓴 댓글 조회')
    @marshal_with(CommentListSchema(many=True), code=200, description="내가 쓴글 조회")
    @login_required
    def get_mycomments(self):
        comments = Comment.objects(user=g.user_id, is_deleted=False)
        return comments, 200

    # 내가 좋아요한 글 조회
    @route('/mypage/posts/likes', methods=['GET'])
    @doc(description='내가 좋아요 한 글 조회', summary='내가 좋아요 한 글 조회')
    @marshal_with(PostListSchema(many=True), code=200, description="내가 좋아요 한 글 조회")
    @login_required
    def get_myposts_likes(self):
        posts = Post.objects(likes__exact=str(g.user_id), is_deleted=False)
        return posts, 200
