import pytest

from tests.factories.board import BoardFactory
from tests.factories.user import UserFactory
from tests.factories.post import PostFactory

from app.models.board import *


class Test_게시글좋아요:
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

    class Test_게시글_좋아요:
        @pytest.fixture(scope="function")
        def subject(self, client, headers, url_get):
            url = url_get + "/likes"
            return client.post(url, headers=headers, content_type="application/json")

        class Test_정상요청:
            def test_200_반환(self, subject):
                assert subject.status_code == 201

            def test_좋아요갯수_1개반환(self, subject):
                post = Post.objects.first()
                assert post.likes_cnt == 1

            class Test_좋아요취소:
                @pytest.fixture(scope="function")
                def subject2(self, client, headers, url_get):
                    url = url_get + "/unlikes"
                    return client.post(url, headers=headers, content_type="application/json")

                def test_200_반환(self, subject2):
                    assert subject2.status_code == 201

                def test_좋아요갯수_0개반환(self, subject, subject2):
                    post = Post.objects.first()
                    assert post.likes_cnt == 0

        class Test_삭제된게시글:
            @pytest.fixture(scope="function")
            def subject(self, client, headers, url_get_deleted):
                url = url_get_deleted + "/likes"
                return client.post(url, headers=headers, content_type="application/json")

            def test_400_반환(self, subject):
                assert subject.status_code == 404
