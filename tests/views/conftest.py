import jwt
import pytest

from flask import current_app
from bson.json_util import dumps as bson_dumps


@pytest.fixture()
def token(logged_in_user):
    if logged_in_user:
        return jwt.encode({"user_id": bson_dumps(logged_in_user.id), "username": bson_dumps(logged_in_user.username)},
                          current_app.config['SECRET'],
                          current_app.config['ALGORITHM'])
    else:
        return None


@pytest.fixture
def headers(token):
    if token:
        headers = {
            'Authorization': token
        }
    else:
        headers = None
    return headers
