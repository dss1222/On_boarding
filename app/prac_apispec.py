import flask
from webargs import fields
from flask_apispec import use_kwargs, marshal_with

from app.user.userModel import User
from app.user.userSchema import UserCreateSchema

from app.post.postModel import Post
from app.post.postSchema import PostListSchema

app = flask.Flask(__name__)
@app.route('/pets')
@use_kwargs({'species': fields.Str()})
@marshal_with(PostListSchema(many=True))
def list_Post(**kwargs):
    return Post.query.filter_by(**kwargs).all()