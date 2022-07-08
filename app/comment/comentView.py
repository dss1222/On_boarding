from flask_classful import FlaskView, route
from flask import request, g

from app.comment.commentSchema import CommentCreateSchema, CommentListSchema
from app.comment.commentModel import Comment
from app.post.postModel import Post
from app.utils.validator import *
from app.utils.ErrorHandler import *


class CommentView(FlaskView):
    # 코멘트 작성
    @route('/<post_id>', methods=['POST'])
    @login_required
    @post_validator
    def create_comment(self, post_id):
        comment = CommentCreateSchema().load(json.loads(request.data))
        post = Post.objects(id=post_id).get()
        comment.user = g.user_id
        comment.post = post

        comment.save()

        post.update(push__comments=str(comment))

        return Success()

    @route('/recomment/<comment_id>', methods=['POST'])
    @login_required
    @comment_validator
    def create_recomment(self, comment_id):
        recomment = CommentCreateSchema().load(json.loads(request.data))
        comment = Comment.objects(id=comment_id).get()

        recomment.user = g.user_id

        recomment.save()

        comment.update(push__recomment=str(recomment))

        return Success()

    # 좋아요 기능
    @route('/likes/<comment_id>', methods=['POST'])
    @login_required
    @comment_validator
    def like_comment(self, comment_id):
        comment = Comment.objects(id=comment_id).get()
        comment.like(g.user_id)
        return Success()

    @route('/<post_id>/order/created', methods=['GET'])
    @login_required
    @post_validator
    def get_comments_created(self, post_id):
        comment_limit_10 = Comment.objects(post=post_id).order_by('-created_at').limit(10)
        comment_list = CommentListSchema(many=True).dump(comment_limit_10)
        return {'comments': comment_list}, 200
