import datetime
from marshmallow import fields

from flask_mongoengine import Document
from mongoengine import StringField, DateTimeField, ReferenceField, ListField
from app.user.userModel import User


class Post(Document):
    user = ReferenceField(User, required=True)
    title = StringField(required=True)
    content = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now())
    likes = ListField(StringField())
    comments = ListField(StringField())
    tag = StringField()

    def is_user(self, user_id):
        return self.user.id == user_id

    def like(self, user):
        if str(user) not in self.likes:
            self.update(push__likes=str(user))  # push__likes에 user를 추가함. likes는 push된 유저의 갯수, push 해당 값 추가
        else:
            self.update(pull__likes=str(user))

