from marshmallow import fields, Schema, post_load
from app.comment.commentModel import Comment

from app.user.userSchema import UserSchemaName


class CommentCreateSchema(Schema):
    content = fields.Str(required=True)

    @post_load()
    def create_comment(self, data, **kwargs):
        comment = Comment(**data)
        return comment


class CommentSchema(Schema):
    id = fields.Str()
    content = fields.Str()
    user = fields.Nested(UserSchemaName)


class CommentListSchema(Schema):
    id = fields.Str()
    content = fields.Str()
    user = fields.Nested(UserSchemaName)
    total_likes_cnt = fields.Method('count_likes')
    total_recomment_cnt = fields.Method('count_recomment')

    def count_likes(self, obj):
        return len(obj.likes)

    def count_recomment(self, obj):
        return len(obj.recomment)

