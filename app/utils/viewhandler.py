from app.user.userView import UserView
from app.post.postView import PostView
from app.comment.comentView import CommentView
from app.board.boardView import BoardView


def register_api(app):
    UserView.register(app, route_base='/users', trailing_slash=False)
    PostView.register(app, route_base='/boards/<board_id>/posts', trailing_slash=False)
    CommentView.register(app, route_base='/boards/<board_id>/posts/<post_id>/comments', trailing_slash=False)
    BoardView.register(app, route_base='/boards', trailing_slash=False)
