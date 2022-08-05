import pytest

from tests.factories.board import BoardFactory
from tests.factories.user import UserFactory
from tests.factories.post import PostFactory
from tests.factories.comment import CommentFactory

from app.models.models import *


class Test_댓글_좋아요:
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
    def comment(self, board, post, logged_in_user):
        return CommentFactory.create(post=post.id, user=logged_in_user.id)

    @pytest.fixture()
    def url_get(self, board, post, comment):
        return "/boards/" + str(board.id) + "/posts/" + str(post.id) + "/comments/" + str(comment.id) + "/"

    @pytest.fixture()
    def url_get_deleted(self, board, post_delete, comment):
        return "/boards/" + str(board.id) + "/posts/" + str(post_delete.id) + "/comments/" + str(comment.id) + "/"

    class Test_댓글_좋아요:
        @pytest.fixture(scope="function")
        def subject(self, client, headers, url_get):
            url = url_get + "likes"
            return client.post(url, headers=headers, content_type="application/json")

        class Test_좋아요:
            def test_200_반환(self, subject):
                print(subject)
                assert subject.status_code == 201

            def test_좋아요갯수_1개_반환(self, subject):
                comment = Comment.objects.first()
                assert comment.likes_cnt == 1

            class Test_좋아요취소:
                @pytest.fixture(scope="function")
                def subject2(self, client, headers, url_get):
                    url = url_get + "unlikes"
                    return client.post(url, headers=headers, content_type="application/json")

                def test_200_반환(self, subject2):
                    assert subject2.status_code == 201

                def test_좋아요갯수_0개_반환(self, subject, subject2):
                    comment = Comment.objects.first()
                    assert comment.likes_cnt == 0


