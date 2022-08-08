from mongoengine import ReferenceField, ListField, IntField, BooleanField, StringField, DateTimeField
import datetime

from flask_mongoengine import Document
from app.models.user import User
from app.models.board import Board


# 질문 EnumFiled 값 넘기는법을 모름,

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
        from app.models.comment import Comment
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
