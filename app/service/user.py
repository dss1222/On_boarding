import jwt
import bcrypt
from flask import g, current_app
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

        token = jwt.encode({"user_id": dumps(user.id), "username": dumps(user.username)},
                           current_app.config['SECRET'], current_app.config['ALGORITHM'])
        return AuthToken.create(token_=token)

    @classmethod
    def user_update(cls, username):
        if not User.objects(username=username):
            user = User.objects(id=g.user_id).get()
            user.update(username=username)
            return 201
        else:
            return 409
