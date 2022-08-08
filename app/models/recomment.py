from mongoengine import ReferenceField, ListField, IntField, BooleanField, StringField, ComplexDateTimeField
import datetime

from flask_mongoengine import Document
from app.models.user import User


class ReComment(Document):
    from app.models.comment import Comment
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

    def like_recomment(self, user):
        if str(user) not in self.likes:
            self.update(push__likes=str(user))
            self.update(inc__likes_cnt=1)

    def cancel_like_recomment(self, user):
        if str(user) in self.likes:
            self.update(pull__likes=str(user))
            self.update(dec__likes_cnt=1)

    def soft_delete_recomment(self):
        self.update(is_deleted=True)
