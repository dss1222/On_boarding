from app.serializers.recomments import *


class CommentCreateSchema(Schema):
    content = fields.Str(required=True)


class CommentSchema(Schema):
    id = fields.Str()
    content = fields.Str()
    user = fields.Nested(UserSchemaName)


# class CommentListSchema(Schema):
#     id = fields.Str()
#     content = fields.Str()
#     user = fields.Nested(UserSchemaName)
#     likes_cnt = fields.Int()
#     # recomments = fields.Method('get_comments')
#
#     def get_comments(self, obj):
#         comment_list = CommentListSchema(many=True).dump(Comment.objects(recomment=obj.id))
#         return comment_list


class CommentDetailSchema(Schema):
    id = fields.Str()
    user = fields.Nested(UserSchemaName)
    content = fields.Str()
    likes_cnt = fields.Int()
    recomment = fields.Nested(ReCommentDetailSchema(many=True))
