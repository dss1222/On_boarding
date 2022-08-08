from marshmallow import fields, Schema


class OauthFormSchema(Schema):
    code = fields.String(required=True)
