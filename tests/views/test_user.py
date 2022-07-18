import bcrypt
import pytest
import json

from tests.factories.user import UserFactory
from app.user.userModel import User


class Test_user:
    @pytest.fixture()
    def logged_in_user(self):
        return UserFactory.create()

    class Test_signup:
        @pytest.fixture()
        def form(self):
            return {
                "username": "test",
                "password": "test1234",
                "passwordCheck": "test1234"
            }

        @pytest.fixture(scope="function")
        def subject(self, client, form):
            return client.post("users/signup", data=json.dumps(form))

        class Test_정상요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

            def test_user_count_up(self, subject):
                total_user_cnt = User.objects.count()
                print(total_user_cnt)
                assert total_user_cnt == 1

            def test_username_OK(self, subject, form):
                username = User.objects()[0].username
                assert username == form["username"]

        class Test_중복계정:
            @pytest.fixture
            def form(self, logged_in_user):
                return {
                    "username": logged_in_user.username,
                    "password": "test1234",
                    "passwordCheck": "test1234"
                }

            def test_return_400(self, subject):
                # print(subject)
                assert subject.status_code == 409

    class Test_login():
        @pytest.fixture()
        def form(self, logged_in_user):
            return {
                "username": logged_in_user.username,
                "password": "test1234",
            }

        @pytest.fixture(scope="function")
        def subject(self, client, logged_in_user, form):
            return client.post("/users/login", data=json.dumps(form))

        class Test_정상요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

        class Test_아이디틀림:
            @pytest.fixture()
            def form(self):
                return {
                    "username": "aaron",
                    "password": "test1234",
                }

            def test_return_400(self, subject):
                assert subject.status_code == 401

        class Test_비밀번호틀림:
            @pytest.fixture()
            def form(self, logged_in_user):
                return {
                    "username": logged_in_user.username,
                    "password": "test12345678",
                }

            def test_return_400(self, subject):
                assert subject.status_code == 401

    class Test_update:
        @pytest.fixture()
        def form(self):
            return {
                "username": "update"
            }

        @pytest.fixture(scope="function")
        def subject(self, client, form, headers):
            return client.patch("/users/update", headers=headers, data=json.dumps(form))

        class Test_정상요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

        class Test_중복된닉네임일경우:
            @pytest.fixture()
            def form(self, logged_in_user):
                return {
                    "username": logged_in_user.username
                }

            def test_return_200(self, subject):
                assert subject.status_code == 409
