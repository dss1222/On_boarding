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


# db조회 부분을 밖으로 빼고싶은데 빼는 방법을 모르겠습니다 ㅠㅠ
class CommentListSchema(Schema):
    id = fields.Str()
    content = fields.Str()
    user = fields.Nested(UserSchemaName)
    likes_cnt = fields.Int()
    recomments = fields.Method('get_comments')

    def get_comments(self, obj):
        comment_list = CommentListSchema(many=True).dump(Comment.objects(recomment=obj.id))
        return comment_list


