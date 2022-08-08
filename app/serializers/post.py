from marshmallow import fields, Schema
from marshmallow_enum import EnumField

from app.utils.enumOrder import OrderEnum
from app.serializers.user import UserSchemaName
from app.serializers.comment import CommentDetailSchema
from app.serializers.board import BoardFormSchema


class PostCreateFormSchema(Schema):
    title = fields.String(required=True)
    content = fields.String(required=True)
    tag = fields.String()


class PostDetailSchema(Schema):
    id = fields.String()
    user = fields.Nested(UserSchemaName, dump_only=("id", "username"))
    title = fields.String()
    content = fields.String()
    created_at = fields.DateTime(dump_only=True)
    likes_cnt = fields.Integer()
    comments_cnt = fields.Integer()
    tag = fields.String()
    comment = fields.Nested(CommentDetailSchema(many=True))


class PostListSchema(Schema):
    board = fields.Nested(BoardFormSchema)
    id = fields.String()
    user = fields.Nested(UserSchemaName, dump_only=("id", "username"))
    title = fields.String()
    likes_cnt = fields.Integer()
    comments_cnt = fields.Integer()
    created_at = fields.DateTime()


class PostSearchParamSchema(Schema):
    search = fields.String()


class PostListParamSchema(Schema):
    page = fields.Integer()
    size = fields.Integer()
    # orderby = fields.EnumField(OrderEnum, required=True)  # enum 으로 수됨
    orderby = fields.String()


class PostUpdateFormSchema(Schema):
    title = fields.String()
    content = fields.String()
    tag = fields.String()
