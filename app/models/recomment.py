from mongoengine import *
import datetime

from flask_mongoengine import Document
from mongoengine import StringField
from app.models.user import User
from app.models.comment import Comment


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
