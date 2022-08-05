import bcrypt
from flask import g

from app.models.user import User
from app.service.auth import *


class UserService:
    @classmethod
    def signup(cls, username, password):
        if User.objects(username=username):
            return 409
        else:
            hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            user = User(username=username, password=hash_password, provider='default')
            user.save()
            return 201

    @classmethod
    def login(cls, username, password):
        if not User.objects(username=username):
            return 401
        else:
            user = User.objects().get(username=username)

        if user.provider == 'default':
            if not user.check_password(password):
                return 401
        return AuthToken.create(user=user)

    @classmethod
    def check(cls):
        user = User.objects().get(id=g.user_id)
        return user

    @classmethod
    def refresh(cls):
        user = User.objects().get(id=g.user_id)
        return AuthToken.create_access_token(user=user)

    @classmethod
    def user_update(cls, username):
        if not User.objects(username=username):
            user = User.objects().get(id=g.user_id)
            user.update(username=username)
            return 201
        else:
            return 409
