from marshmallow import fields, Schema, post_load

from app.board.boardModel import Board


class BoardCreateSchema(Schema):
    name = fields.Str(required=True)

    @post_load()
    def create_board(self,data,**kwargs):
        board = Board(**data)
        return board