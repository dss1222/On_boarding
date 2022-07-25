import marshmallow
from flask_classful import FlaskView, route
from bson import ObjectId
from flask_apispec import use_kwargs, marshal_with, doc

from app.post.postSchema import *
from app.utils.validator import *
from app.utils.ErrorHandler import *

from app.utils.enumOrder import OrderEnum


class PostView(FlaskView):
    decorators = (doc(tags=['POST']),)

    # 게시글 작성
    @route('', methods=['POST'])
    @doc(description='게시글 작성', summary='게시글 작성')
    @use_kwargs(PostCreateSchema())
    @marshal_with(SuccessSchema, code=200, description="성공")
    @login_required
    @create_post_validator
    @board_validator
    def create_post(self, board_id, post):
        post.board = ObjectId(board_id)
        post.user = g.user_id
        post.save()

        return SuccessDto()

    # 게시글 상세조회 1개
    @route('/<string:post_id>', methods=['GET'])
    @doc(description='게시글 조회', summary='게시글 조회')
    @marshal_with(PostDetailSchema(), code=200, description="게시물 상세 정보")
    @login_required
    @post_validator
    @board_validator
    def get_posts_detail(self, post_id, board_id):
        post = Post.objects(board=board_id, id=post_id, is_deleted=False).get()
        return post, 200

    # 게시글 리스트 조회
    @route('/', methods=['GET'])
    @doc(description='게시글 리스트 조회', summary='게시글 리스트 조회')
    @marshal_with(PostListSchema(many=True), code=200, description="게시물 상세 정보")
    @login_required
    @board_validator
    @post_list_validator
    def get_posts_pagination(self, board_id):
        params = request.args.to_dict()

        page = int(params["page"])
        size = int(params["size"])
        order_by = OrderEnum[str(params["orderby"])].value

        posts = Post.objects(board=board_id, is_deleted=False).order_by(order_by)[
                        (page - 1) * size: page * size]

        return posts, 200

    # 게시글 수정 <회원정보 일치해야 함>
    @route('/<string:post_id>', methods=['PATCH'])
    @doc(description='게시글 수정', summary='게시글 수정')
    @use_kwargs(PostUpdateSchema())
    @marshal_with(SuccessSchema, code=200, description="성공")
    @login_required
    @post_user_validator
    def update_post(self, post_id, board_id, post):
        try:
            Post.objects(id=post_id, user=g.user_id,is_deleted=False).update(**request.json)

            return SuccessDto()
        except marshmallow.exceptions.ValidationError as err:
            return ApiError(message=err.messages), 422

    # 게시글 삭제
    @route('/<string:post_id>', methods=['DELETE'])
    @doc(description='게시글 삭제', summary='게시글 삭제')
    @marshal_with(SuccessSchema, code=200, description="성공")
    @login_required
    @post_user_validator
    def delete_post(self, post_id, board_id):
        post = Post.objects(board=board_id, id=post_id).get()

        comment_list = Comment.objects(post=post_id)

        for comment in comment_list:
            comment.soft_delete()

        post.soft_delete()
        return SuccessDto()

    # 좋아요 기능
    @route('/<string:post_id>/likes', methods=['POST'])
    @doc(summary="게시물 좋아요", description="게시물 좋아요")
    @marshal_with(SuccessSchema, code=200, description="성공")
    @login_required
    @post_validator
    def like_post(self, board_id, post_id):
        post = Post.objects(board=board_id, id=post_id).get()
        post.like(g.user_id)
        return SuccessDto()

    # 좋아요 취소
    @route('/<string:post_id>/unlikes', methods=['POST'])
    @doc(summary="게시물 좋아요 취소", description="게시물 좋아요 취소")
    @marshal_with(SuccessSchema, code=200, description="성공")
    @login_required
    @post_validator
    def unlike_post(self, board_id, post_id):
        post = Post.objects(board=board_id, id=post_id).get()
        post.cancel_like(g.user_id)
        return SuccessDto()

    # 태그 검색 기능
    @route('/search/<search>', methods=['GET'])
    @doc(description='게시글 검색 조회', summary='게시글 검색 조회')
    @marshal_with(PostListSchema(many=True), code=200, description="게시물 상세 정보")
    @login_required
    @board_validator
    def search_post(self, board_id, search):
        posts = Post.objects(tag__contains=str(search))
        return posts, 200