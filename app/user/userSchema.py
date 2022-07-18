import bcrypt

from marshmallow import fields, Schema, post_load
from app.user.userModel import User


class UserCreateSchema(Schema):
    username = fields.Str(required=True, unique=True)
    password = fields.Str(required=True, load_only=True)
    passwordCheck = fields.Str(required=True, load_only=True)


class UserSchema(Schema):
    id = fields.Str()
    username = fields.Str(required=True, unique=True)
    password = fields.Str(required=True)
    created_at = fields.DateTime()


class UserUpdateSchema(Schema):
    username = fields.Str()


class UserSchemaName(Schema):
    id = fields.Str()
    username = fields.Str()
