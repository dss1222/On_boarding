from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, doc

from app.serializers.comment import CommentCreateSchema,CommentListSchema, ReCommentCreateSchema
from app.service.validator import *

from app.service.recomment import ReCommentService


class ReCommentView(FlaskView):
    decorators = (doc(tags=['Re_COMMENT']),)

    # 대댓글
    @route('', methods=['POST'])
    @doc(description='reComment 작성', summary='reComment 작성')
    @marshal_with(SuccessSchema, code=201, description="성공")
    @use_kwargs(ReCommentCreateSchema())
    @login_required
    @comment_validator
    def create_recomment(self, board_id, post_id, comment_id, content):
        ReCommentService.create(post_id, comment_id, content)
        return "", 201
