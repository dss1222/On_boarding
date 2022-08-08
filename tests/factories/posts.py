from datetime import datetime

import factory
from factory import fuzzy
from factory.mongoengine import MongoEngineFactory

from app.models.post import Post
from tests.factories.board import BoardFactory
from tests.factories.user import UserFactory


class PostFactory(MongoEngineFactory):
    class Meta:
        model = Post

    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)
    title = fuzzy.FuzzyText(length=10, prefix='post_')
    content = fuzzy.FuzzyText(length=20, prefix='post_')
    tag = fuzzy.FuzzyText(length=10, prefix='post_')
    created_at = factory.LazyAttribute(lambda _: datetime.utcnow())
