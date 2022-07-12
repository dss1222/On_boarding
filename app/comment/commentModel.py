import datetime

from flask_mongoengine import Document
from mongoengine import StringField, DateTimeField, ReferenceField, ListField, IntField
from app.user.userModel import User
from app.post.postModel import Post


class Comment(Document):
    user = ReferenceField(User)
    post = ReferenceField(Post)
    content = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now())
    likes = ListField(StringField())
    likes_cnt = IntField(default=0)
    recomment = ListField(StringField())

    def is_user(self, user_id):
        return self.user.id == user_id

    def is_post(self, post_id):
        return self.post.id == post_id

    def like(self, user):
        if str(user) not in self.likes:
            self.update(push__likes=str(user))
            self.update(inc__likes_cnt=1)
        else:
            self.update(pull__likes=str(user))
            self.update(dec__likes_cnt=1)