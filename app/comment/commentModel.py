import datetime

from flask_mongoengine import Document
from mongoengine import StringField, DateTimeField, ReferenceField, ListField, IntField, BooleanField
from app.user.userModel import User
from app.post.postModel import Post
from app.utils.ErrorHandler import *


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
