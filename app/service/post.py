from bson import ObjectId

from app.service.validator import *
from app.utils.enumOrder import OrderEnum
from app.models.post import Post
from app.models.comment import Comment
from app.models.recomment import ReComment


class PostService:
    @classmethod
    def create(cls, board_id, title, content, tag):
        post = Post(title=title, content=content, tag=tag)
        post.board = ObjectId(board_id)
        post.user = g.user_id
        post.save()

    @classmethod
    def get_detail(cls, post_id, board_id):
        post = Post.objects().get(board=board_id, id=post_id, is_deleted=False)
        return post, 200

    @classmethod
    def get_posts(cls, board_id, page, size, orderby):
        order_by = OrderEnum[str(orderby)].value

        posts = Post.objects(board=board_id, is_deleted=False).order_by(order_by)[
                (page - 1) * size: page * size]

        return posts, 200

    @classmethod
    def post_update(cls, post_id, title, content, tag):
        Post.objects(id=post_id, user=g.user_id, is_deleted=False).update(title=title, content=content, tag=tag)

    @classmethod
    def delete(cls, post_id):
        post = Post.objects().get(id=post_id)

        comment_list = Comment.objects(post=post_id, is_deleted=False)

        for comment in comment_list:
            recomment_list = ReComment.objects(comment=comment)
            for recomment in recomment_list:
                recomment.soft_delete()
            comment.soft_delete()

        post.soft_delete()

    @classmethod
    def like(cls, post_id):
        post = Post.objects().get(id=post_id, is_deleted=False)
        post.like(g.user_id)

    @classmethod
    def unlike(cls, post_id):
        post = Post.objects().get(id=post_id, is_deleted=False)
        post.cancel_like(g.user_id)

    @classmethod
    def search(cls, board_id, search):
        posts = Post.objects(tag__contains=str(search), is_deleted=False)
        return posts, 200
