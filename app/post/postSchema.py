from marshmallow import fields, Schema, post_load
from app.Model import Post, Comment

from app.user.userSchema import UserSchemaName
from app.comment.commentSchema import CommentListSchema
from app.board.boardSchema import BoardSchema


class PostCreateSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    tag = fields.Str()

    @post_load()
    def create_post(self, data, **kwargs):
        return {'post': Post(**data)}


class PostDetailSchema(Schema):
    id = fields.Str()
    user = fields.Nested(UserSchemaName, dump_only=("id", "username"))
    title = fields.Str()
    content = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    likes_cnt = fields.Int()
    comments_cnt = fields.Int()
    tag = fields.Str()
    comments = fields.Method('get_comments')

    def get_comments(self, obj):
        comment_list = CommentListSchema(many=True).dump(Comment.objects(post=obj.id).order_by('created_at'))
        return comment_list


class PostListSchema(Schema):
    board = fields.Nested(BoardSchema)
    id = fields.Str()
    user = fields.Nested(UserSchemaName, dump_only=("id", "username"))
    title = fields.Str()
    likes_cnt = fields.Int()
    comments_cnt = fields.Int()
    created_at = fields.DateTime()


class PostUpdateSchema(Schema):
    title = fields.Str()
    content = fields.Str()
    tag = fields.Str()

    @post_load()
    def update_post(self, data, **kwargs):
        return {'post': Post(**data)}

# paginate 구현 못함
# class PostListInBoardSchema(PostListSchema):
#     class Meta:
#         fields = ['id', 'user', 'title', 'likes_count', 'comments_count', "created_at"]
#
#
# class PaginatedPostsInBoardSchema(Schema):
#     total = fields.Integer()
#     items = fields.Nested(PostListInBoardSchema, many=True)
