import bcrypt

from marshmallow import fields, Schema, post_load, pre_load
from app.user.userModel import User


class UserCreateSchema(Schema):
    username = fields.String(required=True, unique=True)
    password = fields.String(required=True, load_only=True)
    passwordCheck = fields.Str(required=True, load_only=True)
    # @pre_load
    # def strip_name(self, data, **kwargs):
    #     data["username"] = data["username"].strip()
    #     return data

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
