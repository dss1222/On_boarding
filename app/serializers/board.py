from marshmallow import fields, Schema


class BoardCreateFormSchema(Schema):
    name = fields.Str(required=True)


class BoardFormSchema(Schema):
    id = fields.Str()
    name = fields.Str()
