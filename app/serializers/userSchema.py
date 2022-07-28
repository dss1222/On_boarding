import bcrypt

from marshmallow import fields, Schema, post_load
from app.Model import User


class UserCreateSchema(Schema):
    username = fields.String(required=True, unique=True)
    password = fields.String(required=True, load_only=True)

    @post_load()
    def create_user(self, data, **kwargs):
        data["password"] = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())
        user = User(username=data['username'], password=data['password'])
        return user


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
