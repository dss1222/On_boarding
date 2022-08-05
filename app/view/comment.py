from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, doc

from app.serializers.comment import CommentCreateFormSchema, CommentDetailSchema
from app.service.validator import *


class CommentView(FlaskView):
    decorators = (doc(tags=['Comment']), login_required)

    # 코멘트 작성
    @route('/', methods=['POST'])
    @doc(description='댓글 작성', summary='댓글 작성')
    @marshal_with(SuccessSchema, code=201, description="성공")
    @use_kwargs(CommentCreateFormSchema())
    @post_validator
    def create(self, post_id, board_id, content):
        post = Post.objects().get(id=post_id)
        comment = Comment(content=content, user=g.user_id, post=post)
        comment.save()

        post.update(push__comments=str(comment))
        post.update(inc__comments_cnt=1)
        return "", 201

    # 좋아요 기능
    @route('/<string:comment_id>/likes', methods=['POST'])
    @doc(summary="댓글 좋아요", description="댓글 좋아요")
    @marshal_with(SuccessSchema, code=201, description="성공")
    @comment_validator
    def like(self, comment_id, board_id, post_id):
        comment = Comment.objects().get(id=comment_id)
        comment.like(g.user_id)
        return "", 201

    # 좋아요 취소
    @route('/<string:comment_id>/unlikes', methods=['POST'])
    @doc(summary="댓글 좋아요 취소", description="댓글 좋아요 취소")
    @marshal_with(SuccessSchema, code=201, description="성공")
    @comment_validator
    def unlike(self, comment_id, board_id, post_id):
        comment = Comment.objects().get(id=comment_id)
        comment.cancel_like(g.user_id)
        return "", 201

    # 댓글 조회
    @route('', methods=['GET'])
    @doc(summary="댓글 리스트 조회", description="댓글 리스트 조회")
    @marshal_with(CommentDetailSchema(many=True), code=200, description="댓글 리스트 조회")
    @post_validator
    def get_comments(self, board_id, post_id):
        comments = Comment.objects(post=post_id).order_by('-created_at').limit(10)

        return comments, 200
