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
