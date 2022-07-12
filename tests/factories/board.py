import factory
from factory import fuzzy
from factory.mongoengine import MongoEngineFactory

from app.board.boardModel import Board

class BoardFactory(MongoEngineFactory):
    class Meta:
        model = Board

    name = fuzzy.FuzzyText(prefix='board_')
