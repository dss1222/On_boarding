from app.service.validator import *
from bson import ObjectId


class CommentService:
    @classmethod
    def create(cls, post_id, content):
        comment = Comment(content=content)
        post = Post.objects().get(id=post_id)
        comment.user = g.user_id
        comment.post = post

        comment.save()

        post.update(push__comments=str(comment))
        post.update(inc__comments_cnt=1)

    @classmethod
    def comment_re_create(cls, post_id, comment_id, content):
        re_comment = Comment(content=content)
        re_comment.user = g.user_id
        re_comment.post = ObjectId(post_id)
        re_comment.recomment = ObjectId(comment_id)
        re_comment.save()

    @classmethod
    def like(cls, comment_id):
        comment = Comment.objects().get(id=comment_id)
        comment.like(g.user_id)

    @classmethod
    def unlike(cls, comment_id):
        comment = Comment.objects().get(id=comment_id)
        comment.cancel_like(g.user_id)

    @classmethod
    def get_comments(cls, post_id):
        comments = Comment.objects(post=post_id).order_by('-created_at').limit(10)

        return comments, 200

