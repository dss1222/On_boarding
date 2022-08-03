import datetime

import jwt
import bcrypt
from flask import g, current_app, request
from bson.json_util import dumps

from app.utils.ApiErrorSchema import *
from app.models.user import User


class UserService:
    @classmethod
    def signup(cls, username, password):
        if User.objects(username=username):
            return 409
        else:
            hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            user = User(username=username, password=hash_password, type='default')
            user.save()
            return 201

    @classmethod
    def login(cls, username, password):
        if not User.objects(username=username):
            return 401
        else:
            user = User.objects().get(username=username)

        if user.type == 'default':
            if not user.check_password(password):
                return 401
        return AuthToken.create(user=user)

    @classmethod
    def refresh(cls):
        user = User.objects().get(id=g.user_id)
        return AuthToken.create_access_token(user=user)

    @classmethod
    def user_update(cls, username):
        if not User.objects(username=username):
            user = User.objects(id=g.user_id).get()
            user.update(username=username)
            return 201
        else:
            return 409
