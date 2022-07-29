from app.service.validator import *
from bson import ObjectId


class CommentService:
    @classmethod
    def comment_create(cls, post_id, content):
        comment = Comment(content=content)
        post = Post.objects(id=post_id).get()
        comment.user = g.user_id
        comment.post = post

        comment.save()

        post.update(push__comments=str(comment))
        post.update(inc__comments_cnt=1)

        return SuccessDto()

    @classmethod
    def comment_re_create(cls, post_id, comment_id, content):
        re_comment = Comment(content=content)
        re_comment.user = g.user_id
        re_comment.post = ObjectId(post_id)
        re_comment.recomment = ObjectId(comment_id)
        re_comment.save()

        return SuccessDto()

    @classmethod
    def comment_like(cls, comment_id):
        comment = Comment.objects(id=comment_id).get()
        comment.like(g.user_id)
        return SuccessDto()

    @classmethod
    def comment_unlike(cls, comment_id):
        comment = Comment.objects(id=comment_id).get()
        comment.cancel_like(g.user_id)
        return SuccessDto()

    @classmethod
    def comment_get_list(cls, post_id):
        comments = Comment.objects(post=post_id).order_by('-created_at').limit(10)
        return comments, 200
