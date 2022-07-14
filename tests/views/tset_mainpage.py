import factory
import pytest
import json
import random

from tests.factories.board import BoardFactory
from tests.factories.user import UserFactory
from tests.factories.post import PostFactory

from app.post.postModel import Post


class Test_post_get:
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
    def url_get(self, board):
        return "/boards/" + str(board.id) + "/posts/order"

    class Test_order_by_likes:
        @pytest.fixture()
        def posts(self, board, logged_in_user):
            PostFactory.create(board=board.id, user=logged_in_user.id, likes_cnt=20)
            PostFactory.create(board=board.id, user=logged_in_user.id, likes_cnt=0)
            for _ in range(8):
                PostFactory.create(board=board.id, user=logged_in_user.id, likes_cnt=random.randint(1, 20))

        @pytest.fixture()
        def subject(self, client, headers, posts, url_get):
            url = url_get + "/likes"
            return client.get(url, headers=headers)

        class Test_정상요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_return_list(self, subject):
                body = subject.json
                assert len(body['posts']) == 10

            def test_return_most_many_likes(self, subject):
                body = subject.json
                posts = body['posts']
                max_num = posts[0]['likes_cnt']
                min_num = posts[9]['likes_cnt']

                assert max_num == 20
                assert min_num == 0

    class Test_order_by_comments:
        @pytest.fixture()
        def posts(self, board, logged_in_user):
            PostFactory.create(board=board.id, user=logged_in_user.id, comments_cnt=20)
            PostFactory.create(board=board.id, user=logged_in_user.id, comments_cnt=0)
            for _ in range(8):
                PostFactory.create(board=board.id, user=logged_in_user.id, comments_cnt=random.randint(1, 20))

        @pytest.fixture()
        def subject(self, client, headers, posts, url_get):
            url = url_get + "/comments"
            return client.get(url, headers=headers)

        class Test_정상요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_return_list(self, subject):
                body = subject.json
                assert len(body['posts']) == 10

            def test_return_most_many_likes(self, subject):
                body = subject.json
                posts = body['posts']
                max_num = posts[0]['comments_cnt']
                min_num = posts[9]['comments_cnt']

                assert max_num == 20
                assert min_num == 0

    # class Test_order_by_created: