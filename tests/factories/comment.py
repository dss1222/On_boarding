from datetime import datetime

import factory
from factory import fuzzy
from factory.mongoengine import MongoEngineFactory

from app.comment.commentModel import Comment
from tests.factories.post import PostFactory
from tests.factories.user import UserFactory

class CommentFactory(MongoEngineFactory):
    class Meta:
        model = Comment

    post = factory.SubFactory(PostFactory)
    user = factory.SubFactory(UserFactory)
    content = fuzzy.FuzzyText(prefix='comment_')
    created_at = factory.LazyAttribute(lambda _: datetime.utcnow())