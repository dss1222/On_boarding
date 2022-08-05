import pytest

from flask import url_for

from tests.factories.board import BoardFactory
from tests.factories.user import UserFactory
from tests.factories.post import PostFactory

from app.models.Model import *


class Test_게시글조회:
    @pytest.fixture()
    def logged_in_user(self):
        return UserFactory.create()

    @pytest.fixture()
    def board(self):
        return BoardFactory.create()

    @pytest.fixture()
    def post(self, board, logged_in_user):
        return PostFactory.create(board=board.id, user=logged_in_user.id)

    @pytest.fixture()
    def post_delete(self, board, logged_in_user):
        return PostFactory.create(board=board.id, user=logged_in_user.id, is_deleted=True)

    @pytest.fixture()
    def url_get(self, board, post):
        return f"/boards/{str(board.id)}/posts/{str(post.id)}"

    @pytest.fixture()
    def url_get_deleted(self, board, post_delete):
        return f"/boards/{str(board.id)}/posts/{str(post_delete.id)}"

    # 조회기능
    class Test_게시글_조회:
        @pytest.fixture(scope="function")
        def subject(self, url_get, headers, client):
            return client.get(url_get, headers=headers, content_type="application/json")

        def test_게시글_자세히보기_내용검증(self, subject, post):
            post_object = Post.objects.first()
            assert post_object.title == post.title

        class Test_삭제된게시글_조회:
            @pytest.fixture(scope="function")
            def subject(self, url_get_deleted, headers, client):
                return client.get(url_get_deleted, headers=headers, content_type="application/json")

            def test_자세히보기_400_반환(self, subject):
                assert subject.status_code == 404

        class Test_페이징게시글_조회:
            @pytest.fixture()
            def post_list(self, board, logged_in_user):
                for _ in range(4):
                    PostFactory.create(board=board.id, user=logged_in_user.id)

            @pytest.fixture(scope="function")
            def subject(self, headers, client, board, post_list):
                # url = "/boards/" + str(board.id) + "/posts/?page=1&size=3&orderby=created"
                # url = url_for(f"/boards/{str(board.id)}/posts/", page=1, size=3, orderby="created")

                url = f"/boards/{str(board.id)}/posts/?page={1}&size={3}&orderby=created"
                return client.get(url, headers=headers, content_type="application/json", )
                # params={'page': 1, 'size': 3, 'orderby': 'created'},)

            def test_200_반환(self, subject):
                assert subject.status_code == 200

            def test_게시글_갯수(self, subject):
                body = subject.json
                assert len(body) == 3

            # class Test_페이징조회_에러:
            #     @pytest.fixture()
            #     def subject(self, headers, client, board, post_list):
            #         url = "/boards/" + str(board.id) + "/posts/?page=1&size=3&orderby=create"
            #         return client.get(url, headers=headers, content_type="application/json")
            #
            #     def test_400_반환(self, subject):
            #         assert subject.status_code == 422

    # 검색기능
    class Test_검색기능:
        @pytest.fixture(scope="function")
        def subject(self, headers, client, board, post):
            url = f"/boards/{str(board.id)}/posts/search/?search={str(post.tag)}"
            return client.get(url, headers=headers, content_type="application/json")

        def test_태그_검색(self, subject, post):
            body = subject.json
            assert body[0]['title'] == post.title
            assert len(body) == 1

        @pytest.fixture(scope="function")
        def subject2(self, headers, client, board, post):
            url = f"/boards/{str(board.id)}/posts/search/?search=없는검색어"
            return client.get(url, headers=headers, content_type="application/json")

        def test_없는태그_검색(self, subject2):
            body = subject2.json
            with pytest.raises(IndexError):
                print(body[0])
