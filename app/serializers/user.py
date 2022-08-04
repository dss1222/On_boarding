from marshmallow import fields, Schema


class UserCreateSchema(Schema):
    username = fields.String(required=True, unique=True)
    password = fields.String(required=True, load_only=True)


class UserSchema(Schema):
    id = fields.Str()
    username = fields.Str(required=True, unique=True)
    password = fields.Str()
    provider = fields.Str()
    created_at = fields.DateTime()


class UserUpdateSchema(Schema):
    username = fields.Str()


class UserSchemaName(Schema):
    id = fields.Str()
    username = fields.Str()
