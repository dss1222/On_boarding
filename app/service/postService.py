import marshmallow
from bson import ObjectId

from app.utils.validator import *
from app.utils.enumOrder import OrderEnum


class PostService:
    @classmethod
    def post_create(cls, board_id, post):
        post.board = ObjectId(board_id)
        post.user = g.user_id
        post.save()

        return SuccessDto()

    @classmethod
    def post_get_detail(cls, post_id, board_id):
        post = Post.objects(board=board_id, id=post_id, is_deleted=False).get()
        return post, 200

    @classmethod
    def post_get_post_list(cls, board_id, page, size, orderby):
        order_by = OrderEnum[str(orderby)].value

        posts = Post.objects(board=board_id, is_deleted=False).order_by(order_by)[
                (page - 1) * size: page * size]

        return posts, 200

    @classmethod
    def post_update(cls, post_id, board_id, post):
        try:
            Post.objects(id=post_id, user=g.user_id, is_deleted=False).update(**request.json)

            return SuccessDto()
        except marshmallow.exceptions.ValidationError as err:
            return ApiError(message=err.messages), 422

    @classmethod
    def post_delete(cls, post_id, board_id):
        post = Post.objects(board=board_id, id=post_id).get()

        comment_list = Comment.objects(post=post_id, is_deleted=False)

        for comment in comment_list:
            comment.soft_delete()

        post.soft_delete()
        return SuccessDto()

    @classmethod
    def post_like(cls, board_id, post_id):
        post = Post.objects(board=board_id, id=post_id, is_deleted=False).get()
        post.like(g.user_id)
        return SuccessDto()

    @classmethod
    def post_unlike(cls, board_id, post_id):
        post = Post.objects(board=board_id, id=post_id, is_deleted=False).get()
        post.cancel_like(g.user_id)
        return SuccessDto()

    @classmethod
    def post_search(cls, board_id, search):
        posts = Post.objects(tag__contains=str(search), is_deleted=False)
        return posts, 200