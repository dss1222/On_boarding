import pytest
import json

from tests.factories.board import BoardFactory
from tests.factories.user import UserFactory
from tests.factories.post import PostFactory

from app.post.postModel import Post
from app.user.userModel import User

class Test_mypage:
    @pytest.fixture()
    def logged_in_user(self):
        return UserFactory.create()

    @pytest.fixture()
    def board(self):
        return BoardFactory.create()

    @pytest.fixture()
    def post(self, board, logged_in_user):
        return PostFactory.create(board=board.id,user=logged_in_user.id)

    @pytest.fixture()
    def url_get(self, board, post):
        return "/users/mypage"

    class Test_mypost:
        @pytest.fixture(scope="function")
        def subject(self, client, headers, url_get, post):
            url = url_get + "/posts"
            return client.get(url, headers=headers)

        def test_return_200(self, subject):
            assert subject.status_code == 200
