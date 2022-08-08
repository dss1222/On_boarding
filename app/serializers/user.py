from marshmallow import fields, Schema


class UserCreateFormSchema(Schema):
    username = fields.String(required=True, unique=True)
    password = fields.String(required=True, load_only=True)


class UserDetailSchema(Schema):
    id = fields.String()
    username = fields.String(required=True, unique=True)
    password = fields.String()
    provider = fields.String()
    created_at = fields.DateTime()


class UserUpdateFormSchema(Schema):
    username = fields.String()


class UserSchemaName(Schema):
    id = fields.String()
    username = fields.String()
