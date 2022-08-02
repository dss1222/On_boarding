from marshmallow import fields, Schema


class BoardCreateSchema(Schema):
    name = fields.Str(required=True)


class BoardSchema(Schema):
    id = fields.Str()
    name = fields.Str()
