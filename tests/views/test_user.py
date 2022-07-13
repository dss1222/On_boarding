import bcrypt
import pytest
import uuid
import factory
import jwt
import json

from flask import url_for, current_app
from json import dumps

from tests.factories.board import BoardFactory
from tests.factories.user import UserFactory
from app.user.userModel import User
from app.post.postModel import Post


class Test_user:
    @pytest.fixture()
    def logged_in_user(self):
        return UserFactory.create()

    class Test_signup:
        @pytest.fixture()
        def form(self):
            return {
                "username": "test",
                "password": "test1234"
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
                    "password": "test1234"
                }

            def test_return_400(self, subject):
                # print(subject)
                assert subject.status_code == 409

    class Test_login():
        @pytest.fixture()
        def signup_user(self):
            return UserFactory.create(username="username", password=bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))

        @pytest.fixture()
        def form(self):
            return {
                "username": "username",
                "password": "password",
            }

        @pytest.fixture(scope="function")
        def subject(self, client, signup_user, form):
            return client.post("/users/login", data=json.dumps(form))

        class Test_정상요청:
            def test_return_200(self, subject):
                assert subject.status_code == 200

