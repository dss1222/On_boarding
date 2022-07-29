from flask import g, current_app

from app.serializers.post import *


class MyPageService:
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
