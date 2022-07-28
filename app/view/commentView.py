from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, doc

from app.serializers.commentSchema import CommentListSchema, ReCommentCreateSchema
from app.utils.validator import *

from app.service.commentService import CommentService


class CommentView(FlaskView):
    decorators = (doc(tags=['COMMENT']),)

    # 코멘트 작성
    @route('/', methods=['POST'])
    @doc(description='Comment 작성', summary='Comment 작성')
    @marshal_with(SuccessSchema, code=200, description="성공")
    @use_kwargs(CommentCreateSchema())
    @login_required
    @create_comment_validator
    @post_validator
    def create_comment(self, post_id, board_id, comment):
        return CommentService.comment_create(post_id, comment)

    # 대댓글
    @route('/<string:comment_id>/recomment', methods=['POST'])
    @doc(description='reComment 작성', summary='reComment 작성')
    @marshal_with(SuccessSchema, code=200, description="성공")
    @use_kwargs(ReCommentCreateSchema())
    @login_required
    @comment_validator
    def create_recomment(self, board_id, post_id, comment_id, re_comment):
        return CommentService.comment_re_create(post_id, comment_id, re_comment)

    # 좋아요 기능
    @route('/<string:comment_id>/likes', methods=['POST'])
    @doc(summary="댓글 좋아요", description="댓글 좋아요")
    @marshal_with(SuccessSchema, code=200, description="성공")
    @login_required
    @comment_validator
    def like_comment(self, comment_id, board_id, post_id):
        return CommentService.comment_like(comment_id)

    # 좋아요 취소
    @route('/<string:comment_id>/unlikes', methods=['POST'])
    @doc(summary="게시물 좋아요 취소", description="게시물 좋아요 취소")
    @marshal_with(SuccessSchema, code=200, description="성공")
    @login_required
    @comment_validator
    def unlike_comment(self, comment_id, board_id, post_id):
        return CommentService.comment_unlike(comment_id)

    # 댓글 조회
    @route('/order/created', methods=['GET'])
    @doc(summary="게시글 리스트 조회", description="게시글 리스트 조회")
    @marshal_with(CommentListSchema(many=True), code=200, description="댓글 목록 조회")
    @login_required
    @post_validator
    def get_comments_created(self, post_id):
        return CommentService.comment_get_list(post_id)
