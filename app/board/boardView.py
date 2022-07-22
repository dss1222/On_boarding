import traceback

import marshmallow.exceptions
from flask_classful import FlaskView, route
from flask_apispec import marshal_with, doc, use_kwargs

from app.utils.validator import *
from app.board.boardSchema import BoardCreateSchema
from app.utils.error.ApiErrorSchema import *

from flask_apispec import FlaskApiSpec


class BoardView(FlaskView):
    decorators = (doc(tags=["Boards"]),)

    @route('/', methods=['POST'])
    @doc(description="boards 등록", summary="boards 등록")
    @login_required
    @use_kwargs(BoardCreateSchema())
    @marshal_with(SuccessSchema(), code=200, description="success")
    @marshal_with(ApiErrorSchema(), code=422, description="validation error")
    @marshal_with(ApiErrorSchema(), code=500, description="SERVER_ERROR")
    @board_crate_validator
    def create_board(self, board=None):
        board.save()
        return SuccessDto(), 200

