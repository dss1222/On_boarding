import json

import bcrypt
import jwt

from flask_classful import FlaskView, route
from flask import request, g, current_app
from bson.json_util import dumps
from webargs import fields
from flask_apispec import use_kwargs, marshal_with, doc

from app.user.userSchema import UserCreateSchema, UserSchema, UserUpdateSchema
from app.user.userModel import User
from app.utils.validator import user_create_validator, user_validator, login_required
from app.utils.ErrorHandler import *

from app.post.postSchema import PostListSchema
from app.post.postModel import Post
from app.comment.commentSchema import CommentListSchema
from app.comment.commentModel import Comment


class UserView(FlaskView):
    # decorators = (
    #     doc(tags=['User']),
    # )

    # 회원가입
    @route('/signup', methods=['POST'])
    # @doc(description='User 회원가입', summary='User 회원가입')
    # @use_kwargs(UserCreateSchema(), locations=('json',))
    @user_create_validator
    def signup(self):
        user_schema = UserCreateSchema().load(json.loads(request.data))
        user = User(username=user_schema['username'], password=user_schema['password'])
        user.save()
        return Success()

    # 로그인
    @route('/login', methods=['POST'])
    @user_validator
    def login(self):
        login_request = json.loads(request.data)
        user = UserSchema().load(login_request)

        user = User.objects(username=user['username']).get()

        if not user.check_password(login_request['password']):
            return {'message': '잘못된 비밀번호 입니다'}, 401

        token = jwt.encode({"user_id": dumps(user.id), "username": dumps(user.username)},
                           current_app.config['SECRET'], current_app.config['ALGORITHM'])
        # print(jwt.decode())
        return jsonify(token), 200

    # 회원정보수정
    @route('/update', methods=['PATCH'])
    @login_required
    def update_user(self):
        data = UserUpdateSchema().load(json.loads(request.data))
        user = User.objects(id=g.user_id).get()

        if not User.objects(username=data['username']):
            user.update(**data)
            return Success()
        else:
            return {'message': '이미 등록된 ID입니다'}, 409

    # 내가 쓴글 조회
    @route('/mypage/posts', methods=['GET'])
    @login_required
    def get_myposts(self):
        post = Post.objects(user=g.user_id)
        post_list = PostListSchema(many=True).dump(post)
        print(g.user_id)
        return {'post': post_list}, 200

    # 내가 작성한 코멘트 조회
    @route('/mypage/comments', methods=['GET'])
    @login_required
    def get_mycomments(self):
        comment = Comment.objects(user=g.user_id)
        comment_list = CommentListSchema(many=True).dump(comment)
        return {'comment': comment_list}, 200

    # 내가 좋아요한 글 조회
    @route('/mypage/posts/likes')
    @login_required
    def get_myposts_likes(self):
        post = Post.objects(likes__exact=str(g.user_id))
        post_list = PostListSchema(many=True).dump(post)
        return {'post': post_list}, 200
