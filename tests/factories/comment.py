from datetime import datetime

import factory
from factory import fuzzy
from factory.mongoengine import MongoEngineFactory

from app.models.Model import Comment
from tests.factories.post import PostFactory
from tests.factories.user import UserFactory


class CommentFactory(MongoEngineFactory):
    class Meta:
        model = Comment

    post = factory.SubFactory(PostFactory)
    user = factory.SubFactory(UserFactory)
    content = fuzzy.FuzzyText(length=10, prefix='comment_')
    created_at = factory.LazyAttribute(lambda _: datetime.utcnow())
