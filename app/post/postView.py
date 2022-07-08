from flask_classful import FlaskView, route
from flask import request, g

from app.post.postSchema import PostCreateSchema, PostDetailSchema, PostListSchema, PostUpdateSchema
from app.post.postModel import Post
from app.utils.validator import *
from app.utils.ErrorHandler import *


class PostView(FlaskView):
    # 게시글 작성
    @route('', methods=['POST'])
    @login_required
    def create_post(self):
        post = PostCreateSchema().load(json.loads(request.data))

        post.user = g.user_id
        post.save()

        return Success()

    # 게시글 상세조회 1개
    @route('/<post_id>', methods=['GET'])
    @login_required
    @post_validator
    def get_posts_detail(self, post_id):
        post = Post.objects(id=post_id).get()
        print(g.user_id)
        print(g.username)
        return PostDetailSchema().dump(post), 200

    # 게시글 조회 최신순 10개
    @route('/order/created', methods=['GET'])
    @login_required
    def get_posts(self):
        post_limit_10 = Post.objects().order_by('-created_at').limit(10)
        post_list = PostListSchema(many=True).dump(post_limit_10)
        return {'posts': post_list}, 200

    # 게시글 조회 좋아요 많은 순 10개
    @route('/order/likes', methods=['GET'])
    @login_required
    def get_posts_likes(self):
        post_limit_10 = Post.objects().order_by('-created_at').order_by('-likes').limit(10)
        post_list = PostListSchema(many=True).dump(post_limit_10)
        return {'posts': post_list}, 200

    @route('/order/comments', methods=['GET'])
    @login_required
    def get_posts_comeents(self):
        post_limit_10 = Post.objects().order_by('-created_at').order_by('-comments').limit(10)
        post_list = PostListSchema(many=True).dump(post_limit_10)
        return {'posts' : post_list}, 200

    # 게시글 수정 <회원정보 일치해야 함>
    @route('/<post_id>', methods=['PATCH'])
    @login_required
    @post_validator
    def update_post(self, post_id):
        data = PostUpdateSchema().load(json.loads(request.data))
        post = Post.objects(id=post_id).get()

        if not post.is_user(g.user_id):
            return NotCreatedUser()
        post.update(**data)

        print(post.content)
        return Success()

    # 게시글 삭제
    @route('/<post_id>', methods=['DELETE'])
    @login_required
    @post_validator
    def delete_post(self, post_id):
        post = Post.objects(id=post_id).get()

        if not post.is_user(g.user_id):
            return NotCreatedUser()

        post.delete()
        return Success()

    #좋아요 기능
    @route('/likes/<post_id>', methods=['POST'])
    @login_required
    @post_validator
    def like_post(self, post_id):
        post = Post.objects(id=post_id).get()
        post.like(g.user_id)
        return Success()