from marshmallow import fields, Schema, post_load
from app.Model import Comment

from app.serializers.user import UserSchemaName


class ReCommentCreateSchema(Schema):
    content = fields.Str(required=True)
