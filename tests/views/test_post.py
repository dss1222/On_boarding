import factory
import pytest

import factory
import pytest
import json

from flask import url_for
from json import dumps

from tests.factories.board import BoardFactory
from tests.factories.user import UserFactory
from tests.factories.post import PostFactory


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

    class Test_post:
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