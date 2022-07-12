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
