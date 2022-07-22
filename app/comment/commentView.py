from flask_classful import FlaskView, route

from app.comment.commentSchema import CommentCreateSchema, CommentListSchema
from app.utils.validator import *
from app.utils.ErrorHandler import *
from bson import ObjectId


class CommentView(FlaskView):
    # 코멘트 작성
    @route('/', methods=['POST'])
    @marshal_with(SuccessSchema, code=200, description="성공")
    @login_required
    @create_comment_validator
    @post_validator
    def create_comment(self, post_id, board_id):
        comment = CommentCreateSchema().load(json.loads(request.data))
        post = Post.objects(id=post_id).get()
        comment.user = g.user_id
        comment.post = post

        comment.save()

        post.update(push__comments=str(comment))
        post.update(inc__comments_cnt=1)

        return SuccessDto()

    # 대댓글
    @route('/<string:comment_id>/recomment', methods=['POST'])
    @marshal_with(SuccessSchema, code=200, description="성공")
    @login_required
    @comment_validator
    def create_recomment(self, board_id, post_id, comment_id):
        re_comment = CommentCreateSchema().load(json.loads(request.data))
        comment = Comment.objects(id=comment_id).get()

        re_comment.user = g.user_id
        re_comment.post = ObjectId(post_id)
        re_comment.recomment = ObjectId(comment_id)
        re_comment.save()

        return SuccessDto()

    # 좋아요 기능
    @route('/<string:comment_id>/likes', methods=['POST'])
    @marshal_with(SuccessSchema, code=200, description="성공")
    @login_required
    @comment_validator
    def like_comment(self, comment_id, board_id, post_id):
        comment = Comment.objects(id=comment_id).get()
        comment.like(g.user_id)
        return SuccessDto()

    # 좋아요 취소
    @route('/<string:comment_id>/unlikes', methods=['POST'])
    @marshal_with(SuccessSchema, code=200, description="성공")
    @login_required
    @comment_validator
    def unlike_comment(self, comment_id, board_id, post_id):
        comment = Comment.objects(id=comment_id).get()
        comment.cancel_like(g.user_id)
        return SuccessDto()

    #댓글 조회
    @route('/order/created', methods=['GET'])
    @login_required
    @post_validator
    def get_comments_created(self, post_id):
        comment_limit_10 = Comment.objects(post=post_id).order_by('-created_at').limit(10)
        comment_list = CommentListSchema(many=True).dump(comment_limit_10)
        return {'comments': comment_list}, 200
