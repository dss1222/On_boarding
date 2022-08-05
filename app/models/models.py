from mongoengine import *
import datetime

from flask_mongoengine import Document
from mongoengine import StringField, DateTimeField
from app.models.user import User


class Board(Document):
    name = StringField(required=True)


class Post(Document):
    user = ReferenceField(User, required=True)
    board = ReferenceField(Board)
    title = StringField(required=True)
    content = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now())
    likes = ListField(StringField())
    comments = ListField(StringField())
    likes_cnt = IntField(default=0)
    comments_cnt = IntField(default=0)
    tag = StringField()
    is_deleted = BooleanField(required=True, default=False)

    @property
    def comment(self):
        return Comment.objects().filter(post=self)

    def find_user(self, user_id):
        return self.user.id == user_id

    def like(self, user):
        if str(user) not in self.likes:
            self.update(push__likes=str(user))  # push__likes에 user를 추가함. likes는 push된 유저의 갯수, push 해당 값 추가
            self.update(inc__likes_cnt=1)

    def cancel_like(self, user):
        if str(user) in self.likes:
            self.update(pull__likes=str(user))
            self.update(dec__likes_cnt=1)

    def soft_delete(self):
        self.update(is_deleted=True)


class Comment(Document):
    user = ReferenceField(User, required=True)
    post = ReferenceField(Post, required=True)
    content = StringField(required=True)
    created_at = ComplexDateTimeField(default=datetime.datetime.utcnow)
    likes = ListField(StringField())
    likes_cnt = IntField(default=0)
    is_deleted = BooleanField(default=False)
    recomment_cnt = IntField(default=0)

    @property
    def recomment(self):
        return ReComment.objects().filter(comment=self)

    def find_user(self, user_id):
        return self.user.id == user_id

    def find_post(self, post_id):
        return self.post.id == post_id

    def like(self, user):
        if str(user) not in self.likes:
            self.update(push__likes=str(user))
            self.update(inc__likes_cnt=1)

    def cancel_like(self, user):
        if str(user) in self.likes:
            self.update(pull__likes=str(user))
            self.update(dec__likes_cnt=1)

    def soft_delete(self):
        self.update(is_deleted=True)

    def create_recomment(self):
        self.update(inc__recomment_cnt=1)


class ReComment(Document):
    user = ReferenceField(User, required=True)
    content = StringField(required=True)
    created_at = ComplexDateTimeField(default=datetime.datetime.utcnow)
    likes = ListField(StringField())
    likes_cnt = IntField(default=0)
    comment = ReferenceField(Comment, required=True)
    is_deleted = BooleanField(default=False)

    @property
    def recomment(self):
        return ReComment.objects().filter(comment=self)

    def like(self, user):
        if str(user) not in self.likes:
            self.update(push__likes=str(user))
            self.update(inc__likes_cnt=1)

    def cancel_like(self, user):
        if str(user) in self.likes:
            self.update(pull__likes=str(user))
            self.update(dec__likes_cnt=1)

    def soft_delete(self):
        self.update(is_deleted=True)
