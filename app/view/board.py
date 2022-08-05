from flask_classful import FlaskView, route
from flask_apispec import doc, use_kwargs

from app.service.validator import *
from app.serializers.board import BoardCreateFormSchema
from app.utils.ApiErrorSchema import *


class BoardView(FlaskView):
    decorators = (doc(tags=["Board"]),)

    @route('/', methods=['POST'])
    @doc(description="게시판 등록", summary="게시판 등록")
    @login_required
    @use_kwargs(BoardCreateFormSchema())
    @marshal_with(SuccessSchema(), code=201, description="성공")
    def create(self, name):
        board = Board(name=name)
        board.save()
        return "", 201
