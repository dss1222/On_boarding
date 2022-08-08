from marshmallow import fields, Schema


class BoardCreateFormSchema(Schema):
    name = fields.String(required=True)


class BoardFormSchema(Schema):
    id = fields.String()
    name = fields.String()
