from flask_classful import FlaskView, route
from bson import ObjectId
from enum import Enum

from mongoengine import *
from app.post.postSchema import *
from app.comment.commentModel import Comment
from app.utils.validator import *
from app.utils.ErrorHandler import *

from app.utils.enumOrder import OrderEnum



class PostView(FlaskView):
    # 게시글 작성
    @route('', methods=['POST'])
    @login_required
    @create_post_validator
    @board_validator
    def create_post(self, board_id):
        post = PostCreateSchema().load(json.loads(request.data))
        post.board = ObjectId(board_id)
        post.user = g.user_id
        post.save()

        return Success()

    # 게시글 상세조회 1개
    @route('/<post_id>', methods=['GET'])
    # @login_required
    @post_validator
    @board_validator
    def get_posts_detail(self, post_id, board_id):
        post = Post.objects(board=board_id, id=post_id).get()
        print(PostDetailSchema().dump(post))
        return PostDetailSchema().dump(post), 200

    # 게시글 리스트 조회
    @route('/', methods=['GET'])
    @login_required
    @board_validator
    @post_list_validator
    def get_posts_pagination(self, board_id):
        params = request.args.to_dict()

        page = int(params["page"])
        size = int(params["size"])
        order_by = OrderEnum[str(params["orderby"])].value

        post_limit_10 = Post.objects(board=board_id, is_deleted=False).order_by(order_by)[
                        (page - 1) * size: page * size]
        post_list = PostListSchema(many=True).dump(post_limit_10)

        return jsonify(post_list), 200

    # 게시글 수정 <회원정보 일치해야 함>
    @route('/<post_id>', methods=['PATCH'])
    @login_required
    @post_validator
    def update_post(self, post_id, board_id):
        data = PostUpdateSchema().load(json.loads(request.data))
        post = Post.objects(id=post_id).get()

        if not post.find_user(g.user_id):
            return NotCreatedUser()
        post.update(**data)

        print(post.content)
        return Success()

    # 게시글 삭제
    @route('/<post_id>', methods=['DELETE'])
    @login_required
    @post_validator
    def delete_post(self, post_id, board_id):
        post = Post.objects(board=board_id, id=post_id).get()

        if not post.find_user(g.user_id):
            return NotCreatedUser()

        comment_list = Comment.objects(post=post_id)

        for comment in comment_list:
            comment.soft_delete()

        post.soft_delete()
        return Success()

    # 좋아요 기능
    @route('/<post_id>/likes', methods=['POST'])
    @login_required
    @post_validator
    def like_post(self, board_id, post_id):
        post = Post.objects(board=board_id, id=post_id).get()
        post.like(g.user_id)
        return Success()

    # 좋아요 취소
    @route('/<post_id>/unlikes', methods=['POST'])
    @login_required
    @post_validator
    def unlike_post(self, board_id, post_id):
        post = Post.objects(board=board_id, id=post_id).get()
        post.cancel_like(g.user_id)
        return Success()

    # 태그 검색 기능
    @route('/search/<search>', methods=['GET'])
    @login_required
    def search_post(self, board_id, search):
        post = Post.objects(tag__contains=str(search))
        post_list = PostListSchema(many=True).dump(post)
        return {'posts': post_list}, 200
