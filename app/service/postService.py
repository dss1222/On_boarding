import marshmallow
from bson import ObjectId

from app.service.validator import *
from app.utils.enumOrder import OrderEnum


class PostService:
    @classmethod
    def create(cls, board_id, title, content, tag):
        post = Post(title=title, content=content, tag=tag)
        post.board = ObjectId(board_id)
        post.user = g.user_id
        post.save()

        return SuccessDto()

    @classmethod
    def get_detail(cls, post_id, board_id):
        post = Post.objects(board=board_id, id=post_id, is_deleted=False).get()
        return post, 200

    @classmethod
    def get_posts(cls, board_id, page, size, orderby):
        order_by = OrderEnum[str(orderby)].value

        posts = Post.objects(board=board_id, is_deleted=False).order_by(order_by)[
                (page - 1) * size: page * size]

        return posts, 200

    @classmethod
    def post_update(cls, post_id, title, content, tag):
        try:
            Post.objects(id=post_id, user=g.user_id, is_deleted=False).update(title=title,content=content,tag=tag)

            return SuccessDto()
        except marshmallow.exceptions.ValidationError as err:
            return ApiError(message=err.messages), 422

    @classmethod
    def delete(cls, post_id):
        post = Post.objects(id=post_id).get()

        comment_list = Comment.objects(post=post_id, is_deleted=False)

        for comment in comment_list:
            comment.soft_delete()

        post.soft_delete()
        return SuccessDto()

    @classmethod
    def like(cls, post_id):
        post = Post.objects(id=post_id, is_deleted=False).get()
        post.like(g.user_id)
        return SuccessDto()

    @classmethod
    def unlike(cls, post_id):
        post = Post.objects(id=post_id, is_deleted=False).get()
        post.cancel_like(g.user_id)
        return SuccessDto()

    @classmethod
    def search(cls, board_id, search):
        posts = Post.objects(tag__contains=str(search), is_deleted=False)
        return posts, 200