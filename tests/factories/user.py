import bcrypt
from factory.mongoengine import MongoEngineFactory

from factory import fuzzy
from app.models.board import User


class UserFactory(MongoEngineFactory):
    class Meta:
        model = User

    username = fuzzy.FuzzyText(length=10, prefix='username_')
    password = bcrypt.hashpw('test1234'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    provider = 'default'
