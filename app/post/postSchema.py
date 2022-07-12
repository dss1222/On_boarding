from marshmallow import fields, Schema, post_load
from app.post.postModel import Post

from app.user.userSchema import UserSchemaName
from app.comment.commentModel import Comment
from app.comment.commentSchema import CommentListSchema
from app.board.boardSchema import BoardSchema


class PostCreateSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    tag = fields.Str()

    @post_load()
    def create_post(self, data, **kwargs):
        post = Post(**data)
        return post


class PostDetailSchema(Schema):
    id = fields.Str()
    user = fields.Nested(UserSchemaName, dump_only=("id", "username"))
    title = fields.Str()
    content = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    likes_cnt = fields.Int()
    comments_cnt = fields.Int()
    tag = fields.Str()
    comments = fields.Method('get_comments')

    def get_comments(self, obj):
        comment_list = CommentListSchema(many=True).dump(Comment.objects(post=obj.id).order_by('created_at'))
        print(comment_list)
        return comment_list


class PostListSchema(Schema):
    board = fields.Nested(BoardSchema)
    id = fields.Str()
    user = fields.Nested(UserSchemaName, dump_only=("id", "username"))
    title = fields.Str()
    likes_cnt = fields.Int()
    comments_cnt = fields.Int()
    created_at = fields.DateTime()


class PostUpdateSchema(Schema):
    title = fields.Str()
    content = fields.Str()
    tag = fields.Str()
