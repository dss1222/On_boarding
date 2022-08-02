from marshmallow import fields, Schema

from app.serializers.user import UserSchemaName


class ReCommentCreateSchema(Schema):
    content = fields.Str(required=True)


class ReCommentDetailSchema(Schema):
    id = fields.Str()
    user = fields.Nested(UserSchemaName)
    likes_cnt = fields.Int()
    content = fields.Str()
