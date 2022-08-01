from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, doc

from app.serializers.post import *
from app.service.validator import *

from app.service.post import PostService


class PostView(FlaskView):
    decorators = (doc(tags=['POST']), login_required, board_validator)

    # 게시글 작성
    @route('', methods=['POST'])
    @doc(description='게시글 작성', summary='게시글 작성')
    @use_kwargs(PostCreateSchema())
    @marshal_with(SuccessSchema, code=201, description="성공")
    def create(self, board_id, title, content, tag):
        PostService.create(board_id, title, content, tag)
        return "", 201

    # 게시글 상세조회 1개
    @route('/<string:post_id>', methods=['GET'])
    @doc(description='게시글 조회', summary='게시글 조회')
    @marshal_with(PostDetailSchema(), code=200, description="게시물 상세 정보")
    @post_validator
    def get_detail(self, post_id, board_id):
        return PostService.get_detail(post_id, board_id)

    # 게시글 리스트 조회
    @route('/', methods=['GET'])
    @doc(description='게시글 리스트 조회', summary='게시글 리스트 조회')
    @use_kwargs(PostListFilterSchema, location='query')
    @marshal_with(PostListSchema(many=True), code=200, description="게시글 리스트 조회")
    def get_posts(self, board_id, page, size, orderby):
        return PostService.get_posts(board_id, page, size, orderby)

    # 게시글 수정 <회원정보 일치해야 함>
    @route('/<string:post_id>', methods=['PATCH'])
    @doc(description='게시글 수정', summary='게시글 수정')
    @use_kwargs(PostUpdateSchema())
    @marshal_with(SuccessSchema, code=201, description="성공")
    @post_user_validator
    def update(self, post_id, board_id, title, content, tag):
        PostService.post_update(post_id, title, content, tag)
        return "", 201

    # 게시글 삭제
    @route('/<string:post_id>', methods=['DELETE'])
    @doc(description='게시글 삭제', summary='게시글 삭제')
    @marshal_with(SuccessSchema, code=201, description="성공")
    @post_user_validator
    def delete(self, post_id, board_id):
        PostService.delete(post_id)
        return "", 201

    # 좋아요 기능
    @route('/<string:post_id>/likes', methods=['POST'])
    @doc(summary="게시물 좋아요", description="게시물 좋아요")
    @marshal_with(SuccessSchema, code=201, description="성공")
    @post_validator
    def like(self, board_id, post_id):
        return PostService.like(post_id)

    # 좋아요 취소
    @route('/<string:post_id>/unlikes', methods=['POST'])
    @doc(summary="게시물 좋아요 취소", description="게시물 좋아요 취소")
    @marshal_with(SuccessSchema, code=201, description="성공")
    @post_validator
    def unlike(self, board_id, post_id):
        PostService.unlike(post_id)
        return "", 201

    # 태그 검색 기능
    @route('/search/<search>', methods=['GET'])
    @doc(description='게시글 검색 조회', summary='게시글 검색 조회')
    @marshal_with(PostListSchema(many=True), code=200, description="게시물 상세 정보")
    def search(self, board_id, search):
        return PostService.search(board_id, search)