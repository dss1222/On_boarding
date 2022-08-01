from marshmallow import fields, Schema, post_load
from app.Model import Comment

from app.serializers.user import UserSchemaName


class CommentCreateSchema(Schema):
    content = fields.Str(required=True)


class CommentSchema(Schema):
    id = fields.Str()
    content = fields.Str()
    user = fields.Nested(UserSchemaName)


class CommentListSchema(Schema):
    id = fields.Str()
    content = fields.Str()
    user = fields.Nested(UserSchemaName)
    likes_cnt = fields.Int()
    recomments = fields.Method('get_comments')
    comment = fields.Nested(CommentSchema(many=True))

    def get_comments(self, obj):
        comment_list = CommentListSchema(many=True).dump(Comment.objects(recomment=obj.id))
        return comment_list
