from datetime import datetime

import factory
from factory import fuzzy
from factory.mongoengine import MongoEngineFactory

from app.models.models import ReComment

from tests.factories.post import PostFactory
from tests.factories.user import UserFactory
from tests.factories.comment import CommentFactory


class ReCommentFactory(MongoEngineFactory):
    class Meta:
        model = ReComment

    post = factory.SubFactory(PostFactory)
    user = factory.SubFactory(UserFactory)
    content = fuzzy.FuzzyText(length=10, prefix='re_comment_')
    created_at = factory.LazyAttribute(lambda _: datetime.utcnow())
    comment = factory.SubFactory(CommentFactory)
