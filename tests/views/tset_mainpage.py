import pytest
import random

from tests.factories.board import BoardFactory
from tests.factories.user import UserFactory
from tests.factories.posts import PostFactory


class Test_메인페이지:
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

    class Test_좋아요순_정렬:
        @pytest.fixture()
        def posts(self, board, logged_in_user):
            PostFactory.create(board=board.id, user=logged_in_user.id, likes_cnt=20)
            PostFactory.create(board=board.id, user=logged_in_user.id, likes_cnt=0)
            for _ in range(8):
                PostFactory.create(board=board.id, user=logged_in_user.id, likes_cnt=random.randint(1, 20))

        @pytest.fixture()
        def subject(self, client, headers, board, posts, url_get):
            url = "/boards/" + str(board.id) + "/posts/?page=1&size=20&orderby=likes"
            return client.get(url, headers=headers, content_type="application/json")

        class Test_정상요청:
            def test_200_반환(self, subject):
                assert subject.status_code == 200

            def test_리스트_반환(self, subject):
                body = subject.json
                assert len(body) == 10

            def test_좋아요_가장많은것_반환(self, subject):
                body = subject.json
                posts = body
                max_num = posts[0]['likes_cnt']
                min_num = posts[9]['likes_cnt']

                assert max_num == 20
                assert min_num == 0

    class Test_댓글_많은순:
        @pytest.fixture()
        def posts(self, board, logged_in_user):
            PostFactory.create(board=board.id, user=logged_in_user.id, comments_cnt=20)
            PostFactory.create(board=board.id, user=logged_in_user.id, comments_cnt=0)
            for _ in range(8):
                PostFactory.create(board=board.id, user=logged_in_user.id, comments_cnt=random.randint(1, 20))

        @pytest.fixture()
        def subject(self, client, headers, board, posts, url_get):
            url = "/boards/" + str(board.id) + "/posts/?page=1&size=20&orderby=comments"
            return client.get(url, headers=headers, content_type="application/json")

        class Test_정상요청:
            def test_200_반환(self, subject):
                assert subject.status_code == 200

            def test_리스트_반환(self, subject):
                body = subject.json
                assert len(body) == 10

            def test_좋아요가장많은것_반환(self, subject):
                body = subject.json
                posts = body
                max_num = posts[0]['comments_cnt']
                min_num = posts[9]['comments_cnt']

                assert max_num == 20
                assert min_num == 0

    # class Test_order_by_created: