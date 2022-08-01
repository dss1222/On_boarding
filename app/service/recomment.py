from app.service.validator import *
from bson import ObjectId


class ReCommentService:
    @classmethod
    def create(cls, post_id, comment_id, content):
        comment = Comment.objects().get(id=comment_id)
        ReComment(content=content, user=g.user_id,  comment=comment).save()
        comment.create_recomment()

    # @classmethod
    # def create(cls, post_id, comment_id, content):
    #     re_comment = Comment(content=content)
    #     re_comment.user = g.user_id
    #     re_comment.post = ObjectId(post_id)
    #     re_comment.recomment = ObjectId(comment_id)
    #     re_comment.save()
