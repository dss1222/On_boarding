from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, marshal_with, doc

from app.service.validator import login_required
from app.serializers.post import *
from app.serializers.comment import CommentListSchema
from app.service.mypage import MyPageService


class MyPageView(FlaskView):
    decorators = (doc(tags=['My_Page']),)

    # 내가 쓴글 조회
    @route('/posts', methods=['GET'])
    @doc(description='내가 쓴글 조회', summary='내가 쓴글 조회')
    @marshal_with(PostListSchema(many=True), code=200, description="내가 쓴글 조회")
    @login_required
    def get_myposts(self):
        return MyPageService.get_myposts()

    # 내가 작성한 코멘트 조회
    @route('/comments', methods=['GET'])
    @doc(description='내가 쓴 댓글 조회', summary='내가 쓴 댓글 조회')
    @marshal_with(CommentListSchema(many=True), code=200, description="내가 쓴글 조회")
    @login_required
    def get_mycomments(self):
        return MyPageService.get_mycomments()

    # 내가 좋아요한 글 조회
    @route('/posts/likes', methods=['GET'])
    @doc(description='내가 좋아요 한 글 조회', summary='내가 좋아요 한 글 조회')
    @marshal_with(PostListSchema(many=True), code=200, description="내가 좋아요 한 글 조회")
    @login_required
    def get_myposts_likes(self):
        return MyPageService.get_mylikes()
