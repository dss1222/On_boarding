# import factory
# import pytest
#
# from flask import url_for
# from json import dumps
#
# from tests.factories.user import UserFactory
# from tests.factories.board import BoardFactory
#
#
# class Describe_BoardView:
#     @pytest.fixture()
#     def logged_in_user(self):
#         return UserFactory.create()
#
#     @pytest.fixture()
#     def board(self):
#         return BoardFactory.create()
#
#     class Describe_post:
#         @pytest.fixture()
#         def form(self):
#             return {'name': factory.Faker('sentence').generate()}
