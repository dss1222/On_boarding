from flask_classful import FlaskView, route
from bson import ObjectId

from app.post.postSchema import PostCreateSchema, PostDetailSchema, PostListSchema, PostUpdateSchema
from app.utils.validator import *
from app.utils.ErrorHandler import *


class PostView(FlaskView):
    # 게시글 작성
    @route('', methods=['POST'])
    @login_required
    @board_validator
    def create_post(self, board_id):
        post = PostCreateSchema().load(json.loads(request.data))
        post.board = ObjectId(board_id)
        post.user = g.user_id
        post.save()

        return Success()

    # 게시글 상세조회 1개
    @route('/<post_id>', methods=['GET'])
    @login_required
    @post_validator
    @board_validator
    def get_posts_detail(self, post_id, board_id):
        post = Post.objects(board=board_id, id=post_id).get()
        print(g.user_id)
        print(g.username)
        return PostDetailSchema().dump(post), 200

    # 게시글 조회 최신순 10개
    @route('/order/created', methods=['GET'])
    @login_required
    @board_validator
    def get_posts(self, board_id):
        post_limit_10 = Post.objects(board=board_id).order_by('-created_at').limit(10)
        post_list = PostListSchema(many=True).dump(post_limit_10)
        return {'posts': post_list}, 200

    # 게시글 조회 좋아요 많은 순 10개
    @route('/order/likes', methods=['GET'])
    @login_required
    @board_validator
    def get_posts_likes(self, board_id):
        post_limit_10 = Post.objects(board=board_id).order_by('-created_at').order_by('-likes_cnt').limit(10)
        post_list = PostListSchema(many=True).dump(post_limit_10)
        return {'posts': post_list}, 200

    # 게시글 조회 댓글 많은 순 10개
    @route('/order/comments', methods=['GET'])
    @login_required
    def get_posts_comeents(self, board_id):
        post_limit_10 = Post.objects(board=board_id).order_by('-comments_cnt').limit(10)
        post_list = PostListSchema(many=True).dump(post_limit_10)
        return {'posts': post_list}, 200

    # 게시글 수정 <회원정보 일치해야 함>
    @route('/<post_id>', methods=['PATCH'])
    @login_required
    @post_validator
    def update_post(self, post_id, board_id):
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
    def delete_post(self, post_id, board_id):
        post = Post.objects(id=post_id).get()

        if not post.is_user(g.user_id):
            return NotCreatedUser()

        post.delete()
        return Success()

    # 좋아요 기능
    @route('/<post_id>/likes', methods=['POST'])
    @login_required
    @post_validator
    def like_post(self, board_id, post_id):
        post = Post.objects(board=board_id, id=post_id).get()
        post.like(g.user_id)
        return Success()

    # 태그 검색 기능
    @route('/search/<search>', methods=['GET'])
    @login_required
    def search_post(self, board_id, search):
        post = Post.objects(tag__contains=str(search))
        post_list = PostListSchema(many=True).dump(post)
        return {'post': post_list}, 200
