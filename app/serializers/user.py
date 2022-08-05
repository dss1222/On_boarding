from marshmallow import fields, Schema


class UserCreateFormSchema(Schema):
    username = fields.String(required=True, unique=True)
    password = fields.String(required=True, load_only=True)


class UserDetailSchema(Schema):
    id = fields.Str()
    username = fields.Str(required=True, unique=True)
    password = fields.Str()
    provider = fields.Str()
    created_at = fields.DateTime()


class UserUpdateFormSchema(Schema):
    username = fields.Str()


class UserSchemaName(Schema):
    id = fields.Str()
    username = fields.Str()
