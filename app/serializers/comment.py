from app.serializers.recomments import *


class CommentCreateFormSchema(Schema):
    content = fields.Str(required=True)


class CommentFormSchema(Schema):
    id = fields.Str()
    content = fields.Str()
    user = fields.Nested(UserSchemaName)


class CommentDetailSchema(Schema):
    id = fields.Str()
    user = fields.Nested(UserSchemaName)
    content = fields.Str()
    likes_cnt = fields.Int()
    recomment = fields.Nested(ReCommentDetailSchema(many=True))
