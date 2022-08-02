from flask_classful import FlaskView, route
from flask_apispec import doc, use_kwargs

from app.service.validator import *
from app.serializers.board import BoardCreateSchema
from app.utils.ApiErrorSchema import *


class BoardView(FlaskView):
    decorators = (doc(tags=["Boards"]),)

    @route('/', methods=['POST'])
    @doc(description="boards 등록", summary="boards 등록")
    @login_required
    @use_kwargs(BoardCreateSchema())
    @marshal_with(SuccessSchema(), code=201, description="성")
    def create(self, name):
        board = Board(name=name)
        board.save()
        return "", 201
