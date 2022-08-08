from marshmallow import fields, Schema

from app.serializers.user import UserSchemaName


class ReCommentCreateFormSchema(Schema):
    content = fields.String(required=True)


class ReCommentDetailSchema(Schema):
    id = fields.String()
    user = fields.Nested(UserSchemaName)
    likes_cnt = fields.Integer()
    content = fields.String()
