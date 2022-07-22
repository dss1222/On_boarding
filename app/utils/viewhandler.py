from flask import Flask, Blueprint, jsonify, render_template, url_for
from flask_swagger_ui import get_swaggerui_blueprint
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec

from app.user.userView import UserView
from app.post.postView import PostView
from app.comment.commentView import CommentView
from app.board.boardView import BoardView

api = Blueprint("api", __name__)


def register_swagger(bp):
    from app.apidocs_utils import generate_api_spec

    @bp.route("/apispec")
    def apispec():
        return jsonify(
            generate_api_spec(title="abcd", version="v1", bp_name=bp.name if isinstance(bp, Blueprint) else None))


def register_api(app):
    UserView.register(api, route_base='/users', trailing_slash=False)
    PostView.register(api, route_base='/boards/<board_id>/posts', trailing_slash=False)
    CommentView.register(api, route_base='/boards/<board_id>/posts/<post_id>/comments', trailing_slash=False)
    BoardView.register(api, route_base='/boards', trailing_slash=False)

    register_swagger(api)
    app.register_blueprint(api)
    SWAGGER_URL = '/api-docs'  # URL for exposing Swagger UI (without trailing '/')
    API_URL = '/apispec'  # Our API url (can of course be a local resource)

    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "Test application"
        },
    )

    app.register_blueprint(swaggerui_blueprint)
