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

    # 수정 기능
    class Test_post_update:
        @pytest.fixture()
        def form(self):
            return {
                "title": "test_title_update",
                "content": "test_content_update",
                "tag": "test_tags_update"
            }

        @pytest.fixture(scope="function")
        def subject(self, client, headers, form, url_get):
            return client.patch(url_get, headers=headers, data=json.dumps(form))

        class Test_정상요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_return_update_get(self, subject, form, logged_in_user):
                post = Post.objects.first()
                assert post.title == 'test_title_update'
                assert post.content == form['content']
                assert post.tag == form['tag']
                assert post.user == logged_in_user

        class Test_삭제된게시글:
            @pytest.fixture(scope="function")
            def subject(self, client, headers, form, url_get_deleted):
                return client.patch(url_get_deleted, headers=headers, data=json.dumps(form))

            def test_return_404(self, subject):
                assert subject.status_code == 404

