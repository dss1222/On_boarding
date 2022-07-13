import factory
import bcrypt
from factory.mongoengine import MongoEngineFactory

from app.user.userModel import User
from factory import fuzzy


class UserFactory(MongoEngineFactory):
    class Meta:
        model = User

    username = "test5678"
    password = bcrypt.hashpw('test1234'.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
