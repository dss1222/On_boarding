from marshmallow import fields, Schema, post_load
from app.Model import Comment

from app.serializers.userSchema import UserSchemaName


class CommentCreateSchema(Schema):
    content = fields.Str(required=True)

    @post_load()
    def create_comment(self, data, **kwargs):
        return {'comment': Comment(**data)}


class ReCommentCreateSchema(Schema):
    content = fields.Str(required=True)

    @post_load()
    def create_recomment(self, data, **kwargs):
        return {'re_comment': Comment(**data)}


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

    # recomments = fields.Function(lambda comment, context: comment == context[])

    def get_comments(self, obj):
        comment_list = CommentListSchema(many=True).dump(Comment.objects(recomment=obj.id))
        return comment_list
    # 컨텍스트
