import factory
from factory import fuzzy
from factory.mongoengine import MongoEngineFactory

from app.Model import Board


class BoardFactory(MongoEngineFactory):
    class Meta:
        model = Board

    name = fuzzy.FuzzyText(length=10, prefix='board_')
