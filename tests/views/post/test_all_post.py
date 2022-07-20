import pytest
import json

from tests.factories.board import BoardFactory
from tests.factories.user import UserFactory
from tests.factories.post import PostFactory

from app.post.postModel import Post
from tests.views.post.test_create_post import Test_게시글작성


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
    def url_get(self, board, post):
        return "/boards/" + str(board.id) + "/posts/" + str(post.id)

    class Test_post_create:
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
            return client.post(url, headers=headers, data=json.dumps(form))

        class Test_정상요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_return_count_one(self, subject):
                assert Post.objects.count() == 1

        class Test_보드id_error:
            @pytest.fixture(scope="function")
            def subject(self, client, headers, form):
                url = "/boards/" + "asdaasd" + "/posts"
                return client.post(url, headers=headers, data=json.dumps(form))

            def test_return_404(self, subject):
                assert subject.status_code == 404

        class Test_토큰이이상할경우:
            @pytest.fixture(scope="function")
            def subject(self, client, form, board):
                url = "/boards/" + str(board.id) + "/posts"
                return client.post(url, headers={"Authorization": "asd"}, data=json.dumps(form))

            def test_return_401(self, subject):
                assert subject.status_code == 401

    # 조회기능
    class Test_post_get:
        @pytest.fixture(scope="function")
        def subject(self, url_get, headers, client):
            return client.get(url_get, headers=headers)

        def test_details_post(self, subject, post):
            post_object = Post.objects.first()
            assert post_object.title == post.title

    # 검색기능
    class Test_search_tag:
        @pytest.fixture(scope="function")
        def subject(self, headers, client, board, post):
            url = "/boards/" + str(board.id) + "/posts/search/" + str(post.tag)
            return client.get(url, headers=headers)

        def test_search_tag(self, subject, post):
            body = subject.json
            posts = body['posts']
            assert posts[0]['title'] == post.title

        @pytest.fixture(scope="function")
        def subject2(self, headers, client, board, post):
            url = "/boards/" + str(board.id) + "/posts/search/없는검색어"
            return client.get(url, headers=headers)

        def test_search_tag_no(self, subject2):
            body = subject2.json
            posts = body['posts']
            with pytest.raises(IndexError):
                print(posts[0])

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

    # 삭제 기능
    class Test_post_delete:
        @pytest.fixture(scope="function")
        def subject(self, client, headers, board, post, url_get):
            return client.delete(url_get, headers=headers)

        class Test_삭제_정상요청:
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

    # 좋아요 기능
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
