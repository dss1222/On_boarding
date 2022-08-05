from marshmallow import fields, Schema

from app.serializers.user import UserSchemaName
from app.serializers.comment import CommentDetailSchema
from app.serializers.board import BoardFormSchema


class PostCreateFormSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    tag = fields.Str()


class PostDetailSchema(Schema):
    id = fields.Str()
    user = fields.Nested(UserSchemaName, dump_only=("id", "username"))
    title = fields.Str()
    content = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    likes_cnt = fields.Int()
    comments_cnt = fields.Int()
    tag = fields.Str()
    comment = fields.Nested(CommentDetailSchema(many=True))


class PostListSchema(Schema):
    board = fields.Nested(BoardFormSchema)
    id = fields.Str()
    user = fields.Nested(UserSchemaName, dump_only=("id", "username"))
    title = fields.Str()
    likes_cnt = fields.Int()
    comments_cnt = fields.Int()
    created_at = fields.DateTime()


class PostSearchParamSchema(Schema):
    search = fields.Str()


class PostListParamSchema(Schema):
    page = fields.Int()
    size = fields.Int()
    orderby = fields.Str()  # enum 으로 수됨


class PostUpdateFormSchema(Schema):
    title = fields.Str()
    content = fields.Str()
    tag = fields.Str()
