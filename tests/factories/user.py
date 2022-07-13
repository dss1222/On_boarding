import factory
from factory.mongoengine import MongoEngineFactory

from app.user.userModel import User
from factory import fuzzy


class UserFactory(MongoEngineFactory):
    class Meta:
        model = User

    username = "test5678"
    password = "test1234"
