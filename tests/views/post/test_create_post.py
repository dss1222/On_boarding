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
    def url_get(self, board, post):
        return "/boards/" + str(board.id) + "/posts/" + str(post.id)

    class Test_post_create:
        @pytest.fixture()
        def form(self):
            return {
                "title": "test_title",
                "content": "test_content",
                "tag": "test_tags"
            }

        @pytest.fixture(scope="function")
        def subject(self, client, headers, form, board):
            url = "/boards/" + str(board.id) + "/posts"
            return client.post(url, headers=headers, data=json.dumps(form))

        class Test_정상요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_return_count_one(self, subject):
                assert Post.objects.count() == 1

        class Test_보드id_error:
            @pytest.fixture(scope="function")
            def subject(self, client, headers, form):
                url = "/boards/" + "asdaasd" + "/posts"
                return client.post(url, headers=headers, data=json.dumps(form))

            def test_return_404(self, subject):
                assert subject.status_code == 404

        class Test_토큰이이상할경우:
            @pytest.fixture(scope="function")
            def subject(self, client, form, board):
                url = "/boards/" + str(board.id) + "/posts"
                return client.post(url, headers={"Authorization": "asd"}, data=json.dumps(form))

            def test_return_401(self, subject):
                assert subject.status_code == 401

        class Test_입력오류:
            @pytest.fixture()
            def form(self):
                return {
                    "title" : "title",
                    "con" : "contnet",
                    "tag" : "tag"
                }

            def test_return_400(self, subject):
                assert subject.status_code == 422