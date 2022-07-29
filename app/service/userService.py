import jwt
import bcrypt

from flask import  g, current_app
from bson.json_util import dumps

from app.utils.ApiErrorSchema import *
from app.Model import *
from app.serializers.postSchema import *


class UserService:
    @classmethod
    def signup(cls, username, password):
        if User.objects(username=username):
            return 409
        else:
            hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            user = User(username=username, password=hash_password)
            user.save()
            return 201

    @classmethod
    def login(cls, username, password):
        try:
            user = User.objects(username=username).get()
        except DoesNotExist as err:
            return 401

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

    @classmethod
    def get_myposts(cls):
        posts = Post.objects(user=g.user_id, is_deleted=False)
        return posts, 200

    @classmethod
    def get_mycomments(cls):
        comments = Comment.objects(user=g.user_id, is_deleted=False)
        return comments, 200

    @classmethod
    def get_mylikes(cls):
        posts = Post.objects(likes__exact=str(g.user_id), is_deleted=False)
        return posts, 200
