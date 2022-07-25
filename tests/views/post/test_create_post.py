import pytest
import json

from tests.factories.board import BoardFactory
from tests.factories.user import UserFactory
from tests.factories.post import PostFactory

from app.post.postModel import Post

class Test_게시글작성:
    @pytest.fixture()
    def logged_in_user(self):
        return UserFactory.create()

    @pytest.fixture()
    def board(self):
        return BoardFactory.create()

    @pytest.fixture()
    def post(self, board, logged_in_user):
        return PostFactory.create(board=board.id, user=logged_in_user.id, content_type="application/json")

    @pytest.fixture()
    def url_get(self, board, post):
        return "/boards/" + str(board.id) + "/posts/" + str(post.id)

    class Test_게시글_작성:
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
            return client.post(url, headers=headers, data=json.dumps(form), content_type="application/json")

        class Test_정상요청:
            def test_200_반환(self, subject):
                assert subject.status_code == 200

            def test_게시글갯수_1개_반환(self, subject):
                assert Post.objects.count() == 1

        class Test_보드id_에러:
            @pytest.fixture(scope="function")
            def subject(self, client, headers, form):
                url = "/boards/" + "asdaasd" + "/posts"
                return client.post(url, headers=headers, data=json.dumps(form), content_type="application/json")

            def test_400_반환(self, subject):
                assert subject.status_code == 404

        class Test_토큰이이상할경우:
            @pytest.fixture(scope="function")
            def subject(self, client, form, board):
                url = "/boards/" + str(board.id) + "/posts"
                return client.post(url, headers={"Authorization": "asd"}, data=json.dumps(form), content_type="application/json")

            def test_400_반환(self, subject):
                assert subject.status_code == 403

        class Test_입력오류:
            @pytest.fixture()
            def form(self):
                return {
                    "title" : "title",
                    "con" : "contnet",
                    "tag" : "tag"
                }

            def test_400_반환(self, subject):
                assert subject.status_code == 422