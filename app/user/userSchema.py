import bcrypt

from marshmallow import fields, Schema, post_load
from app.user.userModel import User


class UserCreateSchema(Schema):
    username = fields.Str(required=True, unique=True)
    password = fields.Str(required=True, load_only=True)

    @post_load
    def create_users(self, data, **kwargs):
        if not User.objects(username=data['username']):  # 중복이침없다면
            password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            data['password'] = password
            user = User(**data)
            return user
        return False


class UserSchema(Schema):
    id = fields.Str()
    username = fields.Str(required=True, unique=True)
    password = fields.Str(required=True)
    created_at = fields.DateTime()

    @post_load
    def check_user(self, data, **kwargs):
        if not User.objects(username=data['username']):
            return False
        else:
            return User.objects(username=data['username']).get()


class UserUpdateSchema(Schema):
    username = fields.Str()


class UserSchemaName(Schema):
    id = fields.Str()
    username = fields.Str()