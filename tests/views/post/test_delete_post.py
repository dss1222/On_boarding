import pytest
import json

from tests.factories.board import BoardFactory
from tests.factories.user import UserFactory
from tests.factories.post import PostFactory
from tests.factories.comment import CommentFactory

from app.post.postModel import Post
from app.comment.commentModel import Comment


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

    # 삭제 기능
    class Test_post_delete:
        class Test_삭제_정상요청:
            @pytest.fixture(scope="function")
            def subject(self, client, headers, board, post, url_get):
                return client.delete(url_get, headers=headers)

            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_return_count_zero(self, subject):
                post_cnt = Post.objects(is_deleted=False).count()
                assert post_cnt == 0

            def test_return_count_one_soft_delete(self, subject):
                post_cnt = Post.objects(is_deleted=True).count()
                assert post_cnt == 1

        class Test_삭제_실패:
            @pytest.fixture(scope="function")
            def subject(self, client, headers, board, post, url_get):
                return client.delete(url_get, headers={"Authorization": "asd"})

            def test_return_401(self, subject):
                assert subject.status_code == 401

            def test_return_count_1(self, subject):
                assert Post.objects(is_deleted=False).count() == 1

            def test_return_comment_ten(self, subject):
                comment_cnt = Comment.objects(is_deleted=False).count()
                assert comment_cnt == 10

            class Test_삭제된게시글:
                @pytest.fixture(scope="function")
                def subject(self, client, headers, board, post, url_get_deleted):
                    return client.delete(url_get_deleted, headers=headers)

                def test_return_404(self, subject):
                    assert subject.status_code == 404
