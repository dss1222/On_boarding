from flask_classful import FlaskView, route

from app.utils.validator import *
from app.board.boardSchema import BoardCreateSchema


class BoardView(FlaskView):
    @route('/', methods=['POST'])
    @login_required
    @board_crate_validator
    def create_board(self):
        board = BoardCreateSchema().load(json.loads(request.data))

        board.save()
        return Success()
