from app.user.userView import UserView
from app.post.postView import PostView
from app.comment.comentView import CommentView


def register_api(app):
    UserView.register(app, route_base='/users', trailing_slash=False)
    PostView.register(app, route_base='/posts', trailing_slash=False)
    CommentView.register(app, route_base='/comments', trailing_slash=False)
