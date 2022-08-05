from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, doc

from app.service.validator import *
from app.serializers.recomments import *

from app.service.recomment import ReCommentService


class ReCommentView(FlaskView):
    decorators = (doc(tags=['Re_Comment']), login_required, comment_validator)

    # 대댓글
    @route('', methods=['POST'])
    @doc(description='대댓글 작성', summary='대댓글 작성')
    @marshal_with(SuccessSchema, code=201, description="성공")
    @use_kwargs(ReCommentCreateFormSchema())
    def create(self, board_id, post_id, comment_id, content):
        ReCommentService.create(post_id, comment_id, content)
        return "", 201

    @route('/<string:re_comment_id>/likes', methods=['POST'])
    @doc(summary="대댓글 좋아요", description="대댓글 좋아요")
    @marshal_with(SuccessSchema, code=201, description="성공")
    def like(self, re_comment_id, comment_id, board_id, post_id):
        ReCommentService.like(re_comment_id)
        return "", 201

    # 좋아요 취소
    @route('/<string:re_comment_id>/unlikes', methods=['POST'])
    @doc(summary="대댓글 좋아요 취소", description="대댓글 좋아요 취소")
    @marshal_with(SuccessSchema, code=201, description="성공")
    def unlike(self, re_comment_id, comment_id, board_id, post_id):
        ReCommentService.unlike(re_comment_id)
        return "", 201
