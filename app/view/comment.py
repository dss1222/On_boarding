from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, doc

from app.serializers.comment import CommentCreateSchema, CommentListSchema
from app.service.validator import *

from app.service.comment import CommentService


class CommentView(FlaskView):
    decorators = (doc(tags=['COMMENT']),)

    # 코멘트 작성
    @route('/', methods=['POST'])
    @doc(description='Comment 작성', summary='Comment 작성')
    @marshal_with(SuccessSchema, code=201, description="성공")
    @use_kwargs(CommentCreateSchema())
    @login_required
    @post_validator
    def create(self, post_id, board_id, content):
        CommentService.create(post_id, content)
        return "", 201

    # 좋아요 기능
    @route('/<string:comment_id>/likes', methods=['POST'])
    @doc(summary="댓글 좋아요", description="댓글 좋아요")
    @marshal_with(SuccessSchema, code=201, description="성공")
    @login_required
    @comment_validator
    def like(self, comment_id, board_id, post_id):
        CommentService.like(comment_id)
        return "", 201

    # 좋아요 취소
    @route('/<string:comment_id>/unlikes', methods=['POST'])
    @doc(summary="게시물 좋아요 취소", description="게시물 좋아요 취소")
    @marshal_with(SuccessSchema, code=201, description="성공")
    @login_required
    @comment_validator
    def unlike(self, comment_id, board_id, post_id):
        CommentService.unlike(comment_id)
        return "", 201

    # 댓글 조회
    @route('', methods=['GET'])
    @doc(summary="게시글 리스트 조회", description="게시글 리스트 조회")
    @marshal_with(CommentListSchema(many=True), code=200, description="댓글 목록 조회")
    @login_required
    @post_validator
    def get_comments(self, board_id, post_id):
        return CommentService.get_comments(post_id)
