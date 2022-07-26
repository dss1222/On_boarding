from mongoengine import *
import datetime
import bcrypt

from flask_mongoengine import Document
from mongoengine import StringField, DateTimeField


class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now())

    def check_password(self, password):
        if not bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8')):
            return False
        else:
            return True

    def update_token(self, token):
        self.update(token=token)


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
    user = ReferenceField(User)
    post = ReferenceField(Post)
    content = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now())
    likes = ListField(StringField())
    likes_cnt = IntField(default=0)
    recomment = ReferenceField('self')
    is_deleted = BooleanField(required=True, default=False)

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
