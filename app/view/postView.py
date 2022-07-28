from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, doc

from app.serializers.postSchema import *
from app.utils.validator import *

from app.service.postService import PostService


class PostView(FlaskView):
    decorators = (doc(tags=['POST']), login_required, board_validator)

    # 게시글 작성
    @route('', methods=['POST'])
    @doc(description='게시글 작성', summary='게시글 작성')
    @use_kwargs(PostCreateSchema())
    @marshal_with(SuccessSchema, code=200, description="성공")
    @create_post_validator
    def create_post(self, board_id, post):
        return PostService.post_create(board_id, post)

    # 게시글 상세조회 1개
    @route('/<string:post_id>', methods=['GET'])
    @doc(description='게시글 조회', summary='게시글 조회')
    @marshal_with(PostDetailSchema(), code=200, description="게시물 상세 정보")
    @post_validator
    def get_posts_detail(self, post_id, board_id):
        return PostService.post_get_detail(post_id, board_id)

    # 게시글 리스트 조회
    @route('/', methods=['GET'])
    @doc(description='게시글 리스트 조회', summary='게시글 리스트 조회')
    @use_kwargs(PostListFilterSchema, location='query')
    @marshal_with(PostListSchema(many=True), code=200, description="게시글 리스트 조회")
    @post_list_validator
    def get_posts_pagination(self, board_id, page, size, orderby):
        return PostService.post_get_post_list(board_id, page, size, orderby)

    # 게시글 수정 <회원정보 일치해야 함>
    @route('/<string:post_id>', methods=['PATCH'])
    @doc(description='게시글 수정', summary='게시글 수정')
    @use_kwargs(PostUpdateSchema())
    @marshal_with(SuccessSchema, code=200, description="성공")
    @post_user_validator
    def update_post(self, post_id, board_id, post):
        return PostService.post_update(post_id, board_id, post)

    # 게시글 삭제
    @route('/<string:post_id>', methods=['DELETE'])
    @doc(description='게시글 삭제', summary='게시글 삭제')
    @marshal_with(SuccessSchema, code=200, description="성공")
    @post_user_validator
    def delete_post(self, post_id, board_id):
        return PostService.post_delete(post_id, board_id)

    # 좋아요 기능
    @route('/<string:post_id>/likes', methods=['POST'])
    @doc(summary="게시물 좋아요", description="게시물 좋아요")
    @marshal_with(SuccessSchema, code=200, description="성공")
    @post_validator
    def like_post(self, board_id, post_id):
        return PostService.post_like(board_id, post_id)

    # 좋아요 취소
    @route('/<string:post_id>/unlikes', methods=['POST'])
    @doc(summary="게시물 좋아요 취소", description="게시물 좋아요 취소")
    @marshal_with(SuccessSchema, code=200, description="성공")
    @post_validator
    def unlike_post(self, board_id, post_id):
        return PostService.post_unlike(board_id, post_id)

    # 태그 검색 기능
    @route('/search/<search>', methods=['GET'])
    @doc(description='게시글 검색 조회', summary='게시글 검색 조회')
    @marshal_with(PostListSchema(many=True), code=200, description="게시물 상세 정보")
    def search_post(self, board_id, search):
        return PostService.post_search(board_id, search)
