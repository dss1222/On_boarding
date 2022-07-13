import pytest

from flask import current_app


@pytest.fixture(scope="session") #fixture : 테스트함수를 실행할 때 필요한 조건을 미리 준비하는 함수
def app():
    from app import create_app
    app = create_app("test")
    return app


@pytest.fixture(scope='function', autouse=True) #호출하지 않아도 항상 호출됨(모든 상황에 필요한 경우 autouse=True)
def db(app):
    import mongoengine
    mongoengine.connect(host=current_app.config['MONGO_URI'])
    yield
    mongoengine.disconnect()


#conftest.py 테스트 실행에 공통적으로 필요한 것들을 정의해 놓는 파일

# import os
#
# import pytest
# import sys
# from flask import current_app, g
# from unittest import mock
#
# from pprint import pprint
#
#
# @pytest.fixture(scope="session")
# def app():
#     from app import create_app
#
#     os.environ["APP_ENV"] = "test"
#     app = create_app()
#     return app
#
#
# @pytest.fixture(scope="session", autouse=True)
# def app_context(app):
#     ctx = app.app_context()
#     ctx.push()
#     yield
#     ctx.pop()
#
#
# def create_mock_session():
#     return mock.Mock()
#
#
# @pytest.fixture
# def client(app):
#     return app.test_client()
#
#
# @pytest.fixture(scope="function", autouse=True)
# def db(app):
#     import mongoengine
#
#     mongoengine.connect(host=current_app.config["MONGO_URI"])
#     yield
#     mongoengine.disconnect()