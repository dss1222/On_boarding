from marshmallow import fields, Schema, post_load

from app.Model import *


class BoardCreateSchema(Schema):
    name = fields.String(required=True)

    @post_load()
    def create_board(self, data, **kwargs):
        board = Board(**data)
        return board


class BoardSchema(Schema):
    id = fields.Str()
    name = fields.Str()
