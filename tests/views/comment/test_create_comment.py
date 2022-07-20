import json
import pytest

from tests.factories.board import BoardFactory
from tests.factories.user import UserFactory
from tests.factories.post import PostFactory
from tests.factories.comment import CommentFactory

from app.post.postModel import Post
from app.comment.commentModel import Comment


class Test_댓글작성:
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
        return CommentFactory.create(post=post.id, user=logged_in_user.id)

    @pytest.fixture()
    def url_get(self, board, post):
        return "/boards/" + str(board.id) + "/posts/" + str(post.id) + "/comments/"

    class Test_댓글_작성:
        @pytest.fixture()
        def form(self):
            return {
                "content": "test_content"
            }

        @pytest.fixture(scope="function")
        def subject(self, client, headers, form, url_get):
            return client.post(url_get, headers=headers, data=json.dumps(form))

        class Test_댓글_생성:
            def test_200_반환(self, subject):
                assert subject.status_code == 200

            def test_댓글갯수_1개_반환(self, subject):
                assert Comment.objects.count() == 1

            def test_댓글내용_검증(self, subject):
                comments = Comment.objects.first()
                assert comments.content == "test_content"

            # @pytest.fixture()
            # def post_subject(self, client, subject, board, post, headers):
            #     url = "/boards/" + str(board.id) + "/posts/" + str(post.id)
            #     return client.get(url, headers=headers)
            #
            # def test_get_post_comment_cnt_one(self, subject, post_subject):
            #     body = post_subject.json
            #     comments = Comment.objects.first()
            #     assert body['comments_cnt'] == 1
            #     assert comments.is_deleted == False
            #
            # @pytest.fixture()
            # def post_delete_subject(self, client, subject, board, post, headers):
            #     url = "/boards/" + str(board.id) + "/posts/" + str(post.id)
            #     return client.delete(url, headers=headers)
            #
            # def test_get_post_comment_cnt_zero(self, subject, post_delete_subject, post_subject):
            #     comments = Comment.objects.first()
            #     assert comments.is_deleted == True

        class Test_대댓글_생성:
            @pytest.fixture()
            def form(self):
                return {
                    "content": "test_recontent"
                }

            @pytest.fixture(scope="function")
            def subject(self, client, headers, form, url_get, comment):
                url = url_get + str(comment.id) + "/recomment"
                return client.post(url, headers=headers, data=json.dumps(form))

            def test_200_반환(self, subject):
                assert subject.status_code == 200

            def test_내용_검증(self, subject):
                comments = Comment.objects()[1].content
                assert comments == "test_recontent"

            def test_댓글총갯수_2개(self, subject):
                comments_cnt = Comment.objects.count()
                assert comments_cnt == 2

        class Test_댓글_생성_오류:
            @pytest.fixture()
            def form(self):
                return {
                    "contentt": "contentt"
                }

            def test_400_반환(self, subject):
                assert subject.status_code == 422
