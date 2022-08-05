import factory
import pytest
import json

from flask import url_for
from json import dumps

from tests.factories.user import UserFactory
from tests.factories.board import BoardFactory


class Test_BoardView:
    @pytest.fixture()
    def logged_in_user(self):
        return UserFactory.create()

    @pytest.fixture()
    def create_board(self, logged_in_user):
        return BoardFactory.create(name="testname",user=logged_in_user.id)

    class Test_게시판_작성:
        @pytest.fixture()
        def form(self):
            return {"name": "testname"}

        @pytest.fixture(scope="function")
        def subject(self, client, headers, form):
            return client.post("/boards/", data=json.dumps(form), headers=headers, content_type="application/json")

        def test_return_200(self, subject):
            print(subject)
            assert subject.status_code == 201
