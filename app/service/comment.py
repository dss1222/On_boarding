from app.service.validator import *

from app.models.post import Post
from app.models.comment import Comment


class CommentService:
    @classmethod
    def create(cls, post_id, content):
        post = Post.objects().get(id=post_id)
        comment = Comment(content=content, user=g.user_id, post=post)
        comment.save()

        post.update(push__comments=str(comment))
        post.update(inc__comments_cnt=1)

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

