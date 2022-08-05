from flask_classful import FlaskView, route
from flask_apispec import marshal_with, doc

from app.service.validator import login_required
from app.serializers.post import *
from app.serializers.comment import *
from app.models.post import Post
from app.models.comment import Comment


class MyPageView(FlaskView):
    decorators = (doc(tags=['My_Page']),)

    # 내가 쓴글 조회
    @route('/posts', methods=['GET'])
    @doc(description='내가 쓴글 조회', summary='내가 쓴글 조회')
    @marshal_with(PostListSchema(many=True), code=200, description="내가 쓴글 조회")
    @login_required
    def get_myposts(self):
        posts = Post.objects(user=g.user_id, is_deleted=False)
        return posts, 200

    # 내가 작성한 코멘트 조회
    @route('/comments', methods=['GET'])
    @doc(description='내가 쓴 댓글 조회', summary='내가 쓴 댓글 조회')
    @marshal_with(CommentDetailSchema(many=True), code=200, description="내가 쓴 댓글 조회")
    @login_required
    def get_mycomments(self):
        comments = Comment.objects(user=g.user_id, is_deleted=False)
        return comments, 200

    # 내가 좋아요한 글 조회
    @route('/posts/likes', methods=['GET'])
    @doc(description='내가 좋아요 한 글 조회', summary='내가 좋아요 한 글 조회')
    @marshal_with(PostListSchema(many=True), code=200, description="내가 좋아요 한 글 조회")
    @login_required
    def get_myposts_likes(self):
        posts = Post.objects(likes__exact=str(g.user_id), is_deleted=False)
        return posts, 200
