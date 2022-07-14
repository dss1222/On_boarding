from datetime import datetime

import factory
from factory import fuzzy
from factory.mongoengine import MongoEngineFactory

from app.post.postModel import Post
from tests.factories.board import BoardFactory
from tests.factories.user import UserFactory


class PostFactory(MongoEngineFactory):
    class Meta:
        model = Post

    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)
    title = "test_title"
    content = "test_content"
    tag = "test_tag"
    created_at = factory.LazyAttribute(lambda _: datetime.utcnow())
