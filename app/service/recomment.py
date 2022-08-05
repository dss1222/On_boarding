from app.service.validator import *

from app.models.comment import Comment
from app.models.recomment import ReComment


class ReCommentService:
    @classmethod
    def create(cls, post_id, comment_id, content):
        comment = Comment.objects().get(id=comment_id)
        ReComment(content=content, user=g.user_id, comment=comment).save()
        comment.create_recomment()

    @classmethod
    def like(cls, re_comment_id):
        recomment = ReComment.objects().get(id=re_comment_id)
        recomment.like(g.user_id)

    @classmethod
    def unlike(cls, re_comment_id):
        recomment = ReComment.objects().get(id=re_comment_id)
        recomment.cancel_like(g.user_id)
