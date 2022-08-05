from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, doc

from app.service.validator import *
from app.serializers.recomments import *

from app.models.models import *
from app.models.user import User


class ReCommentView(FlaskView):
    decorators = (doc(tags=['Re_Comment']), login_required, comment_validator)

    # 대댓글
    @route('', methods=['POST'])
    @doc(description='대댓글 작성', summary='대댓글 작성')
    @marshal_with(SuccessSchema, code=201, description="성공")
    @use_kwargs(ReCommentCreateFormSchema())
    def create(self, board_id, post_id, comment_id, content):
        comment = Comment.objects().get(id=comment_id)
        ReComment(content=content, user=g.user_id, comment=comment).save()
        comment.create_recomment()
        return "", 201

    @route('/<string:re_comment_id>/likes', methods=['POST'])
    @doc(summary="대댓글 좋아요", description="대댓글 좋아요")
    @marshal_with(SuccessSchema, code=201, description="성공")
    def like(self, re_comment_id, comment_id, board_id, post_id):
        recomment = ReComment.objects().get(id=re_comment_id)
        recomment.like(g.user_id)
        return "", 201

    # 좋아요 취소
    @route('/<string:re_comment_id>/unlikes', methods=['POST'])
    @doc(summary="대댓글 좋아요 취소", description="대댓글 좋아요 취소")
    @marshal_with(SuccessSchema, code=201, description="성공")
    def unlike(self, re_comment_id, comment_id, board_id, post_id):
        recomment = ReComment.objects().get(id=re_comment_id)
        recomment.cancel_like(g.user_id)
        return "", 201
