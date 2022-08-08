from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, doc, marshal_with
from flask import g
from bson import ObjectId
from app.serializers.post import PostListSchema, PostDetailSchema, PostListParamSchema, PostCreateFormSchema, \
    PostUpdateFormSchema, PostSearchParamSchema
from app.service.validator import login_required, board_validator, post_validator, post_user_validator
from app.utils.enumOrder import OrderEnum
from app.utils.ApiErrorSchema import SuccessSchema

from app.models.post import Post
from app.models.comment import Comment
from app.models.recomment import ReComment


class PostView(FlaskView):
    decorators = (doc(tags=['POST']), login_required, board_validator)

    # 게시글 작성
    @route('', methods=['POST'])
    @doc(description='게시글 작성', summary='게시글 작성')
    @use_kwargs(PostCreateFormSchema())
    @marshal_with(SuccessSchema, code=201, description="성공")
    def create(self, board_id, title, content, tag):
        post = Post(title=title, content=content, tag=tag)
        post.board = ObjectId(board_id)
        post.user = g.user_id
        post.save()
        return "", 201

    # 게시글 상세조회 1개
    @route('/<string:post_id>', methods=['GET'])
    @doc(description='게시글 조회', summary='게시글 조회')
    @marshal_with(PostDetailSchema(), code=200, description="게시물 상세 정보")
    @post_validator
    def get_detail(self, post_id, board_id):
        post = Post.objects().get(board=board_id, id=post_id, is_deleted=False)
        return post, 200

    # 게시글 리스트 조회
    @route('/', methods=['GET'])
    @doc(description='게시글 리스트 조회', summary='게시글 리스트 조회')
    @use_kwargs(PostListParamSchema, location='query')
    @marshal_with(PostListSchema(many=True), code=200, description="게시글 리스트 조회")
    def get_posts(self, board_id, page, size, orderby):
        order_by = OrderEnum[str(orderby)].value

        posts = Post.objects(board=board_id, is_deleted=False).order_by(order_by)[
                (page - 1) * size: page * size]

        return posts, 200

    # 게시글 수정 <회원정보 일치해야 함>
    @route('/<string:post_id>', methods=['PATCH'])
    @doc(description='게시글 수정', summary='게시글 수정')
    @use_kwargs(PostUpdateFormSchema())
    @marshal_with(SuccessSchema, code=201, description="성공")
    @post_user_validator
    def update(self, post_id, board_id, title, content, tag):
        Post.objects(id=post_id, user=g.user_id, is_deleted=False).update(title=title, content=content, tag=tag)
        return "", 201

    # 게시글 삭제
    @route('/<string:post_id>', methods=['DELETE'])
    @doc(description='게시글 삭제', summary='게시글 삭제')
    @marshal_with(SuccessSchema, code=204, description="성공")
    @post_user_validator
    def delete(self, post_id, board_id):
        post = Post.objects().get(id=post_id)

        comment_list = Comment.objects(post=post_id, is_deleted=False)

        for comment in comment_list:
            recomment_list = ReComment.objects(comment=comment)
            for recomment in recomment_list:
                recomment.soft_delete_recomment()
            comment.soft_delete_comment()

        post.soft_delete()
        return "", 204

    # 좋아요 기능
    @route('/<string:post_id>/likes', methods=['POST'])
    @doc(summary="게시물 좋아요", description="게시물 좋아요")
    @marshal_with(SuccessSchema, code=201, description="성공")
    @post_validator
    def like(self, board_id, post_id):
        post = Post.objects().get(id=post_id, is_deleted=False)
        post.like(g.user_id)
        return "", 201

    # 좋아요 취소
    @route('/<string:post_id>/unlikes', methods=['POST'])
    @doc(summary="게시물 좋아요 취소", description="게시물 좋아요 취소")
    @marshal_with(SuccessSchema, code=201, description="성공")
    @post_validator
    def unlike(self, board_id, post_id):
        post = Post.objects().get(id=post_id, is_deleted=False)
        post.cancel_like(g.user_id)
        return "", 201

    # 태그 검색 기능
    @route('/search/', methods=['GET'])  # 검색어도 쿼리스트링으로 받게 수정,
    @doc(description='게시글 검색 조회', summary='게시글 검색 조회')
    @use_kwargs(PostSearchParamSchema, location='query')
    @marshal_with(PostListSchema(many=True), code=200, description="게시물 상세 정보")
    def search(self, board_id, search):
        posts = Post.objects(tag__contains=str(search), is_deleted=False)
        return posts, 200
