from flask_classful import FlaskView, route
from flask import jsonify, request, g
from marshmallow import ValidationError

from app.utils.validator import *
from app.board.boardSchema import BoardCreateSchema
from app.board.boardModel import Board


class BoardView(FlaskView):
    @route('/', methods=['POST'])
    @login_required
    @board_crate_validator
    def create_board(self):
        board = BoardCreateSchema().load(json.loads(request.data))

        board.save()
        return Success()
