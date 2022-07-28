import jwt

from flask import request, g, current_app
from bson.json_util import dumps

from app.utils.ApiErrorSchema import *
from app.Model import *
from app.serializers.postSchema import *


class UserService:
    @classmethod
    def user_signup(cls, user):
        if User.objects(username=user.username):
            return NotCreateUsername()
        else:
            user.save()
            return SuccessDto(), 200

    @classmethod
    def user_login(cls, user):
        if not user:
            return NotUser()

        if not user.check_password(request.json["password"]):
            return NotPassword()

        token = jwt.encode({"user_id": dumps(user.id), "username": dumps(user.username)},
                           current_app.config['SECRET'], current_app.config['ALGORITHM'])
        return AuthToken.create(token_=token)

    @classmethod
    def user_update(cls, username):
        if not User.objects(username=username):
            user = User.objects(id=g.user_id).get()
            user.update(username=username)
            return SuccessDto(), 200
        else:
            return NotCreateUsername()

    @classmethod
    def user_get_myposts(cls):
        posts = Post.objects(user=g.user_id, is_deleted=False)
        return posts, 200

    @classmethod
    def user_get_mycomments(cls):
        comments = Comment.objects(user=g.user_id, is_deleted=False)
        return comments, 200

    @classmethod
    def user_get_mylikes(cls):
        posts = Post.objects(likes__exact=str(g.user_id), is_deleted=False)
        return posts, 200
