import pytest
import json

from tests.factories.board import BoardFactory
from tests.factories.user import UserFactory
from tests.factories.post import PostFactory
from tests.factories.comment import CommentFactory

from app.Model import *


class Test_게시글_삭제:
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
    def comment(self, post, logged_in_user):
        for _ in range(10):
            CommentFactory.create(post=post.id, user=logged_in_user.id, is_deleted=False)

    @pytest.fixture()
    def post_delete(self, board, logged_in_user):
        return PostFactory.create(board=board.id, user=logged_in_user.id, is_deleted=True)

    @pytest.fixture()
    def url_get(self, board, post):
        return "/boards/" + str(board.id) + "/posts/" + str(post.id)

    @pytest.fixture()
    def url_get_deleted(self, board, post_delete):
        return "/boards/" + str(board.id) + "/posts/" + str(post_delete.id)

    # 삭제 기능
    class Test_게시글삭제:
        class Test_삭제_정상요청:
            @pytest.fixture(scope="function")
            def subject(self, client, headers, board, post, url_get):
                return client.delete(url_get, headers=headers, content_type="application/json")

            def test_200_반환(self, subject):
                assert subject.status_code == 200

            def test_게시글갯수_0개_반환(self, subject):
                post_cnt = Post.objects(is_deleted=False).count()
                assert post_cnt == 0

            def test_softdelete_1개_반환(self, subject):
                post_cnt = Post.objects(is_deleted=True).count()
                assert post_cnt == 1

            def test_댓글갯수_0개_반환(self, comment, subject):
                comment_cnt = Comment.objects(is_deleted=False).count()
                assert comment_cnt == 0

        class Test_삭제실패:
            @pytest.fixture(scope="function")
            def subject(self, client, headers, board, post, url_get):
                return client.delete(url_get, headers={"Authorization": "asd"})

            def test_400_반환(self, subject):
                assert subject.status_code == 403

            def test_게시글갯수_1개_반환(self, subject):
                assert Post.objects(is_deleted=False).count() == 1

            def test_댓글갯수_10개_반환(self, comment, subject):
                comment_cnt = Comment.objects(is_deleted=False).count()
                assert comment_cnt == 10

            class Test_삭제된게시글:
                @pytest.fixture(scope="function")
                def subject(self, client, headers, board, post, url_get_deleted):
                    return client.delete(url_get_deleted, headers=headers)

                def test_400_반환(self, subject):
                    assert subject.status_code == 404
