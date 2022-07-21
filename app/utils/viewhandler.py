from flask import Flask, Blueprint, jsonify
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec import FlaskApiSpec

from app.user.userView import UserView
from app.post.postView import PostView
from app.comment.commentView import CommentView
from app.board.boardView import BoardView


def register_apidocs(bp, title='eimmo API', version='v1'):
    global_params = [
        {'description': '호스트 언어(ko, en, vi)', 'in': 'query', 'name': 'hl', 'schema': {'type': 'string'}},
        {'description': '국가(kr, us, vn)', 'in': 'query', 'name': 'cr', 'schema': {'type': 'string'}}
    ]

    from app.utils.apidocs import apidoc_auth_required, generate_api_spec
    from flask import render_template, url_for

    def get_api_spec_url():
        if isinstance(bp, Blueprint):
            return url_for(f'{bp.name}.apispec')
        else:
            return url_for('apispec')

    @bp.route('/apispec')
    @apidoc_auth_required
    def apispec():
        return jsonify(generate_api_spec(
            title=title,
            version=version,
            bp_name=bp.name if isinstance(bp, Blueprint) else None,
            global_params=global_params
        ))

    @bp.route('/swagger')
    @apidoc_auth_required
    def swagger():
        return render_template('swagger-ui.html', spec_url=get_api_spec_url())

    @bp.route('/redoc')
    @apidoc_auth_required
    def redoc():
        return render_template('redoc.html', spec_url=get_api_spec_url())


def register_api(app):
    UserView.register(app, route_base='/users', trailing_slash=False)
    PostView.register(app, route_base='/boards/<board_id>/posts', trailing_slash=False)
    CommentView.register(app, route_base='/boards/<board_id>/posts/<post_id>/comments', trailing_slash=False)
    BoardView.register(app, route_base='/boards', trailing_slash=False)

    # register_apidocs(app, title='eimmo API', )
