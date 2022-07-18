import pytest
import json

from tests.factories.board import BoardFactory
from tests.factories.user import UserFactory
from tests.factories.post import PostFactory

from app.post.postModel import Post


class Test_Post:
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
        return "/boards/" + str(board.id) + "/posts/" + str(post.id)

    @pytest.fixture()
    def url_get_deleted(self, board, post_delete):
        return "/boards/" + str(board.id) + "/posts/" + str(post_delete.id)

    # 조회기능
    class Test_get_post:
        @pytest.fixture(scope="function")
        def subject(self, url_get, headers, client):
            return client.get(url_get, headers=headers)

        def test_details_post(self, subject):
            post = Post.objects.first()
            assert post.title == 'test_title'

        class Test_error_get_post:
            @pytest.fixture(scope="function")
            def subject(self, url_get_deleted, headers, client):
                return client.get(url_get_deleted, headers=headers)

            def test_details_post_error(self, subject):
                assert subject.status_code == 404

    # 검색기능
    class Test_search_tag:
        @pytest.fixture(scope="function")
        def subject(self, headers, client, board, post):
            url = "/boards/" + str(board.id) + "/posts/search/test"
            return client.get(url, headers=headers)

        def test_search_tag(self, subject):
            body = subject.json
            posts = body['posts']
            assert posts[0]['title'] == "test_title"
            assert len(posts) == 1

        @pytest.fixture(scope="function")
        def subject2(self, headers, client, board, post):
            url = "/boards/" + str(board.id) + "/posts/search/없는검색어"
            return client.get(url, headers=headers)

        def test_search_tag_no(self, subject2):
            body = subject2.json
            posts = body['posts']
            with pytest.raises(IndexError):
                print(posts[0])

