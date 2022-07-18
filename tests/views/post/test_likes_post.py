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

    class Test_post_likes:
        @pytest.fixture(scope="function")
        def subject(self, client, headers, url_get):
            url = url_get + "/likes"
            return client.post(url, headers=headers)

        class Test_정상요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_return_likecnt_one(self, subject):
                post = Post.objects.first()
                assert post.likes_cnt == 1

            class Test_좋아요취소:
                @pytest.fixture(scope="function")
                def subject2(self, client, headers, url_get):
                    url = url_get + "/unlikes"
                    return client.post(url, headers=headers)

                def test_return_200(self, subject2):
                    assert subject2.status_code == 200

                def test_return_count_0(self, subject, subject2):
                    post = Post.objects.first()
                    assert post.likes_cnt == 0

                class Test_다른계정_두번좋아요:
                    @pytest.fixture(scope="function")
                    def subject2(self, client, headers, url_get):
                        url = url_get + "/likes"
                        return client.post(url, headers={
                            "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoie1wiJG9pZFwiOiBcIjYyYzc5YTAwYzUxMzZmZmQ3NjliZmRiN1wifSIsInVzZXJuYW1lIjoiXCJkc3MxMjIyNDdcIiJ9.0c12IDYOTc6PHf18yrdTF9seS6tP95dAEhZ6w7rFhYA"})

                    def test_return_200(self, subject2):
                        assert subject2.status_code == 200

                    def test_return_count_2(self, subject, subject2):
                        post = Post.objects.first()
                        assert post.likes_cnt == 2

                class Test_두번좋아요_실패:
                    @pytest.fixture(scope="function")
                    def subject2(self, client, headers, url_get):
                        url = url_get + "/likes"
                        return client.post(url, headers={
                            "Authorization": "zI1NiJ9.eyJ1c2VyX2lkIjoie1wiJG9pZFwiOiBcIjYyYzc5YTAwYzUxMzZmZmQ3NjliZmRiN1wifSIsInVzZXJuYW1lIjoiXCJkc3MxMjIyNDdcIiJ9.0c12IDYOTc6PHf18yrdTF9seS6tP95dAEhZ6w7rFhYB"})

                    def test_return_401(self, subject2):
                        assert subject2.status_code == 401

                    def test_return_count_1(self, subject, subject2):
                        post = Post.objects.first()
                        assert post.likes_cnt == 1

        class Test_삭제된게시글:
            @pytest.fixture(scope="function")
            def subject(self, client, headers, url_get_deleted):
                url = url_get_deleted + "/likes"
                return client.post(url, headers=headers)

            def test_return_404(self, subject):
                assert subject.status_code == 404
