from marshmallow import Schema, fields

from app.serializers.recomments import ReCommentDetailSchema
from app.serializers.user import UserSchemaName


class CommentCreateFormSchema(Schema):
    content = fields.String(required=True)


class CommentFormSchema(Schema):
    id = fields.String()
    content = fields.String()
    user = fields.Nested(UserSchemaName)


class CommentDetailSchema(Schema):
    id = fields.String()
    user = fields.Nested(UserSchemaName)
    content = fields.String()
    likes_cnt = fields.Integer()
    recomment = fields.Nested(ReCommentDetailSchema(many=True))
